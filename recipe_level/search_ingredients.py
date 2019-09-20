import os
import json

_HOME = os.path.expanduser("~")
_RECIPEDB_DIR = os.path.join(_HOME, 'var/data/recipe/weekcook/recipe_root')

_OUTPUT_DIR = './search_ingredients'
_OUTPUT_FILES = 'search_ingredients.json'


def extarct_from_weekcook_db(filepath: str) -> dict:
    nest_1 = "Recipe_Infos"
    nest_2 = "Recipe_Ingredients"
    nest_3 = "Four"
    with open(filepath, 'r', encoding='utf-8') as r:
        json_data = json.load(r)

        target_data = json_data[nest_1]
        recipe_id = target_data[0]['recipe_id']
        recipe_title = target_data[0]['recipe_name']

        target_data = json_data[nest_2]
        target_data = target_data[nest_3]

        ingredients = []
        for d in target_data:
            ingredients.append(d['ingredient_name'])

        set_ingredients = set(ingredients)
        ingredients = sorted(list(set_ingredients))
        numofingredients = len(ingredients)

        target_dict = {
            'id': recipe_id,
            'title': recipe_title,
            'ingredients': ingredients,
            'numof': numofingredients
        }

    return target_dict


def main():
    if os.path.exists(_OUTPUT_DIR) is False:
        os.makedirs(_OUTPUT_DIR)
    else:
        pass

    file_list = os.listdir(_RECIPEDB_DIR)

    extract_datas = []
    for f in file_list:
        read_filepath = os.path.join(_RECIPEDB_DIR, f)
        extract_data = extarct_from_weekcook_db(read_filepath)
        extract_datas.append(extract_data)

    dst_filepath = os.path.join(_OUTPUT_DIR, _OUTPUT_FILES)
    with open(dst_filepath, 'w', encoding='utf-8') as w:
        json.dump(extract_datas, w, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
