import os

import numpy as np
import pandas as pd


_ANNOTATION_DIR = 'annotation'
_COLUMNS = ['ID', 'number', 'new_word', 'new_tag', 'Targ', 'dependency_dst', 'arclabel']


def find_dependency_tag(df, word):
    print(word)
    target = df[df['new_word'] == word]
    print(target)
    if len(target) > 1:
        print('**************** duplicated ****************')
        select_id = input(
            "the dependency word is duplicated. "\
            "select manually dependency tag's ID."
        )
        dependency_tag = df[df['ID'] == select_id]
        print('dependency_tag')
        print(dependency_tag)
    else:
        dependency_tag = target['new_word']
        print('dependency_tag')
        print(dependency_tag)

    return dependency_tag


def main():
    sample_file = os.listdir(_ANNOTATION_DIR)[1]
    print('sample_file')
    print(sample_file)
    filepath = os.path.join(_ANNOTATION_DIR, sample_file)
    df = pd.read_csv(filepath, names=_COLUMNS, dtype='object')

    dependency_words_list = np.array(
        [find_dependency_tag(df, word) for word in df['dependency_dst'].__iter__()]
    )
    print('dependency_words_list')
    print(dependency_words_list)


if __name__ == '__main__':
    main()
