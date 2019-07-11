import codecs
from gensim.models import word2vec
from janome.tokenizer import Tokenizer

with codecs.open('aru_kokorono_fukei.txt', 'r', 'sjis') as r:
    text = r.read()

print(text)
text = text.replace(' ', '')


t = Tokenizer()

def extract_words(text):
    tokens = t.tokenize(text)
    # print(tokens)

    return [token.base_form for token in tokens
            if token.part_of_speech.split(',')[0] in ['名詞', '動詞']]


extract_words(text)

print('ret')
ret = extract_words(text)
for word in ret:
    print('word')
    print(word)

print('sentence')
sentences = text.split('。')
word_list = [extract_words(sentence) for sentence in sentences]

for word in word_list[0]:
    print(word)

model = word2vec.Word2Vec(word_list, size=100, min_count=5, window=5, iter=100)
print(model.__dict__['wv']['たかし'])

print(word_list[0])
ret = model.wv.most_similar(positive=['たかし'])
for item in ret:
    print(item[0], [1])
