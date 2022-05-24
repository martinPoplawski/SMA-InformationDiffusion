import sys
sys.path.insert(0, 'Helpers')
from Preprocessing import combineFiles
import Config
from Database import _getNxFromCSVFile, pushNxToNeo4j
import networkx as nx
import InformationDiffusion

args = {"-loadAll": 0, "-noverbose": 0, "-help\t": 0, "-community": 0, "-optimization": 0}
desc = {"-loadAll": "loads the higgs activity and social graph into neo4j",
        "-noverbose": "prevent too much output",
        "-help\t": "prints this help",
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
    skipnext = False
    lastarg = ""
    for i, arg in enumerate(sys.argv): 

        #if the argument is a flag, skip it
        if skipnext:
            if argcheck(arg, args):
                print(f"expected argument after {lastarg}, got {arg} instead")
                return
            skipnext = False
            continue

        if argcheck(arg, args):
            #community parsing
            if arg == "-community" or arg == "-c":
                lastarg = arg
                if arg == "-c": arg = "-community"
                skipnext = True                
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
                skipnext = True
                if len(sys.argv) <= i+1:
                    print(f"expected argument after {lastarg}, got  no more arguments instead")
                    return
                if argcheck(sys.argv[i+1], args):
                    print(f"expected argument after {lastarg}, got {sys.argv[i+1]} instead")
                    return
                args[arg] = str(sys.argv[i+1]).strip().lower()                
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

    #if -noverbose is given, set verbose to false
    if args["-noverbose"]:
        Config.verbose = False

    #if -loadAll is given, load all data into neo4j
    if args["-loadAll"]:        
        loadAllDataIntoNeo4j()
    
    #if -community is given, load the community into neo4j
    if args["-community"] > 0:
        comminityNumber = args["-community"]
        G = _getNxFromCSVFile(f"data/Comms/higgs-Comm-{comminityNumber}.edgelist")
        pushNxToNeo4j(G)     

    #if -optimization is given, run optimization
    if args["-optimization"] != 0 and args["-optimization"] in ["loss", "lossfast", "costandgain", "percentage"]:   
        otype = args["-optimization"]
        if otype == "costandgain":
            S = InformationDiffusion.maxCascCostAndGain(G)
        elif otype == "percentage":
            S = InformationDiffusion.maxCascPercentage(G) 
        elif otype == "loss":
            S = InformationDiffusion.maxCasc(G)
        elif otype == "lossfast":
            S = InformationDiffusion.maxCascOne(G)



if __name__ == "__main__":
    main()