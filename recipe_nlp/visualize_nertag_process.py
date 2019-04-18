import os
import time

import numpy as np
import matplotlib.pyplot as plt

import nesearch as ne


_4_1_DIR = 'C:/Users/tsukuda/var/data/recipe/orangepage/procedure_4_1'
_4_2_DIR = 'C:/Users/tsukuda/var/data/recipe/orangepage/procedure_4_2'
_DST_DIR = 'C:/Users/tsukuda/var/data/recipe/orangepage/visualization/procedure_4_1'


def main():
    scorefile_list = os.listdir(_4_1_DIR)
    print(scorefile_list)
    target_scorefile = scorefile_list[0]
    scorefile_path = os.path.join(_4_1_DIR, target_scorefile)
    print('file_path')
    print(scorefile_path)

    food_list, tag_list, prob_list = ne.text_to_list(scorefile_path)
    num_prob_list = np.array([np.array(x).astype(np.float) for x in prob_list])
    print('num_prob_list')
    print(num_prob_list)

    resultfile_list = os.listdir(_4_2_DIR)
    print(resultfile_list)

    target_resultfile = resultfile_list[0]
    resultfile_path = os.path.join(_4_2_DIR, target_resultfile)
    print('resultfile_path')
    print(resultfile_path)

    with open(resultfile_path, 'r', encoding='utf-8') as r:
        lines = r.readlines()
    for line in lines:
        print(line)

    print('lines')
    print(lines[0].split(' '))
    food_result = lines[0].split(' ')

    target_dir, _ = os.path.splitext(target_scorefile)
    for idx, (food, tag, num_prob) in enumerate(zip(food_result, tag_list, num_prob_list)):
        food = food.replace('/', '_')
        prob_argmax = np.argmax(num_prob)
        tag_argmax = np.argmax(prob_argmax)
        org_tag_argmax = tag[tag_argmax]
        image_dir = os.path.join(_DST_DIR, target_dir)
        if os.path.isdir(image_dir) is False:
            os.makedirs(image_dir)
        else:
            pass
        image_path = os.path.join(image_dir, str(idx) + '_' + org_tag_argmax + '_' + food + '.png')
        plt.figure(figsize=(10, 6))
        print('**************** ' + org_tag_argmax + ' ' + food + ' ****************')
        print(tag, num_prob)
        plt.title(org_tag_argmax + ' ' + food)
        plt.bar(tag, num_prob)
        plt.savefig(image_path)


if __name__ == '__main__':
    main()
