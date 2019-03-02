from __future__ import division
import  matplotlib
from pylab import *
import random as rnd
import networkx as nx
from random import randrange
import random


def reduce(ad_list,node):
    for neigh in ad_list[node-1]:         #for each neighour in the given node
        if node in ad_list[neigh-1]:      #if node is in the neighbour list
            ad_list[neigh-1].remove(node) #remove from the neigbour the node   
    ad_list[node-1] = []                  #finally delete this node

def build_adjacency(filename, min_degree, num_nodes): #0 indexed, but actual index = stored index-1
    adjacency = [[] for i in range(num_nodes)]   
#    count = [[] for i in range(num_nodes)]
    with open(filename) as f:
        for line in f:
            cur_line = line.split(" ")     # space is delimiter
            cur_node = int(cur_line[0])    #Which node are we dealing with
            cur_neigh = int(cur_line[1])   #what is it's neighbour
            if (cur_node == num_nodes+1):    #num_nodes + 1th node, we're done
                break
            if (cur_neigh > num_nodes):          # if the neigh>num_nodes it is out of range
                continue
            else:
                adjacency[cur_node-1].append(cur_neigh)       #connect node to neighbour
                adjacency[cur_neigh-1].append(cur_node)       #connect neighbor to node
#    for i in xrange(0,len(adjacency)):     #debugging code:creates a copy of adjacency before modification
#        count[i] = adjacency[i][:] 
    for node in xrange(1,num_nodes+1):            #see all the nodes
        if (len(adjacency[node-1])< min_degree): # if less than min_degree
            temp_neigh = adjacency[node-1]       #store a copy if it's neighbours
            reduce(adjacency,node)                 #remove the node and remove it from it's neighbours
            for neigh in temp_neigh:        #check the neighbours to see if they need to be deleted
                if(len(adjacency[neigh-1])< min_degree):
                    reduce(adjacency,neigh)
            
    return adjacency#,count





rcParams['figure.figsize'] = 12, 12  # that's default image size for this interactive session

def draw_graph(graph, labels=None, graph_layout='shell',
               node_size=1600, node_color='blue', node_alpha=0.3,
               node_text_size=12,
               edge_color='blue', edge_alpha=0.3, edge_tickness=1,
               edge_text_pos=0.3,
               text_font='sans-serif'):
    """ 
    Based on: https://www.udacity.com/wiki/creating-network-graphs-with-python
    We describe a graph as a list enumerating all edges.
    Ex: graph = [(1,2), (2,3)] represents a graph with 2 edges - (node1 - node2) and (node2 - node3)
    """
    
    # create networkx graph
    G=nx.Graph()

    # add edges
    for edge in graph:
        G.add_edge(edge[0], edge[1])

    # these are different layouts for the network you may try
    # shell seems to work best
    if graph_layout == 'spring':
        graph_pos=nx.spring_layout(G)
    elif graph_layout == 'spectral':
        graph_pos=nx.spectral_layout(G)
    elif graph_layout == 'random':
        graph_pos=nx.random_layout(G)
    else:
        graph_pos=nx.shell_layout(G)

    # draw graph
    nx.draw_networkx_nodes(G,graph_pos,node_size=node_size, 
                           alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_edges(G,graph_pos,width=edge_tickness,
                           alpha=edge_alpha,edge_color=edge_color)
    nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size,
                            font_family=text_font)
    # show graph
    plt.show()
    
    








def adjacency_to_graph(adjacency):
    graph = []    #initialise
    for num in xrange(1,len(adjacency)+1):  #we need to check every node
        for neigh in adjacency[num-1]:      #for the neighbour of the current node in the adjacency list
            tup = (num,neigh)               #create a tuple of the current node and it's current neighbor
            if (neigh,num) not in graph:     #since (node,neigh) is the same as (neigh,node), only append to graph if tuple isn't used
                graph.append(tup)       #append the tuple
    return graph
    
    
    
    
    



