import os
import time

import numpy as np
import pandas as pd


_ANNOTATION_DIR = 'annotation'
_COLUMNS = ['ID', 'number', 'new_word', 'new_tag', 'Targ', 'dependency_dst', 'arclabel']


def generate_dependency_pair(df):
    return np.array(
        [(x, y) for (x, y) in zip(df['new_word'], df['dependency_dst'])])


def has_dependency_or_not(array1, array2):
    if all(array1 == array2):
        return 1
    else:
        return 0


def generate_depencency_list_foreach_words(df, idx):
    df['org'] = df['new_word'].apply(
        lambda x: df['new_word'][idx]
    )
    df['dst'] = df['new_word'].apply(
        lambda x: x
    )
    # print('org')
    # print(df['org'])
    # print('dst')
    # print(df['dst'])

    df['org'] = df['dst'].apply(
        lambda x: df['new_word'][idx]
    )
    df['dst'] = df['new_word'][idx+1:]
    df_new = pd.concat([df['org'], df['dst']], axis=1)
    # print(df_new)
    df_new = df_new.dropna(how='any', axis=0)
    # print(df_new)

    return df_new


def labelling_dependencies(df, dependency_pair, idx):
    nd_new = df.values
    # print('nd_new')
    # print(nd_new)
    nd_new_label = np.array(
        [has_dependency_or_not(x, dependency_pair[idx]) for x in nd_new]
    )
    nd_new_label = nd_new_label[:, np.newaxis]
    nd_new = np.hstack((nd_new, nd_new_label))
    # print('nd_new')
    # print(nd_new)

    return nd_new


def convert_ndarray_to_df(ndarray):
    column_names = ['org', 'dst', 'label']
    df_join = pd.DataFrame(ndarray)
    df_join.columns = column_names
    # print('df_join')
    # print(df_join)

    return df_join


def generate_all_data(df, idx):
    # generate_all_dependency_list
    df_new = generate_depencency_list_foreach_words(df, idx)

    # label data
    dependency_pair = generate_dependency_pair(df)

    # convert ndarray
    nd_new = labelling_dependencies(df_new, dependency_pair, idx)

    # convert pandas dataframe
    df_join = convert_ndarray_to_df(nd_new)

    return df_join


def join_dataframe(df, all_df, idx):
    df_join = generate_all_data(df, idx)
    all_df = pd.concat([all_df, df_join])

    return all_df


def main():
    sample_file = os.listdir(_ANNOTATION_DIR)[0]
    print('sample_file')
    print(sample_file)
    filepath = os.path.join(_ANNOTATION_DIR, sample_file)
    df = pd.read_csv(filepath, names=_COLUMNS, header=0)
    print(df.head())

    t0 = time.time()
    file_list = os.listdir(_ANNOTATION_DIR)
    all_df = pd.DataFrame({})
    for f in file_list:
        filepath = os.path.join(_ANNOTATION_DIR, f)
        df = pd.read_csv(filepath, names=_COLUMNS, header=0)
        # join all dataframe
        for idx in range(len(df)):
            all_df = join_dataframe(df, all_df, idx)
    t1 = time.time()
    all_df = all_df.reset_index(drop=True)
    print('all_df')
    print(all_df)
    all_df.to_csv('lr_train_20190425.csv')
    print('time')
    print(t1 - t0)


if __name__ == '__main__':
    main()
