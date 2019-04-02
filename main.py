import sys
sys.path.append('/home/ganesh/Documents/RumorSource/code/DiffusionModel')
sys.path.append('/home/ganesh/Documents/RumorSource/code/Create_Instance')
sys.path.append('/home/ganesh/Documents/RumorSource/code/BetaStage')
from SI import siModel
from edgewt import createInstance
from firststage import *
from secondStage import *

actualSource, bfs_dict, g = siModel('code/DiffusionModel/higgs-retweet_network.txt')

createInstance()

firstStage()

predictedSource = secondStage()

print('actualSource = ',actualSource)
print('predictedSource = ', predictedSource)

neighbours = bfs_dict[actualSource]
print('neighbours = ', neighbours)

nodeList = []
flag = 0
if(predictedSource in neighbours):
	print('within 1 hop')

else:
	for node in neighbours:
		if(node in bfs_dict.keys()):
			if(predictedSource in bfs_dict[node]):		#check if key is in dict
				print('within 2 hop')
				flag = 1
				break
			else:
				nodeList.extend(bfs_dict[node])	

if(flag == 0):
	for node in nodeList:
		if(node in bfs_dict.keys()):
			if(predictedSource in bfs_dict[node]):		#check if key is in dict
				print('within 3 hop')
				break
	
nx.draw_spring(g, cmap = plt.get_cmap('jet'), node_size=100, with_labels= True)
plt.show()

