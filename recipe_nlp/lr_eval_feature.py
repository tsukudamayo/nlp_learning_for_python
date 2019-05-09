import os
import time

import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.externals import joblib

import create_matrix as cm
import featureselect as fs


_CORPUS_DIR = 'C:/Users/tsukuda/var/data/recipe/orangepage/procedure_3'
_RESULT_DIR = 'C:/Users/tsukuda/var/data/recipe/orangepage/ner_result'
_TXT_FILE = 'detail_103522_proc3.txt'
_RNE_FILE = 'detail_103522_ner_result.txt'
_DST_DIR = 'C:/Users/tsukuda/var/data/recipe/orangepage/visualization/lr'


def load_dataset(ner_result_dir, rne_result_file):
    # rne-tag
    rnetag_file = os.path.join(ner_result_dir, rne_result_file)
    # # non rne-tag
    # sample_data = os.path.join(corpus_dir, split_file)
    with open(rnetag_file, 'r', encoding='utf-8') as r:
        lines = np.array([x for x in r.read().splitlines()])
    print(lines)

    return lines


def one_hot_to_feature(one_hot_array, idx):
    feature = np.array(
        [np.dot(one_hot_array[idx], x) for x in one_hot_array]
    )
    feature = feature[:, np.newaxis]
    print('feature')
    print(feature)

    return feature


def split_dependency_words(lines, word_to_id):
    split_line = lines[0].split(' ')
    print('split line')
    print(split_line)

    t0 = time.time()
    rne_tag_words = np.array(
        [x for x in split_line if x.find('/') >= 0]
    )
    t1 = time.time()
    print('rne_tag_words')
    print(rne_tag_words)
    print('time : ', t1 - t0)

    dependency_words = np.array(
        [x.split('/')[0] for x in rne_tag_words]
    )
    print('dependency_words')
    print(dependency_words)

    return dependency_words


def dependency_words_to_ids(dependency_words, word_to_id):
    # TODO about "=" joined words ---------------------------
    todo_dependency_words = np.array(
        [x for x in dependency_words if x.find('=') < 0]
    )
    print('todo_dependency_words')
    print(todo_dependency_words)

    dependency_ids = np.array(
        [word_to_id[x] for x in todo_dependency_words]
    )
    print('dependency_ids')
    print(dependency_ids)
    # --------------------------------------------------------

    return dependency_ids, todo_dependency_words


def search_argmax_foreach_idx(feature, idx):
    feature = feature[(idx+1):]

    return np.argmax(feature) + (idx+1)


def eval_dependency(one_hot_array, idx, dependency_words, dst_dir):
    # one-hot to feature
    feature = one_hot_to_feature(one_hot_array, idx)
    # depdency id
    try:
        argmax_id = search_argmax_foreach_idx(feature, idx)
        # --------------
        # normalization
        # --------------
        scaler = MinMaxScaler()
        X = scaler.fit_transform(feature)
        print('StandardScaler')
        print(X)

        clf = joblib.load('lr.pkl')

        pred = clf.predict_proba(X)
        # print('pred')
        # print(pred)
        plt.figure(figsize=(12, 10))
        for w_idx, (x, y) in enumerate(zip(dependency_words, pred)):
            if w_idx <= idx:
                continue
            print(x, y[1])
            plt.bar(x, y[1])
        plt.xticks(dependency_words, rotation='vertical')
        plt.title(
            str(dependency_words[idx])+' - '+str(dependency_words[argmax_id])
            )
        print('idx')
        print(idx)
        plt.savefig(os.path.join(dst_dir, str(idx) + ".png"))
        # plt.show()
        plt.close()

    except ValueError:
        print('!!!!!!!!!!!!!!!! return empty data !!!!!!!!!!!!!!!!')
        print('attempt to get argmax of an empty sequence')
        pass

    return


def eval_run(rne_result_dir, rne_result_file, word_to_id, matrix, dst_dir):
    # --------------
    # load dataset
    # --------------
    lines = load_dataset(rne_result_dir, rne_result_file)

    # ---------------
    # preprocessing
    # ---------------
    dependency_words = split_dependency_words(lines, word_to_id)
    dependency_ids, todo_dependency_words = dependency_words_to_ids(
        dependency_words, word_to_id
    )

    feature_one_hot = np.array([matrix[x] for x in dependency_ids])
    print('feature_one_hot')
    print(feature_one_hot)

    for idx, word in enumerate(todo_dependency_words):
        eval_dependency(
            feature_one_hot,
            idx,
            todo_dependency_words,
            dst_dir
        )

    return 0


def mkdir_if_not_exists(dst_dir):
    if os.path.isdir(dst_dir) is False:
        os.makedirs(dst_dir)
    else:
        pass

    return 0


def split_fname_ext(filename):
    header, ext = os.path.splitext(filename)

    return header


def main():
    # ---------------
    # create feature
    # ---------------
    word_list = cm.generate_wordlist(_CORPUS_DIR)
    word_to_id, id_to_word = cm.generate_word_id_map(word_list)
    matrix = fs.extract_feature(_CORPUS_DIR, 'procedure')
    print('matrix')
    print(matrix)

    # -----------
    # evaluation
    # -----------
    file_list = [os.path.join(_RESULT_DIR, f) for f in os.listdir(_RESULT_DIR)]
    filenames = [os.path.basename(f) for f in file_list]
    dirnames = [os.path.join(_DST_DIR, split_fname_ext(f)) for f in filenames]
    print('dirnames')
    print(dirnames)
    make_dirs = [mkdir_if_not_exists(os.path.join(_DST_DIR, d)) for d in dirnames]
    evaluation = [eval_run(_RESULT_DIR, f, word_to_id, matrix, d)
                  for f, d in zip(file_list, dirnames)]


if __name__ == '__main__':
    main()
