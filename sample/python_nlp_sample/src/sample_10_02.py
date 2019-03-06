import ruleclassifier
import solrindexer     as indexer
import sqlitedatastore as datastore
from annoutil import find_xs_in_y

if __name__ == '__main__':
    datastore.connect()
    results = indexer.search_annotation(
        fl_keyword_pairs=[
            ('name_s', [['sentence']]),
        ], rows=3000)
    sentences = []
    for r in results['response']['docs']:
        sent = datastore.get_annotation(r['doc_id_i'], 'sentence')[
            r['anno_id_i']]
        tokens = find_xs_in_y(datastore.get_annotation(
            r['doc_id_i'], 'token'), sent)
        sentences.append((r['doc_id_i'], sent, tokens))

    # ルール取得
    rule = ruleclassifier.get_rule()

    # 分類
    features = ruleclassifier.convert_into_features_using_rules(sentences, rule)
    predicteds = ruleclassifier.classify(features, rule)
    for predicted, (doc_id, sent, tokens) in zip(predicteds, sentences):
        if predicted == 1:
            text = datastore.get(doc_id, ['content'])['content']
            print(predicted, text[sent['begin']:sent['end']])
    datastore.close()
