import penman
from penman.graph import Graph
g = penman.decode('''
(w / want-01
   :ARG0 (b / boy)
   :polarity -
        :ARG1 (g / go
            :ARG0 b))''')
print(g.triples)
print(g.attributes())
print(g.variables())
a = g.triples

graph = Graph(a)

en = penman.encode(graph, top='w')
print(en)
