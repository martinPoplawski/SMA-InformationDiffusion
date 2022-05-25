import networkx as nx 
from networkx.algorithms.community import greedy_modularity_communities
import random
import csv
import time



class CommunitiesM:
    """Object for community detection and handling of similar"""

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
        print("started Greedy")
        return greedy_modularity_communities(graph)


    #TODO
    def saveCommunity(graph):
        pass

    def splitGraphIntoCommunities(sample=10000):
        """
        Sample the graph and calculate all Communities of the sampled graph      
        """

        #Import prepocessed graph
        Data = open('data/preprocessed_1653041656.csv', "r")
        Graphtype = nx.DiGraph()

        print("importing Graph...")
        G = nx.parse_edgelist(Data, delimiter=',', create_using=Graphtype,
                        nodetype=int, data=(('weight', float),('rand', float)))

        print("Adding Weights to graph...")
        for edge in G.edges():
            edges = G.get_edge_data(edge[0],edge[1])
            #TODO calculate better weight distribution
            if edges['weight'] == 1: 
                G.edges[edge[0], edge[1]]['weight'] = random.randint(3,7)/10
            elif edges['weight'] == 2: 
                G.edges[edge[0], edge[1]]['weight'] = random.randint(5,9)/10

        startTime = time.time()
        sampled_nodes = random.sample(list(G.nodes), sample)
        sampled_graph = G.subgraph(sampled_nodes)

        #TODO DANA isch das immerno nötig? 
        nx.write_edgelist(sampled_graph, 'data/sampled-graph.edgelist')

        #Create Communities
        communities = CommunitiesM.getAllComm(sampled_graph)
        print("Finished Community Algorithm")

        executionTime = (time.time() - startTime)
        print('Execution time in seconds: ' + str(executionTime / 60))

        #Store the big enough communities in CSV files for transfer
        counter = 0
        for c, v_c in enumerate(communities):
            if len(v_c) > 20: 
                comm = G.subgraph(v_c)
                file = open(f"data/{'Comms/higgs-Comm-' + str(counter)}.csv", "w", newline="")
                data = csv.writer(file)
                for edge in comm.edges():
                    data.writerow([edge[0], edge[1], comm.edges[edge[0], edge[1]]['weight'], 0])
                counter += 1
        exit()

