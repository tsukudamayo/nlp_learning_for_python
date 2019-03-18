from ahocorapy.keywordtree import KeywordTree

dic_positive = KeywordTree()
dic_negative = KeywordTree()

# 用言編
with open('data/wago.121808.pn') as yougen:
    for line in yougen:
        line_splitted = line.strip().split('\t')
        if len(line_splitted) != 2:
            continue
        polarity_, term_ = line_splitted[:2]
        polarity = polarity_[:2]
        term = term_.replace(' ', '')
        if polarity == 'ポジ':
            dic_positive.add(term)
        elif polarity == 'ネガ':
            dic_negative.add(term)

# 名詞編
with open('data/pn.csv.m3.120408.trim') as meishi:
    for line in meishi:
        term, polarity = line.strip().split('\t')[:2]
        if polarity == 'p':
            dic_positive.add(term)
        elif polarity == 'n':
            dic_negative.add(term)

dic_positive.finalize()
dic_negative.finalize()


def get_sentiment_dictionaries():
    return dic_positive, dic_negative


def search_terms(text, dic):
    results = dic.search_all(text)
    return list(results)
