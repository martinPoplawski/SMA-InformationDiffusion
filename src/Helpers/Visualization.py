from operator import sub
import matplotlib.pyplot as plt
import numpy as np



class Visualization:

    # Shows the distribution of weights in edges

    def edges_weights(graph):

        #get all weights from edges and sort
        edge_sequence_string = sorted(str(weight) for u,v,weight in graph.edges.data("weight"))
        edge_sequence = sorted(weight for u,v,weight in graph.edges.data("weight"))

        print(edge_sequence)

        #get the maximum edge weight
        emax = max(edge_sequence)
        print("Edge weight maximum: ",emax)   

        #use a bar plot to show results
        plt.title("Distribution of edge weights")
        plt.xlabel("edge weight")
        plt.ylabel("number of edges")
        #print(*np.unique(edge_sequence, return_counts=True))

        plt.bar(*np.unique(edge_sequence_string, return_counts=True))
        plt.show()

    
    #Show the distribution of number of neighbours nodes have (degree)

    def neighbors_nodes(graph):

        degree_sequence = sorted((d for n, d in graph.degree()), reverse=True)
        print(degree_sequence)

        #get maximum degree (nb of neighbours)
        dmax = max(degree_sequence)
        print("Maximal degree of nodes: ",dmax)
        
        #bar plot
        plt.title("Number of nodes with a specific degree")
        plt.xlabel("Degree")
        plt.ylabel("Number of nodes")
        print(*np.unique(degree_sequence, return_counts=True))
        plt.bar(*np.unique(degree_sequence, return_counts=True))
        plt.show()


    def numberOfEdges(graph):
        nbEdges = graph.number_of_edges()
        print("Number of edges in graph: ",nbEdges)
        return nbEdges

    def numberOfNodes(graph):
        nbNodes = graph.number_of_nodes()
        print("Number of nodes in graph: ",nbNodes)
        return nbNodes

    #----------------------------------------------------------------------------------
    #Create file for gephi: one community as a graph

    def community(graph):
    
        nx.write_gexf(graph, "data/visualization/community.gexf", version="1.2draft")
    

    #Create file for gephi: one community in whole graph
    def oneCommunityInGraph(graph, comm):
        nx.set_node_attributes(graph, 0, name="in_community")

        for node in graph.nodes():
            for member in comm:
                if(node==member):
                    graph.nodes[node]["in_community"]=1
        nx.write_gexf(graph, "data/visualization/oneCommunityInG.gexf", version="1.2draft")

    #Create file for gephi: all communities in graph colored
    def allCommunitiesInGraph(graph, array_of_comm):

        print(len(array_of_comm))
        
        nx.set_node_attributes(graph, 0, name="community")

        for x in range(0,len(array_of_comm)):
            print("round",x,"of",len(array_of_comm))
            for member in array_of_comm[x]:
                for node in graph.nodes():
                    if node==member:
                        graph.nodes[node]["community"]=x
        
        print(graph)
        nx.write_gexf(graph, "data/visualization/allCommunitiesGraph.gexf", version="1.2draft")

    #----------------------------------------------------------------------------------

    def spreading(graph, infected):
        #show each step which node infected (retweeted)

        print("infected",infected)

        for x in range(0,len(infected)):
            print("x",x)
            nx.set_node_attributes(graph, 0, name="infected")
            for node in graph.nodes():
                for infected_node in infected[x]:
                    if(infected_node==node):
                        graph.nodes[node]["infected"]=1

            nx.write_gexf(graph, "data/visualization/spreading"+ str(x) +".gexf", version="1.2draft")

        print("")    


    def nbOfStepsToCover(graph, steps):

        #print(steps)
        graph_size = graph.number_of_nodes()
        #print(graph_size)

        percentage_list = [0] * (len(steps))
        index=0
        index_list=[]
        for step in steps:
            percentage_list[index] = len(step)/graph_size*100
            index = index+1
            index_list.append(str(index))

        #print(percentage_list)

        x = index_list
        y = percentage_list #how many nodes in a community

        #print(index_list,percentage_list)
        plt.title("Percentage of infected per step")
        plt.xlabel("Step")
        plt.ylabel("Percentage")

        plt.plot(x,y)
        plt.show()

    #----------------------------------------------------------------------------------


    def nodesEdgesInCommunities(array_of_subgraphs): #better to show ranges like how many communities have 0-1000 members, how many have +10'000 etc.
        nbOfEdges=[]
        nbOfNodes= []

        for subgraph in array_of_subgraphs:
            nbOfNodes.append(subgraph.number_of_nodes())
            nbOfEdges.append(subgraph.number_of_edges())

      
        print(nbOfNodes,nbOfEdges)
        plt.title("Nodes and Edges in communities")
        plt.xlabel("Number of Edges")
        plt.ylabel("Number of Nodes")

        #if many have the same (x,y) the dot gets darker, so we can see which is more common. (many/little nodes, many/little edges)
        plt.scatter(nbOfEdges,nbOfNodes,alpha=.1, s=200, color='red')
        plt.show()

    def getEdgeWithHighestWeight(graph):
        #just calc with the function on top
        edge_sequence = [{"uv":(u,v),"weight":weight} for u,v,weight in graph.edges.data()]
        #maxWeight = max(edge_sequence["weight"])
        print(edge_sequence)
        for key, val in edge_sequence:
            print(key,val)
            


