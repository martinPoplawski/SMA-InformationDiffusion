import networkx as nx 
import matplotlib.pyplot as plt
from Helpers.Community import Community
from Helpers.InformationDiffusion import InformationDiffusion
import random

#Starting values

#TODO make a function that takes cost of contacting person and gain of person influenced and calculate best number of nodes 
lossThresshold = 1
cost = 20
gain = 0.5



#Necessary Variables
G = None


#End Products

#Biggest Community (list with node names)
Comm = None
#Graph form of biggest Community
cliq = None
#DANA some more variables for 3 different kinds of algorithms and Verfärbungen 
#Best starting nodes for Information Diffusion (list)
bestStartingNodes = None
bestStartingNodesCostGain = None
bestStartingNodesPerc = None
#Steps for the InformationDiffusion (A list at each index a set of infected nodes)
steps = None
stepsCostGain = None
stepsPerc = None


##########################

def graphPrep():
    """
    Prepare and Import all the necessary graphs 

    :param graph: Graph for Algorithm
    :param startingNodes: Nodes that are activated at the beginning
       
    :return: All nodes activated at each iteration step 
    """

    global G
    global cliq

    # DANA Change the Comm number to bigger to have a smaller community for testing and change it to smaller for bigger communities. 
    G = nx.read_edgelist('data/Comms/higgs-Comm-11.edgelist', nodetype=int, create_using=nx.DiGraph())

    #TODO find sigmoid function to convert to [0,1]
    for edge in G.edges():
        edges = G.get_edge_data(edge[0],edge[1])
        if edges['weight'] == 1: 
            G.edges[edge[0], edge[1]]['weight'] = random.randint(3,7)/10
        elif edges['weight'] == 2: 
            G.edges[edge[0], edge[1]]['weight'] = random.randint(5,9)/10


    activity = nx.read_edgelist('data/higgs-activity_time.txt', nodetype=int, create_using= nx.MultiDiGraph(), data=[('time', int),('type',str)])
    activity = activity.subgraph(G.nodes())
    nx.write_edgelist(activity, 'data/higgs-activity_time_shortened.edgelist')

    threshholds = Community.calculateNodeThreshholdBasedIncOut(activity, G.nodes())
    
    cliq = G
    nx.set_node_attributes(cliq, threshholds, "threshholds")


def preOnce():

    Data = open('data/preprocessed_1653041656.csv', "r")
    Graphtype = nx.DiGraph()

    print("importing Graph...")
    G = nx.parse_edgelist(Data, delimiter=',', create_using=Graphtype,
                      nodetype=int, data=(('weight', float),('rand', float)))

    print("Adding Weights to graph...")
    for edge in G.edges():
        edges = G.get_edge_data(edge[0],edge[1])
        G.edges[edge[0], edge[1]]['weight'] = edges['weight']

    print("Starting shortening")
    k = 20000
    sampled_nodes = random.sample(G.nodes, k)
    sampled_graph = G.subgraph(sampled_nodes)
    print(sampled_graph)

    #TODO create all Communities as edgelists for faster execution
    communities = Community.getAllComm(sampled_graph)
    print("Finished all Comms")

    counter = 0
    for c, v_c in enumerate(communities):
        if len(v_c) > 20: 
            nx.write_edgelist(G.subgraph(v_c), 'data/Comms/higgs-Comm-' + str(counter) + '.edgelist')
            counter += 1

    exit()
    


########################   COST    ###############################################
    
            
def calculateBestCost():

    global cliq
    global bestStartingNodes
    global bestStartingNodesCostGain
    global bestStartingNodesPerc

    print("Start Calculation")
    
    bestStartingNodes = InformationDiffusion.maxCasc(cliq)
    bestStartingNodesCostGain = InformationDiffusion.maxCascCostAndGain(cliq, cost=cost, gain=gain)
    bestStartingNodesPerc = InformationDiffusion.maxCascPercentage(cliq, percentage=0.9)


    print("==================================")
    for name, startingNodes in zip(["Loss", "Cost and Gain", "Percentage"],[bestStartingNodes, bestStartingNodesCostGain, bestStartingNodesPerc]):
        nodes = InformationDiffusion.ltm(cliq, startingNodes)
        coveredNodes = nodes[len(nodes) - 1]
        print(name)
        print(f"Number of starting Nodes: {len(startingNodes)}")
        print(f"Coverage: {len(coveredNodes)}/{len(cliq.nodes())}")
        print(f"Starting Nodes: {startingNodes}")
        print(f"================================")




############  Visualization  ############################

def visualize():

    global cliq
    global bestStartingNodes
    color_map = []
    for node in cliq.nodes():

        if node in bestStartingNodes:
            color_map.append('red')
        else: 
            color_map.append('green')


    nx.draw(cliq, node_color=color_map)
    plt.show()


if __name__ == "__main__":
    #Uncomment to generate edgelists for smaller subset and faster testing times. 
    #DANA preOnce muss passiere damit de graph chli kürzt wird bevor du 6 Johr wartisch. 
    #preOnce()
    #preOnceMarco()


    #This should work but not with combined graphs
    graphPrep()

    #Still under testing. 
    #graphPrepMarco()
    print(G)
    calculateBestCost()
    visualize()
    pass