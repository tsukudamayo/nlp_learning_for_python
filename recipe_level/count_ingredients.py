import os
import json

_HOME = os.path.expanduser("~")
_INGREDIENTS_DIR = '../recipe_conv/weekcook/ingredient_json'
_SENTENCES_DIR = './rne_wakachi'
_ACTIONS_DIR = './countAC'
_RECIPEDB_DIR = os.path.join(_HOME, 'var/data/recipe/weekcook/recipe_root')

_OUTPUT_DIR = './num_of_params'


def count_action_category(action_category: str, text_file: str, category_file: str) -> int:
    category_count = 0
    strings = open(text_file, 'r', encoding='utf-8').read()
    words = strings.split(' ')
    print('words', words)

    with open(category_file, 'r', encoding='utf-8') as r:
        data = json.load(r)

    print('action category : ', data)
    for w in words:
        try:
            if data[w] == action_category:
                print(w)
                category_count += 1
            else:
                pass
        except KeyError:
            pass

    return category_count


def count_elements(json_file: str) -> int:
    with open(json_file, 'r', encoding='utf-8') as r:
        data = json.load(r)

    return len(data)


def count_lf(text_file: str) -> int:
    strings = open(text_file, 'r', encoding='utf-8').read()
    data = strings.split(' ')

    return data.count('。')


def output_jsondata(*args) -> str:
    print('args', args)
    output = [d for d in args]
    print('output : ', output)

    return json.dumps(output)


def fetch_recipename(json_file: str) -> str:
    with open(json_file, 'r', encoding='utf-8') as r:
        input_data = json.load(r)
        recipe_name = input_data['Recipe_Infos'][0]['recipe_name']
        print(recipe_name)

    return recipe_name


def compute_mean(dict_data: dict) -> float:
    all_value = [v for v in dict_data.values() if type(v) is not str]
    length_all_value = len(all_value)
    mean_value = float(sum(all_value) / length_all_value)

    return mean_value


def main():
    if os.path.exists(_OUTPUT_DIR) is False:
        os.makedirs(_OUTPUT_DIR)
    else:
        pass

    file_list = os.listdir(_INGREDIENTS_DIR)

    # ---------------- #
    # define index key #
    # ---------------- #
    recipename_dict = {'key': 'recipename'}
    ingredints_dict = {'key': 'ingredients'}
    sentences_dict = {'key': 'sentences'}
    actions_dict = {'key': 'actions'}
    for f in file_list:
        print(f)
        # --------------- #
        # define filepath #
        # --------------- #
        # ingredients path
        read_ingredients_path = os.path.join(_INGREDIENTS_DIR, f)
        read_key_fname, _ = os.path.splitext(f)
        # sentences path
        sentences_fname, _ = os.path.splitext(f)
        read_sentences_fname = sentences_fname + '_ner_result.txt'
        read_sentences_path = os.path.join(
            _SENTENCES_DIR, read_sentences_fname
        )
        # actions path
        actions_fname, _ = os.path.splitext(f)
        read_actions_fname = actions_fname + '_ner_result.json'
        read_actions_path = os.path.join(
            _ACTIONS_DIR, read_actions_fname
        )
        # recipedb(recipename) path
        read_recipedb_path = os.path.join(_RECIPEDB_DIR, f)

        # ------------------ #
        # fetch target value #
        # ------------------ #
        target_recipename = fetch_recipename(read_recipedb_path)
        count_ingredients = count_elements(read_ingredients_path)
        count_sentences = count_lf(read_sentences_path)
        count_actions = count_elements(read_actions_path)

        recipename_dict.update({read_key_fname: target_recipename})
        ingredints_dict.update({read_key_fname: count_ingredients})
        sentences_dict.update({read_key_fname: count_sentences})
        actions_dict.update({read_key_fname: count_actions})

    # compute mean each objects
    ingredients_score_mean = compute_mean(ingredints_dict)
    sentences_score_mean = compute_mean(sentences_dict)
    actions_score_mean = compute_mean(actions_dict)

    # add mean to each object dict
    ingredints_dict.update({'mean': ingredients_score_mean})
    sentences_dict.update({'mean': sentences_score_mean})
    actions_dict.update({'mean': actions_score_mean})

    # output data
    output_data = output_jsondata(
        recipename_dict,
        ingredints_dict,
        sentences_dict,
        actions_dict,
    )
    data = json.loads(output_data)
    dst_filepath = os.path.join(_OUTPUT_DIR, 'radar-chart.json')
    with open(dst_filepath, 'w', encoding='utf-8') as w:
        json.dump(data, w, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
