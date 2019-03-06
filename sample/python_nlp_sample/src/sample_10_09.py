import json

import bottle
import chainer
import nets
import numpy
from sklearn.externals import joblib

import dlclassifier
import mlclassifier
import ruleclassifier
import solrindexer     as indexer
import sqlitedatastore as datastore
from annoutil import find_xs_in_y

# ルールによるテキスト分類の設定
rule = ruleclassifier.get_rule()

# 教師あり学習によるテキスト分類の設定
model_ml = joblib.load('result/model.pkl')
vocab_ml = joblib.load('result/vocab.pkl')

# ディープラーニングによるテキスト分類の設定
w = numpy.load('result/w_dl.npy')
encoder = dlclassifier.Encoder(w)
model_dl = nets.TextClassifier(encoder, n_class=2)
chainer.serializers.load_npz('result/model_dl.npz', model_dl)
with open('result/vocab_dl.json') as f:
    vocab_dl = json.load(f)


@bottle.route('/')
def index_html():
    return bottle.static_file('sample_10_10.html', root='./src/static')


@bottle.route('/file/<filename:path>')
def static(filename):
    return bottle.static_file(filename, root='./src/static')


@bottle.get('/get')
def get():
    keywords = bottle.request.params.keywords.split()
    classifier_name = bottle.request.params.classifier

    results = indexer.search_annotation(
        fl_keyword_pairs=[
            ('sentence_txt_ja', [keywords]),
            ('name_s',          [['sentence']])
        ], rows=1000)

    for r in results['response']['docs']:
        sent = datastore.get_annotation(r['doc_id_i'], 'sentence')[
            r['anno_id_i']]
        tokens = find_xs_in_y(datastore.get_annotation(
            r['doc_id_i'], 'token'), sent)

        if classifier_name == 'ml':
            features = mlclassifier.convert_into_features_using_vocab(
                [(r['doc_id_i'], sent, tokens)], vocab_ml)
            predicteds = mlclassifier.classify(features, model_ml)
        elif classifier_name == 'dl':
            features = dlclassifier.convert_into_features_using_vocab(
                [(r['doc_id_i'], sent, tokens)], vocab_dl)
            predicteds = dlclassifier.classify(features, model_dl)
        elif classifier_name == 'rule':
            features = ruleclassifier.convert_into_features_using_rules(
                [(r['doc_id_i'], sent, tokens)], rule)
            predicteds = ruleclassifier.classify(features, rule)

        r['predicted'] = int(predicteds[0])  # covert from numpy.int to int
        print(r['predicted'], r['sentence_txt_ja'])

    return json.dumps(results, ensure_ascii=False)


if __name__ == '__main__':
    datastore.connect()
    bottle.run(host='0.0.0.0', port='8702')
    datastore.close()
