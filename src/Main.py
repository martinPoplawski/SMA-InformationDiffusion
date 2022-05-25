import sys
sys.path.insert(0, 'Helpers')
from Preprocessing import combineFiles
import Config as Config
from Database import _getNxFromCSVFile, pushNxToNeo4j
import networkx as nx
from InformationDiffusion import InformationDiffusion
from PostProcessing import prepareGraph
from CommunitiesM import CommunitiesM as Community


args = {"-loadAll": 0, "-noverbose": 0, "-help\t": 0, "-community": 0, "-optimization": 0, 'args': [], '-sample': 0}
desc = {"-loadAll": "loads the higgs activity and social graph into neo4j",
        "-noverbose": "prevent too much output",
        "-help\t": "prints this help",
        "-sample": "samples the Graph and splits it into communities",
        "-community" : "community [N] | -c [N]\n\t\t\t\tchoose the community N",
        "-optimization": "optimization [opt] | -o [opt]\n\t\t\t\tchoose from Loss | Lossfast | CostAndGain | Percentage (case insensitive)"}

G = nx.DiGraph()
S = set()


def loadAllDataIntoNeo4j():
    filename = combineFiles()
    G = _getNxFromCSVFile(f"src/data/{filename}.csv", f"src/data/{filename}_vertexlist.csv")
    pushNxToNeo4j(G)   
    
def printHelp():
    helpstr = """Usage:
python3 src/Main.py [options]
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


    #if -noverbose is given, set verbose to false
    if args["-noverbose"]:
        Config.verbose = False

    #if -loadAll is given, load all data into neo4j
    if args["-loadAll"]:        
        loadAllDataIntoNeo4j()
    
    #if -sample is given, sample the graph and create communities
    if args["-sample"]: 
        print(len(sys.argv))
        if len(sys.argv) < 3: 
            print("-sample requires an argument (int)")
        
        #if len(sys.argv) <= :
        #G = _getNxFromCSVFile(f"data/Comms/higgs-Comm-9.csv")
        Community.splitGraphIntoCommunities(int(sys.argv[2]))
        
       

    #if -community is given, load the community into neo4j
    if args["-community"] > 0:
        comminityNumber = args["-community"]
        G = _getNxFromCSVFile(f"data/Comms/higgs-Comm-{comminityNumber}.csv")
        pushNxToNeo4j(G)     

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



if __name__ == "__main__":
    main()