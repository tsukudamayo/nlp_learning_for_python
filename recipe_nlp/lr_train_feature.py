import os

import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

import create_matrix as cm


_LOG_DIR = 'C:/Users/tsukuda/var/data/recipe/orangepage/procedure_3'


def main():
    word_list = cm.generate_wordlist(_LOG_DIR)
    word_to_id, id_to_word = cm.generate_word_id_map(word_list)
    cm.id_to_word_to_txt(id_to_word)

    corpus = np.array([word_to_id[w] for w in word_list])
    vocab_size = len(id_to_word)
    matrix = cm.create_co_matrix(corpus, vocab_size, id_to_word)
    print('matrix')
    print(matrix)

    df = pd.read_csv('lr_train_20190425.csv')
    print(df.head())

    # ---------------------------
    # adjust the number of data
    # ---------------------------
    df_0 = df[df['label'] == 0]
    df_1 = df[df['label'] == 1]
    print('0')
    print(len(df_0))
    print('1')
    print(len(df_1))

    X_0 = df_0[:4000]
    X_1 = df_1

    df = pd.concat([X_0, X_1])
    print(len(df))
    # ---------------------------

    # -------
    # train
    # -------
    X_org_word = df['org'].values
    X_dst_word = df['dst'].values
    y = df['label'].values

    # print('X_org_word')
    # print(X_org_word)
    # print('X_dst_word')
    # print(X_dst_word)
    # print('y')
    # print(y)

    X_org_to_id = np.array([word_to_id[x] for x in X_org_word])
    X_dst_to_id = np.array([word_to_id[x] for x in X_dst_word])

    # print('X_org_to_id')
    # print(X_org_to_id)
    # print('X_dst_to_id')
    # print(X_dst_to_id)

    X_org_feature = np.array([matrix[x] for x in X_org_to_id])
    X_dst_feature = np.array([matrix[x] for x in X_dst_to_id])

    # print('X_org_feature')
    # print(X_org_feature)
    # print('X_dst_feature')
    # print(X_dst_feature)

    X = np.array([np.dot(x, y) for x, y in zip(X_org_feature, X_dst_feature)])
    X = X[:, np.newaxis]

    # print('X')
    # print(X)
    # print(len(X))

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
