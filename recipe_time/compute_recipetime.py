import os
import json
from typing import List
from functools import reduce
from operator import add

import matplotlib.pyplot as plt


_NER_DIR = '../recipe_nlp/orangepage/ner_result'
_NER_FILE = 'detail_126982_ner_result.txt'
_TIME_PARAMS = './action_time/orangepage/action_category.json'

# # 今日の料理
# _GROUND_TRUTH = {
#     '2250_豚肉とれんこんの炒め煮': 15,
#     '2992_冷やしなすのごまソース': 15,
#     '4662_えのき豚': 8,
#     '5578_簡単えびマヨ': 15,
#     '9748_もやしタンタン': 15
# }
# _RECIPE_ID = {
#     '2250_豚肉とれんこんの炒め煮': '豚肉とれんこんの炒め煮',
#     '2992_冷やしなすのごまソース': '冷やしなすのごまソース',
#     '4662_えのき豚': 'えのき豚',
#     '5578_簡単えびマヨ': '5578_簡単えびマヨ',
#     '9748_もやしタンタン': 'もやしタンタン',
# }

# オレンジページ
_GROUND_TRUTH = {
    '白菜と鶏ひき肉のはさみ蒸し': 45,
    'あじフライ': 40,
    '春菊のごまあえ': 20,
    '三色ナムルのビビンバ': 35,
    '簡単酢豚': 15,
    'かぼちゃと鶏肉の甘酢いため': 20
}
_RECIPE_ID = {
    'detail_121930': '白菜と鶏ひき肉のはさみ蒸し',
    'detail_122140': 'あじフライ',
    'detail_118622': '春菊のごまあえ',
    'detail_118984': '三色ナムルのビビンバ',
    'detail_135679': '簡単酢豚',
    'detail_126982': 'かぼちゃと鶏肉の甘酢いため'
}


def summation_time(wakati_array: List, time_params: dict) -> int:
    target = [time_params[n] for n in wakati_array if n in time_params]
    return reduce(add, target)


def extract_actionword(wakati_file: str) -> List:
    strings = open(wakati_file, 'r', encoding='utf-8').read()
    strings = strings.split(' ')
    action_strings = [n for n in strings if n.find('Ac') >= 0]
    action_words = [n.split('/')[0] for n in action_strings]

    return action_words


def debug_params(wakati_array: List, time_params: dict) -> dict:
    debug_log = {}
    for n in wakati_array:
        if n not in time_params:
            continue
        if n in debug_log:
            debug_log[n] += time_params[n]
        else:
            debug_log.update({n: time_params[n]})

    # debug_log = {n: time_params[n] for n in wakati_array if n in time_params}

    return debug_log


def fetch_timeparams(target_file: str) -> dict:
    with open(target_file, 'r', encoding='utf-8') as r:
        jsondata = json.load(r)

    return jsondata


def main():
    target_file = os.path.join(_NER_DIR, _NER_FILE)
    action_words = extract_actionword(target_file)
    time_params = fetch_timeparams(_TIME_PARAMS)
    print(action_words)

    print(summation_time(action_words, time_params))

    print(debug_params(action_words, time_params))

    debug_log = debug_params(action_words, time_params)

    x_value = debug_log.keys()
    y_value = debug_log.values()

    recipe_fname, _ = os.path.splitext(_NER_FILE)
    recipe_id = recipe_fname.split('_ner_result')[0]
    recipe_name = _RECIPE_ID[recipe_id]
    expected_time = summation_time(action_words, time_params)

    result_display = recipe_name + ' '\
      + 'expected = ' + str(expected_time) + ' '\
      + 'ground truth = ' + str(_GROUND_TRUTH[recipe_name])

    plt.title(result_display)
    plt.bar(x_value, y_value)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
