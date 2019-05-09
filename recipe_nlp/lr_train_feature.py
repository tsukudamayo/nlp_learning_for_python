import os, gc

import numpy as np
import pandas as pd
import scipy.sparse as sp

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.externals import joblib

import create_matrix as cm
import featureselect as fs


_CORPUS_DIR = 'C:/Users/tsukuda/var/data/recipe/orangepage/procedure_3'


def main():
    word_list = cm.generate_wordlist(_CORPUS_DIR)
    word_to_id, id_to_word = cm.generate_word_id_map(word_list)
    cm.id_to_word_to_txt(id_to_word)
    corpus = np.array([word_to_id[w] for w in word_list])
    vocab_size = len(id_to_word)

    df = pd.read_csv('lr_train_20190425.csv')
    print(df.head())

    # # ---------------------------
    # # adjust the number of data
    # # ---------------------------
    # df_0 = df[df['label'] == 0]
    # df_1 = df[df['label'] == 1]
    # print('0')
    # print(len(df_0))
    # print('1')
    # print(len(df_1))

    # X_0 = df_0[:4000]
    # X_1 = df_1

    # df = pd.concat([X_0, X_1])
    # print(len(df))
    # # ---------------------------

    # -------
    # train
    # -------
    X_org_word = df['org'].values
    X_dst_word = df['dst'].values
    y = df['label'].values

    X_org_to_id = np.array([word_to_id[x] for x in X_org_word])
    X_dst_to_id = np.array([word_to_id[x] for x in X_dst_word])
    print('X_org_to_id')
    print(type(X_org_to_id))
    print('X_dst_to_id')
    print(type(X_dst_to_id))

    print('X_ort_to_id')
    print(X_org_to_id)
    print('X_dst_to_id')
    print(X_dst_to_id)

    del df
    del X_org_word, X_dst_word
    del word_to_id, id_to_word
    gc.collect()

    matrix = fs.extract_feature(_CORPUS_DIR, 'procedure')
    print('matrix')
    print(matrix)
    print('matrix shape')
    print(matrix.shape)
    org_split_ids = np.array_split(X_org_to_id, 10)
    dst_split_ids = np.array_split(X_dst_to_id, 10)
    # print('org_split_ids')
    # print(org_split_ids)
    # print(len(org_split_ids))
    # print('dst_split_ids')
    # print(dst_split_ids)
    # print(len(dst_split_ids))
    X = np.zeros((len(y)))
    # print('X')
    # print(X)
    # print(X.shape)
    for org_ids, dst_ids in zip(org_split_ids, dst_split_ids):
        # print('org_ids, dst_ids :', org_ids, dst_ids)
        for i, (dst, org) in enumerate(zip(org_ids, dst_ids)):
            # print('dst, org', dst, org)
            X_org_feature = np.array([matrix[org]])
            # print('X_org_feature')
            # print(X_org_feature)
            # print(X_org_feature.shape)
            X_dst_feature = np.array([matrix[dst]])
            # print('X_dst_feature')
            # print(X_dst_feature)
            # print(X_dst_feature.shape)
            # print('dst, org', dst, org)
            # print('X_org_feature')
            # print(X_org_feature)
            # print('X_dst_feature')
            # print(X_dst_feature)
            X[dst] = np.array([np.dot(x, y) for x, y in zip(X_org_feature, X_dst_feature)])

    X = X[:, np.newaxis]
    print('np.newaxis')
    print(X)

    print('X')
    print(X)
    print(X.shape)
    print('y')
    print(y.shape)

    scaler = MinMaxScaler()
    X_scaler = scaler.fit_transform(X)
    print('StandardScaler')
    print(X_scaler)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaler, y, test_size=0.2, random_state=0
    )

    clf = LogisticRegression(
        random_state=0,
        solver='liblinear',
    ).fit(X_train, y_train)

    joblib.dump(clf, 'lr.pkl')

    # ------
    # eval
    # ------
    print(clf.score(X_test, y_test))
    pred = clf.predict(X_test)
    print(accuracy_score(pred, y_test))
    print(classification_report(pred, y_test))
    print(confusion_matrix(pred, y_test))


    print(clf.predict_proba(X_test))


if __name__ == '__main__':
    main()
