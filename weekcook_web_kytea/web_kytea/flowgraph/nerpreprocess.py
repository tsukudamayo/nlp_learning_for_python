import os
import subprocess

import numpy as np

from . import kyteagraph as ky
from . import nesearch as ne


_KBM_MODEL = 'kytea-win-0.4.2/model/jp-0.4.7-1.mod'
_KNM_MODEL = 'kytea-win-0.4.2/RecipeNE-sample/recipe416.knm'
_KYTEA_PATH = 'kytea-win-0.4.2/kytea.exe'
_NESEARCH_PATH = 'kytea-win-0.4.2/RecipeNE-sample/bin/nesearch.py'
_LOG_DIR = 'C:/Users/tsukuda/var/data/recipe/weekcook/test'


class Finalizer:
    def __init__(self, morphology_file, ner_file, output_path):
        super(Finalizer, self).__init__()
        self.morphology_file = morphology_file
        self.ner_file = ner_file
        self.output_path = output_path
        self.m_lists = []
        self.ner_lists = []

    def result_output(self):
        with open(self.output_path, 'w', encoding='utf-8') as w:
            for line in open(self.morphology_file, 'r', encoding='utf-8'):
                print('line1')
                print(line)
                line = line.replace('\n', '').split(' ')
                print('line2w')
                print(line)
                self.m_lists.append(line)
            print(self.m_lists)

            for line in open(self.ner_file, 'r', encoding='utf-8'):
                line = line.replace('\n', '').split(' ')
                print('line2r')
                print(line)
                self.ner_lists.append(self.modify_viob(line))
            print(self.ner_lists)

            for m_list, ner_list in zip(self.m_lists, self.ner_lists):
                restored_list = self.restore(m_list, ner_list)
                print('restored_list')
                print(restored_list)
                output_list = self.join_words(restored_list)
                print('output_list')
                print(output_list)
                w.write(' '.join(output_list) + '\n')

        return

    def modify_viob(self, input_list):
        output_list = []
        for item in input_list:
            if item == '':
                continue
            item = item.split('/')
            if item[1] == 'O':
                output_list.append(item[0])
            else:
                output_list.append(item[0] + '/' + item[1].split('-')[0])

        return output_list

    def restore(self, morphology_list, ner_list):
        output_list = []
        for m_item, ner_item in zip(morphology_list, ner_list):
            m_item = m_item.split('/')
            if '/' in ner_item:
                ner_item = ner_item.split('/')
            else:
                ner_item = [ner_item, '']
            if m_item[0] != ner_item[0]:
                print('ERROR: m_item != ner_item at restore')
                print(m_item[0])
                print(ner_item[0])
                # # tsukuda change
                # sys.exite()
                pass
            if ner_item[1] == '':
                output_list.append(','.join(m_item))
            else:
                output_list.append(','.join(m_item) + '/' + ner_item[1])

        return output_list

    def join_words(self, input_list):
        tag_list = []
        for item in input_list:
            item = item.split('/')
            if len(item) == 1:
                tag_list.append('')
            else:
                tag_list.append(item[1])
        i = 0
        output_str = ''
        for item in input_list:
            if tag_list[i] == '':
                output_str += item + ' '
            else:
                if i == (len(input_list) - 1):
                    output_str += item + ' '
                else:
                    if tag_list[i] == tag_list[i + 1]:
                        output_str += item.split('/')[0] + '='
                    else:
                        output_str += item + ' '
            i += 1
        output_list = output_str.split(' ')[:-1]

        return output_list


# def ner_tagger_2(nesearch_path, input_file, output_file):
#     cmd = subprocess.call(
#         ['python', nesearch_path, input_file, output_file],
#     )
# 
#     return


def ner_tagger_2(input_file, output_file):
    rnetag_list = np.array(['Ac', 'Af', 'F', 'Sf', 'St', 'Q', 'D', 'T'])

    tag_kinds = np.array([ne.BIOtag_append(tag) for tag in rnetag_list])
    tag_kinds = tag_kinds.flatten()

    head_tag = np.array([ne.genereate_headtag(tag) for tag in tag_kinds])

    # /O tag
    tag_kinds = np.append(tag_kinds, ['O'], axis=0)
    head_tag = np.append(head_tag, [1], axis=0)

    connect_matrix = np.array(
        [ne.generate_connection_matrix(tag, tag_kinds) for tag in tag_kinds]
    )

    # -----
    # test
    # -----
    # print('tag_kinds')
    # print(tag_kinds)

    # print('head_tag')
    # print(head_tag)

    # print('tag_kinds')
    # print(tag_kinds)
    # print('head_tag')
    # print(head_tag)

    # print('connect_matrix')
    # print(connect_matrix)

    # --------------------------------------
    # get result of tag estimation by kytea
    # --------------------------------------
    read_file = input_file
    food_list, tag_list, prob_list = ne.text_to_list(read_file)

    # print('foods', food_list)
    # print('tags', tag_list)
    # print('probs', prob_list)

    # ---------------
    # generate hash
    # ---------------
    foods_tags_hash = {food: tag for (food, tag) in zip(food_list, tag_list)}
    # print('foods_tags_hash')
    # print(foods_tags_hash)
    foods_probs_hash = {food: prob for (food, prob) in zip(food_list, prob_list)}
    # print('foods_probs_hash')
    # print(foods_probs_hash)
    foods_number_hash = {i: food for (i, food) in enumerate(food_list)}
    # print('foods_number_hash')
    # print(foods_number_hash)

    # --------------------------
    # viterbi forward algorithm
    # --------------------------
    prob_matrix, edge_matrix = ne.viterbi_forward(
        food_list,
        tag_kinds,
        head_tag,
        connect_matrix,
        foods_tags_hash,
        foods_number_hash,
        foods_probs_hash
    )
    print('**************** prob_matrix ****************')
    for i in prob_matrix:
        print(i)

    print('**************** edge_matrix ****************')
    for i in edge_matrix:
        print(i)

    # --------------------------
    # viterbi forward algorithm
    # --------------------------
    result_rnetag = ne.viterbi_backward(
        tag_kinds,
        food_list,
        prob_matrix,
        edge_matrix
    )
    print('result_rnetag')
    print(result_rnetag)

    # -----------------------
    # result output to text
    # -----------------------
    with open(output_file, 'w', encoding='utf-8') as w:
        for word, tag in zip(food_list, result_rnetag):
            w.write(word)
            w.write('/')
            w.write(tag)
            w.write(' ')

    return


