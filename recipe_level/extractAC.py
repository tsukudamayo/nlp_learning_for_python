import os
import json
from collections import Counter


_NER_DIR = '../recipe_conv/weekcook/ner_result'
_DST_DIR = './countAC'


def count_actag(ner_strings):
    actag_words_list = []
    split_ner_strings = ner_strings.split(' ')
    for word in split_ner_strings:
        if word.find('/Ac') >= 0:
            delete_tag = word.replace('/Ac', '')
            delete_equal = delete_tag.replace('=', '')
            actag_words_list.append(delete_equal)

    count_actag_words = dict(Counter(actag_words_list))

    return count_actag_words


def main():
    file_list = os.listdir(_NER_DIR)
    for f in file_list:
        sample_file = os.path.join(_NER_DIR, f)
        with open(sample_file, 'r', encoding='utf-8') as r:
            ner_strings = r.read()
        actag_count = count_actag(ner_strings)
        print(actag_count)

        if os.path.isdir(_DST_DIR) is False:
            os.makedirs(_DST_DIR)
        else:
            pass

        fname, _ = os.path.splitext(f)
        dstpath = os.path.join(_DST_DIR, fname + '.json')
        with open(dstpath, 'w', encoding='utf-8') as w:
            json.dump(actag_count, w, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
