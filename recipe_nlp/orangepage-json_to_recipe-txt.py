import os
import json


_DST_DIR = './orangepage/org'
_ORG_DIR = './orangepage/json'


def fetch_recipe(filepath: str) -> dict:
    with open(filepath, 'r', encoding='utf-8') as r:
        jsondata = json.load(r)
        recipedata = jsondata['recipe']

    return recipedata


def main():
    if os.path.exists(_DST_DIR) is False:
        os.makedirs(_DST_DIR)

    file_list = os.listdir(_ORG_DIR)
    print(file_list)

    for f in file_list:
        read_file_path = os.path.join(_ORG_DIR, f)
        recipedata = fetch_recipe(read_file_path)
        file_header, _ = os.path.splitext(f)
        write_fname = file_header + '.txt'
        write_file_path = os.path.join(_DST_DIR, write_fname)
        with open(write_file_path, 'w', encoding='utf-8') as w:
            w.write(recipedata)


if __name__ == '__main__':
    main()
