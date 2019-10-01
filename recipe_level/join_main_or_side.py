import os
import json

import numpy as np
import pandas as pd


_ORG_FILE = './search_ingredients/dbdata_ingredients_20190924.json'
_TARGET_FILE = './main_or_side/maindish_or_sidedish_20190925_322.csv'
_DST_FILE = './search_ingredients/dbdata_ingredients.json'


def main():
    with open(_ORG_FILE, 'r', encoding='utf-8') as r:
        jsondata = json.load(r)
    df = pd.read_csv(_TARGET_FILE, delimiter=',', encoding='utf-8')
    print(df.head())

    search_json = [n for n in jsondata if n['id'] == 10]
    print(search_json)

    array_length = len(df)
    header_index = df.columns.values
    print(header_index)
    id_idx = np.where(header_index == '旧レシピID')[0][0]
    print(id_idx)
    main_or_side_id = np.where(header_index =='主菜・副菜')[0][0]
    print(main_or_side_id)

    target_array = []
    for idx in range(array_length):
        recipe_id = df.iloc[idx, id_idx]
        print('recipe_id : ', recipe_id)
        ref_orgdata = [n for n in jsondata if n['id'] == recipe_id][0]
        print('ref_orgdata : ', ref_orgdata)
        target_data = df.iloc[idx, main_or_side_id]
        print('target_data : ', target_data)
        main_or_side_data = {'main_or_side': target_data}
        ref_orgdata.update(main_or_side_data)
        target_array.append(ref_orgdata)

    with open(_DST_FILE, 'w', encoding='utf-8') as w:
        json.dump(target_array, w, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
