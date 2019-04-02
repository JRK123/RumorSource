import random

for j in range(1, 5):
	fileHandle = open("code/Create_Instance/instance"+str(j)+".txt","w")
	with open('code/DiffusionModel/network.txt') as file:
		array = file.readlines()
	
		for i in range(0,len(array)):
			src, dst = array[i].split(" ")
			dst = dst.strip('\n')	
			fileHandle.write(str(src) + " " + str(dst) + " " + str("{0:.2f}".format(random.random())) + "\n")
	fileHandle.close()
