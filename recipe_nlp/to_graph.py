import pandas as pd
from graphviz import Digraph


def output_graph():
    G = Digraph(format="png")
    G.attr("node", shape="square", style="filled", fontname='MS Gothic')
    G.edge("ほうれん草","切る",label="0.8")
    G.edge("根元","切り",label="0.2")
    G.edge("切り","切る",label="0.2")
    G.edge("幅4cm","切る",label="0.5")
    G.edge("じゃがいも","切る", label="0.8")
    G.edge("皮","むく",label="0.5")
    G.render("graphs")

def main():
    output_graph()


if __name__ == '__main__':
    main()
