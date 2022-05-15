import networkx as nx 
from networkx.algorithms.community import louvain_communities


class Community:
    """Object for community detection and handling of similar"""

    ##TODO check if communities are well formed with stuff from slides
    def getBiggestComm(graph):
        biggest= []
        print(f"Starting Calculations...")
        for clique in louvain_communities(graph):
            if len(clique) > len(biggest): 
                biggest = clique

        return biggest
    
    def saveCommunity(graph):
        pass


    #TODO Not working yet because we have no tweets graph/set
    def calculateNodeThreshholdBasedTweeets(graph):
        for neigh in graph.neighbors(node):
                print(neigh)
                print(graph.out_edges(neigh))
                if len(graph.out_edges(neigh)) > 0: 
                    print(graph.out_edges(neigh)['type'])
                return 
        pass



    def calculateNodeThreshholdBasedIncOut(graph):
        threshholds = {} 
        for node in graph.nodes(): 
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

            

            if inc+out == 0: 
                threshholds[node] = 20
            else: 
                threshholds[node] = out/(inc + out)

             
        print(threshholds)
        return threshholds 
