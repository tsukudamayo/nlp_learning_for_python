import statistics

import sqlitedatastore as datastore

if __name__ == '__main__':
    datastore.connect()
    lm = statistics.create_language_model(datastore.get_all_ids(limit=-1), N=3)
    context = ('古く', 'から')
    print(context, '->')

    prob_list = [(word, lm.score(word, context)) for word
                 in lm.context_counts(lm.vocab.lookup(context))]
    prob_list.sort(key=lambda x: x[1], reverse=True)
    for word, prob in prob_list:
        print('\t{:s}: {:f}'.format(word, prob))
    datastore.close()