adjacency = build_adjacency('out.facebook-wosn-links',4,100)
graph = adjacency_to_graph(adjacency)
draw_graph(graph)



def generate_source(adjacency):
    picks = list(range(0,len(adjacency)))                          #Get all choices
    source = random.choice(picks)                                  #pick one
    while (not adjacency[source]):                                 #make sure it's not empty
        source = random.choice(picks)
    return source                                                 #send it back




def si_model_rumor_spreading(source, adjancency, N):
    temp = [[] for i in range(len(adjacency))]
    for i in xrange(0,len(adjacency)):     # create a copy of adjacency so we don't accidently mutate it
         temp[i] = adjacency[i][:]  
             
    infected_nodes = [-1]*N;               #contains original indices
    who_infected = [[] for i in range(N)]  #the infection subgraph
    
     
    
    # adding the source node to the list of infected nodes
    # n=0
    infected_nodes[0] = source #set infected_nodes[0] = v*
    susceptible_nodes = temp[source]      #get neighbours
#    susceptible_indices = [0] * len(susceptible_nodes) not used
        
    for i in range(1,N):
        cur_inf = random.choice(susceptible_nodes)   #select v* neigbor randomly 
        infected_nodes[i] = cur_inf                  #put it in infected_nodes
           #index is 1 less
        susceptible_nodes.extend(temp[cur_inf - 1]) #put all the neighbours of curr infected into susceptible nodes
        susceptible_nodes.remove(cur_inf)           #remove the first occurunce of the current_infected node
        who_infected[i-1].append(i) # append n to kth
        who_infected[i]= [i-1]      # set nth to k

    return who_infected,infected_nodes




# run this script to test the above functions
N = 50
num_nodes = len(adjacency)
source = generate_source(adjacency)
print "source is : ", source , "\n" 
who_infected, infctn_pattern = si_model_rumor_spreading(source, adjacency, N)
#print infctn_pattern
#print len(infctn_pattern)

#print who_infected
graph = []
for i in xrange(len(infctn_pattern)):
    for j in xrange(len(who_infected[i])):
        graph.append((infctn_pattern[i], infctn_pattern[who_infected[i][j]]))
draw_graph(graph, node_color = 'red')     #prints infected graph





#lab7 starts here
def message_passing_up(up_messages, who_infected, calling_node, called_node):
    if called_node == calling_node:  # root node
        for i in who_infected[called_node]:
                up_messages = message_passing_up(up_messages, who_infected, called_node, i)
    elif len(who_infected[called_node]) == 1:   # leaf node
        up_messages[calling_node] += 1 
    else:
        for i in who_infected[called_node]: #
            if i != calling_node:
                up_messages = message_passing_up(up_messages, who_infected, called_node, i)
        up_messages[calling_node] += up_messages[called_node]
    return up_messages  

'''
# creating a toy graph (tree)
adjacency = [ [] for i in range(7)]
adjacency[0] = [1, 2]
adjacency[1] = [0, 3, 4]
adjacency[2] = [0, 5, 6]
adjacency[3] = [1]
adjacency[4] = [1]
adjacency[5] = [2]
adjacency[6] = [2]

root_node = 0 # can use any arbitrary index for the root node
up_messages = [1]*len(who_infected) 
messages = message_passing_up(up_messages, who_infected, root_node, root_node)
print messages
graph = adjacency_to_graph(who_infected)
draw_graph(graph)
'''







