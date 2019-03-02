import community
import networkx as nx
import matplotlib.pyplot as plt
import sys

G = nx.read_edgelist('higgs-retweet_network.txt', nodetype=int,
  data=(('weight',float),), create_using=nx.Graph())
dict = community.best_partition(G)
print(dict)
labels = nx.get_edge_attributes(G,'weight')
values = [dict.get(node) for node in G.nodes()]

nx.draw_spring(G, cmap = plt.get_cmap('jet'), node_color = values, node_size=100, with_labels= True)
plt.show()

fileHandle = open("newgateway.txt","w")
adj = [[] for i in range(len(dict)+1)]
#flag = 0
#print(adjacency)
with open('higgs-retweet_network.txt') as file:
	array1 = file.readlines()
	#print(array1)
	for i in range(0,len(array1)):
		src, dest = array1[i].split(" ")
		adj[int(src)].append(int(dest))
		adj[int(dest)].append(int(src))
	#print(adj)
	for j in range(1,len(adj)):
		flag = 0
		for k in range(0,len(adj[j])):
			if(dict[j] != dict[adj[j][k]]):
				flag = 1
				break;
		#print(j, flag)
		if(flag == 0):
			#print(adj[j])
			for p in range(0,len(adj[j])):
				#print(adj[j][p])
				adj[adj[j][p]].remove(j)
			adj[j] = []
	print(adj)
	for a in range(len(adj)):
		for b in range(len(adj[a])):
			fileHandle.write(str(a) + " " + str(adj[a][b]) + "\n") 
fileHandle.close()
	
G = nx.read_edgelist('newgateway.txt', nodetype=int,
  data=(('weight',float),), create_using=nx.Graph())
b = nx.betweenness_centrality(G)
print(b)

labels = nx.get_edge_attributes(G,'weight')
nx.draw_spring(G, cmap = plt.get_cmap('jet'), node_size=100, with_labels= True)
plt.show()
