import numpy as np
import matplotlib.pyplot as plt

import create_matrix as cm
import featureselect as fs


_LOG_DIR = '../recipe_conv/weekcook/procedure_3'
_POS_DIR = '../recipe_conv/weekcook/procedure_2'
_RNE_DIR = '../recipe_conv/weekcook/procedure_4_2'


def ppmi(matrix, verbose=False, eps=1e-8):
    M = np.zeros_like(matrix, dtype=np.float32)
    N = np.sum(matrix)
    S = np.sum(matrix, axis=0)
    total = matrix.shape[0] * matrix.shape[1]
    cnt = 0
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            pmi = np.log2(matrix[i, j] * N / (S[j] * S[i]) + eps)
            M[i, j] = max(0, pmi)

            if verbose:
                cnt += 1
                if cnt % (total//100) == 0:
                    print('%.1f%% done' % (100 * cnt/total))

    return M


def cos_similarity(x, y, eps=1e-8):
    nx = x / np.sqrt(np.sum(x**2) + eps)
    ny = y / np.sqrt(np.sum(y**2) + eps)

    return np.dot(nx, ny)


def most_similar(query, word_to_id, id_to_word, vectors, top=5):
    if query not in word_to_id:
        print('{} is not found'.format(query))
        return
    print('\n[query] ' + query)
    query_id = word_to_id[query]
    query_vec = vectors[query_id]

    vocab_size = len(id_to_word)
    similarity = np.zeros(vocab_size)
    for i in range(vocab_size):
        similarity[i] = cos_similarity(vectors[i], query_vec)
    # high
    print('\n[query] ' + query + ' high-score')
    high_count = 0
    for i in (-1 * similarity).argsort():
        print('i', i)
        if id_to_word[i] == query:
            continue
        print(' %s: %s' % (id_to_word[i], similarity[i]))
        high_count += 1
        if high_count >= top:
            break
    # low
    print('\n[query] ' + query + ' low-score')
    low_count = 0
    for j in (similarity).argsort():
        print('j', j)
        if id_to_word[j] == query:
            continue
        print(' %s: %s' % (id_to_word[j], similarity[j]))
        low_count += 1
        if low_count >= top:
            break

    return


def rank_similarity(matrix, querys, word_to_id, id_to_word, vector_size=40):
    U, S, V = np.linalg.svd(matrix)
    vectors = U[:, :vector_size]
    for query in querys:
        most_similar(query, word_to_id, id_to_word, vectors, top=5)

    return


def plot_vector(matrix, word_to_id):
    U, S, V = np.linalg.svd(matrix)
    print(U)
    print(U[:, :2])

    for word, word_id in word_to_id.items():
        plt.annotate(word, (U[word_id, 0], U[word_id, 1]))
    plt.scatter(U[:, 0], U[:, 1], alpha=0.5)
    plt.show()

    return


def main():
    data_dir = _LOG_DIR
    pos_dir = _POS_DIR
    rne_dir = _RNE_DIR
    word_list = cm.generate_wordlist(data_dir)
    word_to_id, id_to_word = cm.generate_word_id_map(word_list)
    corpus = np.array([word_to_id[w] for w in word_list])
    vocab_size = len(id_to_word)
    feature = fs.extract_feature('trigram', data_dir, pos_dir, rne_dir)

    ppmi_score = ppmi(feature)
    print('ppmi')
    print(ppmi_score)

    plot_vector(ppmi_score, word_to_id)

    querys = ['油抜き']
    rank_similarity(ppmi_score, querys, word_to_id, id_to_word)


if __name__ == '__main__':
    main()
