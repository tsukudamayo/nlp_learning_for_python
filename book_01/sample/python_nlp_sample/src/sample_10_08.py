import json

import chainer
import gensim
import numpy

import dlclassifier
import sqlitedatastore as datastore
from annoutil import find_xs_in_y


def extract_w_and_vocab(model):
    w_ls = []
    vocab = {}
    for word in model.wv.index2word:
        vocab[word] = len(vocab)
        w_ls.append(model[word])
    for word in ['<eos>', '<unk>']:
        vocab[word] = len(vocab)
        w_ls.append(2 * numpy.random.rand(300) - 1)
    return numpy.array(w_ls).astype(numpy.float32), vocab


if __name__ == '__main__':
    datastore.connect()
    w2v_model = gensim.models.Word2Vec.load('./data/ja.bin')
    w, vocab = extract_w_and_vocab(w2v_model)

    # ラベル付きデータ読み込み
    sentences = []
    labels = []
    with open('./data/labels.txt') as f:
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

    num_train = int(len(sentences) * 0.8)
    sentences_train = sentences[:num_train]
    labels_train = labels[:num_train]
    features = dlclassifier.convert_into_features_using_vocab(sentences_train, vocab)

    # 学習
    model = dlclassifier.train(labels_train, features, w)

    # 学習モデルをファイルに保存
    chainer.serializers.save_npz('result/model_dl.npz', model)
    numpy.save('result/w_dl.npy', w)
    with open('result/vocab_dl.json', 'w') as f:
        json.dump(vocab, f)

    # 分類の実行
    features_test = dlclassifier.convert_into_features_using_vocab(
        sentences[num_train:], vocab)
    predicteds = dlclassifier.classify(features_test, model)
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
