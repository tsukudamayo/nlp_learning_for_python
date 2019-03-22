from graphviz import Digraph


# -------------
# load dataset
# -------------
scores = {}
words = ['boys', 'often', 'play', 'games']
with open('mst_data_sample.csv', 'r', encoding='utf-8') as r:
    lines = r.readlines()

for line in lines:
    line = line.rstrip('\n')
    line = line.split(',')
    print(line)
    edges = []
    edges.append(line[0])
    edges.append(line[1])
    edges = tuple(edges)
    nodes = {edges: line[2]}
    scores.update(nodes)

# ---------------
# original graph
# ---------------
G = Digraph(format='png')
G.attr('node', shape='square', style='filled', fontname='MS Gothic')
for k, v in scores.items():
    print(k, v)
    print(k[0] + ' => ' + k[1])
    G.edge(k[0], k[1], label=v)
G.render('mst_before')

# -----------------
# Chi-Liu Edomonds
# -----------------
# 1. find max score dependency word for each words (not ROOT)
for k, v in sorted(scores.items(), key=lambda x: -int(x[1])):
    for word in words:
        print('word', word)
        if k[0] == word:
            print(k, v)

