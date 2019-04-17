import os
import sys

import pandas as pd


_LOG_DIR = 'C:/Users/tsukuda/var/data/recipe/orangepage/annotation/dependency'


# _COLUMNS = [
#     'ID', 'number', 'new_word', 'new_tag', 'Agent', 'Targ', 'Dest',
#     'F-comp', 'T-comp', 'F-eq', 'F-part-of', 'F-set', 'T-eq', 'T-part-of',
#     'V-eq', 'V-tm', 'other-mod'
# ]

_COLUMNS = ['ID', 'number', 'new_word', 'new_tag', 'Targ', 'dependency_dst', 'arclabel']


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


def data_preprocessing(filepath, columns_name):
    df = pd.read_csv(filepath, header=0)
    print('columns_name', columns_name)
    df.columns = columns_name

    df['ID'] = df['ID'].astype('int')
    df['Targ'] = df['Targ'].astype('int')

    return df


def main():
    file_list = os.listdir(_LOG_DIR)
    print(file_list)
    dst_filepath = os.path.join(_LOG_DIR, 'all.csv')

    all_df = pd.DataFrame({})
    for f in file_list:
        if f == 'all.csv':
            print('already exist all.csv')
            sys.exit(1)
        print(f)
        read_filepath = os.path.join(_LOG_DIR, f)
        # sample_file = os.path.join(_LOG_DIR, 'weekcook_00000001_combined.csv')
        preprocess_df = data_preprocessing(read_filepath, _COLUMNS)
        df_dependency_tag = convert_id_to_rne(preprocess_df)
        print(df_dependency_tag)
        df_concat = pd.concat([preprocess_df, df_dependency_tag], axis=1)
        print(df_concat.tail)
        target_list = ['new_tag', 'new_word', 'dependency_tag', 'dependency_dst']
        target_df = df_concat[target_list]
        print(target_df.head())
        all_df = pd.concat([all_df, target_df], axis=0)
    all_df = all_df.to_csv(dst_filepath, index=False)


if __name__ == '__main__':
    main()
