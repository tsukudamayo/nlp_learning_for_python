import os
from typing import List
from functools import reduce
from operator import add

import matplotlib.pyplot as plt


_NER_DIR = '../recipe_nlp/kyounoryouri/ner_result'
_NER_FILE = '9748_もやしタンタン_ner_result.txt'
_GROUND_TRUTH = {
    '2250_豚肉とれんこんの炒め煮': 15,
    '2992_冷やしなすのごまソース': 15,
    '4662_えのき豚': 8,
    '5578_簡単えびマヨ': 15,
    '9748_もやしタンタン': 15
}
_TIME_PARAMS = {
    "む": 1,
    "さら": 1,
    "き": 1,
    "切": 1,
    "熱": 2,
    "炒め": 2,
    "足": 1,
    "戻し入れ": 1,
    "加え": 1,
    "煮": 2,
    "かけ": 1,
    "蒸ら": 2,
    "絞": 1,
    "冷や": 1,
    "切り": 1,
    "混ぜ": 1,
    "盛": 1,
    "のせ": 1,
    "切り落と": 1,
    "入れ": 1,
    "蒸": 2,
    "からめ": 1,
    "ふりかけ": 1,
    "注": 1,
    "煮立て": 2,
    "取り分け": 1
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


def main():
    target_file = os.path.join(_NER_DIR, _NER_FILE)
    action_words = extract_actionword(target_file)
    print(action_words)

    print(summation_time(action_words, _TIME_PARAMS))

    print(debug_params(action_words, _TIME_PARAMS))

    debug_log = debug_params(action_words, _TIME_PARAMS)

    x_value = debug_log.keys()
    y_value = debug_log.values()

    recipe_name, _ = os.path.splitext(_NER_FILE)
    recipe_name = recipe_name.split('_ner_result')[0]
    expected_time = summation_time(action_words, _TIME_PARAMS)

    result_display = recipe_name + ' '\
      + 'expected = ' + str(expected_time) + ' '\
      + 'ground truth = ' + str(_GROUND_TRUTH[recipe_name])

    plt.title(result_display)
    plt.bar(x_value, y_value)
    plt.show()


if __name__ == '__main__':
    main()
