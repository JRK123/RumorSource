import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def mle_cal(filename) : 
	G = nx.read_edgelist(filename, nodetype=int, data=(('weight',float),), create_using=nx.Graph())
	#nx.draw_spring(G, node_size=100, with_labels= True)
	#plt.show()

	bfs_dict = {}

	centrality_scores = {}

	no_nodes = len(G)
	nodes_list = list(G.nodes())
	'''
	bfs_list = list(nx.bfs_edges(G, 1))
	g = nx.Graph()
	g.add_edges_from(bfs_list)
	nx.draw_spring(g, node_size=100, with_labels= True)
	plt.show()
	'''

	up_messages_t = []
	up_messages_p = []
	def cal_t(i) :
		count = 0
		for k in bfs_dict[i]:
			count = count + up_messages_t[k]
	
		return count

	def cal_p(i) :
		count_p = 1
		for k in bfs_dict[i]:
			count_p = count_p * up_messages_p[k]
		return count_p

	def rumor_centrality_up(up_messages_t,up_messages_p, source):
		for i in bfs_dict[source] :
			if i not in bfs_dict.keys():
				#up_messages_t[i] = 1
				#up_messages_p[i] = 1
				continue
			else : 
				rumor_centrality_up(up_messages_t,up_messages_p,i)
				up_messages_t[i] = up_messages_t[i] + cal_t(i)
				up_messages_p[i] = up_messages_t[i] * cal_p(i)
				
		return up_messages_t, up_messages_p

	def rumor_centrality(source):
		messages_t,messages_p = rumor_centrality_up(up_messages_t,up_messages_p, source)
		return messages_t,messages_p

	for source in nodes_list : 
		#print("source = ", source)
		bfs_dict = dict(nx.bfs_successors(G, source))
		#print ("successor ", bfs_dict)
		up_messages_t = [1]*50
		up_messages_p = [1]*50
		messages_t,messages_p = rumor_centrality(source)
		messages_t[source] += cal_t(source)
		messages_p[source] =messages_t[source] * cal_p(source)
		centrality_scores[source] = 1.0/float(messages_p[source])
		#print(messages_t)
		#print(messages_p)
		#print("\n")

	#print (centrality_scores)
	#print (max(centrality_scores.values()))
	
	return centrality_scores, nodes_list

