import os

import pandas as pd


_LOG_DIR = 'C:/Users/tsukuda/var/data/recipe/weekcook/annotation'


def main():
    file_list = os.listdir(_LOG_DIR)
    print('file_list')
    print(file_list)

    print('**************** file_list ****************')
    for f in file_list:
        if f.find('combined') >= 0 or f.find('all.csv') >= 0 or f.find('lock') >= 0:
            continue
        print(f)
        read_file = os.path.join(_LOG_DIR, f)
        df = pd.read_csv(read_file)
        print(df.columns)
        print(df[['new_word', 'dependnecy_dst', 'arclabel']])


if __name__ == '__main__':
    main()
