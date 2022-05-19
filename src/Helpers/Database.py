"""
directed graph database with neo4j
store weights with nx.set_node_attributes
"""
import networkx as nx
from neo4j import GraphDatabase
from Helpers import progress
import Config

STEPS=100

def _getNxFromCSVFile(edgelist, vertexlist):
    """
    opens a CSV file and returns the directed and weighted graph
    """
    with open(edgelist, 'r') as elist, open(vertexlist, 'r') as vlist:
        lene = len(elist.readlines())
        lenv = len(vlist.readlines())
        elist.seek(0)
        vlist.seek(0)
        return _getNxFromCSV(elist, lene, vlist, lenv)
    

def _getNxFromCSV(edgelist, lene, vertexlist, lenv):
    """
    get a networkx graph from a csv list in memory with weights and timestamp
    """
    G = nx.DiGraph()
    print("Getting nodes")         
    for i, line in enumerate(vertexlist):        
        line = line.strip().split(",")
        G.add_node(line[0], weight=line[1])        
        progress(i, lenv, steps=STEPS)

    print("Getting edges")    
    for i, line in enumerate(edgelist):
        line = line.strip().split(',')
        G.add_edge(line[0], line[1], weight=int(line[2]), timestamp=int(line[3]))
        progress(i, lene, steps=STEPS)        

    return G

def getNxFromNeo4j():
    """
    get a networkx graph from a neo4j database
    """
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4j"))
    with driver.session() as session:
        #get all nodes from neo4j with their weights
        nodes = session.run("MATCH (n) RETURN n.id, n.weight")
        G = nx.DiGraph()
        print("Getting nodes")
        for i, record in enumerate(nodes):
            G.add_node(nodes["n"]["id"], weight=nodes["n"]["weight"])
            progress(i, len(G.nodes()), steps=STEPS)

        #get all edges from neo4j with their weights and timestamp
        edges = session.run("MATCH (n)-[r]->(m) RETURN n.id, m.id, r.weight, r.timestamp")
        print("Getting edges")
        for i, record in enumerate(edges):
            G.add_edge(record["n"]["id"], record["m"]["id"], weight=record["r"]["weight"], timestamp=record["r"]["timestamp"])
            progress(i, len(G.edges()), steps=STEPS)
    return G

def pushNxToNeo4j(G):
    """
    push a networkx graph to neo4j
    """
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "socialmediaanalytics"))
    with driver.session() as session:
    
        #push all edges with their weights and timestamp from Nx to neo4j
        print("Pushing edges and nodes")
        for i, edge in enumerate(G.edges(data=True)):
            session.run("MERGE (n:Node {id: $id})", id=edge[0])
            session.run("MERGE (m:Node {id: $id})", id=edge[1])
            #add edge edge[0] - edge[1] to neo4j
            session.run("MATCH (n:Node {id: $id}), (m:Node {id: $id2}) MERGE (n)-[r:Edge {weight: $weight, timestamp: $timestamp}]->(m)", id=edge[0], id2=edge[1], weight=edge[2]["weight"], timestamp=edge[2]["timestamp"])
            progress(i, len(G.edges()), steps=STEPS)

if __name__ == "__main__":
    """
    load preprocessed file to neo4j
    """
    Config.verbose = True        
    filename = "preprocessed_1652971137"
    G = _getNxFromCSVFile(f"src/data/{filename}.csv", f"src/data/{filename}_vertexlist.csv")
    pushNxToNeo4j(G)    