import random

import cabochaparser   as parser
import sqlitedatastore as datastore
import statistics

if __name__ == '__main__':
    datastore.connect()
    lm = statistics.create_language_model(datastore.get_all_ids(limit=-1), N=3)

    text = '古くから人が居住する。'
    sentences, chunks, tokens = parser.parse(text)

    probabilities = set([])
    for i in range(1000):
        tokens_ = tokens[1:]
        random.shuffle(tokens_)
        tokens_shuffled = [tokens[0]] + tokens_
        lemmas = ['__BOS__'] + [token['lemma']
                                for token in tokens_shuffled] + ['__EOS__']
        shuffled_text = ''.join(
            [text[token['begin']:token['end']] for token in tokens_shuffled])
        probability = statistics.calc_prob(lm, lemmas, N=3)
        probabilities.add((probability, shuffled_text))

    for probability, shuffled_text in sorted(list(probabilities), reverse=True)[:20]:
        print('{0:e}: {1:s}'.format(probability, shuffled_text))
    datastore.close()
