import random
import os

def createInstance(dirName):
	path = "Create_Instance/" + dirName
	if not os.path.exists(path):
    		os.mkdir(path)
	for j in range(1, 5):
		fileHandle = open(path+"/instance"+str(j)+".txt","w")
		with open('DiffusionModel/InfectedGraph.txt') as file:
			array = file.readlines()
			actualSource = array[0]
			fileHandle.write(actualSource)
			for i in range(1,len(array)):
				src, dst = array[i].split(" ")
				dst = dst.strip('\n')	
				wt = str("{0:.2f}".format(random.random()))
				if(wt == '0.00'):
					wt = '0.02'
				fileHandle.write(str(src) + " " + str(dst) + " " + wt + "\n")
		fileHandle.close()
