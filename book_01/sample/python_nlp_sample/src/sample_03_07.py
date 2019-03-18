import json

import sqlitedatastore as datastore
import solrindexer     as indexer

if __name__ == '__main__':
    datastore.connect()
    data = []
    for doc_id in datastore.get_all_ids(limit=-1):
        row = datastore.get(doc_id, ['id', 'content', 'meta_info'])
        # Solr へ登録するデータ構造へ変換
        meta_info = json.loads(row['meta_info'])
        data.append({
            'id':               str(row['id']),
            'doc_id_i':         row['id'],
            'content_txt_ja':   row['content'],
            'title_txt_ja':     meta_info['title'],
            'url_s':            meta_info['url'],
        })
    # Solr への登録を実行
    indexer.load('doc', data)
    datastore.close()
