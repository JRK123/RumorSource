import community
import networkx as nx
import matplotlib.pyplot as plt
import sys
import heapq
from operator import itemgetter
import glob
from mle import mle_cal

#------------------CALCULATES PROBABILITY OF EACH INSTANCE----------------
def prob():  
	W = [[] for i in range(4)]
	for i in range(4):
		with open('./../Create_Instance/instance' + str(i+1) + '.txt') as file:
			arr = file.readlines()
			for j in range(0,len(arr)):
				src, dest, wgt = arr[j].split(" ")
				W[i].append(float(wgt))
	
	prob_graph = []
	prod = 1
	for i in range(4):
		for j in range(0,len(W[i])):
			prod = prod * W[i][j]
		prob_graph.append(float(prod))
	
	#print(prob_graph)
	return prob_graph

#Randomly assigning timestamps to all the 34 nodes
timestamps = {1: 6.533, 2: 5.422, 3: 0.347, 4: 9.948, 5: 6.051, 6: 2.131, 7: 4.697, 8: 9.287, 9: 9.685, 10: 3.275, 11: 3.919, 12: 1.887, 13: 2.717, 14: 8.284, 15: 4.826, 16: 8.634, 17: 8.075, 18: 3.023, 19: 3.937, 20: 7.450, 21: 7.403, 22: 8.576, 23: 5.567, 24: 8.834, 25: 9.946, 26: 3.674, 27: 9.550, 28: 1.630, 29: 9.053, 30: 0.453, 31: 2.729, 32: 1.461, 33: 5.480, 34: 3.729}

files = glob.glob(r'./../Create_Instance/instance[0-9].txt')
#print(files)

sensorNodes = []
delt = []
centrality_scores = []
prob_grph = prob()
nodes_labels = []

for item in files:
	
	#------------------------CLUSTERING USING LOUVIAN METHOD-----------------------
	
	G = nx.read_edgelist(item, nodetype=int, data=(('weight',float),), create_using=nx.Graph())  
	selected_edge = [(u,v) for u,v,e in G.edges(data=True) if e['weight'] == 1]
	#print (selected_edge)

	for i in range(len(selected_edge)):
		G.remove_edge(selected_edge[i][0], selected_edge[i][1])
	
	dct = community.best_partition(G)
	#print(dct)
	labels = nx.get_edge_attributes(G,'weight')
	values = [dct.get(node) for node in G.nodes()]

	nx.draw_spring(G, cmap = plt.get_cmap('jet'), node_color = values, node_size=100, with_labels= True)
	plt.show()
	print (G.edges())

	fileHandle = open("newgateway.txt","w")
	adj = [[] for i in range(len(dct)+1)]    #Adjacency list of length (no of nodes + 1)
	
	#-------------------------FINDING THE GATEWAY NODES---------------------------	
	
	with open(item) as file: 						# open each instance from directory
		array1 = file.readlines() 						# read lines from each instance
		for i in range(0,len(array1)): 					# i -> 0 to 78
			src, dest, wgt = array1[i].split(" ") 			# split source, dest and weight
			adj[int(src)].append(int(dest))  				# add destination to the index of src 
			adj[int(dest)].append(int(src))  				# add source to the index at dest
		for j in range(1,len(adj)): 					# j-> 1 to 35 
			flag = 0 						# set flag to 0
			for k in range(0,len(adj[j])):				# k -> 0 to no. of neighbours of j
				if(dct[j] != dct[adj[j][k]]):			# if colour of j is not equal to colour of any of its neighbour		
					flag = 1				# then set flag as 1
					break;					# break the loop
			if(flag == 0):						# if all neighbouring colours are same
				for p in range(0,len(adj[j])):			# p-> 0 to no. of neighbours of j
					adj[adj[j][p]].remove(j)		# remove j from the neighbour's list of links
				adj[j] = []					# empty j
		#print(adj)							# return adj
		#print("\n")
		for a in range(len(adj)):
			for b in range(len(adj[a])):
				fileHandle.write(str(a) + " " + str(adj[a][b]) + "\n") 
	fileHandle.close()
	
	#------------------------FINDING THE SENSOR NODES-----------------------------
	
	#print("\n")
	G = nx.read_edgelist('newgateway.txt', nodetype=int,
	  data=(('weight',float),), create_using=nx.Graph())
	b = nx.betweenness_centrality(G)
	#print(b)
	sensor_nodes = heapq.nlargest(8, b.items(), key=itemgetter(1))
	sensor_nodes = dict(sensor_nodes)
	#print(sensor_nodes)
	sensorNodes.append(sensor_nodes)
	sensorNodes_arrivalTime = {}
	#intersect = []
	for item in timestamps.keys():
		if item in sensor_nodes.keys():
			sensorNodes_arrivalTime[item] = timestamps[item]
	#print(sensorNodes_arrivalTime)

	#------------------------CALCULATING DELTA T---------------------------------
	
	node_centrality_mle_file, nodes_list = mle_cal('newgateway.txt')
	centrality_scores.append(node_centrality_mle_file)
	
	#------------------------PLOTTING GATEWAY GRAPHS-----------------------------

	labels = nx.get_edge_attributes(G,'weight')
	nx.draw_spring(G, cmap = plt.get_cmap('jet'), node_size=100, with_labels= True)
	plt.show()

	#----------------------------------------------------------------------------
	
print(sensorNodes)
print("")
print("Centrality scores of graph 1:", centrality_scores[0])
print("")
print("Centrality scores of graph 2:", centrality_scores[1])
print("")
print("Centrality scores of graph 3:", centrality_scores[2])
print("")
print("Centrality scores of graph 4:", centrality_scores[3])
print("")
print("Probability of each instance:", prob_grph)
'''
print(centrality_scores[0]
var = 0


for i in range(0,19):
	for j in range(0,3):
		var += centrality_scores[j][i] * prob_grph[j]
	print(var)
'''	
		
		
		
		
