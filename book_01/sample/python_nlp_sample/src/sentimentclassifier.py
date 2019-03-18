import mlclassifier
import triematcher as matcher


def convert_into_features_using_vocab(sentences, vocab):
    features, _ = convert_into_features(sentences, vocab)
    return features


def convert_into_features(sentences, vocab=None):
    dic_positive, dic_negative = matcher.get_sentiment_dictionaries()
    contents = []
    for doc_id, sent, tokens in sentences:
        # Bag-of-Words特徴量
        lemmas = [token['lemma'] for token in tokens]
        # 評価極性辞書内語句マッチ
        text = ''.join(lemmas)
        terms_positive = matcher.search_terms(text, dic_positive)
        terms_negative = matcher.search_terms(text, dic_negative)
        polarities = []
        if len(terms_positive) > 0:
            polarities.append('［ポジティブ］')
        if len(terms_negative) > 0:
            polarities.append('［ネガティブ］')

        content = ' '.join(lemmas + polarities)
        contents.append(content)

    features, vocab = mlclassifier.vectorize(contents, vocab)
    return features, vocab
