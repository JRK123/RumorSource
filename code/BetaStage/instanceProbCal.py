#------------------CALCULATES PROBABILITY OF EACH INSTANCE----------------
def prob_cal():  
	W = [[] for i in range(4)]
	for i in range(4):
		with open('code/Create_Instance/instance' + str(i+1) + '.txt') as file:
			arr = file.readlines()
			for j in range(0,len(arr)):
				src, dest, wgt = arr[j].split(" ")
				W[i].append(float(wgt))
	
	probGraph = []
	prod = 1
	for i in range(4):
		for j in range(0,len(W[i])):
			prod = prod * W[i][j]
		probGraph.append(float(prod))
	
	#print(probGraph)
	return probGraph

