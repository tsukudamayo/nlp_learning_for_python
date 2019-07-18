import os
import json
import time


_ORG_DIR = 'C:/Users/tsukuda/var/data/recipe/weekcook/recipe_root'
_DST_DIR = './weekcook/ingredient_json'


def main():
    if(os.path.isdir(_DST_DIR)) is False:
        os.makedirs(_DST_DIR)
    else:
        pass


    file_list = os.listdir(_ORG_DIR)
    for f in file_list:
        print('file : ', f)
        new_data = {}
        filepath = os.path.join(_ORG_DIR, f)
        with open(filepath, 'r', encoding='utf-8') as r:
            json_data = json.load(r)
        print('json_data', json_data['Recipe_Ingredients']['Two'])
        for data in json_data['Recipe_Ingredients']['Four']:
            print(data)
            new_data.update({data["ingredient_name"]: data["quantity_string"]})

        fname, ext = os.path.splitext(f)
        outputpath = os.path.join(_DST_DIR, fname + '.json')
        print('new data : ', new_data)
        with open(outputpath, 'w', encoding='utf-8') as w:
            dump = json.dumps(new_data, ensure_ascii=False, indent=4)
            w.write(dump)


if __name__ == '__main__':
    main()
