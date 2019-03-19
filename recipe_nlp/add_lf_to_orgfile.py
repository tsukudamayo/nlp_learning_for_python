import os


_ORG_DIR = 'C:/Users/tsukuda/var/data/recipe/weekcook/org'
_DST_DIR = 'C:/Users/tsukuda/var/data/recipe/weekcook/org_add_lf'


def main():
    if os.path.isdir(_DST_DIR) is False:
        os.makedirs(_DST_DIR)
    else:
        pass
    
    file_list = os.listdir(_ORG_DIR)
    for f in file_list:
        filepath = os.path.join(_ORG_DIR, f)
        with open(filepath, 'r', encoding='utf-8') as r:
            lines = r.readlines()
        dstfile = os.path.join(_DST_DIR, f)
        with open(dstfile, 'w', encoding='utf-8') as w:
            for line in lines:
                w.write(line)
                w.write('\n')


if __name__ == '__main__':
    main()
