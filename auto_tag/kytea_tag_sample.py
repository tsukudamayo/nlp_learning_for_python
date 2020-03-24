import subprocess
from typing import List, Dict, Any, Iterator

import requests
import pandas as pd


_KYTEA_PATH = '../recipe_nlp/kytea-win-0.4.2/kytea.exe'
_MODEL_PATH = '../recipe_nlp/kytea-win-0.4.2/model/jp-0.4.7-1.mod'


def morp_title(text: str, model_path: str, kytea_path: str) -> str:
    print('text: ', text)
    cmd_echo = subprocess.Popen(
        ['echo', text],
        stdout=subprocess.PIPE,
    )
    cmd_kytea = subprocess.Popen(
        [kytea_path, '-model', model_path],
        stdin=cmd_echo.stdout,
        stdout=subprocess.PIPE,
    )
    end_of_pipe = cmd_kytea.communicate()[0].decode('utf-8')

    return end_of_pipe


def title_to_tag(title: str) -> Iterator:
    part_of_sppech = set(["名詞", "動詞", "副詞", "形容詞"])
    morp = morp_title(title, _MODEL_PATH, _KYTEA_PATH)
    morp = morp.split(' ')
    for m in morp:
        print('m')
        print(m)
        if m == '':
            continue
        elif m.split('/')[1] in part_of_sppech:
            print('part_of_speech')
            print(m.split('/')[0])
            yield m.split('/')[0]

def main():
    data = pd.read_csv('sample.csv', encoding='utf-8')
    data.columns = ['idx', 'recipe_id', 'group_id', 'title',
                    'tag_1', 'tag_2', 'tag_3', 'tag_4', 'tag_5', 'tag_6']

    titles = data['title']
    result = [list(title_to_tag(t)) for t in titles]
    print(result)
    csv = pd.DataFrame(result)
    csv.to_csv('kyteatag.csv')


if __name__ == '__main__':
    main()