def rumor_centrality_up(up_messages_t,up_messages_p, who_infected, calling_node, called_node):
    if called_node == [] or calling_node == [] or up_messages_t[calling_node]==[] or who_infected[calling_node] == []  or who_infected[called_node] ==[]: #or up_messages_t[calling_node]==[] or up_messages_p[calling_node]==[] :
        return up_messages_t,up_messages_p
    if called_node == calling_node:  # root node
        for i in who_infected[called_node]:
                up_messages_t,up_messages_p = rumor_centrality_up(up_messages_t,up_messages_p, who_infected, called_node, i)                
    elif len(who_infected[called_node]) == 1:   # leaf node
        up_messages_t[calling_node] += 1        # inr up message
        up_messages_p[calling_node] = up_messages_t[calling_node] * up_messages_p[called_node]  # multiply by all it's neighbors
        
    else:
        for i in who_infected[called_node]: 
            if i != calling_node: 
                up_messages_t,up_messages_p = rumor_centrality_up(up_messages_t,up_messages_p, who_infected, called_node, i)    
        up_messages_t[calling_node] += up_messages_t[called_node] #calcaulate the t message first
        product = 1  #local scope variable 
        for x in who_infected[calling_node]: # Get the product of all the neighbors of calling node
            product =  product * up_messages_p[x] #Parents have an up message of 1 so we aren't worried
        up_messages_p[calling_node]  = up_messages_t[calling_node] * product #multiply by it's t message.  
    return up_messages_t,up_messages_p  
          

def rumor_centrality_down(down_messages, up_messages_t,up_messeges_p, who_infected, calling_node, called_node):
    n = len(who_infected)
    if called_node == [] or calling_node == [] or up_messages_t[calling_node]==[] or who_infected[calling_node] == []  or who_infected[called_node] ==[]: #or up_messages_t[calling_node]==[] or up_messages_p[calling_node]==[] :
        return down_messages
    if called_node == calling_node:  # root node
        product = 1
        for x in who_infected[calling_node]: # Get the product of all the neighbors of calling node
            if x == [] :
                continue
            product =  product * up_messages_p[x] #Parents have an up message of 1 so we aren't worried
        down_messages[calling_node] = 1.0/product
        for i in who_infected[calling_node]:
            down_messages = rumor_centrality_down(down_messages, up_messages_t,up_messages_p, who_infected, calling_node,i)
                
    else:
        down_messages[called_node] = down_messages[calling_node] * (float(up_messages_t[called_node]) /(n-up_messages_t[called_node]))
        for i in who_infected[called_node]:
            if down_messages[i] == -1.0: #Only need to change down messages for children
                down_messages = rumor_centrality_down(down_messages, up_messages_t,up_messages_p, who_infected, calling_node, i)
    return down_messages 


def rumor_centrality(who_infected):
    root_node = 0 # can use any arbitrary index for the root node
    up_messages_t = [1]*len(who_infected) 
    up_messages_p = [1]*len(who_infected)
    down_messages = [-1.0]*len(who_infected)
    messages_t,messages_p = rumor_centrality_up(up_messages_t,up_messages_p, who_infected, root_node, root_node)
    down_messages = rumor_centrality_down(down_messages, messages_t, messages_p, who_infected, root_node, root_node)
    m = max(down_messages)
    highest = [i for i, j in enumerate(down_messages) if j == m]
    return random.choice(highest)
'''
# creating a toy graph (tree) , same as above with slight modification
adjacency = [ [] for i in range(8)]
adjacency[0] = [1, 2]
adjacency[1] = [3, 4]
adjacency[2] = [5, 6]
adjacency[3] = [1]
adjacency[4] = [1]
adjacency[5] = [2]
adjacency[6] = [2 , 7]
adjacency[7] = [6]
'''
root_node = 0 # can use any arbitrary index for the root node
up_messages_t =	 [1]*len(who_infected) 
up_messages_p = [1]*len(who_infected)
index = random.choice([0,1])
messages_t,messages_p = rumor_centrality_up(up_messages_t,up_messages_p, who_infected, root_node, root_node)
#print messages_t
#print messages_p

down_messages = [-1.0]*len(who_infected)
down_messages = rumor_centrality_down(down_messages, messages_t, messages_p, who_infected, root_node, root_node)

print down_messages

#print rumor_centrality(who_infected), index
print infctn_pattern[rumor_centrality(who_infected)]

#graph = adjacency_to_graph(who_infected)
#draw_graph(graph)



