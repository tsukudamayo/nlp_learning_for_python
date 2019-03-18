from nltk.corpus import wordnet


def get_synonyms(text):
    results = []
    for synset in wordnet.synsets(text, lang='jpn'):
        for lemma in synset.lemma_names(lang='jpn'):
            results.append({'term': lemma})
    return results


def calc_similarity(text1, text2):
    synsets1 = wordnet.synsets(text1, lang='jpn')
    synsets2 = wordnet.synsets(text2, lang='jpn')
    max_sim = 0.
    for synset1 in synsets1:
        for synset2 in synsets2:
            sim = synset1.path_similarity(synset2)
            if max_sim < sim:
                max_sim = sim
    return max_sim


def get_hypernym(text):
    synsets = wordnet.synsets(text, lang='jpn')
    results = []
    for synset in synsets:
        for hypernym in synset.hypernyms():
            for lemma in hypernym.lemma_names(lang='jpn'):
                results.append({'term': lemma})
    return results
