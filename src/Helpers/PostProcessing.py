import networkx as nx 
from CommunitiesM import CommunitiesM as Community

def prepareGraph(graph):
    """
    Prepare the graph by calculating the threshholds for each node 

    :param graph: Graph for Algorithm
       
    :return: All nodes activated at each iteration step 
    """

    G = graph
    activity = nx.read_edgelist('data/higgs-activity_time.txt', nodetype=int, create_using= nx.MultiDiGraph(), data=[('time', int),('type',str)])
    activity = activity.subgraph(G.nodes())

    threshholds = calculateNodeThreshholdBasedIncOut(activity, G.nodes())
    
    nx.set_node_attributes(G, threshholds, "threshholds")
    #DANA Weiss nid öb das no bruchsch, abr das müesst mer useneh suscht
    #shortenedG = nx.read_edgelist('data/sampled-graph.edgelist', nodetype=int, create_using=nx.DiGraph())

    return G

# Calculates the Threshhold based on the Incoming and Outgoing edges for each node. 
def calculateNodeThreshholdBasedIncOut(graph, AllNodes):
    """
    Calculates node threshhold based on incoming and outgoing edges and 
    some randomness 
    Uses Retweet, Mention and Replies. In which not every node is present
    All Nodes is the list of all nodes necessary for the original graph

    :param graph: Graph for Algorithm
    :param allNodes: All nodes in the original graph
    
    :return: List of communities  
    """

    threshholds = {} 
    for node in AllNodes: 
        if not node in graph:
            threshholds[node] = 1
            continue
        out = 0 
        inc = 0
        t = nx.get_edge_attributes(graph, "color")
        for o, i in graph.in_edges(node):
            edges = graph.get_edge_data(o,i)
            for key in edges.keys():
                if edges[key]['type'] == 'MT':
                    inc += 1
                elif edges[key]['type'] == 'RE':
                    inc += 1
                elif edges[key]['type'] == 'RT': 
                    inc += 1

        for o, i in graph.out_edges(node):
            edges = graph.get_edge_data(o,i)
            for key in edges.keys():
                if edges[key]['type'] == 'MT':
                    out += 2
                elif edges[key]['type'] == 'RE':
                    out += 1
                elif edges[key]['type'] == 'RT': 
                    out += 3
           

        # If there are no actions from a node, just randomly assign a high value.
        if inc+out == 0: 
            threshholds[node] = random.randint(600,1000) / 1000
        else: 
            #Calculates random distribution with the activity of the user and a little randomness. 
            threshholds[node] = random.randint(max(int(1000*(out/(inc + out)) - 400), 0), int(1000*(out/(inc+out))))/1000

    return threshholds 