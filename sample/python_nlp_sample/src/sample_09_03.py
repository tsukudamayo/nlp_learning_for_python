import json

import sqlitedatastore as datastore
import solrindexer     as indexer
from annoutil import find_x_including_y


def load_sentence():
    data = []
    for doc_id in datastore.get_all_ids(limit=-1):
        row = datastore.get(doc_id, ['content', 'meta_info'])
        text = row['content']
        meta_info = json.loads(row['meta_info'])
        for i, sent in enumerate(datastore.get_annotation(doc_id, 'sentence')):
            # Solr へ登録するデータ構造へ変換
            data.append({
                'id':               '{0:d}.{1:s}.{2:d}'.format(doc_id, 'sentence', i),
                'doc_id_i':         doc_id,
                'anno_id_i':        i,
                'name_s':           'sentence',
                'sentence_txt_ja':  text[sent['begin']:sent['end']],
                'title_txt_ja':     meta_info['title'],
                'url_s':            meta_info['url'],
            })
    # Solr への登録を実行
    indexer.load('anno', data)


def load_affiliation():
    anno_name = 'affiliation'
    data = []
    for doc_id in datastore.get_all_ids(limit=-1):
        row = datastore.get(doc_id, ['content', 'meta_info'])
        text = row['content']
        meta_info = json.loads(row['meta_info'])
        sents = datastore.get_annotation(doc_id, 'sentence')
        for i, anno in enumerate(datastore.get_annotation(doc_id, anno_name)):
            # Solr へ登録するデータ構造へ変換
            sent = find_x_including_y(sents, anno)
            data.append({
                'id':                  '{0:d}.{1:s}.{2:d}'.format(doc_id, anno_name, i),
                'doc_id_i':            doc_id,
                'anno_id_i':           i,
                'name_s':              anno_name,
                'sentence_txt_ja':     text[sent['begin']:sent['end']],
                anno_name + '_txt_ja': text[anno['begin']:anno['end']],
                'title_txt_ja':        meta_info['title'],
                'url_s':               meta_info['url'],
            })
    # Solr への登録を実行
    indexer.load('anno', data)


if __name__ == '__main__':
    datastore.connect()
    load_sentence()
    load_affiliation()
    datastore.close()
