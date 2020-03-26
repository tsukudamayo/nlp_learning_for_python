import os
import json
import requests
import pandas as pd

import nerpreprocess as ner


_KYTEA_PATH = '../recipe_nlp/kytea-win-0.4.2/kytea.exe'
_KBM_MODEL = '../recipe_nlp/kytea-win-0.4.2/model/jp-0.4.7-1.mod'
_KNM_MODEL = '../recipe_nlp/kytea-win-0.4.2/RecipeNE-sample/recipe416.knm'

_DST_DIR = './tmp'


def main():
    if os.path.isdir(_DST_DIR) is False:
        os.makedirs(_DST_DIR)
    data = pd.read_csv('sample.csv', encoding='utf-8')
    data.columns = ['idx', 'recipe_id', 'group_id', 'title',
                    'tag_1', 'tag_2', 'tag_3', 'tag_4', 'tag_5', 'tag_6']
    titles = data['title']
    print(titles)

    for t in range(len(titles)):
        first = titles[t]
        print(first)

        morp = ner.parse_recipe(first, _KBM_MODEL, _KYTEA_PATH)
        wakati = ner.insert_space_between_words(morp)
        score = ner.ner_tagger_1(wakati, _KNM_MODEL, _KYTEA_PATH)
        ner_result = ner.ner_tagger_2(score)
        finalize = ner.Finalizer(wakati, ner_result, first)
        result = finalize.result_output()
        print('result: ', result)
        print('morp: ', morp)
        print('wakati : ', wakati)
        output = {'ner': result, 'morp': morp, 'wakati': wakati}
        with open('./tmp/kytea_recipetag_' + str(t) + '.json', 'w', encoding='utf-8') as w:
            json.dump(output, w, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
