import os
import time
import json
import codecs
from typing import List


_LOG_DIR = './weekcook/ingredient'
_DST_DIR = './weekcook/ingredient_json'


def parse_number_of_serve(strings: str) -> dict:
    serve_dict = {}
    target_strings = '材料'
    parse_strings = strings.strip(target_strings)
    # print('parse_strings')
    # print(parse_strings)
    serve_dict.update({target_strings: parse_strings})

    return serve_dict


def ingredient_div_to_array(data_dir: str, filename: str) -> List[str]:
    filepath = os.path.join(data_dir, filename)
    read_file = open(filepath, 'r', encoding='utf-8')
    read_strings = read_file.read()
    read_file.close()
    delete_space = read_strings.replace(' ', '')
    gather_lf = delete_space.replace('\n\n', '\n')
    delete_lf = gather_lf.replace('\n', ' ')
    split_strings = delete_lf.split(' ')
    strings = [x for x in split_strings if x]

    return strings


def ingredients_to_dict(strings: List[str]) -> dict:
    def debug_print(line: str, serve_dict: dict, key_or_value: str,
                    explanation: str, all_ingredient: dict):
        print(line)
        print('serve_dict')
        print(serve_dict)
        print('tmp_word', tmp_word)

        print(all_ingredient)
        print('################################')
        for k, v in all_ingredient.items():
            print(k, v)
        print('################################')
        time.sleep(0.5)

        return

    all_ingredient = {}
    tmp_word = ''
    count = 0
    for idx, line in enumerate(strings):
        key_or_value = 'key'
        explanation = False
        if idx == 0:
            serve_dict = parse_number_of_serve(line)
            all_ingredient.update(serve_dict)
            continue
        else:
            if line[0] == ('（'):  # an additional explnation about ingredients
                explanation = True
            else:
                pass
            for l in line:
                if l.isdecimal() is True or line == '少々':  # quantity of ingredients
                    key_or_value = 'value'
                else:
                    pass
        # # for debug
        # print('key_or_value')
        # print(key_or_value)
        # print('explanation')
        # print(explanation)
        if explanation is True:
            tmp_word = tmp_word + line
        elif key_or_value == 'value':
            all_ingredient.update({tmp_word: line})
            tmp_word = line
        else:
            tmp_word = line
    # debug_print(line, serve_dict, key_or_value, explanation, all_ingredient)

    return all_ingredient


def main():

    if os.path.isdir(_DST_DIR) is False:
        os.makedirs(_DST_DIR)
    else:
        pass

    data_dir = _LOG_DIR
    file_list = os.listdir(data_dir)
    for f in file_list:
        strings = ingredient_div_to_array(data_dir, f)
        ingredient_dict = ingredients_to_dict(strings)
        dstfname, ext = os.path.splitext(f)
        dstjson = dstfname + '.json'
        dstpath = os.path.join(_DST_DIR, dstjson)
        with codecs.open(dstpath, 'w', encoding='utf-8') as w:
            dump = json.dumps(ingredient_dict, ensure_ascii=False, indent=4)
            w.write(dump)


if __name__ == '__main__':
    main()
