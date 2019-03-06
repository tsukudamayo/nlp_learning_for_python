import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import sqlitedatastore as datastore

if __name__ == '__main__':
    datastore.connect()

    data = []
    doc_ids = []
    for doc_id in datastore.get_all_ids(limit=-1):
        data.append(' '.join(
            [token['lemma'] for token in datastore.get_annotation(doc_id, 'token')]))
        doc_ids.append(doc_id)

    vectorizer = TfidfVectorizer(analyzer='word', max_df=0.9)
    vecs = vectorizer.fit_transform(data)

    sim = cosine_similarity(vecs)
    docs = zip(doc_ids, sim[0])
    for doc_id, similarity in sorted(docs, key=lambda x: x[1], reverse=True):
        meta_info = json.loads(datastore.get(doc_id, ['meta_info'])['meta_info'])
        title = meta_info['title']
        print(doc_id, title, similarity)
    datastore.close()