#TODO
    def nodesInfected(graph,steps):
        lastStep = steps[len(steps)-1]
        print(lastStep)
        nodesInfected = [0]*len(steps)
        degrees = []
        for index, activeNode in enumerate(lastStep):
            degrees.append(graph.degree[activeNode])
            print("degree of active node")
            for neighbor in graph.neighbors(activeNode):
                print("neighbor of activenode")
                if Visualization.contains(neighbor, lastStep):
                    nodesInfected[index]+=1
        

        x = degrees
        y = nodesInfected
        plt.title("nb of neighbors and neighbors infected")
        plt.xlabel("degree")
        plt.ylabel("nodes infected")

        plt.scatter(x,y,alpha=0.2)
        plt.show()


    #compare where two communities are connected, which nodes
    def compareTwoCommunities(comm1, comm2, wholeGraph):
        #print(comm1.nodes(),comm2.nodes())
        sameNodes=[]
        connections=[]
        for node in comm1.nodes():
            for node2 in comm2.nodes():
                #sharing nodes                    
                #print(node,node2)

                if node==node2:
                    sameNodes.append(node)

                #nodes being connected with each other (both directions possible because directional graph)
                if wholeGraph.has_edge(node,node2):
                    connections.append([node,node2])
                if wholeGraph.has_edge(node2,node):
                    connections.append([node2,node])

        
        print("shared nodes between communities:",sameNodes,"nb:", len(sameNodes))
        print("edges between communities",connections,"nb:",len(connections))
        


    def centrality(graph):
        degree_cent=nx.degree_centrality(graph)
        closeness_cent=nx.closeness_centrality(graph)
        eigenvector_cent=nx.eigenvector_centrality(graph)
        print("degree centrality ",degree_cent,"\n")
        Visualization.top_keys(degree_cent,10)
        print(f"================================")
        print("closeness centrality ",closeness_cent,"\n")
        Visualization.top_keys(closeness_cent,10)
        print(f"================================")
        print("eigenvector centrality",eigenvector_cent,"\n")
        Visualization.top_keys(eigenvector_cent,10)
        print(f"================================")



    def centralityAllCommunities(array_comm):
        centForComms = []
        for comm in array_comm:
            print("Community",comm)
            degree_cent=nx.degree_centrality(comm)
            closeness_cent=nx.closeness_centrality(comm)
            eigenvector_cent=nx.eigenvector_centrality(comm)
            print("degree centrality ",degree_cent)
            print("closeness centrality ",closeness_cent)
            print("eigenvector centrality",eigenvector_cent)
            print(f"================================")


            centForComms.append([degree_cent,closeness_cent,eigenvector_cent])

        return centForComms
        
    
    def top_keys(dictionary, top):
        from collections import Counter

        k = Counter(dictionary)
 
        # Finding 3 highest values
        high = k.most_common(top)
        
        print("With max",top,"highest values")
        print("Keys: Values")
        
        for i in high:
            print(i[0]," :",i[1]," ")

    #TODO: vergleiche 2 nodes
    def similarity(graph):
        #https://networkx.org/documentation/stable/reference/algorithms/link_prediction.html
        
        print("jaccard sim",nx.jaccard_coefficient(graph))

    def getNodesSeeingRetweet(graph, steps):
        nodesSeeingRetweet = [[]] * (len(steps))

        for index, step in enumerate(steps):
            #at each step
            for activatedNode in step:
                array=[]
                #take each activated node of this step
                for n in graph[activatedNode]:
                    #take each neighbour of activatedNode
                        
                        #see if neighbour is in activated nodes list
                        if (not Visualization.contains(n,step)):
                            #only add if not activated yet
                            array.append(n)


                nodesSeeingRetweet[index]=np.concatenate((nodesSeeingRetweet[index],array))
                #print(activatedNode,nodesSeeingRetweet[index])
            
            #print("unique",np.unique(nodesSeeingRetweet[index]))

            #save nb of users who can see the retweet and aren't activated yet
            nodesSeeingRetweet[index]={"nodes":len(np.unique(nodesSeeingRetweet[index])),"percentage":len(np.unique(nodesSeeingRetweet[index]))/len(graph.nodes())}

        #all neoghbours of activated nodes - activated nodes - doubles (x an y activated both let z see retweet)
        return nodesSeeingRetweet

    def contains(item,list):
        #print("Is ",item,"in",list)
        for listitem in list:
            if(listitem==item):
                return True
        
        return False


