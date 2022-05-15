import math 


class InformationDiffusion:
    """Algorithm for whole project"""

    def ltm(graph, startingNodes):
        i = 0
        A = startingNodes.copy()
        B = {}
        while i == 0 or A != B:
            B = A 
            inactiveNodes = set(graph.nodes) - A
            for node in inactiveNodes: 
                edges = graph.in_edges(node)
                sum = 0
                for out, inc in edges:
                    if out in A:
                        sum += graph.edges[out,inc]['weight']  

                if sum > graph.nodes[node]["threshholds"]:
                    B.add(node)
            A = B
            i += 1
        return A


    #TODO Reevaluate how many nodes should be contaced or just use fixed number
    # Optimize in terms of error and loss function 
    # with loss being threshholds not inflicted (1 - threshhold)
    # Or people who have not seen it. 
    def maxCasc(graph, budget=10, cost=5):
        i = 0
        S = set()
        
        bestValue = math.inf
        bestNode = 0
        oldValue = math.inf
        while i < budget:
            for node in graph.nodes():
                Stemp = S.copy()
                Stemp.add(node)
                value = InformationDiffusion.loss(graph, InformationDiffusion.ltm(graph, Stemp))
                if value < bestValue: 
                    bestNode = node
                    bestValue = value

            print(bestValue)

            if oldValue - bestValue < cost: 
                break

            S.add(bestNode)
            oldValue = bestValue
            i += 1

        #DANA Set of nodes that is best to start with... 
        # TODO Get set of nodes at each iteration, after you know starting nodes with ltm()
        return S

    
    def loss(graph, activated):
        inactive = set(graph.nodes()) - activated
        sum = 0
        for node in inactive: 
            sum += (1 - graph.nodes[node]['threshholds']) * len(graph.in_edges(node))

        return sum 


    def maxCascWithoutCost(graph, budget=3):
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