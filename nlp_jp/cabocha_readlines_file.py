import sys
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

c = CaboCha.Parser('-f1')

with open('recipe_sample_00.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    tree = c.parse(line)
    print(tree.toString(CaboCha.FORMAT_TREE))
    # print(tree.toString(CaboCha.FORMAT_TREE_LATTICE))
    chunk_dic = {}
    chunk_id = 0
    for i in range(0, tree.size()):
        token = tree.token(i)
        if token.chunk:
            chunk_dic[chunk_id] = token.chunk
            chunk_id += 1
    tuples = []
    for chunk_id, chunk in chunk_dic.items():
        if chunk.link > 0:
            from_surface = get_part_of_speach(tree, chunk)
            to_chunk = chunk_dic[chunk.link]
            to_surface = get_part_of_speach(tree, to_chunk)
            tuples.append((from_surface, to_surface))
    G = Digraph(format='png')
    G.attr('node', shape='square', style='filled', fontname='MS Gothic')
    for t in tuples:
        print(t[0] + ' => ' + t[1])
        G.edge(t[0], t[1])
    G.render(str(idx))

