import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics.SIModel as si
import matplotlib.pyplot as plt

# Network topology
g = nx.read_edgelist('higgs-retweet_network.txt', nodetype=int,
	  data=(('weight',float),), create_using=nx.Graph())
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
iterations = model.iteration_bunch(5)

for i in iterations:
    iter_ind=i['iteration']
    c=i['node_count']
    node_status_list=i['status']
    print("Iteration:",iter_ind)
    print(node_status_list)
    listOfKeys = [key  for (key, value) in node_status_list.items() if value == 1]
    if(listOfKeys != []):
    	inf.extend(listOfKeys)

print(inf)
print(len(inf))
h = g.subgraph(inf)
print(len(h))

edgesOfCandidateCluster = list(h.edges())
f = open('./network.txt', 'w')
for t in edgesOfCandidateCluster:
    line = ' '.join(str(x) for x in t)
    #print(line)
    f.write(line + '\n')
f.close()

bfs_dict = dict(nx.bfs_successors(h, inf[0]))
print ("successor ", bfs_dict)

nx.draw_spring(h, cmap = plt.get_cmap('jet'), node_size=100, with_labels= True)
plt.show()

