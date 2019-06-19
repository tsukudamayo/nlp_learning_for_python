import os
import json
from typing import List


_ORG_DIR = 'weekcook/paramstrings'
_DST_DIR = 'weekcook/warnings'
_BLACKLIST_DIR = 'weekcook/blacklist'


def insert_warnings(word: str, param_strings: str) -> str:
    warning_emoji = '<font color="red">⚠</font>'
    warning_strings = warning_emoji + word
    replace_strings = param_strings.replace(word, warning_strings)

    return replace_strings


def black_list_to_array(black_list_file: str) -> List:
    with open(black_list_file, 'r', encoding='utf-8') as w:
        read_file = json.load(w)
    black_list_array = read_file

    return black_list_array


def annotate_warnings(param_strings_file: str, black_list: List) -> str:
    read_file = open(param_strings_file, 'r', encoding='utf-8')
    strings = read_file.read()
    read_file.close()
    annotate_strings = strings
    for word in black_list:
        annotate_strings = insert_warnings(word, annotate_strings)

    return annotate_strings


def main():
    if os.path.isdir(_DST_DIR) is False:
        os.makedirs(_DST_DIR)

    file_list = os.listdir(_ORG_DIR)
    for f in file_list:
        bname = os.path.basename(f)
        fname, ext = os.path.splitext(bname)
        split_fname_array = fname.split('_')[1]
        number = int(split_fname_array)  # 00000001 -> 1
        zeropadding_number = '{0:08d}'.format(number)

        org_file = os.path.join(_ORG_DIR, f)
        blacklist_file = os.path.join(_BLACKLIST_DIR, 'blacklist_' + zeropadding_number + '.json')
        dst_file = os.path.join(_DST_DIR, 'weekcook_' + str(number) + '_warnings.txt')

        black_list_array = black_list_to_array(blacklist_file)
        annotate_strings = annotate_warnings(org_file, black_list_array)
        with open(dst_file, 'w', encoding='utf-8') as w:
            w.write(annotate_strings)


if __name__ == '__main__':
    main()
