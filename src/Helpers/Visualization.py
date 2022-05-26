import matplotlib.pyplot as plt
import numpy as np
import networkx as nx



class Visualization:


    def edges_weights(graph):

        """
        Show the nb of edges having a certain weight

        :param graph: Graph
       
        :return: void 
        """
    

        print(f"===========EDGES/WEIGHTS=====================")

        #get all weights from edges and sort
        edge_sequence_string = sorted(str(weight) for u,v,weight in graph.edges.data("weight"))
        edge_sequence = sorted(weight for u,v,weight in graph.edges.data("weight"))

        #print(edge_sequence)

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
       

    def neighbors_nodes(graph):

        """
        Show the nb of nodes having a certain degree

        :param graph: Graph
       
        :return: void 
        """

        print(f"===============DEGREE/NB OF NODES=================")

        degree_sequence = sorted((d for n, d in graph.degree()), reverse=True)
        #print(degree_sequence)

        #get maximum degree (nb of neighbours)
        dmax = max(degree_sequence)
        print("Maximal degree of nodes: ",dmax)
        

        #bar plot
        plt.title("Number of nodes with a specific degree")
        plt.xlabel("Degree")
        plt.ylabel("Number of nodes")
        #print(*np.unique(degree_sequence, return_counts=True))
        plt.bar(*np.unique(degree_sequence, return_counts=True))
        plt.show()


    def numberOfEdges(graph):

        """
        Get the nb of edges in graph

        :param graph: Graph
       
        :return: nb of edges
        """

        print(f"=============NB OF EDGES===================")

        nbEdges = graph.number_of_edges()
        print("Number of edges in graph: ",nbEdges)

        return nbEdges


    def numberOfNodes(graph):

        """
        Get the nb of nodes in graph

        :param graph: Graph
       
        :return: nb of nodes
        """

        print(f"==============NB OF NODES==================")

        nbNodes = graph.number_of_nodes()
        print("Number of nodes in graph: ",nbNodes)

        return nbNodes


    def community(graph):

        """
        Load community to gexf for gephi

        :param graph: Graph
       
        :return: void (file in data/visualization) 
        """

        print("graph",graph)

        print(f"============COMMUNITY SAVED TO COMMUNITY.GEXF====================")
        nx.write_gexf(graph, "data/visualization/community.gexf", version="1.2draft")
    

    def oneCommunityInGraph(graph, comm):

        """
        Load one community with whole graph to gexf for gephi

        :param graph, comm: Graph and Community
       
        :return: void (file in data/visualization) 
        """

        print(f"============COMMUNITY SAVED TO ONECOMMUNITYING.GEXF====================")

        nx.set_node_attributes(graph, -1, name="in_community")

        for node in graph.nodes():
            for member in comm:
                if(node==int(member)):
                    graph.nodes[node]["in_community"]=1
                    print("incomm")
        nx.write_gexf(graph, "data/visualization/oneCommunityInG.gexf", version="1.2draft")

    
    def allCommunitiesInGraph(graph, array_of_comm):

        """
        Load all communities with whole graph to gexf for gephi

        :param graph, array_of_comm: Graph and array of all communities
       
        :return: void (file in data/visualization) 
        """

        print(f"============COMMUNITIES SAVED TO ALLCOMMUNITIESGRAPH.GEXF====================")

        
        nx.set_node_attributes(graph, -1, name="community")

        for index,comm in enumerate(array_of_comm):
            for member in comm.nodes():
                for node in graph.nodes():
                    if node==int(member):
                        graph.nodes[node]["community"]=index
        
        nx.write_gexf(graph, "data/visualization/allCommunitiesGraph.gexf", version="1.2draft")


    def spreading(graph, infected):

        """
        Load each step of spreading to a gexf file for gephi

        :param graph, infected: Graph and array with infected/activated nodes of each step
       
        :return: void (files in data/visualization) 
        """

        #show each step which node infected (retweeted)
        print(f"============SPREADING SAVED IN SPREADING.GEXF====================")

        #print("infected",infected)

        for x in range(0,len(infected)):
            nx.set_node_attributes(graph, 0, name="infected")
            for node in graph.nodes():
                for infected_node in infected[x]:
                    if(infected_node==node):
                        graph.nodes[node]["infected"]=1

            nx.write_gexf(graph, "data/visualization/spreading"+ str(x) +".gexf", version="1.2draft")


    def nbOfStepsToCover(graph, steps):

        """
        Shows how many nodes are activated at each step

        :param graph, steps: Graph and array of activated nodes for each step
       
        :return: void
        """

        print(f"============NB OF STEPS TO COVER====================")


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


    def nodesEdgesInCommunities(array_of_subgraphs): 
        
        """
        show nodes/edges of each community

        :param array_of_subgraphs: all communities in an array
       
        :return: void
        """

        print(f"============NODES/EDGES IN COMMUNITIES====================")

        nbOfEdges=[]
        nbOfNodes= []

        for subgraph in array_of_subgraphs:
            nbOfNodes.append(subgraph.number_of_nodes())
            nbOfEdges.append(subgraph.number_of_edges())

      
        #print(nbOfNodes,nbOfEdges)
        plt.title("Nodes and Edges in communities")
        plt.xlabel("Number of Edges")
        plt.ylabel("Number of Nodes")

        #if many have the same (x,y) the dot gets darker, so we can see which is more common. (many/little nodes, many/little edges)
        plt.scatter(nbOfEdges,nbOfNodes,alpha=.1, s=200, color='red')
        plt.show()


    def nodesInfected(graph,steps):
    
        """
        Show degree and how many nodes are activated

        :param graph, steps: Graph and array of activated nodes in each step
       
        :return: void
        """

        lastStep = steps[len(steps)-1]
        #print(lastStep)
        nodesInfected = [0]*len(lastStep)
        degrees = []
        for index, activeNode in enumerate(lastStep):
            degrees.append(graph.degree[activeNode])
            #print("degree of active node")
            for neighbor in graph.neighbors(activeNode):
                if Visualization.contains(neighbor, lastStep):
                    nodesInfected[index]+=1
        

        x = degrees
        y = nodesInfected
        plt.title("nb of neighbors and how many neighbors retweeted")
        plt.xlabel("degree")
        plt.ylabel("nodes who retweeted")

        plt.scatter(x,y,alpha=0.2)
        plt.show()


    def compareTwoCommunities(comm1, comm2, wholeGraph):

        """
        Compare two communities on same nodes and nodes going from one community to the other

        :param comm1,comm2,wholeGraph: two communities and the whole graph
       
        :return: void
        """

        print(f"============COMPARISON OF 2 COMMUNITIES====================")

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


    def centrality(graph, startingNodes):

        """
        Show central nodes with 3 methods (degree, closeness and eigenvector) 
        and compare them with the starting nodes computed by the algorithm
        and the topN central nodes

        :param graph, startingNodes: Graph and all starting nodes in an array
       
        :return: void
        """

        print(f"============CENTRALITY====================")

        degree_cent=nx.degree_centrality(graph)
        closeness_cent=nx.closeness_centrality(graph)
        eigenvector_cent=nx.eigenvector_centrality(graph,max_iter=1000)

        nbOfStartingNodes=len(startingNodes)

        print("degree centrality ")
        topNdegree = Visualization.top_keys(degree_cent,nbOfStartingNodes)
        print(f"================================")
        print("closeness centrality ")
        topNcloseness = Visualization.top_keys(closeness_cent,nbOfStartingNodes)
        print(f"================================")
        print("eigenvector centrality")
        topNeigenvector = Visualization.top_keys(eigenvector_cent,nbOfStartingNodes)
        print(f"================================")

        sameDegree=[]
        for top in topNdegree:
            if (Visualization.contains(top,startingNodes)):
                sameDegree.append(top)
        
        print("Starting Nodes which are top N in degree centrality:",sameDegree,"percentage:",len(sameDegree)/nbOfStartingNodes)

        sameCloseness=[]
        for top in topNcloseness:
            if (Visualization.contains(top,startingNodes)):
                sameCloseness.append(top)
        
        print("Starting Nodes which are top N in closeness centrality:",sameCloseness,"percentage:",len(sameCloseness)/nbOfStartingNodes)

        sameEigenvector=[]
        for top in topNeigenvector:
            if (Visualization.contains(top,startingNodes)):
                sameEigenvector.append(top)
        
        print("Starting Nodes which are top N in eigenvector centrality:",sameEigenvector,"percentage:",len(sameEigenvector)/nbOfStartingNodes)
        

    def centralityAllCommunities(array_comm,topN):

        """
        Show degree and how many nodes are activated for all communities and the topN nodes

        :param array_comm, topN: Array of all communities, and the number of top central nodes
       
        :return: array of each community with the degree,closeness and eigenvector centrality results for each node
        """
        
        print(f"============CENTRALITY OF EACH COMMUNITY====================")

        centForComms = []
        for comm in array_comm:
            print("Community",comm)

            degree_cent=nx.degree_centrality(comm) 
            topNdegree = Visualization.top_keys(degree_cent,topN)
            print(f"================================")
            
            closeness_cent=nx.closeness_centrality(comm) 
            topNcloseness = Visualization.top_keys(closeness_cent,topN)
            print(f"================================")
    
            eigenvector_cent=nx.eigenvector_centrality(comm,max_iter=1000)
            topNeigenvector = Visualization.top_keys(eigenvector_cent,topN)
            print(f"================================")

            centForComms.append([degree_cent,closeness_cent,eigenvector_cent])


        return centForComms
        
    
    def top_keys(dictionary, top):

        """
        Gets the top N central nodes

        :param dictionary, top: dictionary of all nodes with a centrality value
        , number of top central nodes
       
        :return: top nodes
        """

        from collections import Counter

        k = Counter(dictionary)
 
        # Finding 3 highest values
        high = k.most_common(top)
        
        print("With max",top,"highest values")
        print("Keys: Values")
        
        nodes=[]
        for i in high:
            print(i[0]," :",i[1]," ")
            nodes.append(i[0])

        return nodes


    def getNodesSeeingRetweet(graph, steps):

        """
        Gets the nodes which see a retweet in each step

        :param graph, steps: Graph and array of activated nodes in each step
       
        :return: array of nodes seeing retweets at each step
        """

        print(f"============GET NODES SEEING RETWEET AT EACH STEP====================")

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
            nodesSeeingRetweet[index]={"nbNodes":len(np.unique(nodesSeeingRetweet[index])),"percentage":len(np.unique(nodesSeeingRetweet[index]))/len(graph.nodes())}

        #all neoghbours of activated nodes - activated nodes - doubles (x an y activated both let z see retweet)
        print(nodesSeeingRetweet)

        return nodesSeeingRetweet


    def contains(item,list):

        """
        Returns if item is in a list

        :param item, list: a node, a list of nodes
       
        :return: true or false depending if node is in list
        """

        #print("Is ",item,"in",list)
        for listitem in list:
            if(listitem==item):
                return True
        
        return False


#creating some nx graph to test:

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

#Visualization.centrality(graph,[1,2]) #test ok
#Visualization.centralityAllCommunities([graph1,graph2, graph],10) #test ok

#Visualization.getNodesSeeingRetweet(graph,steps)
