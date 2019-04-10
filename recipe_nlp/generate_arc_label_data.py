import os

import pandas as pd


_LOG_DIR = 'C:/Users/tsukuda/var/data/recipe/weekcook/annotation'


def convert_id_to_word(df, idx):
    try:
        dependency = list(df[df['Unnamed: 0'] == idx]['new_word'])[0]
    except IndexError:
        dependency = ''

    return dependency


def main():
    file_list = os.listdir(_LOG_DIR)
    print('file_list')
    print(file_list)

    for f in file_list:
        if f.find('all') >= 0 or f.find('lock') >= 0 or f.find('arclabel') >= 0:
            continue
        print(f)
        read_file = os.path.join(_LOG_DIR, f)
        dst_file = read_file.replace('combined', 'arclabel')
        df = pd.read_csv(read_file)
        df = df.dropna(thresh=5)
        print(df.head())
        print(f)
        df = df.astype({'Targ': int})
        print(df.dtypes)
        df['dependnecy_dst'] = df['Targ'].apply(
            lambda x: convert_id_to_word(df, x)
        )
        df['arclabel'] = df['Targ'].apply(
            lambda x: ''
        )
        df.to_csv(dst_file, index=False)


if __name__ == '__main__':
    main()
