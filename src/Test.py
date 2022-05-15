import networkx as nx 
from networkx.algorithms.community import louvain_communities
import matplotlib.pyplot as plt
from Helpers.Community import Community
from Helpers.InformationDiffusion import InformationDiffusion
import random

print(f"Importing Graph...")
G = nx.read_edgelist('data/higgs-social_network_shortened.edgelist', nodetype=int)
G = G.to_directed()

total = nx.read_edgelist('data/higgs-activity_time.txt', nodetype=int, create_using= nx.MultiDiGraph(), data=[('time', int),('type',str)])
total = total.subgraph(G.nodes())
nx.write_edgelist(total, 'data/higgs-activity_time_shortened.edgelist')

# mentions = nx.read_edgelist('data/higgs-mention_network.edgelist', nodetype=int, create_using= nx.MultiDiGraph(), data=[('rep',int)])
# mentions = mentions.subgraph(G.nodes())
# nx.write_edgelist(mentions, 'data/higgs-mention_network_shortened.edgelist')



#reMen = nx.compose(retweets, mentions)

Community.calculateNodeThreshholdBasedIncOut(total)

##Random Sample of Graph 
#print("Starting shortening")
#k =5000
#sampled_nodes = random.sample(G.nodes, k)
#sampled_graph = G.subgraph(sampled_nodes)
#nx.write_edgelist(sampled_graph, 'data/higgs-social_network_shortened.edgelist')

Comm = Community.getBiggestComm(G)

thresholds = {}
for node in G.nodes:
    thresholds[node] = random.uniform(0,1)

G = nx.DiGraph(G)
nodes = list(G.nodes())
for i in range(len(nodes)):
    for j in range(i + 1, len(nodes)):

        rand = random.randint(0,10)
        if rand < 1: 
            G.add_edge(nodes[i], nodes[j])

for (u,v) in G.edges():
    G.edges[u,v]['weight'] = random.randint(0,10)/10
cliq = G.subgraph(Comm)
print(cliq)
pos = nx.spring_layout(cliq)
            

nx.set_node_attributes(cliq, thresholds, "threshholds")
startingNode = None
for node in cliq.nodes:
    startingNode = node
    break




#ltm(cliq, {startingNode})
bestStartingNodes = InformationDiffusion.maxCasc(cliq, 10)
print("=========")
print(bestStartingNodes)
print(f"Covering {len(InformationDiffusion.ltm(cliq, bestStartingNodes))}/{len(cliq.nodes())}")

#pos = nx.spring_layout(cliq)
color_map = []
for node in cliq.nodes():

    if node in bestStartingNodes:
        color_map.append('red')
    else: 
        color_map.append('green')

print(len(color_map))
print(len(cliq.nodes))
nx.draw(cliq, node_color=color_map)
plt.show()