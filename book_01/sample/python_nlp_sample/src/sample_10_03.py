import solrindexer     as indexer
import sqlitedatastore as datastore

# ラベル付与用データの作成
if __name__ == '__main__':
    datastore.connect()
    print('#label', 'doc_id', 'sentence_id', 'text')

    results = indexer.search_annotation(
            fl_keyword_pairs=[
                ('sentence_txt_ja', [[
                    '肉', '魚', '茶', '塩', '野菜', '油', '森林',
                    '砂漠', '草原', '海', '木材', '果樹', '麦', '米',
                    ]]),
                ('name_s', [['sentence']]),
                ], rows=1000)
    for r in results['response']['docs']:
        text = datastore.get(r['doc_id_i'], ['content'])['content']
        sent = datastore.get_annotation(r['doc_id_i'], 'sentence')[
            r['anno_id_i']]
        # ラベルファイルのデータ構造へ変換
        print(0, r['doc_id_i'], r['anno_id_i'], text[sent['begin']:sent['end']])
    datastore.close()
