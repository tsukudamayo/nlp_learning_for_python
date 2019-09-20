import os
import json


_HOME = os.environ['HOME']
_ORG_DIR = os.path.join(_HOME, 'var/data/weekcook_recipe_data/recipe')
_DST_DIR = os.path.join(_HOME, 'var/data/weekcook_convert_data/recipe')


def main():
    if os.path.isdir(_DST_DIR) is False:
        os.makedirs(_DST_DIR)
    else:
        pass

    file_list = os.listdir(_ORG_DIR)
    print(file_list)

    for f in file_list:
        sample_file_path = os.path.join(_ORG_DIR, f)
        with open(sample_file_path, 'r', encoding='utf-8') as r:
            jsondata = json.load(r)
            print(json.dumps(jsondata, indent=4, ensure_ascii=False))
        dst_file_path = os.path.join(_DST_DIR, f)
        with open(dst_file_path, 'w', encoding='utf-8') as w:
            json.dump(jsondata, w, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