#creating some nx graph to test:

import networkx as nx

steps = [[1],[1,2],[1,2,3]]

graph=nx.DiGraph()
graph.add_node(1)
graph.add_node(2)
graph.add_node(3)
graph.add_node(4)

#counts 1,2 and 2,1 as two edges in DiGraph and as one edge in Graph
graph.add_edge(1,2,weight=10)
graph.add_edge(2,1,weight=15)
graph.add_edge(1,3,weight=5)
graph.add_edge(1,4,weight=10)
graph.add_edge(2,4,weight=10)


#TEST Compare Two communities ----------------------------------
graph1=nx.Graph()
graph1.add_node(1)
graph1.add_node(2)

graph1.add_edge(1,2,weight=10)

graph2=nx.Graph()
graph2.add_node(1)
graph2.add_node(4)

graph2.add_edge(1,4,weight=10)
#Visualization.compareTwoCommunities(graph1,graph2,graph) #test done and works fine
#------------------------------------------------------------------

#TEST

#Visualization.edges_weights(graph) #test ok
#Visualization.neighbors_nodes(graph) #test ok
#Visualization.numberOfEdges(graph) #test ok
#Visualization.numberOfNodes(graph) #test ok

#Visualization.community(graph)
#Visualitation.oneCommunityInGraph(graph, graph1)
#Visualization.allCommunitiesInGraph(graph,[graph1,graph2])

#Visualization.spreading(graph,steps)
#Visualization.nbOfStepsToCover(graph,steps) #test ok

#Visualization.nodesEdgesInCommunities([graph,graph1,graph2]) #test ok
#Visualization.getEdgeWithHighestWeight(graph)

#Visualization.nodesInfected(graph,steps) #test ok

#Visualization.compareTwoCommunities(graph1,graph2,graph) #test ok

#Visualization.centrality(graph) #test ok
#Visualization.centralityAllCommunities([graph1,graph2, graph]) #test ok

Visualization.getNodesSeeingRetweet(graph,steps)
