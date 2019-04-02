def gatewayProb(item, dct):
	fileHandle = open("code/BetaStage/newgateway.txt","w")
	adj = [[] for i in range(max(dct, key=int)+1)]    #Adjacency list of length (no of nodes + 1)
	
	#-------------------------FINDING THE GATEWAY NODES---------------------------	
	
	with open(item) as file: 						# open each instance from directory
		array = file.readlines() 					# read lines from each instance
		for i in range(0,len(array)): 					# i -> 0 to 78
			src, dest, wgt = array[i].split(" ") 			# split source, dest and weight
			adj[int(src)].append(int(dest))  			# add destination to the index of src 
			adj[int(dest)].append(int(src))  			# add source to the index at dest
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
