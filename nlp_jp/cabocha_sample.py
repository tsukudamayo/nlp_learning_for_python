import sys
import CaboCha

c = CaboCha.Parser()

sentence = str(sys.argv[1])

print(c.parseToString(sentence))

tree = c.parse(sentence)

print(tree.toString(CaboCha.FORMAT_TREE))
print(tree.toString(CaboCha.FORMAT_LATTICE))
