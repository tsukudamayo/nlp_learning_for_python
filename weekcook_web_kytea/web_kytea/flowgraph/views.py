from django.shortcuts import render
from django.http import HttpResponse
from . import nerpreprocess as pre
from . import kyteagraph as ky

import os

import pandas as pd


_KBM_MODEL = os.path.join(os.path.dirname(__file__), 'kytea-win-0.4.2/model/jp-0.4.7-1.mod')
_KNM_MODEL = os.path.join(os.path.dirname(__file__), 'kytea-win-0.4.2/RecipeNE-sample/recipe416.knm')
_KYTEA_PATH = os.path.join(os.path.dirname(__file__), 'kytea-win-0.4.2/kytea.exe')
_NESEARCH_PATH = os.path.join(os.path.dirname(__file__), 'kytea-win-0.4.2/RecipeNE-sample/bin/NESearch.pl')
_LOG_DIR = os.path.join(os.path.dirname(__file__), 'test')


# Create your views here.
def index(request):
    params = {
        'title': 'こんにちは',
        'msg': 'レシピを下のテキストボックスに入力してボタンをクリックして下さい。',
        'warning': 'そして、1~2分ほどお待ち下さい。',
    }
    return render(request, 'flowgraph/index.html', params)


def form(request):
    msg = request.POST['msg']
    params = {
        'title': 'こんにちは',
        'answer': msg,
    }

    # msg = msg.split()

    # --------------
    # preprocessing
    # --------------
    org_add_lf_dir = os.path.join(_LOG_DIR, 'org_add_lf')
    pre.mkdir_if_not_exists(org_add_lf_dir)

    # msg = msg.split()
    output_file = os.path.join(org_add_lf_dir, 'org_add_lf.txt')
    with open(output_file, 'w', encoding='utf-8') as add_lf:
        add_lf.write(msg)
        add_lf.write('\n')

    print('procedure_2')
    org_path = os.path.join(_LOG_DIR, 'org_add_lf')
    proc2_path = os.path.join(_LOG_DIR, 'procedure_2')
    pre.mkdir_if_not_exists(org_path)
    pre.mkdir_if_not_exists(proc2_path)
    input_file = os.path.join(org_path, 'org_add_lf.txt')
    output_file = os.path.join(proc2_path, 'proc2.txt')
    pre.parse_recipe(_KBM_MODEL, _KYTEA_PATH, input_file, output_file)

    print('procedure_3')
    proc3_path = os.path.join(_LOG_DIR, 'procedure_3')
    pre.mkdir_if_not_exists(proc3_path)
    input_file = output_file
    output_file = os.path.join(proc3_path, 'proc3.txt')
    morphology_file = output_file
    pre.insert_space_between_words(input_file, output_file)

    print('procedure_4_1')
    proc4_1_path = os.path.join(_LOG_DIR, 'procedure_4_1')
    pre.mkdir_if_not_exists(proc4_1_path)
    input_file = output_file
    output_file = os.path.join(proc4_1_path, 'proc4_1.txt')
    pre.ner_tagger_1(_KYTEA_PATH, _KNM_MODEL, input_file, output_file)

    print('procedure_4_2')
    proc4_2_path = os.path.join(_LOG_DIR, 'procedure_4_2')
    pre.mkdir_if_not_exists(proc4_2_path)
    input_file = output_file
    output_file = os.path.join(proc4_2_path, 'proc4_2.txt')
    ner_file = output_file
    pre.ner_tagger_2(_NESEARCH_PATH, input_file, output_file)

    print('result')
    result_path = os.path.join(_LOG_DIR, 'ner_result')
    pre.mkdir_if_not_exists(result_path)
    output_file = os.path.join(result_path, 'ner_result.txt')
    result = pre.Finalizer(
        morphology_file,
        ner_file,
        output_file,
    )
    result.result_output()

    # -----------------
    # output flowgraph
    # -----------------
    # likelifood data config
    index = [0, 2, 4, 5, 8]
    index_list = pd.DataFrame({
        'index': index,
    })
    likelihood_csv = os.path.join(_LOG_DIR, 'likelihood', 'likelihood.csv')
    likelihood = ky.load_likelihood(likelihood_csv, index_list)

    rne_map = os.path.join(_LOG_DIR, 'rne_category.txt')
    read_file = os.path.join(_LOG_DIR, 'ner_result', 'ner_result.txt')

    print('**************** rne_to_num_map ****************')
    rne_to_num_map = ky.rne_to_num(rne_map)
    print(rne_to_num_map)

    print('**************** num_to_rne_map ****************')
    num_to_rne_map = ky.num_to_rne(rne_map)
    print(num_to_rne_map)

    print('**************** word_to_order ****************')
    word_order = ky.word_to_order(read_file)
    print(word_order)

    print('**************** rne_word_map ****************')
    word_to_rne_map = ky.word_to_rne(read_file)
    print('rne_word_map')
    print(word_to_rne_map)

    print('**************** rne_word_map ****************')
    rne_to_word_map = ky.rne_to_word(read_file)
    print('rne_word_map')
    print(rne_to_word_map)

    dependency_list = ky.parse_dependency(
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
    ky.output_flowgraph(dependency_list)

    return render(request, 'flowgraph/index.html', params)
