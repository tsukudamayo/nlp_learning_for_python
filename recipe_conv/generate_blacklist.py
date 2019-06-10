import os
import json
from typing import List


_NER_RESULT_DIR = 'weekcook/ner_result'
_PARAM_STRINGS_DIR = 'weekcook/paramstrings'
_DST_DIR = 'weekcook/blacklist'


def split_food_tag(word: str) -> str:
    if word.find('/F') >= 0:
        food_array = word.split('/')
        food_string = food_array[0]
        if food_string.find('=') >= 0:
            target_string = food_string.replace('=', '')
        else:
            target_string = food_string
    else:
        target_string = ''

    return target_string


def extract_ner_foodlist(ner_result_text: str) -> list:
    read_file = open(ner_result_text, 'r', encoding='utf-8')
    strings = read_file.read()
    read_file.close()
    split_strings = strings.split(' ')
    ner_food_list = [split_food_tag(f) for f in split_strings if split_food_tag(f)]

    return ner_food_list


def is_param_in_parameterstrings(word: str, param_strings: str) -> str:
    if param_strings.find(word) >= 0:
        parameters = word
    else:
        parameters = ''

    return parameters


def compare_foodlist_with_parmeters(food_list: list, param_strings_file: str) -> list:
    read_file = open(param_strings_file, 'r', encoding='utf-8')
    strings = read_file.read()
    read_file.close()

    food_black_list = [is_param_in_parameterstrings(f, strings) for f in food_list
                       if is_param_in_parameterstrings(f, strings)]

    return food_black_list


def main():
    if os.path.isdir(_DST_DIR) is False:
        os.makedirs(_DST_DIR)
    else:
        pass

    filelist = os.listdir(_PARAM_STRINGS_DIR)
    for f in filelist:
        filenumber = str(f.split('_')[1])
        print(filenumber)
        padding_number = '{0:08d}'.format(int(filenumber))
        print(padding_number)

        sample_file = os.path.join(_NER_RESULT_DIR, 'weekcook_' + padding_number + '_ner_result.txt')
        dst_path = os.path.join(_DST_DIR, 'blacklist_' + padding_number + '.json')
        food_list = extract_ner_foodlist(sample_file)
        param_strings_file = os.path.join(_PARAM_STRINGS_DIR, 'weekcook_' + filenumber + '_convrecipe.txt')
        blacklist = compare_foodlist_with_parmeters(food_list, param_strings_file)
        
        with open(dst_path, 'w', encoding='utf-8') as w:
            json.dump(blacklist, w, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
