import sys


sys.path.insert(0, 'Helpers')
from Visualization import Visualization
from Preprocessing import combineFiles
import Config as Config
from Database import _getNxFromCSVFile, pushNxToNeo4j
import networkx as nx
from InformationDiffusion import InformationDiffusion
from PostProcessing import prepareGraph
from CommunitiesM import CommunitiesM as Community


args = {"-loadAll": 0, "-noverbose": 0, "-help\t": 0, "-community": 0, "-optimization": 0, 'args': [], '-sample': 0, '-visualization':0}
desc = {"-loadAll": "loads the higgs activity and social graph into neo4j",
        "-noverbose": "prevent too much output",
        "-help\t": "prints this help",
        "-sample": "samples the Graph and splits it into communities",
        "-community" : "community [N] | -c [N]\n\t\t\t\tchoose the community N",
        "-optimization": "optimization [opt] | -o [opt]\n\t\t\t\tchoose from Loss | Lossfast | CostAndGain | Percentage (case insensitive)",
        "-visualization":"visualize findings, visualization [N], choose a community N"}

#TODO complete description
G = nx.DiGraph()
S = set()


def loadAllDataIntoNeo4j():
    filename = combineFiles()
    G = _getNxFromCSVFile(f"data/{filename}.csv", f"data/{filename}_vertexlist.csv")    
    #pushNxToNeo4j(G)   
    
def printHelp():
    helpstr = """Usage:
cd src & python3 Main.py [options]
Options:
"""
    for key in args:
        helpstr += f"\t{key} \t- {desc[key]}\n"        
    print(helpstr)


def argcheck(arg, args):
    return arg in args or arg == "-c" or arg == "-o"