def ner_tagger_1(kytea_path, model_path, input_file, output_file):
    try:
        cmd_cat = subprocess.Popen(
            ['cat', input_file],
            stdout=subprocess.PIPE,
        )
    # if "cat" command is not exist
    except FileNotFoundError:
        cmd_cat = subprocess.Popen(
            ['type', input_file],
            stdout=subprocess.PIPE,
            shell=True,
        )
    cmd_kytea = subprocess.Popen(
        [kytea_path, '-model', model_path,
         '-out', 'conf', '-nows',
         '-tagmax', '0', '-unktag', '/UNK',
         input_file
         ],
        stdin=cmd_cat.stdout,
        stdout=subprocess.PIPE,
    )
    end_of_pipe = cmd_kytea.communicate()[0].decode('utf-8')
    print(end_of_pipe)

    with open(output_file, 'w', encoding='utf-8') as w:
        w.write(end_of_pipe)

    return


def insert_space_between_words(input_file, output_file):
    fp = open(output_file, 'w', encoding='utf-8')
    for line in open(input_file, 'r', encoding='utf-8'):
        print(len(line))
        if len(line) == 1: # only line feed
            pass
        else:
            line = line.replace('\n', '')
            words = [w.split('/')[0] for w in line.split(' ')]
            fp.write(' '.join(words) + '\n')
    fp.close()

    return


def parse_recipe(model_path, kytea_path, input_file, output_file):
    print('input_file')
    print(input_file)
    print('cat')
    try:
        print('try')
        cmd_cat = subprocess.Popen(
            ['cat', input_file],
            stdout=subprocess.PIPE,
        )
    # if "cat" command is not exist
    except FileNotFoundError:
        print('file not found error')
        cmd_cat = subprocess.Popen(
            ['type', input_file],
            stdout=subprocess.PIPE,
            shell=True,
        )
    cmd_kytea = subprocess.Popen(
        [kytea_path, '-model', model_path],
        stdin=cmd_cat.stdout,
        stdout=subprocess.PIPE,
    )
    end_of_pipe = cmd_kytea.communicate()[0].decode('utf-8')
    end_of_pipe = end_of_pipe.replace('\n', '')

    print(end_of_pipe)
    with open(output_file, 'w', encoding='utf-8') as w:
        w.write(end_of_pipe)

    return


def mkdir_if_not_exists(path):
    if os.path.isdir(path) is False:
        os.makedirs(path)
    else:
        pass

    return


def main():
    header_name = 'test_'
    file_number = len(os.listdir(os.path.join(_LOG_DIR, 'org_add_lf')))
    for i in range(1, file_number + 1):
        filenumber = f'{i:08}'
        print('procedure_2')
        org_path = os.path.join(_LOG_DIR, 'org_add_lf')
        proc2_path = os.path.join(_LOG_DIR, 'procedure_2')
        mkdir_if_not_exists(org_path)
        mkdir_if_not_exists(proc2_path)
        input_file = os.path.join(org_path, header_name + filenumber + '.txt')
        output_file = os.path.join(proc2_path, header_name + filenumber + '_proc2.txt')
        parse_recipe(_KBM_MODEL, _KYTEA_PATH, input_file, output_file)

        print('procedure_3')
        proc3_path = os.path.join(_LOG_DIR, 'procedure_3')
        mkdir_if_not_exists(proc3_path)
        input_file = output_file
        output_file = os.path.join(proc3_path, header_name + filenumber + '_proc3.txt')
        morphology_file = output_file
        insert_space_between_words(input_file, output_file)

        print('procedure_4_1')
        proc4_1_path = os.path.join(_LOG_DIR, 'procedure_4_1')
        mkdir_if_not_exists(proc4_1_path)
        input_file = output_file
        output_file = os.path.join(proc4_1_path, header_name + filenumber + '_proc4_1.txt')
        ner_tagger_1(_KYTEA_PATH, _KNM_MODEL, input_file, output_file)

        print('procedure_4_2')
        proc4_2_path = os.path.join(_LOG_DIR, 'procedure_4_2')
        mkdir_if_not_exists(proc4_2_path)
        input_file = output_file
        output_file = os.path.join(proc4_2_path, header_name + filenumber + '_proc4_2.txt')
        ner_file = output_file
        # before
        ner_tagger_2(input_file, output_file)

        print('result')
        result_path = os.path.join(_LOG_DIR, 'ner_result')
        mkdir_if_not_exists(result_path)
        output_file = os.path.join(result_path, header_name + filenumber + '_ner_result.txt')
        result = Finalizer(
            morphology_file,
            ner_file,
            output_file,
        )
        result.result_output()


if __name__ == '__main__':
    main()
