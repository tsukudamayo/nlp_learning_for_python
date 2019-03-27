import os
from collections import defaultdict

import pandas as pd
from graphviz import Digraph


_LOG_DIR = 'C:/Users/tsukuda/var/data/recipe/weekcook/test/ner_result'
_LIKELIFOOD_CSV = 'C:/Users/tsukuda/var/data/recipe/weekcook/test/likelihood/likelihood.csv'
_RNE_MAP = 'rne_category.txt'


def parse_dependency(likelihood, word_order, word_to_rne_map,
                     rne_to_num_map, num_to_rne_map, rne_to_word_map,):
    dependency_list = []
    for idx, word_t in enumerate(word_order):
        print('++++++++++++++++++++++++++++++++')
        print(idx, word_t)
        print('++++++++++++++++++++++++++++++++')
        print(word_t[1] in word_to_rne_map)
        if str(word_t[1]) not in word_to_rne_map:
            print('{} is not exists in rne dictionary'.format(word_t[1]))
            continue
        rne_tag = word_to_rne_map[word_t[1]]
        tag_likelihood_column = rne_to_num_map[rne_tag[0]]
        print('rne_tag', rne_tag[0])
        print('tag_likelihood_column', tag_likelihood_column)
        rne_argmax_tag = rne_argmax(
            word_t[1],
            rne_tag[0],
            likelihood,
            rne_to_num_map,
        )
        print('rne_argmax_tag', rne_argmax_tag)
        dependency_tag = num_to_rne_map[rne_argmax_tag]
        print('dependecy_tag', dependency_tag)
        dependency_candidate = rne_to_word_map[dependency_tag]
        print(dependency_candidate)

        compare_dependency = []
        for order in list(word_order):
            for d_word in dependency_candidate:
                if idx >= order[0]:
                    # print(idx)
                    # print(order[0])
                    # print('big')
                    pass
                else:
                    if d_word in order:
                        compare_dependency.append(order)
                        dependency_word = sorted(compare_dependency)[0][1]
                        print('dependency_word')
                        print(dependency_word)
                    else:
                        pass
        if len(compare_dependency) != 0:
            candidate_agent = sorted(compare_dependency)[0]
            # for duplicating words
            agent_join_word = str(word_t[0]) + '-' + str(word_t[1])
            targs_join_word = str(candidate_agent[0]) + '-' + str(candidate_agent[1])
            dependency_tuple = (agent_join_word, targs_join_word)
            dependency_list.append(dependency_tuple)
        else:
            pass
        # print(dependency_list)
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print(dependency_list)

    return dependency_list


def load_likelihood(likelihood_csv, index_list):
    print('**************** read loglikelihood data ****************')    
    likelihood = pd.read_csv(likelihood_csv, index_col=0)
    likelihood = pd.concat([likelihood, index_list], axis=1)
    likelihood = likelihood.set_index('index')
    print(likelihood.head())

    return likelihood


def rne_probability(word, tag, likelihood, rne_map):
    tag_id = rne_map[tag]
    probability = max(likelihood[str(tag_id)])

    return probability


def rne_argmax(word, tag, likelihood, rne_map):
    tag_id = rne_map[tag]
    rne_argmax = likelihood[str(tag_id)].idxmax()

    return rne_argmax


def rne_to_num(filepath):
    rne_to_num_map = {}
    with open(filepath, 'r', encoding='utf-8') as r:
        lines = r.readlines()
    for line in lines:
        line = line.rstrip('\n')
        line = line.split(':')
        rne_to_num_map.update({line[1]: int(line[0])})

    return rne_to_num_map


def num_to_rne(filepath):
    num_to_rne_map = {}
    with open(filepath, 'r', encoding='utf-8') as r:
        lines = r.readlines()
    for line in lines:
        line = line.rstrip('\n')
        line = line.split(':')
        num_to_rne_map.update({int(line[0]): line[1]})

    return num_to_rne_map


def word_to_order(filepath):
    ordered_list = []
    count = 0
    with open(filepath, 'r', encoding='utf-8') as r:
        lines = r.readlines()
    for line in lines:
        line = line.rstrip('\n')
        line = line.split(' ')
        for word in line:
            word = word.split('/')
            current_data = (count, word[0])
            ordered_list.append(current_data)
            count += 1

    return ordered_list


def word_to_rne(filepath):
    word_to_rne_map = defaultdict(list)
    with open(filepath, 'r', encoding='utf-8') as r:
        lines = r.readlines()
    for line in lines:
        line = line.split(' ')
        for word in line:
            word = word.split('/')
            if len(word) >= 2:
                print(word)
                word_to_rne_map[word[0]].append(word[1])
            else:
                pass

    return word_to_rne_map


def rne_to_word(filepath):
    rne_to_word_map = defaultdict(list)
    with open(filepath, 'r', encoding='utf-8') as r:
        lines = r.readlines()
    for line in lines:
        line = line.split(' ')
        for word in line:
            word = word.split('/')
            if len(word) >= 2:
                print(word)
                rne_to_word_map[word[1]].append(word[0])
            else:
                pass

    return rne_to_word_map


def output_flowgraph(dependency_list):
    dst_dir = os.path.join(os.path.dirname(__file__), 'static/flowgraph/assets/img')
    G = Digraph(format='png')
    G.attr('node', shape='square', style='filled', fontname='MS Gothic')
    for pair in dependency_list:
        print(pair)
        G.edge(pair[0], pair[1])
    G.render(os.path.join(dst_dir, 'flowgraph'))

    return


def main():
    # likelifood data config
    index = [0, 2, 4, 5, 8]
    index_list = pd.DataFrame({
        'index': index,
    })
    likelihood = load_likelihood(_LIKELIFOOD_CSV, index_list)

    read_file = os.path.join(_LOG_DIR, 'test_00000002_ner_result.txt')

    print('**************** rne_to_num_map ****************')
    rne_to_num_map = rne_to_num(_RNE_MAP)
    print(rne_to_num_map)

    print('**************** num_to_rne_map ****************')
    num_to_rne_map = num_to_rne(_RNE_MAP)
    print(num_to_rne_map)

    print('**************** word_to_order ****************')
    word_order = word_to_order(read_file)
    print(word_order)

    print('**************** rne_word_map ****************')
    word_to_rne_map = word_to_rne(read_file)
    print('rne_word_map')
    print(word_to_rne_map)

    print('**************** rne_word_map ****************')
    rne_to_word_map = rne_to_word(read_file)
    print('rne_word_map')
    print(rne_to_word_map)

    dependency_list = parse_dependency(
        likelihood,
        word_order,
        word_to_rne_map,
        rne_to_num_map,
        num_to_rne_map,
        rne_to_word_map,
    )
    print('dependency_list')
    print(dependency_list)

    print('################ original file ################')
    with open(read_file, 'r', encoding='utf-8') as read_f:
        lines = read_f.readlines()
    print(lines)
    print('################ dependencies ################')
    print(dependency_list)

    output_flowgraph(dependency_list)


if __name__ == '__main__':
    main()
