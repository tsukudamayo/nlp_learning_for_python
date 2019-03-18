import gensim

model = gensim.models.Word2Vec.load('./data/ja.bin')


def get_synonyms(text):
    results = []
    for word, sim in model.most_similar(text, topn=10):
        results.append({'term': word, 'similarity': sim})
    return results


def calc_similarity(text1, text2):
    sim = model.similarity(text1, text2)
    return sim


def analogy(X_Y, x):
    X, Y = X_Y
    results = []
    for word, sim in model.most_similar(positive=[Y, x], negative=[X], topn=10):
        results.append({'term': word, 'similarity': sim})
    return results
