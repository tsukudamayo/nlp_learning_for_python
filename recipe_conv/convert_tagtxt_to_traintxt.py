import os


_LOG_DIR = 'weekcook/procedure_4_2'
_DST_DIR = 'weekcook/particle/train'


def main():
    file_list = os.listdir(_LOG_DIR)
    for f in file_list:
        filepath = os.path.join(_LOG_DIR, f)
        text = open(filepath, 'r', encoding='utf-8')
        strings = text.read()
        text.close()
        print('strings')
        print(strings)

        split_txt = strings.split(' ')
        print('spilt_txt')
        print(split_txt)

        dst_file = 'train_20190515.txt'
        dstpath = os.path.join(_DST_DIR, dst_file)
        with open(dstpath, 'a', encoding='utf-8') as w:
            for line in split_txt:
                w.write(line)
                w.write('\n')


if __name__ == '__main__':
    main()
