import os
import time

import numpy as np
import matplotlib.pyplot as plt

import nesearch as ne

_LOG_FILE = 'C:/Users/tsukuda/var/data/recipe/orangepage/procedure_4_1/detail_103522_proc4_1.txt'
_4_2_FILE = 'C:/Users/tsukuda/var/data/recipe/orangepage/procedure_4_2/detail_103522_proc4_2.txt'
_DST_DIR = 'C:/Users/tsukuda/var/data/recipe/orangepage/visualization/viterbi_forward'

def main():
    rnetag_list = np.array(['Ac', 'Af', 'F', 'Sf', 'St', 'St', 'Q', 'D', 'T'])
    tag_kinds = np.array([ne.BIOtag_append(tag) for tag in rnetag_list])
    tag_kinds = tag_kinds.flatten()
    head_tag = np.array([ne.genereate_headtag(tag) for tag in tag_kinds])
    tag_kinds = np.append(tag_kinds, ['O'], axis=0)
    head_tag = np.append(head_tag, [1], axis=0)
    connect_matrix = np.array(
        [ne.generate_connection_matrix(tag, tag_kinds) for tag in tag_kinds]
    )
    print('connect_matrix')
    print(connect_matrix)

    read_file = _LOG_FILE

    food_list, tag_list, prob_list = ne.text_to_list(read_file)
    foods_tags_hash = {food: tag for (food, tag) in zip(food_list, tag_list)}
    foods_probs_hash = {food: prob for (food, prob) in zip(food_list, prob_list)}
    foods_number_hash = {i: food for (i, food) in enumerate(food_list)}
    print('foods_tags_hash')
    print(foods_tags_hash)
    print('foods_probs_hash')
    print(foods_probs_hash)
    print('foods_number_hash')
    print(foods_number_hash)

    # # test
    # for f, food, prob in zip(food_list, foods_tags_hash.values(), foods_probs_hash.values()):
    #     time.sleep(1)
    #     print(f)
    #     print(food)
    #     print(prob)

    resultfile_path = _4_2_FILE
    print('resultfile_path')
    print(resultfile_path)

    with open(resultfile_path, 'r', encoding='utf-8') as r:
        lines = r.readlines()
    for line in lines:
        print(line)
    print('lines')
    print(lines[0].split(' '))
    food_result = lines[0].split(' ')
    print('food_result')
    print(food_result)

    # prob_matrix, edge_matrix, prob_history = ne.viterbi_forward(
    #     food_list,
    #     tag_kinds,
    #     head_tag,
    #     connect_matrix,
    #     foods_tags_hash,
    #     foods_number_hash,
    #     foods_probs_hash
    # )
    prob_matrix, edge_matrix, prob_history = ne.viterbi_forward(
        food_list,
        tag_list,
        prob_list,
        tag_kinds,
        head_tag,
        connect_matrix
    )

    print('prob_matrix')
    print(prob_matrix.shape)
    print('edge_matrix')
    print(edge_matrix.shape)
    print('prob_history')
    print(len(prob_history))
    print('prob_history[0]')
    print(len(prob_history[0]))

    with open(_4_2_FILE, 'r', encoding='utf-8') as r:
        lines = r.readlines()

    food_list = lines[0].split(' ')
    target_dir, _ = os.path.splitext(read_file)
    target_dir = os.path.basename(os.path.dirname(target_dir))
    for idx, (food, prob) in enumerate(zip(food_result, prob_matrix)):
        food = food.replace('/', '_')
        prob_argmax = np.argmax(prob)
        org_tag_argmax = tag_kinds[prob_argmax]
        image_dir = os.path.join(_DST_DIR, target_dir)
        if os.path.isdir(image_dir) is False:
            os.makedirs(image_dir)
        else:
            pass

        image_path = os.path.join(image_dir, str(idx) + '_' + org_tag_argmax + '_' + food + '.png')
        plt.figure(figsize=(10, 6))
        print('**************** ' + org_tag_argmax + ' ' + food + ' ****************')
        plt.title(org_tag_argmax + ' ' + food)
        print('prob')
        for i in range(len(prob)):
            print(tag_kinds[i])
        print('**************** prob_history ****************')
        if idx >= 1:
            for k, v in prob_history[idx - 1].items():
                print(v)
            print('**************** prob_history argmax ****************')
            prev_scores = np.array([x for x in prob_history[idx - 1].values()])
            print('prev_scores')
            print(prev_scores)
            print(prev_scores.shape)
            prev_max = np.argmax(prev_scores)
            print('prev argmax')
            print(prev_max)
            print('prev max value')
            print(prev_scores[prev_max])

            print('**************** current probability ****************')
            current_prob = np.array([x for x in prob_matrix[idx]])
            print(current_prob.shape)
            print(current_prob)
            print(tag_kinds.shape)
            # plt.bar(tag_kinds, current_prob)
            # plt.show()

            print('**************** forward ****************')
            foward_prob = np.array([x*prev_scores[prev_max] for x in prob])
            print(foward_prob.shape)
            print(tag_kinds.shape)
            for i in range(len(foward_prob)):
                print(foward_prob[i])
            # plt.bar(tag_kinds, foward_prob)
            # plt.show()

        else:
            pass

        print('**************** prob_matrix ****************')
        for i in prob_matrix[idx]: 
            print(i)

        print('**************** argmax ****************')
        print(tag_kinds[np.argmax(prob)])
        print('prob')
        print(prob)
        print(len(prob))
        plt.bar(tag_kinds, prob)
        plt.title(org_tag_argmax + ' ' + food)
        plt.savefig(image_path)
        # plt.show()

    result_rnetag = ne.viterbi_backward(
        tag_kinds,
        food_list,
        prob_matrix,
        edge_matrix,
    )
    print('result_rnetag')
    print(result_rnetag)


if __name__ == '__main__':
    main()
