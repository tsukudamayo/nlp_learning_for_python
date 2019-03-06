import sqlitedatastore as datastore
from annoutil import find_xs_in_y


def extend_phrase(chunk, chunk_tokens, tokens, all_chunks):
    def _extend(chunk, chunk_tokens):
        for child in all_chunks:
            _, link = child['link']
            if link == -1:
                continue
            if all_chunks[link] != chunk:
                continue
            child_tokens = find_xs_in_y(tokens, child)
            if child_tokens[0]['POS'] == chunk_tokens[0]['POS']:
                return [child] + _extend(child, child_tokens)
        return []

    phrase = [chunk] + _extend(chunk, chunk_tokens)
    return {
        'begin': min(phrase, key=lambda x: x['begin'])['begin'],
        'end':   max(phrase, key=lambda x: x['end'])['end'],
    }


def find_child(parent, chunks_in_sent, tokens_in_sent, text, all_chunks, child_cond):
    for child in chunks_in_sent:
        _, link = child['link']
        if link == -1 or all_chunks[link] != parent:
            continue
        child_tokens = find_xs_in_y(tokens_in_sent, child)
        if text[child['begin']:child['end']] in child_cond.get('text', []):
            return child, child_tokens
        if child_tokens[-1]['POS'] in child_cond.get('pos1', []) and \
                child_tokens[-1]['lemma'] in child_cond.get('lemma1', []) and \
                child_tokens[-2]['POS'] not in child_cond.get('pos2_ng', []):
            return child, child_tokens
    return None, None


def extract_relation(doc_id):
    text = datastore.get(doc_id, fl=['content'])['content']
    all_chunks = datastore.get_annotation(doc_id, 'chunk')
    all_tokens = datastore.get_annotation(doc_id, 'token')
    anno_id = 0
    for sent in datastore.get_annotation(doc_id, 'sentence'):
        chunks = find_xs_in_y(all_chunks, sent)
        tokens = find_xs_in_y(all_tokens, sent)
        for chunk in chunks:
            chunk_tokens = find_xs_in_y(tokens, chunk)
            if not any([chunk_token['lemma'] == '与える'
                        for chunk_token in chunk_tokens]):
                continue

            affect, affect_tokens = find_child(
                chunk, chunks, tokens, text, all_chunks,
                child_cond={ 'text': ['影響を'] })
            if affect is None:
                continue

            cause, cause_tokens = find_child(
                chunk, chunks, tokens, text, all_chunks,
                child_cond={
                    'pos1':    ['助詞'],
                    'lemma1':  ['は', 'も', 'が'],
                    'pos2_ng': ['助詞'],
                })
            if cause is None:
                continue

            effect, effect_tokens = find_child(
                chunk, chunks, tokens, text, all_chunks,
                child_cond={
                    'pos1':    ['助詞'],
                    'lemma1':  ['に'],
                    'pos2_ng': ['助詞'],
                })
            if effect is None:
                continue
            
            cause  = extend_phrase(cause,  cause_tokens,  tokens, all_chunks)
            effect = extend_phrase(effect, effect_tokens, tokens, all_chunks)

            relation = {
                'cause':  {
                    'begin': cause['begin'],
                    'end':   cause['end'],
                    'link':  ('effect', anno_id),
                },
                'effect':  {
                    'begin': effect['begin'],
                    'end':   effect['end'],
                }
            }

            anno_id += 1
            yield sent, relation


if __name__ == '__main__':
    datastore.connect()
    for doc_id in datastore.get_all_ids(limit=-1):
        text = datastore.get(doc_id, fl=['content'])['content']
        annotations = {}
        for sent, relation in extract_relation(doc_id):
            print('文書{0:d} {1}'.format(doc_id, text[sent['begin']:sent['end']]))
            for anno_name, anno in relation.items():
                print('\t{0}: {1}'.format(
                    anno_name, text[anno['begin']:anno['end']]))
                annotations.setdefault(anno_name, []).append(anno)
            print()
        for anno_name, annos in annotations.items():
            datastore.set_annotation(doc_id, anno_name, annos)
    datastore.close()
