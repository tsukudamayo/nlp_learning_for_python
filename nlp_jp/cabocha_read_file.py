import sys
import CaboCha

c = CaboCha.Parser('-f1')

for line in open('recipe_sample_00.txt', 'r', encoding='utf-8'):
    tree = c.parse(line)
    print(tree.toString(CaboCha.FORMAT_TREE))
    print(tree.toString(CaboCha.FORMAT_TREE_LATTICE))
