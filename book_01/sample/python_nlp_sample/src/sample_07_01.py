import json

from sklearn.feature_extraction.text import TfidfVectorizer

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

    for doc_id, vec in zip(doc_ids, vecs.toarray()):
        meta_info = json.loads(datastore.get(doc_id, ['meta_info'])['meta_info'])
        title = meta_info['title']
        print(doc_id, title)

        for w_id, tfidf in sorted(enumerate(vec), key=lambda x: x[1], reverse=True)[:10]:
            lemma = vectorizer.get_feature_names()[w_id]
            print('\t{0:s}: {1:f}'.format(lemma, tfidf))
    datastore.close()
