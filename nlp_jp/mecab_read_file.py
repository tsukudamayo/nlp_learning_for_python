import sys
import MeCab

# m = MeCab.Tagger('-Owakati')
m = MeCab.Tagger()

for line in open('recipe_sample.txt', 'r', encoding='utf-8'):
    words = m.parse(line)
    # words = words.rstrip('\n')
    print(words)
