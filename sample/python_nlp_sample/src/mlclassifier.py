from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer


def vectorize(contents, vocab=None):
    vectorizer = CountVectorizer(analyzer='word', vocabulary=vocab)
    vecs = vectorizer.fit_transform(contents)
    vocab = vectorizer.vocabulary_
    return vecs, vocab


def convert_into_features_using_vocab(sentences, vocab):
    features, _ = convert_into_features(sentences, vocab)
    return features


def convert_into_features(sentences, vocab=None):
    contents = []
    for doc_id, sent, tokens in sentences:
        lemmas = [token['lemma'] for token in tokens if token['POS'] in ['名詞', '動詞']]
        content = ' '.join(lemmas)
        contents.append(content)
    features, vocab = vectorize(contents, vocab=vocab)
    return features, vocab


def train(labels, features):
    model = svm.LinearSVC()
    model.fit(features, labels)
    return model


def classify(features, model):
    predicts = model.predict(features)
    return predicts
