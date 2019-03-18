from django.shortcuts import render
from django.http import HttpResponse

import os
import pandas as pd
import CaboCha
from graphviz import Digraph

from . import ontology_filter


# Create your views here.
def index(request):
    params = {
        'title': 'Hello/Index',
        'msg': 'お名前は?',
        }

    return render(request, 'hello/index.html', params)


def form(request):
    message = request.POST['msg']
    recipe = message.split()
    print(recipe)

    c = CaboCha.Parser('-f1')

    # with open('recipe_sample_00.txt', 'r', encoding='utf-8') as f:
    #     lines = f.readlines()

    # -------------------
    # recipe to ontology
    # -------------------
    ontology_file = os.path.join(os.path.dirname(__file__), 'data/ontology/synonym.tsv')
    df = pd.read_csv(ontology_file, delimiter='\t', header=None, encoding='utf-8')
    # convert format
    query_col = 2
    answer_col = 1
    converted_recipe, converted_strings = ontology_filter.convert_sentence_format(
        c, recipe, df, query_col, answer_col
    )
    # generate flowgraph
    ontology_filter.generate_convert_flowgraph(
        c, converted_recipe, converted_strings, 'yellow'
    )

    params = {
        'title': 'Hello/Form',
        'msg': 'レシピをテキストボックスに入力し下さい',
        'answer': recipe,
        }

    return render(request, 'hello/index.html', params)
