import os
import codecs
import MeCab
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


# sample data
sample = codecs.open('recipe_sample.txt', 'r', 'utf-8').read().splitlines()
print(sample)
sample_strings = ''
for i in range(len(sample)):
    sample_strings = sample_strings + str(sample[i])

print(sample_strings)

sample_tagger = MeCab.Tagger('-Owakati')
sample_corpus = sample_tagger.parse(sample_strings)
print('sample_corpus')
print(sample_corpus)

sample_vectorizder = CountVectorizer(token_pattern=u'(?u)\\b\\w+\\b')
sample_transformer = TfidfTransformer()
sample_tf= sample_vectorizder.fit_transform(sample)
print(sample_tf)
sample_tfidf = sample_transformer.fit_transform(sample_tf)
print(sample_tfidf)




text_files = os.listdir('data')

for f in text_files:
    print(f)
    corpus = codecs.open('data/' + f, 'r', 'utf-8').read().splitlines()    
    tagger = MeCab.Tagger('-Owakati')
    corpus = [tagger.parse(line).strip() for line in corpus]
    # print(corpus)
    print(*corpus, sep='\n', file=codecs.open('recipe_sample_mecab.txt', 'w', 'utf-8'))


    vectorizer = CountVectorizer(token_pattern=u'(?u)\\b\\w+\\b')
    transformer = TfidfTransformer()

    tf = vectorizer.fit_transform(corpus)
    tfidf = transformer.fit_transform(tf)

    # similarity = cosine_similarity(sample_tfidf, tfidf)[0]
    # print('similarity')
    # print(similarity)

    print(tfidf.toarray())
    print(tfidf.shape)

    # print(vectorizer.vocabulary_)

    # print(vectorizer.get_feature_names())
