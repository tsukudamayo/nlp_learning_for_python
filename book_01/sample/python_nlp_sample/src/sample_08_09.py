import wordnetknowledge

if __name__ == '__main__':
    text1 = 'アメリカ合衆国'
    text2 = '米国'
    similarity = wordnetknowledge.calc_similarity(text1, text2)
    print(similarity, text1, text2)
    text1 = 'アメリカ合衆国'
    text2 = '日本'
    similarity = wordnetknowledge.calc_similarity(text1, text2)
    print(similarity, text1, text2)
