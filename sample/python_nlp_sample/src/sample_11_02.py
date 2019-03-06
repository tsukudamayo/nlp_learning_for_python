import sqlitedatastore as datastore
import triematcher as matcher
from annoutil import find_xs_in_y

if __name__ == '__main__':
    datastore.connect()
    dic_positive, dic_negative = matcher.get_sentiment_dictionaries()
    doc_id = 1
    for sent in datastore.get_annotation(doc_id, 'sentence'):
        tokens = find_xs_in_y(
            datastore.get_annotation(doc_id, 'token'), sent)
        text = ''.join([token['lemma'] for token in tokens])
        print(text, '-->')
        print('\tpositive:', matcher.search_terms(text, dic_positive))
        print('\tnegative:', matcher.search_terms(text, dic_negative))
    datastore.close()
