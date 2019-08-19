import os
import json


_INGREDIENTS_DIR = '../recipe_conv/weekcook/ingredient_json'
_SENTENCES_DIR = './rne_wakachi'
_ACTIONS_DIR = './countAC'

_OUTPUT_DIR = './num_of_params'


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


def main():
    if os.path.exists(_OUTPUT_DIR) is False:
        os.makedirs(_OUTPUT_DIR)
    else:
        pass
    
    file_list = os.listdir(_INGREDIENTS_DIR)
    print('file_list')
    print(file_list)

    for f in file_list:
        read_ingredients_path = os.path.join(_INGREDIENTS_DIR, f)

        sentences_fname, _ = os.path.splitext(f)
        read_sentences_fname = sentences_fname + '_ner_result.txt'
        read_sentences_path = os.path.join(
            _SENTENCES_DIR, read_sentences_fname
        )
 
        actions_fname, _ = os.path.splitext(f)
        read_actions_fname = actions_fname + '_ner_result.json'
        read_actions_path = os.path.join(
            _ACTIONS_DIR, read_actions_fname
        )
        
        dst_filepath = os.path.join(_OUTPUT_DIR, f)
        count_ingredients = count_elements(read_ingredients_path)
        count_ingredients_dict = {
            'number_of_ingredients': count_ingredients
        }
        count_sentences = count_lf(read_sentences_path)
        count_sentences_dict = {
            'number_of_sentences': count_sentences
        }
        count_actions = count_elements(read_actions_path)
        count_actions_dict = {
            'number_of_actions': count_actions
        }
        output_data = output_jsondata(
            count_ingredients_dict,
            count_sentences_dict,
            count_actions_dict,
        )
        data = json.loads(output_data)
        with open(dst_filepath, 'w', encoding='utf-8') as w:
            json.dump(data, w, indent=4, ensure_ascii=False)

            
if __name__ == '__main__':
    main()
