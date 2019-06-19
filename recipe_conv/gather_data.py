import os
import shutil


_DST_DIR = './data'
_ORG_DIR = './weekcook/org'
_CONV_DIR = './weekcook/paramstring'
_PARAM_DIR = './weekcook/parameters'
_LOG_DIR = 'C:/Users/tsukuda/var/data/recipe/weekcook/recipe_root'


def main():
    logfiles = os.listdir(_LOG_DIR)
    print('logfiles')
    print(logfiles)
    log_number = []
    for f in logfiles:
        fname, _ = os.path.splitext(f)
        number = fname.split('_')[1]
        print(number)
        log_number.append(number)

    print('number')
    print(log_number)

    for n in log_number:
        dirpath = os.path.join(_DST_DIR, str(n))
        if os.path.isdir(dirpath) is False:
            os.makedirs(dirpath)
        else:
            pass

    for n in log_number:
        dstpath = os.path.join(_DST_DIR, str(n))
        fname = 'recipe_' + str(n) + '.json'
        filepath = os.path.join(dstpath, fname)
        orgpath = os.path.join(_LOG_DIR, fname)
        shutil.copy2(orgpath, filepath)

    for n in log_number:
        dstpath = os.path.join(_DST_DIR, str(n))
        fname = 'recipe_' + str(n) + '.txt'
        filepath = os.path.join(_DST_DIR, fname)
        orgpath = os.path.join(_ORG_DIR, fname)
        shutil.copy2(orgpath, filepath)

    for n in log_number:
        dstpath = os.path.join(_DST_DIR, str(n))
        fname = 'recipe_' + str(n) + '_convrecipe.txt'
        filepath = os.path.join(_DST_DIR, fname)
        orgpath = os.path.join(_CONV_DIR, fname)
        shutil.copy2(orgpath, filepath)

    for n in log_number:
        dstpath = os.path.join(_DST_DIR, str(n))
        fname = 'recipe_' + str(n) + '_params.json'
        filepath = os.path.join(_DST_DIR, fname)
        orgpath = os.path.join(_PARAM_DIR, fname)
        shutil.copy2(orgpath, filepath)

if __name__ == '__main__':
    main()
