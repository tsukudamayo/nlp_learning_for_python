import os

import numpy as np

_LOG_DIR = 'C:/Users/tsukuda/var/data/recipe/weekcook/procedure_3'


def id_to_word_to_txt(id_to_word):
    with open('id_to_word.txt', 'w', encoding='utf-8') as w:
        for k, v in id_to_word.items():
            w.write(str(k))
            w.write(':')
            w.write(v)
            w.write('\n')

    return


def create_co_matrix(corpus, vocab_size, id_to_word, window_size=3):
    corpus_size = len(corpus)
    co_matrix = np.zeros((vocab_size, vocab_size), dtype=np.int32)
    for idx, word_id in enumerate(corpus):
        print(idx)
        print(id_to_word[word_id])
        for i in range(1, window_size + 1):
            print(i)
            left_idx = idx - i
            right_idx = idx + i

            if left_idx >= 0:
                left_word_id = corpus[left_idx]
                co_matrix[word_id, left_word_id] = 1
            if right_idx < corpus_size:
                right_word_id = corpus[right_idx]
                co_matrix[word_id, right_word_id] = 1

    return co_matrix


def main():
    file_list = os.listdir(_LOG_DIR)
    word_list = []
    word_to_id = {}
    id_to_word = {}
    for f in file_list:
        read_filepath = os.path.join(_LOG_DIR, f)
        with open(read_filepath, 'r', encoding='utf-8') as lines:
            for line in lines:
                line = line.replace('\n', '')
                line = line.split(' ')
                word_list.extend(line)

    for word in word_list:
        new_id = len(word_to_id)
        word_to_id[word] = new_id
        id_to_word[new_id] = word

    id_to_word_to_txt(id_to_word)

    corpus = np.array([word_to_id[w] for w in word_list])

    vocab_size = len(id_to_word)

    matrix = create_co_matrix(corpus, vocab_size, id_to_word)
    for v, m in zip(id_to_word.values(), matrix):
        print(v, m)
        print(len(m))


if __name__ == '__main__':
    main()
