import os
import json
import time

import numpy as np
import matplotlib.pyplot as plt

import create_matrix as cm
import featureselect as fs
import vectorapi as vec


_LOG_DIR = '../recipe_conv/weekcook/procedure_3'
_POS_DIR = '../recipe_conv/weekcook/procedure_2'
_RNE_DIR = '../recipe_conv/weekcook/procedure_4_2'
_AC_DIR = './countAC'


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

    for idx, j in enumerate(json_list):
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


if __name__ == '__main__':
    main()
