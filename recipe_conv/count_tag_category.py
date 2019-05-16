import os


_LOG_DIR = 'weekcook/particle/train'


def main():
    target_filename = 'train_20190515.txt'
    target_file = os.path.join(_LOG_DIR, target_filename)

    with open(target_file, 'r', encoding='utf-8') as r:
        lines = r.readlines()

    # tags = []
    # for idx, line in enumerate(lines):
    #     line = line.replace('\n', '')
    #     print(idx)
    #     print(line)
    #     tag = line.split('/')[1]
    #     tags.append(tag)

    # print('tags')
    # print(tags)

    tags = [line.replace('\n', '').split('/')[1] for line in lines if line != '']
    tags_set = set(tags)
    print('tags_set')
    print(tags_set)
    print('number of tags')
    print(len(tags_set))



if __name__ == '__main__':
    main()
