import json

import sqlitedatastore as datastore
import solrindexer     as indexer
from annoutil import find_x_including_y


def create_index_data(doc_id, meta_info, anno_name, anno, i, sent, text):
    ref_anno_name, link = anno['link']
    ref_anno = datastore.get_annotation(doc_id, ref_anno_name)[link]
    data = {
        'id':                       '{0:d}.{1:s}.{2:d}'.format(doc_id, anno_name, i),
        'doc_id_i':                 doc_id,
        'anno_id_i':                i,
        'name_s':                   anno_name,
        'sentence_txt_ja':          text[sent['begin']:sent['end']],
        anno_name + '_txt_ja':      text[anno['begin']:anno['end']],
        ref_anno_name + '_txt_ja':  text[ref_anno['begin']:ref_anno['end']],
        'title_txt_ja':             meta_info['title'],
        'url_s':                    meta_info['url'],
    }
    return data


if __name__ == '__main__':
    datastore.connect()
    anno_name = 'cause'
    data = []
    for doc_id in datastore.get_all_ids(limit=-1):
        row = datastore.get(doc_id, fl=['content', 'meta_info'])
        text = row['content']
        meta_info = json.loads(row['meta_info'])
        sents = datastore.get_annotation(doc_id, 'sentence')
        for i, anno in enumerate(datastore.get_annotation(doc_id, anno_name)):
            sent = find_x_including_y(sents, anno)
            data.append(create_index_data(doc_id, meta_info,
                anno_name, anno, i, sent, text))

    # Solr への登録を実行
    indexer.load('anno', data)
    datastore.close()
