import random

def createInstance():
	for j in range(1, 5):
		fileHandle = open("code/Create_Instance/instance"+str(j)+".txt","w")
		with open('code/DiffusionModel/network.txt') as file:
			array = file.readlines()
	
			for i in range(0,len(array)):
				src, dst = array[i].split(" ")
				dst = dst.strip('\n')	
				wt = str("{0:.2f}".format(random.random()))
				if(wt == '0.00'):
					wt = '0.02'
				fileHandle.write(str(src) + " " + str(dst) + " " + wt + "\n")
		fileHandle.close()
