import community
import networkx as nx
import matplotlib.pyplot as plt
import sys
import heapq
from operator import itemgetter
import glob
from mle import mle_cal
import operator
from instanceProbCal import *
from findingGateway import *

#Randomly assigning timestamps to all the 34 nodes
timestamps = {1: 6.533, 2: 5.422, 3: 0.347, 4: 9.948, 5: 6.051, 6: 2.131, 7: 4.697, 8: 9.287, 9: 9.685, 10: 3.275, 11: 3.919, 12: 1.887, 13: 2.717, 14: 8.284, 15: 4.826, 16: 8.634, 17: 8.075, 18: 3.023, 19: 3.937, 20: 7.450, 21: 7.403, 22: 8.576, 23: 5.567, 24: 8.834, 25: 9.946, 26: 3.674, 27: 9.550, 28: 1.630, 29: 9.053, 30: 0.453, 31: 2.729, 32: 1.461, 33: 5.480, 34: 3.729}



def firstStage(filePath):
	files = glob.glob(filePath + '/instance[0-9].txt')
	#print(files)
	sensorNodes = []
	centralityScores = []
	probGraph, actualSource = prob_cal(filePath)
	maxProbOfGraph = probGraph.index(max(probGraph))
	colorOfMaxGraph = {}
	nodeLabels = []
	likelihoodOfNodes = {}
	instsanceNum = 0 	#this will indicate which istance we are processing in below loop

	for item in files:
	
		#------------------------CLUSTERING USING LOUVIAN METHOD-----------------------
	
		G = nx.read_edgelist(item, nodetype=int, data=(('weight',float),), create_using=nx.Graph())  
		selected_edge = [(u,v) for u,v,e in G.edges(data=True) if e['weight'] == 1]
		#print (selected_edge)

		for i in range(len(selected_edge)):
			G.remove_edge(selected_edge[i][0], selected_edge[i][1])
	
		dct = community.best_partition(G)
		if(instsanceNum == maxProbOfGraph):
			colorOfMaxGraph = dct
			maxProbGraph = G				
		#print(dct)
		labels = nx.get_edge_attributes(G,'weight')
		values = [dct.get(node) for node in G.nodes()]

		if(instsanceNum == 3):
			nx.draw_spring(G, cmap = plt.get_cmap('jet'), node_color = values, node_size=100, with_labels= True)
			plt.show()
		#print (G.edges())
	
		gatewayProb(item, dct)
		#------------------------FINDING THE SENSOR NODES-----------------------------
	
		#print("\n")
		G = nx.read_edgelist('code/BetaStage/newgateway.txt', nodetype=int,
		  data=(('weight',float),), create_using=nx.Graph())
		betweennessCentrality = nx.betweenness_centrality(G)
		#print(betweennessCentrality)
		topnSensorNodes = heapq.nlargest(8, betweennessCentrality.items(), key=itemgetter(1))
		topnSensorNodes = dict(topnSensorNodes)
		#print(topnSensorNodes)
		sensorNodes.append(topnSensorNodes)
		sensorNodesArrivalTime = {}
		#intersect = []
		for item in timestamps.keys():
			if item in topnSensorNodes.keys():
				sensorNodesArrivalTime[item] = timestamps[item]
		#print(sensorNodesArrivalTime)

		#------------------------CALCULATING MLE---------------------------------
	
		cenOfGatewayNodes, nodesList = mle_cal('code/BetaStage/newgateway.txt')
		centralityScores.append(cenOfGatewayNodes)
		for node in nodesList :
			val = cenOfGatewayNodes[node] * probGraph[instsanceNum]
			if node in likelihoodOfNodes :
				likelihoodOfNodes[node] += val
			else :
				likelihoodOfNodes[node] = val
		instsanceNum += 1
		if(instsanceNum == 4):
			#print("likelihood of nodes is :", likelihoodOfNodes)
			#print("\n\n")
	
		#------------------------PLOTTING GATEWAY GRAPHS-----------------------------

			labels = nx.get_edge_attributes(G,'weight')
			nx.draw_spring(G, cmap = plt.get_cmap('jet'), node_size=100, with_labels= True)
			plt.show()

		#----------------------------------------------------------------------------
	
	#print(sensorNodes)
	maxSensorNode = max(likelihoodOfNodes.items(), key=operator.itemgetter(1))[0]
	#print(maxSensorNode)
	print("probabilities of graph : ",probGraph)
	#maxProbOfGraph = probGraph.index(max(probGraph))
	#print(colorOfMaxGraph)
	colorofMaxSensorNode = colorOfMaxGraph[maxSensorNode]
	#print(colorofMaxSensorNode)
	listOfKeys = [key  for (key, value) in colorOfMaxGraph.items() if value == colorofMaxSensorNode]
	#print(listOfKeys)
	H = maxProbGraph.subgraph(listOfKeys)
	nx.draw_spring(H, cmap = plt.get_cmap('jet'), node_size=100, with_labels= True)
	plt.show()
	edgesOfCandidateCluster = list(H.edges())
	f = open('code/BetaStage/secondStageInput.txt', 'w')
	for t in edgesOfCandidateCluster:
	    line = ' '.join(str(x) for x in t)
	    #print(line)
	    f.write(line + '\n')
	f.close()		
	
	return actualSource		

