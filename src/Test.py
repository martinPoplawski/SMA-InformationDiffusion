from venv import create
from warnings import catch_warnings
from xml.dom.expatbuilder import FILTER_ACCEPT
import networkx as nx 
import matplotlib.pyplot as plt
from numpy import short
from Helpers.CommunitiesM import CommunitiesM as Community
from Helpers.InformationDiffusion import InformationDiffusion
from Helpers.Visualization import Visualization
import random
import time
import os
import csv

#Starting values

#TODO make a function that takes cost of contacting person and gain of person influenced and calculate best number of nodes 
lossThresshold = 1
cost = 20
gain = 0.5



#Necessary Variables
#whole graph
G = None

#sampled Graph
shortenedG = None

#End Products

#Biggest Community (list with node names)
Comm = None
#Graph form of biggest Community
cliq = None
#DANA some more variables for 3 different kinds of algorithms and Verfärbungen 
#Best starting nodes for Information Diffusion (list)
bestStartingNodes = None
bestStartingNOdesOneIter = None
bestStartingNodesCostGain = None
bestStartingNodesPerc = None

#Steps for the InformationDiffusion (A list at each index a set of infected nodes)
steps = None
stepsCostGain = None
stepsPerc = None

#number of communities
nbCommunities = 0

##########################

def convertEdgelistToCSVCommunities(): 

    _, _, files = next(os.walk("data/Comms"))
    file_count = len(files)
    print(file_count)

    for i in range(file_count): 
        G = nx.read_edgelist('data/Comms/higgs-Comm-' + str(i) + '.edgelist', nodetype=int, create_using=nx.DiGraph())
        for edge in G.edges():
            edges = G.get_edge_data(edge[0],edge[1])
            if edges['weight'] == 1: 
                G.edges[edge[0], edge[1]]['weight'] = random.randint(3,7)/10
            elif edges['weight'] == 2: 
                G.edges[edge[0], edge[1]]['weight'] = random.randint(5,9)/10

        file = open(f"data/{'Comms/higgs-Comm-' + str(i)}.csv", "w", newline="")
        data = csv.writer(file)

        for edge in G.edges():
            data.writerow([edge[0], edge[1], G.edges[edge[0], edge[1]]['weight'], 0])

        print(f"{i}/{file_count}")


    exit()


def prepareGraph(graph):
    """
    Prepare and Import all the necessary graphs 

    :param graph: Graph for Algorithm
    :param startingNodes: Nodes that are activated at the beginning
       
    :return: All nodes activated at each iteration step 
    """

    global G
    global cliq
    global shortenedG

    # # DANA Change the Comm number to bigger to have a smaller community for testing and change it to smaller for bigger communities. 
    # G = nx.read_edgelist('data/Comms/higgs-Comm-22.edgelist', nodetype=int, create_using=nx.DiGraph())

    # #TODO find sigmoid function to convert to [0,1]
    # for edge in G.edges():
    #     edges = G.get_edge_data(edge[0],edge[1])
    #     if edges['weight'] == 1: 
    #         G.edges[edge[0], edge[1]]['weight'] = random.randint(3,7)/10
    #     elif edges['weight'] == 2: 
    #         G.edges[edge[0], edge[1]]['weight'] = random.randint(5,9)/10


    G = graph
    activity = nx.read_edgelist('data/higgs-activity_time.txt', nodetype=int, create_using= nx.MultiDiGraph(), data=[('time', int),('type',str)])
    activity = activity.subgraph(G.nodes())
    #nx.write_edgelist(activity, 'data/higgs-activity_time_shortened.edgelist')

    threshholds = Community.calculateNodeThreshholdBasedIncOut(activity, G.nodes())
    
    nx.set_node_attributes(G, threshholds, "threshholds")
    #shortenedG = nx.read_edgelist('data/sampled-graph.edgelist', nodetype=int, create_using=nx.DiGraph())
    return G



def preOnce():
    """
    Calculate all Communities of the graph      
    """

    Data = open('data/preprocessed_1653041656.csv', "r")
    Graphtype = nx.DiGraph()

    print("importing Graph...")
    G = nx.parse_edgelist(Data, delimiter=',', create_using=Graphtype,
                      nodetype=int, data=(('weight', float),('rand', float)))

    print("Adding Weights to graph...")
    for edge in G.edges():
        edges = G.get_edge_data(edge[0],edge[1])
        G.edges[edge[0], edge[1]]['weight'] = edges['weight']

    startTime = time.time()
    print("Starting shortening")
    k = 100000
    sampled_nodes = random.sample(G.nodes, k)
    sampled_graph = G.subgraph(sampled_nodes)
    print(sampled_graph)
    nx.write_edgelist(sampled_graph, 'data/sampled-graph.edgelist')

    #TODO create all Communities as edgelists for faster execution
    communities = Community.getAllComm(sampled_graph)
    print("Finished all Comms")

    executionTime = (time.time() - startTime)
    print('Execution time in seconds: ' + str(executionTime / 60))

    # counter = 0
    # for c, v_c in enumerate(communities):
    #     if len(v_c) > 20: 
    #         nx.write_edgelist(G.subgraph(v_c), 'data/Comms/higgs-Comm-' + str(counter) + '.edgelist')
    #         counter += 1

    exit()
    


