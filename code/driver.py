import os
import glob
import sys
sys.path.append('./DiffusionModel')
sys.path.append('./Create_Instance')
from SI import siModel
from edgewt import createInstance


files = glob.glob('./datasets/*.txt')

for filename in files:
	actualSource, g = siModel(filename)#, beta, percentage_infected, numOfIterations
	base = os.path.basename(filename)
	dirName = os.path.splitext(base)[0]
	createInstance(dirName)

