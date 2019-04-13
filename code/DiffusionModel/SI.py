import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics.SIModel as si
import matplotlib.pyplot as plt

def siModel(filename):
	# Network topology
	g = nx.read_edgelist(filename, nodetype=int, data=(('weight',float),), create_using=nx.Graph())
	# Model selection
	model = si.SIModel(g)

	# Model Configuration
	cfg = mc.Configuration()
	cfg.add_model_parameter('beta', 0.34)
	cfg.add_model_parameter("percentage_infected", 0)
	model.set_initial_status(cfg)
	col=[]
	sus=[]
	inf=[]

	# Simulation execution
	iterations = model.iteration_bunch(4)

	for i in iterations:
	    iter_ind=i['iteration']
	    #c=i['node_count']
	    node_status_list=i['status']
	    #print("Iteration:",iter_ind)
	    #print(node_status_list)
	    listOfKeys = [key  for (key, value) in node_status_list.items() if value == 1]
	    #print(listOfKeys)
	    if(listOfKeys != []):
	    	inf.extend(listOfKeys)

	#print("infected nodes = ", inf)
	print("total nodes", len(g))
	print("infected nodes", len(inf))
	if(len(inf) > 5000):
		sys.exit()
	h = g.subgraph(inf)
	#print(len(h))

	edgesOfInfectedGraph = list(h.edges())
	f = open('DiffusionModel/InfectedGraph.txt', 'w')
	f.write(str(inf[0]) + '\n')
	for t in edgesOfInfectedGraph:
	    line = ' '.join(str(x) for x in t)
	    #print(line)
	    f.write(line + '\n')
	f.close()

	#nx.draw_spring(h, cmap = plt.get_cmap('jet'), node_size=100, with_labels= True)
	#plt.show()
	
	return inf[0], h

