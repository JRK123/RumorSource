import random

fileHandle = open("instance4.txt","w")
with open('higgs-retweet_network.txt') as file:
	array = file.readlines()
	
	for i in range(0,len(array)):
		src, dst = array[i].split(" ")
		dst = dst.strip('\n')	
		fileHandle.write(str(src) + " " + str(dst) + " " + str("{0:.2f}".format(random.random())) + "\n")
fileHandle.close()
