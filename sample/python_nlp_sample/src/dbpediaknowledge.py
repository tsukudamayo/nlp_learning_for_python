from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from SPARQLWrapper import JSON, SPARQLWrapper

import cabochaparser as parser


def get_synonyms(text):
    uri = '<http://ja.dbpedia.org/resource/{0}>'.format(text)

    sparql = SPARQLWrapper('http://ja.dbpedia.org/sparql')
    sparql.setReturnFormat(JSON)
    sparql.setQuery('''
        SELECT DISTINCT *
        WHERE {{
            {{ ?redirect <http://dbpedia.org/ontology/wikiPageRedirects> {0} }}
            UNION
            {{ {0} <http://dbpedia.org/ontology/wikiPageRedirects> ?redirect }} .
            ?redirect <http://www.w3.org/2000/01/rdf-schema#label> ?synonym
        }}
    '''.format(uri))

    results = []
    for x in sparql.query().convert()['results']['bindings']:
        word = x['synonym']['value']
        results.append({'term': word})
    return results


def retrieve_abstract(text):
    uri = '<http://ja.dbpedia.org/resource/{0}>'.format(text)

    sparql = SPARQLWrapper('http://ja.dbpedia.org/sparql')
    sparql.setReturnFormat(JSON)
    sparql.setQuery('''
        SELECT DISTINCT *
        WHERE {{
            {0} <http://dbpedia.org/ontology/abstract> ?summary
        }}
    '''.format(uri))
    results = sparql.query().convert()['results']['bindings']
    if len(results) > 0:
        return results[0]['summary']['value']
    else:
        return None


def calc_similarity(text1, text2, vectorizer=None):
    summary1 = retrieve_abstract(text1)
    summary2 = retrieve_abstract(text2)
    if summary1 is None or summary2 is None:
        return 0.

    sentences1, chunks1, tokens1 = parser.parse(summary1)
    doc1 = ' '.join([token['lemma'] for token in tokens1])
    sentences2, chunks2, tokens2 = parser.parse(summary2)
    doc2 = ' '.join([token['lemma'] for token in tokens2])

    vectorizer = CountVectorizer(analyzer='word')
    vecs = vectorizer.fit_transform([doc1, doc2])

    sim = cosine_similarity(vecs)
    return sim[0][1]


def get_population(text):
    uri = '<http://ja.dbpedia.org/resource/{0}>'.format(text)

    sparql = SPARQLWrapper('http://ja.dbpedia.org/sparql')
    sparql.setReturnFormat(JSON)
    sparql.setQuery('''
        SELECT DISTINCT *
        WHERE {{
            {0} <http://ja.dbpedia.org/property/人口値> ?population
        }}
    '''.format(uri))

    results = sparql.query().convert()['results']['bindings']
    if len(results) > 0:
        population = results[0]['population']['value']
        return int(population)
    else:
        return -1
