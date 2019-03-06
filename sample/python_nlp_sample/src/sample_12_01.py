import re

import sqlitedatastore as datastore

ptn_relation = re.compile(
    r'(?P<cause>[^、はもがに]+[はもが])(?P<effect>[^はもが]+に)影響を与え')

def extract_relation(doc_id):
    text = datastore.get(doc_id, fl=['content'])['content']
    anno_id = 0
    for sent in datastore.get_annotation(doc_id, 'sentence'):
        for m in ptn_relation.finditer(text[sent['begin']:sent['end']]):
            relation = {
                'cause':  {'begin': m.start('cause') + sent['begin'],
                           'end':   m.end('cause')   + sent['begin'],
                           'link':  ('effect', anno_id)},
                'effect': {'begin': m.start('effect') + sent['begin'],
                           'end':   m.end('effect')   + sent['begin']},
            }
            anno_id += 1
            yield sent, relation

if __name__ == '__main__':
    datastore.connect()
    for doc_id in datastore.get_all_ids(limit=-1):
        text = datastore.get(doc_id, fl=['content'])['content']
        for sent, relation in extract_relation(doc_id):
            print('文書{0:d} {1:s}'.format(
                doc_id, text[sent['begin']:sent['end']]))
            for anno_name, anno in relation.items():
                print('\t{0}: {1}'.format(
                    anno_name, text[anno['begin']:anno['end']]))
            print()
    datastore.close()
