#from graph import Graph
from hw7ex1_2 import DiGraph, Stack
import networkx as nx
import matplotlib.pyplot as plt

g = DiGraph([(1,2),(2,4),(3,5),(2,5),(1,5),(3,4),(3,1),(6,2),(6,3)])
#g = DiGraph([(1, 0), (0, 2), (2, 1), (0, 3), (3, 4)])
'''
G = nx.DiGraph()
G.add_nodes_from([1,2,3,4,5,6])
G.add_edges_from([(1,2),(2,4),(3,5),(2,5),(1,5),(3,4),(3,1),(6,2),(6,3)])
print("Print all vertices：{}".format(G.nodes()))
print("Print all edges：{}".format(G.edges()))
print("Print the number of edges：{}".format(G.number_of_edges()))
nx.draw_networkx(G)
plt.show()
'''
'''
#g.allDFS()

for s in g.vertexList:
    idx = g.vertexList.index(s)
    print(s)
    for e in g.tree[idx]:
        print(e)
'''
#stack = Stack()
#b = g.singleDFS(stack, 1)
#print(b)

a = g.stronglyConnectedComponent()
print(a)
'''
for i in g:
    print(i)
print("assss")
cc = g.reverse()
print("bssss")
for j in cc:
    print(j)
'''
'''
f = DiGraph([(2,1),(4,2),(5,3),(5,2),(5,1),(4,3),(1,3),(2,6),(3,6)])
stack = Stack()
b = f.singleDFS(stack, 3)
print(b)
'''