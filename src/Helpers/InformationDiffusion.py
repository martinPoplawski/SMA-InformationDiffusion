import math 
from concurrent.futures import ThreadPoolExecutor
from threading import Condition
from Helpers import progress
from Visualization import Visualization as Visualization
import time



class InformationDiffusion:
    """Algorithm for whole project"""
    

    def ltm(graph, startingNodes):
        """
        Check which nodes will be activated in a graph

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

            #Go through all inactive nodes and find best result
            #Sum incoming edges and compare to node threshhold
            for node in inactiveNodes: 
                edges = graph.in_edges(node)
                sum = 0
                for out, inc in edges:
                    if out in A:
                        sum += float(graph.edges[out,inc]['weight'])
                if sum > graph.nodes[node]["threshholds"]:
                    temp.add(node)
            
            A = temp.copy()
            steps.append(temp)
            i += 1
        return steps


    def __ltmOne(graph, startingNodes):

        """
        Check which nodes are activated at next time step

        :param graph: Graph for Algorithm
        :param startingNodes: Nodes that are activated at the beginning
       
        :return: Nodes that are activated at next time step 
        """

        i = 0
        A = startingNodes.copy()
        steps = []  
        temp = A.copy()
        inactiveNodes = set(graph.nodes) - A

        #Go through all inactive nodes and find best result
        #Sum incoming edges and compare to node threshhold
        for node in inactiveNodes: 
            edges = graph.in_edges(node)
            sum = 0
            for out, inc in edges:
                if out in A:
                    sum += float(graph.edges[out,inc]['weight'])
            if sum > graph.nodes[node]["threshholds"]:
                temp.add(node)
        steps.append(temp)
        i += 1
        return steps

    def __partialCascLoss(graph, nodes, S, cond):
        """
        Check for best node to add on given node Range based on smallest loss

        :param graph: Graph for Algorithm
        :param nodes: Node range to check 
        :param S: Set of starting Nodes 
        :param cond: Signal object to wake main thread
       
        :return: A list of the best node name and its Loss value 
        """

        bestValue = math.inf

        #Find the best node to add
        for node in nodes:
            Stemp = S.copy()
            Stemp.add(node)
            value = InformationDiffusion.__loss(graph, InformationDiffusion.ltm(graph, Stemp)[-1])
            if value < bestValue: 
                bestNode = node
                bestValue = value

        #Signal sleeping main thread to check again if necessary
        cond.acquire()
        cond.notify()
        cond.release()

        return [bestNode, bestValue]

    
    def __partialCascLen(graph, nodes, S, cond): 

        """
        Check for best node to add on given node Range based on biggest final set

        :param graph: Graph for Algorithm
        :param nodes: Node range to check 
        :param S: Set of starting Nodes 
        :param cond: Signal object to wake main thread
       
        :return: A list of the best node name and its Loss value 
        """

        bestSet = 0

        #Find the best node to add
        for node in nodes:
            Stemp = S.copy()
            Stemp.add(node)
            value = len(InformationDiffusion.ltm(graph, Stemp)[-1])
            if value > bestSet: 
                bestNode = node
                bestSet = value

        #Signal sleeping main thread to check again if necessary        
        cond.acquire()
        cond.notify()
        cond.release()
        return [bestNode, bestSet]

    def __partialCascPerc(graph, nodes, S, cond): 

        """
        Check for best node to add on given node Range based on biggest final set

        :param graph: Graph for Algorithm
        :param nodes: Node range to check 
        :param S: Set of starting Nodes 
        :param cond: Signal object to wake main thread
       
        :return: A list of the best node name and its Loss value 
        """

        totalNodes= len(graph.nodes())
        bestPerc = 0

        #Find the best node to add
        for node in nodes:
            Stemp = S.copy()
            Stemp.add(node)
            steps = InformationDiffusion.ltm(graph, Stemp)

            result = Visualization.getNodesSeeingRetweet(graph, steps)
            seen = (len(steps[-1]) + result[-1]['nodes'])/totalNodes
            if seen > bestPerc: 
                bestNode = node
                bestPerc = seen

        #Signal sleeping main thread to check again if necessary        
        cond.acquire()
        cond.notify()
        cond.release()
        return [bestNode, bestPerc]


    def __loss(graph, activated):
        """
        Loss of not activated people on the network based on their threshhold
        and incoming edges

        :param graph: Graph for Algorithm
        :param activated: The activated nodes in the graph

        :return: Loss (int)
        """
        inactive = set(graph.nodes()) - activated
        sum = 0
        for node in inactive: 
            #sum += (1 - graph.nodes[node]['threshholds']) * len(graph.in_edges(node))
            sum += len(graph.in_edges(node))

        return sum 
        
 
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

        startTime = time.time()

        #Algorithm variables
        i = 0
        S = set()
        bestValue = math.inf
        bestNode = 0
        oldValue = math.inf

        #Concurrent Variables
        threads = 4
        executor = ThreadPoolExecutor(threads)
        futures = [] 
        nodes = list(graph.nodes())
        cond = Condition()
        print(f"InformationDiffusion starting nodes:")
        while i < budget:

            progress(i, budget, steps=1)

            #Creating Threads and distributing Work
            for j in range(threads):
                beg = int(j*(len(nodes)/threads))
                end = int((j + 1)*(len(nodes)/threads))
                futures.append(executor.submit(InformationDiffusion.__partialCascLoss,graph, nodes[beg:end], S, cond))
            
            #Checking Futures
            for future in futures: 
                cond.acquire()

                #Sleep if result is not ready yet
                while not future.done():
                    cond.wait()
                
                #Compare results
                result  = future.result()
                if result[1] < bestValue: 
                    bestValue = result[1] 
                    bestNode = result[0]
                cond.release()

            #If improvement is smaller then threshhold stop algorithm
            if oldValue - bestValue < cost: 
                break

            S.add(bestNode)
            oldValue = bestValue
            
            i += 1

        executionTime = (time.time() - startTime)
        print('Execution time in seconds: ' + str(executionTime))    
        return S


    def maxCascCostAndGain(graph, cost=10, gain=0.5):

        """
        Searching for best suitable nodes to start with
        Optimize in terms of Cost per node that is in the start set and Gain of node that is activated through ltm  

        :param graph: Graph for Algorithm
        :param cost: Cost to add a node to start set
        :param gain: Gain of activating another node

        :return: Starting set of nodes for biggest spread
        """

        #Algorithm variables
        i = 0
        S = set()
        oldSet = 0
        bestSet = 0
        bestNode = 0

        #Concurrent variables
        threads = 6
        executor = ThreadPoolExecutor(threads)
        futures = [] 
        nodes = list(graph.nodes())
        cond = Condition()

        while (bestSet - oldSet) * gain > cost or i < 3:
            oldSet = bestSet

            #Creating Threads and distributing Work
            for j in range(threads):
                beg = int(j*(len(nodes)/threads))
                end = int((j + 1)*(len(nodes)/threads))
                futures.append(executor.submit(InformationDiffusion.__partialCascLen,graph, nodes[beg:end], S, cond))

            #Checking Futures
            for future in futures: 
                cond.acquire()

                #Sleep if result is not ready yet
                while not future.done():
                    cond.wait()

                #Compare Results
                result  = future.result()

                if result[1] > bestSet: 
                    bestSet = result[1] 
                    bestNode = result[0]
                cond.release()
            
            S.add(bestNode)
            i += 1

        return S

    def maxCascPercentage(graph, percentage=0.9):

        """
        Searching for best suitable nodes to start with such that X percentage of network are activated

        :param graph: Graph for Algorithm
        :param percentage: Goal percentage of network activated

        :return: Starting set of nodes for biggest spread
        """


        #Algorithm variables
        i = 0
        S = set()
        totalNodes = len(graph.nodes())
        bestSet = 0
        bestNode = 0
        #percentage of people that have seen the tweet on the network
        seen = 0


        #Concurrent Variables
        threads = 6
        executor = ThreadPoolExecutor(threads)
        futures = [] 
        nodes = list(graph.nodes())
        cond = Condition()

        print(f"InformationDiffusion starting nodes:")

        while seen < percentage:
            progress(int(seen*1000), int(percentage*1000), steps=1)

            #Creating Threads and distributing Work
            for j in range(threads):
                beg = int(j*(len(nodes)/threads))
                end = int((j + 1)*(len(nodes)/threads))
                futures.append(executor.submit(InformationDiffusion.__partialCascPerc,graph, nodes[beg:end], S, cond))

            #Checking Futures
            for future in futures: 
                cond.acquire()

                #Sleep if result is not ready yet
                while not future.done():
                    cond.wait()

                #Compare Results    
                result  = future.result()
                if result[1] > bestSet: 
                    bestSet = result[1] 
                    bestNode = result[0]
                cond.release()

            
            S.add(bestNode)
            #steps = InformationDiffusion.ltm(graph,S)
            #result = Visualization.getNodesSeeingRetweet(graph, steps)
            #seen = (len(steps[-1]) + result[-1]['nodes'])/totalNodes
            seen = bestSet

            i += 1

        return S


    def maxCascSingle(graph, budget=10, cost=5):
        """
        Searching for best suitable nodes to start with
        Optimize in terms of error and loss function 

        :param graph: Graph for Algorithm
        :param budget: Max number of iterations/nodes that are started with
        :param cost: If the lost improvement is less than cost, the algorithm 
                      stops prematurely

        :return: Starting set of nodes for biggest spread
        """

        startTime = time.time()
        i = 0
        count = 0
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
                count += 1

            if oldValue - bestValue < cost: 
                break
            S.add(bestNode)
            oldValue = bestValue
            i += 1
        
        executionTime = (time.time() - startTime)
        print('Execution time in seconds: ' + str(executionTime))
        return S

    def maxCascFast(graph, budget=10, cost=5):
        """
        Searching for best suitable nodes to start with
        Optimize in terms of error and loss function 

        :param graph: Graph for Algorithm
        :param budget: Max number of iterations/nodes that are started with
        :param cost: If the lost improvement is less than cost, the algorithm 
                      stops prematurely

        :return: Starting set of nodes for biggest spread
        """

        startTime = time.time()

        #Algorithm variables
        i = 0
        S = set()
        bestValue = math.inf
        bestNode = 0
        oldValue = math.inf

        #Concurrent Variables
        threads = 4
        executor = ThreadPoolExecutor(threads)
        futures = [] 
        nodes = list(graph.nodes())
        cond = Condition()

        startTime = time.time()
        i = 0
        count = 0
        S = set()
        bestValue = math.inf
        bestNode = 0
        oldValue = math.inf
        print(f"InformationDiffusion starting nodes:")

        while i < budget:
            progress(i, budget, steps=1)

            for node in graph.nodes():
                Stemp = S.copy()
                Stemp.add(node)
                value = InformationDiffusion.__loss(graph, InformationDiffusion.__ltmOne(graph, Stemp)[-1])
                if value < bestValue: 
                    bestNode = node
                    bestValue = value
                count += 1

            if oldValue - bestValue < cost: 
                break
            S.add(bestNode)
            oldValue = bestValue
            i += 1
        
        executionTime = (time.time() - startTime)
        print('Execution time in seconds: ' + str(executionTime))
        return S
