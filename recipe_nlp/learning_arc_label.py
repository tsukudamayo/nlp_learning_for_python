import os
import time

import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
from sklearn.metrics import confusion_matrix, classification_report

import create_matrix as cm


_ANNOTATION_DIR = 'annotation'
_RECIPE_DIR = 'C:/Users/tsukuda/var/data/recipe/weekcook/procedure_3'


def generate_arc_category_data(log_dir):
    file_list = os.listdir(log_dir)
    train_data = pd.DataFrame({})
    for f in file_list:
        if f.find('combined') >= 0 or\
          f.find('all.csv') >= 0 or\
          f.find('lock') >= 0:
            continue
        print(f)
        read_file = os.path.join(_ANNOTATION_DIR, f)
        df = pd.read_csv(read_file)
        tmp_df = df[['new_word', 'dependnecy_dst', 'arclabel']]
        tmp_df = tmp_df.dropna()
        train_data = pd.concat([train_data, tmp_df], axis=0)
    train_data.to_csv('arc_train.csv', index=False)

    return train_data


def category_mapping(unique_category_array):
    return {k: v for v, k in enumerate(unique_category_array)}


def convert_category_to_numerical(category_array, category_map):
    return np.array([category_map[x] for x in category_array])


def extend_columns(array_1, array_2):

    return np.array(
        [np.vstack((x, y)).flatten() for x, y in zip(array_1, array_2)])


def main():
    # -----------------------------
    # create corpus and co-matirx
    # -----------------------------
    word_list = cm.generate_wordlist(_RECIPE_DIR)
    word_to_id, id_to_word = cm.generate_word_id_map(word_list)
    # output corpus to txt
    cm.id_to_word_to_txt(id_to_word)
    corpus = np.array([word_to_id[w] for w in word_list])
    vocab_size = len(id_to_word)
    matrix = cm.create_co_matrix(corpus, vocab_size, id_to_word)
    print('matrix')
    print(matrix)

    # ---------------------
    # generate label data
    # ---------------------
    label = np.array([x for x in id_to_word.values()])
    label = label[:, np.newaxis]
    print('label')
    print(label)

    # ------------------------
    # generate category data
    # ------------------------
    category_label_data = generate_arc_category_data(_ANNOTATION_DIR)
    unique_category = category_label_data['arclabel'].unique()
    print(category_label_data.head())
    print(category_label_data.tail())
    print(unique_category)

    # ----------------------------
    # generate feature and label
    # ----------------------------
    category_label_data['feature_org_idx'] = category_label_data['new_word']\
      .apply(lambda x: word_to_id[x])
    category_label_data['feature_dst_idx'] = category_label_data['dependnecy_dst']\
      .apply(lambda x: word_to_id[x])
    category_label_data['feature_org'] = category_label_data['feature_org_idx']\
      .apply(lambda x: matrix[x])
    category_label_data['feature_dst'] = category_label_data['feature_dst_idx']\
      .apply(lambda x: matrix[x])
    print('category_label_data')
    print(category_label_data)

    extend_feature = extend_columns(
        category_label_data['feature_org'], category_label_data['feature_dst']
    )
    print('extend_feature')
    print(extend_feature)
    print(extend_feature.shape)
    X = extend_feature

    category_map = category_mapping(unique_category)
    print('category_map')
    print(category_map)
    category_label = category_label_data['arclabel'].values
    category_label = category_label.flatten()
    print('category_label')
    print(category_label)
    y = convert_category_to_numerical(category_label, category_map)
    print('y')
    print(y)

    # ----------
    # training
    # ----------
    print('dataset size')
    print('X: {0} , y:{1}'.format(X.shape, y.shape))
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0
    )
    clf = SVC(kernel='linear', C=1).fit(X_train, y_train)
    t0 = time.time()
    clf.fit(X_train, y_train)
    joblib.dump(word_to_id, 'word_to_id.pkl')
    joblib.dump(matrix, 'matrix.pkl')
    joblib.dump(clf, 'svc.pkl')
    t1 = time.time()
    print('exec time : {}'.format(t1 - t0))

    # ------------
    # validation
    # ------------
    prediction_map = {k: v for v, k in category_map.items()}
    joblib.dump(prediction_map, 'prediction_map.pkl')
    print(clf.score(X_test, y_test))
    print(confusion_matrix(y_test, clf.predict(X_test)))
    print(classification_report(
        y_test,
        clf.predict(X_test),
        target_names=prediction_map.values()
    ))

    # tamanegi test
    print('**************** tamanegi-surioro ****************')
    onion_id = word_to_id['玉ねぎ']
    print('onion_id')
    print(onion_id)
    suri_id = word_to_id['すりおろ']
    print('suri_id')
    print(suri_id)
    onion_feature = matrix[0]
    suri_feature = matrix[2]
    sample_feature = np.hstack((onion_feature, suri_feature)).flatten()
    print('sample_feature')
    print(sample_feature)
    print(clf.predict([sample_feature]))
    pred = clf.predict([sample_feature])
    print(prediction_map[pred[0]])

    # model load
    load_model = joblib.load('svc.pkl')
    print('load_model')
    print(load_model)


if __name__ == '__main__':
    main()

    # test
    # # test data
    # X_1 = np.array([[-1], [-2], [1], [2]])
    # X_2 = np.array([[-1], [-1], [1], [1]])
    # # y = np.array([1, 1, 2, 2])
    # category_map = category_mapping(unique_category)
    # category_y = np.array(['Targ', 'Targ', 'Dest', 'Dest'])
    # y = convert_category_to_numerical(category_y, category_map)
    # print('y')
    # print(y)

    # X_r = np.hstack((X_1, X_2))
    # clf = SVC(gamma='auto')
    # clf.fit(X_r, y)
    # print(clf.predict([[-0.8, -1]]))
