import chainer
import chainer.functions as F
import chainer.links as L
import numpy
from chainer import training
from chainer.training import extensions
import nets
from nlp_utils import convert_seq, transform_to_array


class Encoder(chainer.Chain):
    def __init__(self, w):
        super(Encoder, self).__init__()
        self.out_units = 300
        with self.init_scope():
            self.embed = lambda x: F.embed_id(x, w)
            self.encoder = L.NStepLSTM(
                n_layers=1,
                in_size=300,
                out_size=self.out_units,
                dropout=0.5)

    def forward(self, xs):
        exs = nets.sequence_embed(self.embed, xs)
        last_h, last_c, ys = self.encoder(None, None, exs)
        return last_h[-1]


def train(labels, features, w):
    n_class = len(set(labels))
    print('# data: {0}'.format(len(features)))
    print('# class: {0}'.format(n_class))

    pairs = [(vec, numpy.array([cls], numpy.int32))
             for vec, cls in zip(features, labels)]
    train_iter = chainer.iterators.SerialIterator(pairs, batch_size=16)

    model = nets.TextClassifier(Encoder(w), n_class)

    # Setup an optimizer
    optimizer = chainer.optimizers.Adam()
    optimizer.setup(model)
    optimizer.add_hook(chainer.optimizer.WeightDecay(1e-4))

    # Set up a trainer
    updater = training.updaters.StandardUpdater(
        train_iter, optimizer,
        converter=convert_seq)
    trainer = training.Trainer(updater, (8, 'epoch'), out='./result/dl')

    # Write a log of evaluation statistics for each epoch
    trainer.extend(extensions.LogReport())
    trainer.extend(extensions.PrintReport(
        ['epoch', 'main/loss', 'main/accuracy', 'elapsed_time']))

    trainer.run()
    return model


def classify(features, model):
    with chainer.using_config('train', False), chainer.no_backprop_mode():
        prob = model.predict(features, softmax=True)
    answers = model.xp.argmax(prob, axis=1)
    return answers


def convert_into_features_using_vocab(sentences, vocab):
    contents = []
    for doc_id, sent, tokens in sentences:
        features = [token['lemma'] for token in tokens]
        contents.append(features)

    features = transform_to_array(contents, vocab, with_label=False)
    return features
