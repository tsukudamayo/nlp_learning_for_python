import os

import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA, NMF, LatentDirichletAllocation

_LOG_DIR = 'C:/Users/tsukuda/var/data/recipe/weekcook/procedure_3'


def generate_wordlist(data_dir):
    file_list = os.listdir(data_dir)
    word_list = []
    for f in file_list:
        read_filepath = os.path.join(data_dir, f)
        with open(read_filepath, 'r', encoding='utf-8') as lines:
            for line in lines:
                line = line.replace('\n', '')
                line = line.split(' ')
                word_list.extend(line)

    return word_list


def generate_word_id_map(word_list):
    word_to_id = {}
    id_to_word = {}
    for word in word_list:
        new_id = len(word_to_id)
        word_to_id[word] = new_id
        id_to_word[new_id] = word

    word_to_id = {v: k for (k, v) in id_to_word.items()}

    return word_to_id, id_to_word


def id_to_word_to_txt(id_to_word):
    with open('id_to_word.txt', 'w', encoding='utf-8') as w:
        for k, v in id_to_word.items():
            w.write(str(k))
            w.write(':')
            w.write(v)
            w.write('\n')

    return


def create_co_matrix(corpus, vocab_size, id_to_word, window_size=1):
    corpus_size = len(corpus)
    co_matrix = np.zeros((vocab_size, vocab_size), dtype=np.int32)
    for idx, word_id in enumerate(corpus):
        # print('idx')
        # print(idx)
        # print('word_id')
        # print(word_id)
        # print('id_to_word[word_id]')
        # print(id_to_word[word_id])
        for i in range(1, window_size + 1):
            # print('i')
            # print(i)
            left_idx = idx - i
            right_idx = idx + i
            # print('left_idx')
            # print(left_idx)
            # print('right_idx')
            # print(right_idx)

            if left_idx >= 0:
                left_word_id = corpus[left_idx]
                current_idx = corpus[idx]
                co_matrix[word_id, left_word_id] = 1
                co_matrix[word_id, current_idx] = 1
            if right_idx < corpus_size:
                right_word_id = corpus[right_idx]
                current_idx = corpus[idx]
                co_matrix[word_id, right_word_id] = 1
                co_matrix[word_id, current_idx] = 1

    return co_matrix


def main():
    word_list = generate_wordlist(_LOG_DIR)
    word_to_id, id_to_word = generate_word_id_map(word_list)
    # print('id_to_word')
    # print(id_to_word)
    # print('word_to_id')
    # print(word_to_id)

    id_to_word_to_txt(id_to_word)

    corpus = np.array([word_to_id[w] for w in word_list])
    print('corpus')
    print(corpus)

    vocab_size = len(id_to_word)

    matrix = create_co_matrix(corpus, vocab_size, id_to_word)

    # # label_and_matrix = np.array([np.array([v, m]) for v, m in zip(id_to_word.values(), matrix)])
    print('matrix')
    print(matrix)
    label = np.array([x for x in id_to_word.values()]) 
    label = label[:, np.newaxis]
    print('label')
    print(label)

    # print('matrix')
    # print(matrix[0])
    # where_0 = np.argwhere(matrix[0] == 1)
    # print(where_0)
    # where_0_flatten = where_0.flatten()
    # print('where_0_flatten')
    # print(where_0_flatten)
    # word_index = np.array([label[x] for x in where_0_flatten])
    # print('word_index[0]')
    # print(word_index)
    # # matrix_and_label = np.hstack([matrix, label])
    # # print('matrix_and_label')
    # # print(matrix_and_label)
    # # print(matrix_and_label.shape)
    # # np.savetxt('test.csv', matrix_and_label, delimiter=',', fmt='%s')

    # # feature_label = np.array(list(id_to_word.values()))
    # 
    # print('id_to_word')
    # print(id_to_word)

    # print('word_to_id')
    # print(word_to_id)

    print('matrix[0]')
    print(matrix[0])

    print('玉ねぎ')
    print(word_to_id['玉ねぎ'])
    print(matrix[word_to_id['玉ねぎ']])

    print('word_list')
    print(word_list[:200])

    for idx, (x, y) in enumerate(zip(matrix[0], id_to_word.values())):
        if idx == 50:
            break
        print(idx)
        print(x, y)

    print('matrix')
    print(matrix)

    # U, S, V = np.linalg.svd(matrix)
    # print('U')
    # print(U)
    # print(U[:, :2]) 

    # pca = PCA(n_components=2)
    # X = pca.fit(matrix)
    # X_r = pca.fit_transform(matrix)
    # print('pca')
    # print(X_r)
    # print(X.explained_variance_ratio_)

    # model = NMF(n_components=2, init='random', random_state=0)
    # X_r = model.fit_transform(matrix)

    model = LatentDirichletAllocation(
        n_components=2,
        max_iter=5,
        learning_method='online',
        learning_offset=50.,
        random_state=0
    )
    X = model.fit(matrix)
    X_r = model.fit_transform(matrix)

    for idx, (x, w) in enumerate(zip(X_r, label)):
        plt.scatter(x[0], x[1])
        plt.text(x[0], x[1], w)
    plt.show()

    # import matplotlib.font_manager as fm
    # print(fm.findSystemFonts())


if __name__ == '__main__':
    main()
