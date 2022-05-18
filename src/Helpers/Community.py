import networkx as nx 
from networkx.algorithms.community import louvain_communities, louvain_partitions, girvan_newman, k_clique_communities, greedy_modularity_communities
import random
import community 



class Community:
    """Object for community detection and handling of similar"""

    #TODO use louvain_partitions
    ##TODO check if communities are well formed with stuff from slides
    def getBiggestComm(graph):
        """
        Get the biggest community with Louvain

        :param graph: Graph for Algorithm
       
        :return: List of nodes from biggest community 
        """
        biggest= []
        communities = greedy_modularity_communities(graph)
        for c, v_c in enumerate(communities):

            if len(v_c) > len(biggest): 
                biggest = v_c

        return biggest
    

    def getAllComm(graph, size=20): 
        """
        Split the graph in communities and return only the ones bigger than size 

        :param graph: Graph for Algorithm
        :param size: Number of nodes necessary for a community
       
        :return: List of communities  
        """
        return greedy_modularity_communities(graph, n_communities=20)


    #TODO
    def saveCommunity(graph):
        pass


    #TODO Not working yet because we have no tweets graph/set
    def calculateNodeThreshholdBasedTweets(graph):
        for neigh in graph.neighbors(node):
                print(graph.out_edges(neigh))
                if len(graph.out_edges(neigh)) > 0: 
                    print(graph.out_edges(neigh)['type'])
                return 
        pass


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
                        inc += 2 
                    elif edges[key]['type'] == 'RE':
                        inc += 1
                    elif edges[key]['type'] == 'RT': 
                        inc += 3

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
                threshholds[node] = random.randint(700,1000) / 1000
            else: 
                #TODO maybe take average into consideration from whole network. 
                #Calculates random distribution with the activity of the user and a little randomness. 
                threshholds[node] = random.randint(max(int(1000*(out/(inc + out)) - 300), 0), int(1000*(out/(inc+out))))/1000


        return threshholds 
