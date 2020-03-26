import os
import json
import time
from typing import Iterator

import pandas as pd


_SRC_DIR = './tmp'


def morp_to_tag(morp: str) -> Iterator:
    part_of_sppech = set(["名詞", "動詞", "副詞", "形容詞"])
    print('morp: ', morp)
    for m in morp:
        print('m')
        print(m)
        if m == '':
            continue
        elif m.split('/')[1].find('連語') >= 0 and m.split('/')[1].split('+')[-1] in part_of_sppech:
            print('part_of_speech')
            print(m.split('/')[0])
            yield m.split('/')[0]
            continue
        elif m.split('/')[1] in part_of_sppech:
            print('part_of_speech')
            print(m.split('/')[0])
            yield m.split('/')[0]




def process_POS_for_collocation(data):
    ner_list = data.ner_list
    morp_list = data.morp_list
    print('ner_list : ', ner_list)
    print('morp_list : ', morp_list)
    process = []
    for ner in ner_list:
        if ner == '\r\n':
            return process
            break

        print('ner: ', ner)
        target = ner.split('/')[0]
        print('target : ', target)
        if target.find('=') >= 0:
            words = target.split('=')
            print('words : ', words)
            strings = ''
            pos_init = '連語 '
            pos = []
            yomi = ''
            for word in words:
                print('word : ', word)
                print('morp_list : ', morp_list)
                tmp_morp = morp_list.pop(0)
                print('tmp_morp : ', tmp_morp)
                strings += word
                pos.append(tmp_morp.split('/')[1])
                yomi += tmp_morp.split('/')[2]
                print('strings: ', strings)
                print('pos: ', pos)
                print('yomi: ', yomi)
            pos = '+'.join(pos)
            pos = pos_init + pos
            target = strings + '/' + pos + '/' + yomi
            print('target : ', target)
            process.append(target)
            print('process : ', process)
        else:
            target = morp_list.pop(0)
            print('target : ', target)
            process.append(target)
            print('process : ', process)

    return process


def is_join(data):
    ner_list = data.ner_list
    wakati_list = data.wakati_list
    ner_strings = data.ner_strings

    if len(ner_list) != len(wakati_list) and ner_strings.find('=') >= 0:
        return True
    else:
        return False



class Data:
    def __init__(self, data):
        self.ner_list = data['ner'].rstrip().split(' ')
        self.wakati_list = data['wakati'].rstrip().split(' ')
        self.morp_list = data['morp'].rstrip().split(' ')
        self.ner_strings = data['ner'].rstrip()


def main():
    file_list = os.listdir(_SRC_DIR)
    count = 0
    time0 = time.time()
    preprocessing = []
    for f in range(len(file_list)):
        filepath = os.path.join(_SRC_DIR, 'kytea_recipetag_' + str(f) + '.json')
        with open(filepath, 'r', encoding='utf-8') as r:
            data = json.load(r)
            data = Data(data)

        if is_join(data):
            print('ner_list : ', len(data.ner_list))
            print('wakati_list : ', len(data.wakati_list))
            print(data.ner_list)
            print(data.wakati_list)
            print(data.morp_list)
            print(filepath)
            count += 1
            process = process_POS_for_collocation(data)
        else:
            process = data.morp_list

        preprocessing.append(process)

    time1 = time.time()
    print(time1 - time0)
    print(count)

    time2 = time.time()
    result = [list(morp_to_tag(p)) for p in preprocessing]
    time3 = time.time()
    print(time3 - time2)
    print(result)

    csv = pd.DataFrame(result)
    csv.to_csv('kytearecipetag.csv')


if __name__ == '__main__':
    main()