########################   COST    ###############################################
    
            
def calculateStartingNodes():

    global cliq
    global bestStartingNOdesOneIter 
    global bestStartingNodes
    global bestStartingNodesCostGain
    global bestStartingNodesPerc
    global steps
    global stepsCostGain
    global stepsPerc

    print("Start Calculation")
    
    bestStartingNodes = InformationDiffusion.maxCasc(cliq)
    bestStartingNodesOneIter = InformationDiffusion.maxCascFast(cliq)
    bestStartingNodesCostGain = InformationDiffusion.maxCascCostAndGain(cliq, cost=cost, gain=gain)
    bestStartingNodesPerc = InformationDiffusion.maxCascPercentage(cliq, percentage=0.9)
    steps=InformationDiffusion.ltm(cliq,bestStartingNodes)
    stepsCostGain = InformationDiffusion.ltm(cliq,bestStartingNodesCostGain)
    stepsPerc = InformationDiffusion.ltm(cliq,bestStartingNodesPerc)

    print("how many steps: ",len(steps),len(stepsCostGain),len(stepsPerc))

    print("==================================")
    for name, startingNodes in zip(["Loss", "Loss: One Iteration", "Cost and Gain", "Percentage"],[bestStartingNodes, bestStartingNodesOneIter, bestStartingNodesCostGain, bestStartingNodesPerc]):
        nodes = InformationDiffusion.ltm(cliq, startingNodes)
        coveredNodes = nodes[len(nodes) - 1]
        print(name)
        print(f"Number of starting Nodes: {len(startingNodes)}")
        print(f"Coverage: {len(coveredNodes)}/{len(cliq.nodes())}")
        print(f"Starting Nodes: {startingNodes}")
        print(f"================================")




############  Visualization  ############################

def visualize(graph, S):

    color_map = []
    for node in graph.nodes():

        if node in S:
            color_map.append('red')
        else: 
            color_map.append('green')


    nx.draw(graph, node_color=color_map)
    plt.show()

def visualize2():
    global cliq
    global shortenedG
    global stepsPerc
    
    print("--------------VISUALIZATION--------------")

    comm_array=createCommunityArray()

    #print(len(cliq))
    
    #TODO: Visualization.edges_weights(cliq)
    #Visualization.neighbors_nodes(cliq)
    #Visualization.communities(cliq)
    #Visualization.spreading(cliq,stepsPerc)
    #Visualization.nbOfStepsToCover(cliq,steps)
    #Visualization.allCommunitiesInGraph(shortenedG,comm_array)

    #for x in range(0,20):
     #   for y in range(0,20):
      #      if(x!=y):
       #         print(x,y)
        #        comm1 = nx.read_edgelist('data/Comms/higgs-Comm-'+str(x)+'.edgelist', nodetype=int, create_using=nx.DiGraph())
         #       comm2 = nx.read_edgelist('data/Comms/higgs-Comm-'+str(y)+'.edgelist', nodetype=int, create_using=nx.DiGraph())    
          #      Visualization.compareTwoCommunities(comm1,comm2,wholeG)

    
    
    


def createCommunityArray():
    x=0
    comm_array=[]
    while(True):
        try:
            comm = nx.read_edgelist('data/Comms/higgs-Comm-'+str(x)+'.edgelist', nodetype=int, create_using=nx.DiGraph())
            comm_array.append(comm)
            x=x+1
        except:
            break
    #print("Nb of communities: ",len(comm_array))
    return comm_array
        




if __name__ == "__main__":
    #Uncomment to generate edgelists for smaller subset and faster testing times. 
    #DANA preOnce muss passiere damit de graph chli kürzt wird bevor du 6 Johr wartisch. 
    #preOnce()

    #10k = 8.7 sek
    #30k = 5 min
    #100k = 263 min = 4h 23

    #convertEdgelistToCSVCommunities()


    #This should work but not with combined graphs
    prepareGraph(G)
    #Still under testing. 
    #graphPrepMarco()
    print(G)
    calculateStartingNodes()
    visualize2()
    pass
