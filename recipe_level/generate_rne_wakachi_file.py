import os


_RNE_RESULT_DIR = '../recipe_conv/weekcook/ner_result'
_DST_DIR = './rne_wakachi'


def preprocess_rnetag(rne_strings):
    rne_strings_array = rne_strings.split(' ')
    rne_strings_array = [x.split('/')[0] for x in rne_strings_array]
    rne_strings_array = [x.replace('=', '') for x in rne_strings_array]
    rne_strings_array = ' '.join(rne_strings_array)

    return rne_strings_array


def main():
    if os.path.isdir(_DST_DIR) is False:
        os.makedirs(_DST_DIR)
    else:
        pass

    file_list = os.listdir(_RNE_RESULT_DIR)
    for f in file_list:
        readfile = os.path.join(_RNE_RESULT_DIR, f)
        dstpath = os.path.join(_DST_DIR, f)
        with open(readfile, 'r', encoding='utf-8') as r:
            rne_strings = r.read()
        preprocess_string = preprocess_rnetag(rne_strings)
        with open(dstpath, 'w', encoding='utf-8') as w:
            w.write(preprocess_string)


if __name__ == '__main__':
    main()
