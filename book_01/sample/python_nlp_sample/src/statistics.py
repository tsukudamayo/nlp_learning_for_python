from nltk.lm        import Vocabulary
from nltk.lm.models import MLE
from nltk.util      import ngrams

import sqlitedatastore as datastore
from annoutil import find_xs_in_y


def create_language_model(doc_ids, N=3):
    sents = []
    for doc_id in doc_ids:
        all_tokens = datastore.get_annotation(doc_id, 'token')
        for sent in datastore.get_annotation(doc_id, 'sentence'):
            tokens = find_xs_in_y(all_tokens, sent)
            sents.append(['__BOS__'] + [token['lemma']
                                        for token in tokens] + ['__EOS__'])
    vocab = Vocabulary([word for sent in sents for word in sent])
    text_ngrams = [ngrams(sent, N) for sent in sents]
    lm = MLE(order=N, vocabulary=vocab)
    lm.fit(text_ngrams)
    return lm


def calc_prob(lm, lemmas, N=3):
    probability = 1.0
    for ngram in ngrams(lemmas, N):
        prob = lm.score(lm.vocab.lookup(ngram[-1]), lm.vocab.lookup(ngram[:-1]))
        prob = max(prob, 1e-8)
        probability *= prob
    return probability
