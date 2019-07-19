import os
import json
import time

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

import create_matrix as cm
import featureselect as fs
import vectorapi as vec


_LOG_DIR = './rne_wakachi'
_POS_DIR = '../recipe_conv/weekcook/procedure_2'
_RNE_DIR = '../recipe_conv/weekcook/procedure_4_2'
_AC_DIR = './countAC'

_RANDOM_SEED = 42

_COLOR = ['red', 'blue', 'green']


def compute_svd(matrix, vector_size=2):
    U, S, V = np.linalg.svd(matrix)
    vectors = U[:, :vector_size]

    return vectors


def main():
    data_dir = _LOG_DIR
    pos_dir = _POS_DIR
    rne_dir = _RNE_DIR
    word_list = cm.generate_wordlist(data_dir)
    word_to_id, id_to_word = cm.generate_word_id_map(word_list)
    corpus = np.array([word_to_id[w] for w in word_list])
    vocab_size = len(id_to_word)
    feature = fs.extract_feature('trigram', data_dir, pos_dir, rne_dir)

    ppmi_score = vec.ppmi(feature)
    print('ppmi')
    print(ppmi_score)

    vectors = compute_svd(ppmi_score, 2)
    print('vectors')
    print(vectors)
    print(vectors.shape)


    # vec.plot_vector(ppmi_score, word_to_id)

    sample_querys = ['油抜き']
    querys = '油抜き'
    vec.rank_similarity(ppmi_score, sample_querys, word_to_id, id_to_word)
    query_id = word_to_id[querys]
    query_vec = vectors[query_id]
    print('query_vec')
    print(query_vec)

    json_list = os.listdir(_AC_DIR)
    row = len(json_list)
    column = vectors.shape[1]
    print(row)
    print(column)

    all_recipe_vector = np.zeros((row, column))
    for idx, j in enumerate(json_list):
        recipe_score = np.zeros(column)
        jsonfile = os.path.join(_AC_DIR, j)
        with open(jsonfile, 'r', encoding='utf-8') as r:
            jsondata = json.load(r)
        print('idx')
        print(idx)
        print(jsonfile)
        print('jsondata')
        print(jsondata)
        for k, v in jsondata.items():
            print('key')
            print(k)
            print('value')
            print(v)
            ############################################
            # TODO join word is not include word_to_id #
            ############################################
            try:
                query_id = word_to_id[k]
                query_vector = vectors[query_id]
                print('query_vector')
                print(query_vector)
            except KeyError:
                print('{} is not included in word_to_id'.format(k))
                time.sleep(3)
                continue

            print('recipe_score', recipe_score)
            print('v', v)
            recipe_score += query_vector * v
        all_recipe_vector[idx][0] = recipe_score[0]
        all_recipe_vector[idx][1] = recipe_score[1]
    print(all_recipe_vector)

    kmeans = KMeans(n_clusters=3, random_state=_RANDOM_SEED).fit(all_recipe_vector)
    print('label')
    print(kmeans.labels_)
    labels = kmeans.labels_

    for feature, label in zip(all_recipe_vector, labels):
        plt.scatter(feature[0], feature[1], c=_COLOR[label])
    plt.show()


if __name__ == '__main__':
    main()
