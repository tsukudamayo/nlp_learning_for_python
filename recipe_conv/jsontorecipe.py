import os
import time
import json


_ORG_DIR = 'C:/Users/tsukuda/var/data/recipe/weekcook/recipe_root'
_DST_DIR = './weekcook_db/org'


def main():
    if (os.path.isdir(_DST_DIR)) is False:
        os.makedirs(_DST_DIR)
    else:
        pass
    # filelist = os.listdir(_ORG_DIR)
    # print('filelist', filelist)
    # for f in filelist:
    #     filepath = os.path.join(_ORG_DIR, f)
    #     with open(filepath, 'r', encoding='utf-8') as r:
    #         json_data = json.load(r)
    #         # print(json.dumps(json_data, ensure_ascii=False, indent=4))
    #         print(type(json_data))
    #         print('json_data.items()')
    #         for k, v in json_data.items():
    #             print('k : ', k)
    #             print('v : ', v)
    #         print('Recipe_Directions_Details')
    #         print(json_data['Recipe_Directions_Details'])
    #         print('Two')
    #         for data in json_data['Recipe_Directions_Details']:
    #             print('data : ', data['cooking_procedure_description'])
    #         time.sleep(3)

    filelist = os.listdir(_ORG_DIR)
    for f in filelist:
        # print(f)
        filepath = os.path.join(_ORG_DIR, f)
        # print('filepath', filepath)
        recipe_strings = ''
        with open(filepath, 'r', encoding='utf-8') as r:
            json_data = json.load(r)
            for data in json_data['Recipe_Directions_Details']:
                # print('data : ', data['cooking_procedure_description'])
                recipe_strings += data['cooking_procedure_description']
                recipe_strings += '\n'
            time.sleep(3)
            # print('recipe_strings : ', recipe_strings)

        fname, ext = os.path.splitext(f)
        outputfile = os.path.join(_DST_DIR, fname + '.txt')
        with open(outputfile, 'w', encoding='utf-8') as w:
            w.write(recipe_strings)

if __name__ == '__main__':
    main()
