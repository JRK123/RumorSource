import sys
sys.path.append('./code/BetaStage')
from firststage import *
from secondStage import *

dirName = input("Enter the name of network : ")
instancePath = "./code/Create_Instance/" + str(dirName)
filePath = "./code/datasets/" + str(dirName) + ".txt"
g = nx.read_edgelist(filePath, nodetype=int, data=(('weight',float),), create_using=nx.Graph())

actualSource = int(firstStage(instancePath))

predictedSource = secondStage()
color_map = []

#print(filePath)

bfs_dict = dict(nx.bfs_successors(g, actualSource))
#print ("successor ", bfs_dict)
print('actualSource = ',actualSource)
print('predictedSource = ', predictedSource)

neighbours = bfs_dict[actualSource]
#print('neighbours = ', neighbours)

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


for node in g:
    if node == actualSource :
        color_map.append('yellow')
    elif node == predictedSource :
        color_map.append('blue')
    else :
    	color_map.append('red')	
	
nx.draw(g, node_color = color_map, node_size = 100, with_labels = 'true')
plt.show()

