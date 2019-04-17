import os
import sys

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

import create_matrix as cm


_LOG_DIR = 'C:/Users/tsukuda/var/data/recipe/orangepage/annotation/dependency'
_LIKELIHOOD_DIR = 'C:/Users/tsukuda/var/data/recipe/orangepage/test/likelihood'
_TRAIN_DIR = 'C:/Users/tsukuda/var/data/recipe/orangepage/lr_train'
_RECIPE_DIR = 'C:/Users/tsukuda/local/nlp_learning_for_python/recipe_nlp/procedure_3'
_CATEGORY_DATA = 'rne_category.txt'

_COLUMNS = ['ID', 'number', 'new_word', 'new_tag', 'Targ', 'dependency_dst', 'arclabel']


def convert_txt_to_dict(filepath):
    txt_to_dict = {}
    with open(filepath, 'r', encoding='utf-8') as r:
        lines = r.readlines()
    for line in lines:
        line = line.rstrip('\n')
        line = line.split(':')
        line_dict = {line[1]: int(line[0])}
        txt_to_dict.update(line_dict)

    return txt_to_dict


def data_preprocessing(filepath, columns_name):
    df = pd.read_csv(filepath, header=0)
    print('columns_name', columns_name)
    df.columns = columns_name

    df['ID'] = df['ID'].astype('int')
    df['Targ'] = df['Targ'].astype('int')

    return df


def convert_id_to_rne(df):
    dependency_tag_list = []
    before_v = 0
    for idx, v in df['Targ'].iteritems():
        print('v=', v)
        print(idx)
        if v != -1:
            dependency_tag = df[df['ID'] == v]['new_tag'].values
            print('dependency_tag')
            print(dependency_tag)
            dependency_tag = str(dependency_tag[0])
        elif v == -1:
            # df[df['ID'] == v]['new_tag'] = 'ROOT'
            # dependency_tag = df[df['ID'] == v]['new_tag'].values
            dependency_tag = 'ROOT'
        before_v = v
        print(type(dependency_tag))
        print(dependency_tag)
        dependency_tag_list.append(dependency_tag)

    # print(dependency_tag_list)

    df_dependency_tag = pd.DataFrame({
        'dependency_tag': dependency_tag_list
    })

    return df_dependency_tag



def main():
    # -------------
    # load dataset
    # -------------
    make_dirs = [_LIKELIHOOD_DIR, _TRAIN_DIR]
    for i in make_dirs:
        if os.path.isdir(i) is False:
            os.makedirs(i)
        else:
            pass

    category_data = _CATEGORY_DATA
    rne_map = convert_txt_to_dict(category_data)
    print('rne_map')
    print(rne_map)

    train_data_list = os.listdir(_LOG_DIR)
    print('train_data')
    dst_filepath = os.path.join(_LOG_DIR, 'all.csv')

    all_df = pd.DataFrame({})
    for f in train_data_list:
        if f == 'all.csv':
            print('already exist all.csv')
            sys.exit(1)
        print(f)
        read_filepath = os.path.join(_LOG_DIR, f)
        preprocess_df = data_preprocessing(read_filepath, _COLUMNS)
        df_dependency_tag = convert_id_to_rne(preprocess_df)
        print(df_dependency_tag)
        df_concat = pd.concat([preprocess_df, df_dependency_tag], axis=1)
        print(df_concat.tail)
        target_list = ['new_tag', 'new_word', 'dependency_tag', 'dependency_dst']
        target_df = df_concat[target_list]
        all_df = pd.concat([all_df, target_df], axis=0)
    all_df.to_csv(dst_filepath, index=False)

    dst_file = os.path.join(_TRAIN_DIR, 'lr_train.csv')
    df = all_df
    print('all_df')
    print(all_df)
    print('df')
    print(df.head())
    del all_df

    # ----------------------------
    # create corpus and co-matrix
    # ----------------------------
    word_list = cm.generate_wordlist(_RECIPE_DIR)
    word_to_id, id_to_word = cm.generate_word_id_map(word_list)
    cm.id_to_word_to_txt(id_to_word)
    corpus = np.array([word_to_id[w] for w in word_list])
    vocab_size = len(id_to_word)
    matrix = cm.create_co_matrix(corpus, vocab_size, id_to_word)
    print(matrix)

    # -------------------------
    # label to one-hot-encode
    # -------------------------
    enc = OneHotEncoder()
    label_data = df['new_tag'].values
    label_reshape = label_data[:, np.newaxis]
    print('label_data')
    print(label_data)
    enc.fit(label_reshape)
    onehotlabel = enc.transform(label_reshape).toarray()
    print('onehotlabel')
    print(onehotlabel)

    # ------------------------------------
    # join feature and one-hot-encode
    # ------------------------------------
    category_label_data = df
    category_label_data['feature_org_idx'] = category_label_data['new_word']\
      .apply(lambda x: word_to_id[x])
    category_label_data['feature_org'] = category_label_data['feature_org_idx']\
      .apply(lambda x: matrix[x])

    feature_matrix = category_label_data['feature_org'].values
    train_feature_matrix = np.array([x.flatten() for x in feature_matrix])
    print('train_feature_matrix')
    print(train_feature_matrix)
    print(train_feature_matrix.shape)

    print(onehotlabel.shape)
    train_data = np.hstack((train_feature_matrix, onehotlabel))
    print(train_data)
    print(train_data.shape)

    # filepath = 'lr_train.csv'
    # df = pd.read_csv(filepath)
    # print(df.head())

    # X = df['rne'].values
    # X = X[:, np.newaxis]
    # y = df['dependency'].values
    # y = y[:, np.newaxis]

    # X_train, X_test, y_train, y_test = train_test_split(
    #     X, y, test_size=0.2, random_state=42
    # )
    # print('X_train', X_train.shape)
    # print('X_test', X_test.shape)
    # print('y_train', y_train.shape)
    # print('y_test', y_test.shape)

    # clf = LogisticRegression(
    #     random_state=0,
    #     solver='liblinear',
    # ).fit(X_train, y_train)

    # print('test probability')
    # print(clf.predict_proba(X_test))

    # print('class')
    # print(clf.classes_)

    # print('coef')
    # print(clf.coef_)

    # print('intercept')
    # print(clf.intercept_)
    
    # print('score')
    # print(clf.score(X_test, y_test))

    # likelihood_data = {
    #     0: clf.predict_proba([np.array([0])]).flatten(),
    #     1: clf.predict_proba([np.array([1])]).flatten(),
    #     2: clf.predict_proba([np.array([2])]).flatten(),
    #     3: clf.predict_proba([np.array([3])]).flatten(),
    #     4: clf.predict_proba([np.array([4])]).flatten(),
    #     5: clf.predict_proba([np.array([5])]).flatten(),
    #     6: clf.predict_proba([np.array([6])]).flatten(),
    #     7: clf.predict_proba([np.array([7])]).flatten(),
    #     8: clf.predict_proba([np.array([8])]).flatten(),
    # }

    # print('likelihood')
    # print(likelihood_data)

    # df_likelihood = pd.DataFrame(likelihood_data)
    # print(df_likelihood)

    # dst_filepath = os.path.join(_DST_DIR, 'likelihood.csv')
    # df_likelihood.to_csv(dst_filepath, index=True)

if __name__ == '__main__':
    main()
