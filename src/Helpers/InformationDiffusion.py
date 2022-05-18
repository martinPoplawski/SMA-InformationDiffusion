import math 


class InformationDiffusion:
    """Algorithm for whole project"""
    
    def ltm(graph, startingNodes):

        """
        Check which nodes are activated

        :param graph: Graph for Algorithm
        :param startingNodes: Nodes that are activated at the beginning
       
        :return: All nodes activated at each iteration step 
        """

        i = 0
        A = startingNodes.copy()
        B = {}
        steps = []  
        while i == 0 or A != B:
            B = A.copy()
            temp = A.copy()
            inactiveNodes = set(graph.nodes) - A
            for node in inactiveNodes: 
                edges = graph.in_edges(node)
                sum = 0
                for out, inc in edges:
                    if out in A:
                        sum += graph.edges[out,inc]['weight']  

                if sum > graph.nodes[node]["threshholds"]:
                    temp.add(node)
            A = temp.copy()
            steps.append(temp)
            i += 1
        return steps

 
    def maxCasc(graph, budget=10, cost=5):
        """
        Searching for best suitable nodes to start with
        Optimize in terms of error and loss function 

        :param graph: Graph for Algorithm
        :param budget: Max number of iterations/nodes that are started with
        :param cost: If the lost improvement is less than cost, the algorithm 
                      stops prematurely

        :return: Starting set of nodes for biggest spread
        """

        # TODO Find most central node
        # central = 0
        # centralN = None
        # for node in graph.nodes(): 
        #     if len(graph.out_edges(node)) > central: 
        #         central = len(graph.out_edges(node))
        #         centralN = node

        # print(central)
        # print(centralN)
        # test = set([centralN])
        # print(test)
        # print(len(InformationDiffusion.ltm(graph, test)))

        i = 0
        S = set()
        bestValue = math.inf
        bestNode = 0
        oldValue = math.inf
        while i < budget:

            for node in graph.nodes():
                Stemp = S.copy()
                Stemp.add(node)
                value = InformationDiffusion.loss(graph, InformationDiffusion.ltm(graph, Stemp)[-1])
                if value < bestValue: 
                    bestNode = node
                    bestValue = value

            if oldValue - bestValue < cost: 
                break
            S.add(bestNode)
            oldValue = bestValue
            i += 1
        return S


    # (1 - Threshhold of node) * incoming edges
    # Summed over all non activated nodes
    def loss(graph, activated):
        """
        Loss of not activated people on the network based on their threshhold
        and incoming edges

        :param graph: Graph for Algorithm
        :param activated: The activated nodes in the graph

        :return: Loss (int)
        """
        #print(activated)
        inactive = set(graph.nodes()) - activated
        sum = 0
        for node in inactive: 
            sum += (1 - graph.nodes[node]['threshholds']) * len(graph.in_edges(node))

        return sum 


    #TODO find cost and gain function 
    def maxCascCostAndGain(graph, budget=3, cost=10, gain=0.5):
        i = 0
        S = set()
        bestSet = math.inf
        bestNode = 0
        while i < budget:
            for node in graph.nodes():
                Stemp = S.copy()
                Stemp.add(node)
                value = InformationDiffusion.loss(graph, InformationDiffusion.ltm(graph, Stemp))
                if value < bestSet: 
                    bestNode = node
                    bestSet = value
            S.add(bestNode)
            i += 1

        return S