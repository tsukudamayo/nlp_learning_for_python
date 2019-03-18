import itertools
import json
import logging
import math

from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamodel import LdaModel

from annoutil import find_xs_in_y
import sqlitedatastore as datastore

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

if __name__ == '__main__':
    datastore.connect()
    sentences = []
    for doc_id in datastore.get_all_ids(limit=-1):
        all_tokens = datastore.get_annotation(doc_id, 'token')
        for sent in datastore.get_annotation(doc_id, 'sentence'):
            tokens = find_xs_in_y(all_tokens, sent)
            sentences.append([token['lemma'] for token in tokens 
                              if token.get('NE') == 'O'])

    n_sent = 20
    docs = [list(itertools.chain.from_iterable(sentences[i:i+n_sent]))
            for i in range(0, len(sentences), n_sent)]

    dictionary = Dictionary(docs)
    dictionary.filter_extremes(no_below=2, no_above=0.3)
    corpus = [dictionary.doc2bow(doc) for doc in docs]

    lda = LdaModel(corpus, num_topics=10, id2word=dictionary, passes=10)

    # 主題の確認
    for topic in lda.show_topics(num_topics=-1, num_words=10):
        print('topic id:{0[0]:d}, words={0[1]:s}'.format(topic))

    # 記事の主題分布の推定
    for doc_id in datastore.get_all_ids(limit=-1):
        meta_info = json.loads(datastore.get(doc_id, ['meta_info'])[ 'meta_info'])
        title = meta_info['title']
        print(title)

        doc = [token['lemma'] for token in datastore.get_annotation(doc_id, 'token')
               if token.get('NE') == 'O']
        for topic in sorted(lda.get_document_topics(dictionary.doc2bow(doc)),
                            key=lambda x: x[1], reverse=True):
            print('\ttopic id:{0[0]:d}, prob={0[1]:f}'.format(topic))
    datastore.close()
