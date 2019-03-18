import os


_LOG_DIR = 'C:\\Users\\tsukuda\\var\\data\\recipe\\weekcook\\procedure_3'


def main():
    read_files = os.listdir(_LOG_DIR)
    word_list = []
    for f in read_files:
        read_file = os.path.join(_LOG_DIR, f)
        with open(read_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines:
            print(line)
            line = line.replace('\n', '')
            line = line.replace(' 、', '')
            line = line.replace(' 。', '')
            line = line.split(' ')
            word_list.extend(line)

    word_list = set(word_list)
    print(word_list)
    print(len(word_list))

    with open('word_list.txt', 'w', encoding='utf-8') as w:
        for word in word_list:
            if word is not '':
                w.write(word)
                w.write('\n')
            else:
                pass


if __name__ == '__main__':
    main()
