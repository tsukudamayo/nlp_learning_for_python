import os
import json
from collections import Counter

import matplotlib.pyplot as plt


_AC_DIR = './countAC/kyounoryouri'


def sum_dict(current_dict, next_dict):
    dict1 = Counter(current_dict)
    dict2 = Counter(next_dict)
    summation = dict1 + dict2

    return summation


def main():
    file_list = os.listdir(_AC_DIR)
    output_json = os.path.join(_AC_DIR, 'allcount.json')

    all_sum_dict = {}
    for f in file_list:
        filepath = os.path.join(_AC_DIR, f)
        with open(filepath, 'r', encoding='utf-8') as r:
            jsondata = json.load(r)

        all_sum_dict = sum_dict(all_sum_dict, jsondata)
        all_sum_dict = dict(all_sum_dict)

    with open(output_json, 'w', encoding='utf-8') as w:
        json.dump(all_sum_dict, w, indent=4, ensure_ascii=False)

    counters = Counter(all_sum_dict).most_common(40)
    print('all_sum_dict')
    for c in counters:
        plt.bar(c[0], c[1])
    plt.xticks(rotation=90)
    plt.show()


if __name__ == '__main__':
    main()
