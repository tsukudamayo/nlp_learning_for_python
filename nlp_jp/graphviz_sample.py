from graphviz import Digraph

G = Digraph(format='png')
G.attr('node', shape='circle')

N = 15

for i in range(N):
    G.node(str(i), str(i))
for i in range(N):
    if (i - 1) // 2 >= 0:
        G.edge(str((i - 1) // 2), str(i))
print(G)

G.render('binary_tree')
