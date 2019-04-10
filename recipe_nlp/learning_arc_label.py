import os

import numpy as np
import pandas as pd
from sklearn.svm import SVC


_LOG_DIR = 'annotation'


def generate_arc_category_data(log_dir):
    file_list = os.listdir(log_dir)
    train_data = pd.DataFrame({})
    for f in file_list:
        if f.find('combined') >= 0 or\
          f.find('all.csv') >= 0 or\
          f.find('lock') >= 0:
            continue
        print(f)
        read_file = os.path.join(_LOG_DIR, f)
        df = pd.read_csv(read_file)
        tmp_df = df[['new_word', 'dependnecy_dst', 'arclabel']]
        tmp_df = tmp_df.dropna()
        train_data = pd.concat([train_data, tmp_df], axis=0)
    train_data.to_csv('arc_train.csv', index=False)

    return train_data


def category_mapping(category_array):
    category_map = {
        'Targ': 1,
        'Dest': 2,
    }

    return np.array([category_map[x] for x in category_array])


def main():
    category_label_data = generate_arc_category_data(_LOG_DIR)
    print(category_label_data.head())
    print(category_label_data.tail())
    print(category_label_data['arclabel'].unique())

    X_1 = np.array([[-1], [-2], [1], [2]])
    X_2 = np.array([[-1], [-1], [1], [1]])
    # y = np.array([1, 1, 2, 2])
    category_y = np.array(['Targ', 'Targ', 'Dest', 'Dest'])
    y = category_mapping(category_y)

    X_r = np.hstack((X_1, X_2))
    clf = SVC(gamma='auto')
    clf.fit(X_r, y)
    print(clf.predict([[-0.8, -1]]))
    

if __name__ == '__main__':
    main()
