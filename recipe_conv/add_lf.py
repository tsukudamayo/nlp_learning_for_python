import os


_LOG_DIR = 'C:/Users/tsukuda/local/nlp_learning_for_python/recipe_conv/weekcook/_org'
_DST_DIR = 'C:/Users/tsukuda/local/nlp_learning_for_python/recipe_conv/weekcook/org'


def main():

    if os.path.isdir(_DST_DIR) is False:
        os.makedirs(_DST_DIR)
    else:
        pass

    file_list = os.listdir(_LOG_DIR)
    print(file_list)
    for f in file_list:
        if f == 'sample.txt':
            continue
        filepath = os.path.join(_LOG_DIR, f)
        readfile = open(filepath, 'r', encoding='utf-8')
        strings = readfile.read()
        readfile.close()
        print(strings)

        dstpath = os.path.join(_DST_DIR, f)
        with open(dstpath, 'w', encoding='utf-8') as w:
            w.write(strings)
            w.write('\n')

if __name__ == '__main__':
    main()
