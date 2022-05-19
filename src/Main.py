import sys
sys.path.insert(0, 'Helpers')
from Preprocessing import combineFiles
from Config import verbose

args = {"-loadAll": 0, "-noverbose": 0, "-help\t": 0}
desc = {"-loadAll": "loads the higgs activity and social graph into neo4j",
        "-noverbose": "prevent too much output",
        "-help\t": "prints this help"}

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


def main():    
    #check all arguments and store if they occur
    for arg in sys.argv:
        if arg in args:
            args[arg] = 1
    #if no arguments are given, print help
    if len(sys.argv) == 1 or args["-help\t"]:
        printHelp() 
    #if -noverbose is given, set verbose to false
    if args["-noverbose"]:
        Config.verbose = False
    #if -loadAll is given, load all data into neo4j
    if args["-loadAll"]:
        loadAllDataIntoNeo4j()


if __name__ == "__main__":
    main()