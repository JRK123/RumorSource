import networkx as nx
import matplotlib.pyplot as plt

g = nx.read_edgelist('instance1.txt', nodetype=int,
  data=(('weight',float),), create_using=nx.Graph())

#print(g.edges(data=True))

sp = nx.spring_layout(g)
nx.draw(g, sp)
labels = nx.get_edge_attributes(g,'weight')
nx.draw_networkx_edge_labels(g,pos=sp,edge_labels=labels)

plt.show()
