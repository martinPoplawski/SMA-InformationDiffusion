import networkx as nx 
import matplotlib.pyplot as plt
from Helpers.Community import Community
from Helpers.InformationDiffusion import InformationDiffusion
import random

#Starting values

#TODO make a function that takes cost of contacting person and gain of person influenced and calculate best number of nodes 
costs = [0.5]



#Necessary Variables
G = None


#End Products

#Biggest Community (list with node names)
Comm = None
#Graph form of biggest Community
cliq = None
#Best starting nodes for Information Diffusion (list)
bestStartingNodes = None
#Steps for the InformationDiffusion (A list at each index a set of infected nodes)
steps = None


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

    #TODO implement for real graph
    #TODO do better sampling
    print(f"Importing Graph...")
    G = nx.read_edgelist('data/higgs-social_network_shortened.edgelist', nodetype=int, create_using=nx.DiGraph())

    activity = nx.read_edgelist('data/higgs-activity_time.txt', nodetype=int, create_using= nx.MultiDiGraph(), data=[('time', int),('type',str)])
    activity = activity.subgraph(G.nodes())
    nx.write_edgelist(activity, 'data/higgs-activity_time_shortened.edgelist')

    threshholds = Community.calculateNodeThreshholdBasedIncOut(activity, G.nodes())


    #TODO it has to be here otherwise it takes 7 years
    Comm = Community.getBiggestComm(G)
    testingStuff()
    cliq = G.subgraph(Comm)
    nx.set_node_attributes(cliq, threshholds, "threshholds")


    #TODO replace with Marco 
    for (u,v) in G.edges():
        G.edges[u,v]['weight'] = random.randint(0,10)/10

    print("Finished Graph Prep")

    


def testingStuff():
    """
    Test Stuff because I have no things from Marco  

    :param graph: Graph for Algorithm
    :param startingNodes: Nodes that are activated at the beginning
       
    :return: All nodes activated at each iteration step 
    """

    global G 
    # Random edges to make the graph tighter 
    G = nx.DiGraph(G)
    nodes = list(G.nodes())
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            rand = random.randint(0,200)
            if rand < 1: 
                G.add_edge(nodes[i], nodes[j])




def preOnce():

    ##Random Sample of Graph 
    print("Starting shortening")
    k = 20000
    sampled_nodes = random.sample(G.nodes, k)
    sampled_graph = G.subgraph(sampled_nodes)

    #TODO create all Communities as edgelists for faster execution
    test = Community.getAllComm(sampled_graph)
    print("Finished all Comms")

    comms = [] 
    counter = 0
    for c, v_c in enumerate(communities):

        if len(v_c) > 20: 
            nx.write_edgelist(G.subgraph(v_c), 'data/Comms/higgs-Comm-' + str(counter) + '.edgelist')

            counter += 1
            print(counter)

################################################################################
    
            
def calculateBestCost():

    global cliq
    global bestStartingNodes

    print("Start Calculation")

    bestCost = 0
    bestCoverage = 0
    for cost in costs:
        bestStartingNodes = InformationDiffusion.maxCasc(cliq, budget=10, cost=cost)
        nodes = InformationDiffusion.ltm(cliq, bestStartingNodes)
        coveredNodes = nodes[len(nodes) - 1]

        if bestCoverage < len(coveredNodes): 
            bestCoverage = len(coveredNodes)
            bestCost = cost

    print(f"BestCost = {bestCost}")
    print(f"Coverage: {len(coveredNodes)}/{len(cliq.nodes())}")
    print(f"Starting Nodes: {bestStartingNodes}")






############  Visualization  ############################

def visualize():

    global cliq
    global bestStartingNodes
    pos = nx.spring_layout(cliq)
    color_map = []
    for node in cliq.nodes():

        if node in bestStartingNodes:
            color_map.append('red')
        else: 
            color_map.append('green')


    steps = InformationDiffusion.ltm(cliq,bestStartingNodes)
    # print(len(steps))
    # for step in steps: 
    #     print(len(step))

    nx.draw(cliq, node_color=color_map)
    plt.show()


if __name__ == "__main__":
    graphPrep()
    print(G)
    #testingStuff()
    calculateBestCost()
    visualize()
    pass