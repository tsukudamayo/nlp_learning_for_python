import sqlitedatastore as datastore
from annoutil import find_x_including_y, find_xs_in_y

if __name__ == '__main__':
    datastore.connect()
    anno_name = 'affiliation'

    for doc_id in datastore.get_all_ids(limit=-1):
        row = datastore.get(doc_id, fl=['content'])
        text = row['content']
        sentences = datastore.get_annotation(doc_id, 'sentence')
        tokens = datastore.get_annotation(doc_id, 'token')
        annos = datastore.get_annotation(doc_id, anno_name)
        for sentence in sentences:
            annos_in_sentence = find_xs_in_y(annos, sentence)
            if annos_in_sentence == []:
                continue
            prev = False
            for token in find_xs_in_y(tokens, sentence):
                if find_x_including_y(annos_in_sentence, token) is None:
                    prev = False
                    print('{0}\t{1}\t{2}'.format(
                        text[token['begin']:token['end']], token['POS'], 'O'))
                else:
                    if prev:
                        print('{0}\t{1}\tI-{2}'.format(
                            text[token['begin']:token['end']], token['POS'], anno_name))
                    else:
                        print('{0}\t{1}\tB-{2}'.format(
                            text[token['begin']:token['end']], token['POS'], anno_name))
                        prev = True
            print()  # 文の区切り
    datastore.close()
