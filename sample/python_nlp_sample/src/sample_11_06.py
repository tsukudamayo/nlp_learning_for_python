import json

import bottle
from sklearn.externals import joblib

import mlclassifier
import sentimentclassifier
import solrindexer as indexer
import sqlitedatastore as datastore
from annoutil import find_xs_in_y

# 学習済モデルをファイルから読み込み
model = joblib.load('result/model_sentiment.pkl')
vocab = joblib.load('result/vocab_sentiment.pkl')


@bottle.route('/')
def index_html():
    return bottle.static_file('sample_11_07.html', root='./src/static')


@bottle.route('/file/<filename:path>')
def static(filename):
    return bottle.static_file(filename, root='./src/static')


@bottle.get('/get')
def get():
    title = bottle.request.params.title.strip()
    keywords = bottle.request.params.keywords.split()

    results = indexer.search_annotation(
        fl_keyword_pairs=[
            ('title_txt_ja',    [[title]]),
            ('sentence_txt_ja', [keywords]),
            ('name_s',          [['sentence']])
        ], rows=1000)

    for r in results['response']['docs']:
        sent = datastore.get_annotation(r['doc_id_i'], 'sentence')[
            r['anno_id_i']]
        tokens = find_xs_in_y(datastore.get_annotation(
            r['doc_id_i'], 'token'), sent)

        features = sentimentclassifier.convert_into_features_using_vocab(
            [(r['doc_id_i'], sent, tokens)], vocab)
        predicteds = mlclassifier.classify(features, model)

        r['predicted'] = int(predicteds[0])  # covert from numpy.int to int
        print(r['predicted'], r['sentence_txt_ja'])

    return json.dumps(results, ensure_ascii=False)


if __name__ == '__main__':
    datastore.connect()
    bottle.run(host='0.0.0.0', port='8702')
    datastore.close()
