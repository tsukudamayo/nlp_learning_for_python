import os
import json


_ORG_DIR = 'C:/Users/tsukuda/var/data/recipe/weekcook/recipe_root'


def main():
    filelist = os.listdir(_ORG_DIR)
    print('filelist', filelist)


if __name__ == '__main__':
    main()
