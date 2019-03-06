import CaboCha

cabocha = CaboCha.Parser('-nl')


def parse_sentence(sentence_str, sentence_begin):
    tree = cabocha.parse(sentence_str)
    offset = sentence_begin
    text = sentence_str
    for i in range(tree.chunk_size()):
        chunk = tree.chunk(i)
        chunk_begin = None
        print('chunk:')
        for j in range(chunk.token_pos, chunk.token_pos + chunk.token_size):
            token = tree.token(j)
            features = token.feature.split(',')
            token_begin = text.find(token.surface) + offset
            token_end = token_begin + len(token.surface)
            if chunk_begin is None:
                chunk_begin = token_begin
            print('    token_begin:', token_begin)
            print('    features   :', features)
            print('    lemma      :', features[-3])
            print('    POS        :', features[0])
            print('    POS2       :', features[1])
            print('    NE         :', token.ne)
            print()

            text = text[token_end - offset:]
            offset = token_end

        chunk_end = token_end
        print('   chunk_link :', chunk.link)
        print('   chunk_begin:', chunk_begin)
        print('   chunk_end  :', chunk_end)
        print()


if __name__ == '__main__':
    parse_sentence('プログラムを作って、動かしながら自然言語処理を学ぶ', 0)
