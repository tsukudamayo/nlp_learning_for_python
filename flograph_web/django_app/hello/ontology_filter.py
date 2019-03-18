import os

import pandas as pd
import CaboCha
from graphviz import Digraph


def get_part_of_speach(tree, chunk):
    surface = ''
    for i in range(chunk.token_pos, chunk.token_pos + chunk.token_size):
        token = tree.token(i)
        features = token.feature.split(',')
        if features[0] == '名詞':
            surface += token.surface
        elif features[0] == '形容詞':
            surface += features[6]
        elif features[0] == '動詞':
            surface += features[6]
            break

    return surface


def convert_chunk_format(parser, chunk, df, query_col, answer_col):
    """
    refer a database for each chunk and convert words
    -------------------------------------------------------------------------
    input
      parser: Cabocha.Parser('-f1')
      line: array of strings
      df: an refference data like ontology database
      query_col: the column to send query
      answer_col: the column that refers to the word to be converted
    output
      surface: an array all words
      converted_strings: an array contaning converted words
    -------------------------------------------------------------------------
    """
    surface = ''
    converted_strings = []
    for i in range(chunk.token_pos, chunk.token_pos + chunk.token_size):
        token = parser.token(i)
        # print('pos', i)
        # print('token')
        # print(token.feature)
        # features = token.feature.split(',')
        # print(features[6])
        if len(df[df[query_col] == token.surface]) > 0:
            print(token.surface)
            print(df[df[query_col] == token.surface][answer_col].values[0])
            search_index = df[df[query_col] == token.surface][answer_col].values[0]
            print('================')
            print('before : ', token.surface)
            print('after  : ', search_index)
            print('================')
            if token.surface == search_index:
                surface += token.surface
            else:
                print('* ' + search_index + ' *')
                surface += search_index
                converted_strings.append(search_index)
        else:
            surface += token.surface
    return surface, converted_strings


def convert_sentence_format(parser, lines, df, query_col, answer_col):
    """
    converted words and make the graph an image
    -------------------------------------------------------------------------
    input
      parser: Cabocha.Parser('-f1')
      line: array of strings
      df: an refference data like ontology database
      query_col: the column to send query
      answer_col: the column that refers to the word to be converted
    output
      converted_recipe: an array containing converted recipes
      converted_strings: an array contaning converted words
    ------------------------------------------------------------------------- 
    lines = 'じゃがいもは皮をむいて5mm角の棒状に切り、水に3分ほどさらして水けをきる。'

     -> convert_sentence_format(parser, lines, df, query_col, answer_col)

                                        |
                                    'じゃがいも'
                                        |
                                       df
                            ------------------------
                             answer_col | query_col
                            ------------------------
                            ジャガイモ  | じゃがいも
                                        |
                                        |
    append(converted_strings)<------ジャガイモ

    """
    converted_recipe = []
    converted_strings = []
    for idx, line in enumerate(lines):
        tree = parser.parse(line)
        print(idx)
        print(line)
        chunk_dic = {}
        chunk_id = 0
        for i in range(0, tree.size()):
            token = tree.token(i)
            if token.chunk:
                chunk_dic[chunk_id] = token.chunk
                chunk_id += 1

        convert_sentences = ''
        for chunk_id, chunk in chunk_dic.items():
            sentence, strings = convert_chunk_format(tree, chunk, df, query_col, answer_col)
            convert_sentences += sentence
            converted_strings.extend(strings)
        converted_recipe.append(convert_sentences)
        print(convert_sentences)
        print(converted_strings)

    return converted_recipe, converted_strings


def generate_convert_flowgraph(parser, converted_recipe, converted_strings, convert_color):
    """
    color the converted words and make the graph an image 
    -------------------------------------------------------------------------
    input
      parser: Cabocha.Parser('-f1')
      converted_recipe: array of strings
      converted_strings: set of conveted strings by like ontology database
      converted_color: color name ex. 'yellow', 'blue', 'red'...
    output
      png file which written Graph
    -------------------------------------------------------------------------
    """
    print('convert recipe')
    print(converted_recipe)
    for idx, line in enumerate(converted_recipe):
        convert_tree = parser.parse(line)
        chunk_dic = {}
        chunk_id = 0
        for i in range(0, convert_tree.size()):
            token = convert_tree.token(i)
            if token.chunk:
                chunk_dic[chunk_id] = token.chunk
                chunk_id += 1

        tuples = []
        for chunk_id, chunk in chunk_dic.items():
            if chunk.link > 0:
                from_surface = get_part_of_speach(convert_tree, chunk)
                to_chunk = chunk_dic[chunk.link]
                to_surface = get_part_of_speach(convert_tree, to_chunk)
                tuples.append((from_surface, to_surface))
        G = Digraph(format='png')
        G.attr('node', shape='square', style='filled', fontname='MS Gothic')
        for t in tuples:
            print(t[0] + ' => ' + t[1])
            G.edge(t[0], t[1])
            if t[0] in converted_strings:
                G.node(t[0], shape='square', style='filled', fontname='MS Gothic', color=convert_color)
            elif t[1] in converted_strings:
                G.node(t[1], shape='square', style='filled', fontname='MS Gothic', color=convert_color)
            else:
                pass
        dst_dir = os.path.join(os.path.dirname(__file__), 'static/hello/assets/img')
        G.render(os.path.join(dst_dir, 'flowgraph'))


def main():
    c = CaboCha.Parser('-f1')

    with open('recipe_sample_00.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # -------------------
    # recipe to ontology
    # -------------------
    df = pd.read_csv('data/ontology/synonym.tsv', delimiter='\t', header=None, encoding='utf-8')
    print(df)
    print(df[2])
    print(df[df[2] == 'じゃがいも'])
    print(df[df[2] == 2])
    print(len(df[df[2] == 2]))
    # convert format
    query_col = 2
    answer_col = 1
    converted_recipe, converted_strings = convert_sentence_format(c, lines, df, query_col, answer_col)
    # generate flowgraph
    generate_convert_flowgraph(c, converted_recipe, converted_strings, 'yellow')

    # -------------------------
    # ontology to microwaveBU
    # -------------------------
    df_mw_bu = pd.read_csv('data/microwave_bu.csv', header=0)
    print(df_mw_bu.head())
    print(df_mw_bu['取説では使用なし'].head())
    print(df_mw_bu[df_mw_bu['取説では使用なし'] == '玉ねぎ'])
    # convert format
    query_col = '取説では使用なし'
    answer_col = '正'
    converted_recipe, converted_strings = convert_sentence_format(c, converted_recipe, df_mw_bu, query_col, answer_col)
    # generate flowgraph
    generate_convert_flowgraph(c, converted_recipe, converted_strings, 'blue')


if __name__ == '__main__':
    main()
