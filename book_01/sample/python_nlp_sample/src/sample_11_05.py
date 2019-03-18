import time

from sklearn.externals import joblib

import mlclassifier
import sentimentclassifier
import sqlitedatastore as datastore
from annoutil import find_xs_in_y

if __name__ == '__main__':
    datastore.connect()
    # ラベル付きデータ読み込み
    sentences = []
    labels = []
    with open('data/labels_sentiment.txt') as f:
        for line in f:
            if line.startswith('#'):
                continue
            d = line.rstrip().split()
            label, doc_id, sent_id = int(d[0]), d[1], int(d[2])
            sent = datastore.get_annotation(doc_id, 'sentence')[sent_id]
            tokens = find_xs_in_y(
                datastore.get_annotation(doc_id, 'token'), sent)
            sentences.append((doc_id, sent, tokens))
            labels.append(label)

    # 学習データ特徴量生成
    num_train = int(len(sentences) * 0.8)
    sentences_train = sentences[:num_train]
    labels_train = labels[:num_train]
    features, vocab = sentimentclassifier.convert_into_features(sentences_train)

    # 学習
    time_s = time.time()
    print(':::TRAIN START')
    model = mlclassifier.train(labels_train, features)
    print(':::TRAIN FINISHED', time.time() - time_s)

    # 学習モデルをファイルに保存
    joblib.dump(model, 'result/model_sentiment.pkl')
    joblib.dump(vocab, 'result/vocab_sentiment.pkl')

    # 分類の実行
    features_test = sentimentclassifier.convert_into_features_using_vocab(
        sentences[num_train:], vocab)
    predicteds = mlclassifier.classify(features_test, model)
    for predicted, (doc_id, sent, tokens), label in zip(
            predicteds,
            sentences[num_train:],
            labels[num_train:]):
        # 結果の確認
        text = datastore.get(doc_id, ['content'])['content']
        if predicted == label:
            print('correct  ', '  ', label, predicted,
                  text[sent['begin']:sent['end']])
        else:
            print('incorrect', '  ', label, predicted,
                  text[sent['begin']:sent['end']])
    datastore.close()