def main():      
    #check all arguments and store if they occur
    skipnext = 0
    lastarg = ""
    for i, arg in enumerate(sys.argv): 

        #if the argument is a flag, skip it
        if skipnext > 0:
            if argcheck(arg, args):
                print(f"expected argument after {lastarg}, got {arg} instead")
                return
            skipnext -= 1
            continue

        if argcheck(arg, args):
            #community parsing
            if arg == "-community" or arg == "-c":
                lastarg = arg
                if arg == "-c": arg = "-community"
                skipnext += 1                 
                if len(sys.argv) <= i+1:
                    print(f"expected argument after {lastarg}, got no more arguments instead")
                    return
                if argcheck(sys.argv[i+1], args):
                    print(f"expected argument after {lastarg}, got {sys.argv[i+1]} instead")
                    return
                argument = 0
                try:
                    args[arg] = int(sys.argv[i+1]) 
                except ValueError:
                    print(f"expected argument in number format after {lastarg}, got {sys.argv[i+1]} instead")
                    return
                continue

            #optimization parsing
            if arg == "-optimization" or arg == "-o":
                lastarg = arg
                if arg == "-o": arg = "-optimization"
                skipnext += 1
                if len(sys.argv) <= i+1:
                    print(f"expected argument after {lastarg}, got  no more arguments instead")
                    return
                if argcheck(sys.argv[i+1], args):
                    print(f"expected argument after {lastarg}, got {sys.argv[i+1]} instead")
                    return
                if sys.argv[i+1] in ["percentage"]: 
                    skipnext += 1
                    if len(sys.argv) <= i+2:
                        print(f"expected number after {lastarg}, got  no more arguments instead")
                        return
                    
                    args['args'].append(sys.argv[i+2])

                if sys.argv[i+1] in ["loss", "lossfast", "costandgain"]: 
                    skipnext += 2
                    if len(sys.argv) <= i+3:
                        print(f"expected 2 numbers after {lastarg} (number of max starting nodes, loss threshhold), got no more arguments instead")
                        return
                    
                    args['args'].append(sys.argv[i+2])
                    args['args'].append(sys.argv[i+3])

                args[arg] = str(sys.argv[i+1]).strip().lower()                
                continue
            if arg == "-sample" or arg == "-s":
                lastarg = arg
                if arg == "-s": arg = "-sample"
                skipnext += 1
                if len(sys.argv) <= i+1:
                    print(f"expected argument after {lastarg}, got  no more arguments instead")
                    return
                if argcheck(sys.argv[i+1], args):
                    print(f"expected argument after {lastarg}, got {sys.argv[i+1]} instead")
                    return
                

            #visualization parsing
            if arg == "-visualization":
                lastarg = arg
                skipnext += 1                 
                if len(sys.argv) <= i+1:
                    print(f"expected argument after {lastarg}, got no more arguments instead")
                    return
                if argcheck(sys.argv[i+1], args):
                    print(f"expected argument after {lastarg}, got {sys.argv[i+1]} instead")
                    return
                argument = 0
                try:
                    args[arg] = int(sys.argv[i+1]) 
                except ValueError:
                    print(f"expected argument in number format after {lastarg}, got {sys.argv[i+1]} instead")
                    return
                continue


            args[arg] = 1
        elif i>0:
            print(f"unknown argument {arg}")
            return
        
    #if no arguments are given, print help
    if len(sys.argv) == 1 or args["-help\t"]:
        printHelp()
        return
    
    if args["-loadAll"] and args["-community"] > 0:
        print("-loadAll and -community are mutually exclusive")
        return

    if ("-community" in sys.argv or "-c" in sys.argv) and args["-community"] == 0:
        print("-community requires an argument")
        return

    if args["-optimization"] != 0 and args["-optimization"] not in ["loss", "lossfast", "costandgain", "percentage"]:
        print("optimization must be one of: loss, lossfast, costandgain, percentage")
        return
    
    if ("-visualization" in sys.argv) and args["-visualization"] == 0:
        print("-visualization requires an argument")
        return


    #if -noverbose is given, set verbose to false
    if args["-noverbose"]:
        Config.verbose = False

    #if -loadAll is given, load all data into neo4j
    if args["-loadAll"]:        
        loadAllDataIntoNeo4j()
    
    #if -sample is given, sample the graph and create communities
    if args["-sample"]: 
        if len(sys.argv) < 3: 
            print("-sample requires an argument (int)")
        
        #if len(sys.argv) <= :
        #G = _getNxFromCSVFile(f"data/Comms/higgs-Comm-9.csv")
        Community.splitGraphIntoCommunities(int(sys.argv[2]))
        
       

    #if -community is given, load the community into neo4j
    if args["-community"] > 0:
        comminityNumber = args["-community"]
        G = _getNxFromCSVFile(f"data/Comms/higgs-Comm-{comminityNumber}.csv")
        #TODO remove with DB
        #pushNxToNeo4j(G)     

    #if -optimization is given, run optimization
    if args["-optimization"] != 0 and args["-optimization"] in ["loss", "lossfast", "costandgain", "percentage"]:  
        G = prepareGraph(G)
        otype = args["-optimization"]
        if otype == "costandgain":
            S = InformationDiffusion.maxCascCostAndGain(G, cost= int(args['args'][0]), gain=int(args['args'][1]))
        elif otype == "percentage":
            S = InformationDiffusion.maxCascPercentage(G, percentage=float(args['args'][0])) 
        elif otype == "loss":
            S = InformationDiffusion.maxCasc(G, budget= int(args['args'][0]), cost=int(args['args'][1]))
        elif otype == "lossfast":
            S = InformationDiffusion.maxCascFast(G, budget= int(args['args'][0]), cost=int(args['args'][1]))

        steps = InformationDiffusion.ltm(G,S)
        print(f"Number of starting Nodes: {len(S)}")
        print(f"Coverage: {len(InformationDiffusion.ltm(G, S)[-1])}/{len(G.nodes())}")
        print(f"Starting Nodes: {S}")
        print(f"================================")

        #S = StartingSet
        #G = Community
        #steps = steps

        #DANA stuff should be here to visualize depending on what you wanna do
        #visualize(G,S)
        #communityNumber2=int(args['args'][0])

    if args["-visualization"]:

        wholeG = nx.read_edgelist('data/sampled-graph.edgelist', nodetype=int, create_using=nx.DiGraph())

        print("whole G",wholeG)

      
        arg2 = args["-visualization"]
        print("argument 2: ",arg2)
       
        arrayOfCommunities=createCommunityArray()
        #communityNumber2=10
        
        Visualization.edges_weights(G) #test ok
        Visualization.neighbors_nodes(G) #test ok
        Visualization.numberOfEdges(G) #test ok
        Visualization.numberOfNodes(G) #test ok

        Visualization.community(G) #TODO:need to check
        Visualization.oneCommunityInGraph(wholeG,G)
        Visualization.allCommunitiesInGraph(wholeG,arrayOfCommunities)
        Visualization.spreading(G,steps) #TODO: need to check

        Visualization.nbOfStepsToCover(G,steps) #test ok
        Visualization.nodesEdgesInCommunities(arrayOfCommunities) #test ok
        Visualization.nodesInfected(G,steps) #test ok


        G2 = _getNxFromCSVFile(f"data/Comms/higgs-Comm-{arg2}.csv")
        Visualization.compareTwoCommunities(G,G2,wholeG) #TODO: need whole graph

        Visualization.centrality(G,S) #test ok
        #Visualization.centralityAllCommunities(arrayOfCommunities,10) #takes alot of time
        Visualization.getNodesSeeingRetweet(G,steps) #test ok
       

def createCommunityArray():
    x=0
    comm_array=[]
    while(True):
        try:
            comm = nx.read_edgelist('data/Comms/higgs-Comm-'+str(x)+'.edgelist', nodetype=int, create_using=nx.DiGraph())
            comm_array.append(comm)
            print(comm)
            x=x+1
        except:
            break
    #print("Nb of communities: ",len(comm_array))
    print("nb of nodes communities: ",comm_array)
    return comm_array





if __name__ == "__main__":
    main()