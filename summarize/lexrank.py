import codecs

with codecs.open('aru_kokorono_fukei.txt', 'r', 'sjis') as r:
    text = r.read()

print(text)
