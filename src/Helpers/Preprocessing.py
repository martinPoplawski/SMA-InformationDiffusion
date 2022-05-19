import csv  
import time
import Config 
from Helpers import print, progress


class Tweet:
    person1: int
    person2: int
    timestamp: int
    weight = 1

    def __init__(self, person1, person2, timestamp=0, weight=1):
        self.person1 = int(person1)
        self.person2 = int(person2)
        self.timestamp = int(timestamp)
        self.weight = int(weight)
    
    def __eq__(self, other):
        """
        checks if the persons are the same and the tweettype is the same
        """
        return other.person1 == self.person1 and other.person2 == self.person2
    
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return int(str(self.person1) + "0000000000" + str(self.person2))

    def __str__(self) -> str:
        return f"{self.person1=}, {self.person2=}, {self.timestamp=}"
 

class Tweets:
    tweets: set[Tweet]
    def __init__(self):
        self.tweets = set()

    def add(self, tweet: Tweet):
        if tweet not in self.tweets:
            self.tweets.add(tweet)
        else:
            tweet.weight += 1
            self.tweets.remove(tweet)
            self.tweets.add(tweet)

class Vertex:
    id: int
    weight: int

    def __init__(self, id, weight):
        self.id = int(id)
        self.weight = int(weight)
    
    def __hash__(self) -> int:
        return self.id

    def __eq__(self, other):
        return self.id == other.id
    
    def __ne__(self, other):
        return self.id != other.id

class Vertices:
    vertices: set[Vertex]
    def __init__(self):
        self.vertices = set()

    def add(self, vertex: Vertex):
        if vertex not in self.vertices:
            self.vertices.add(vertex)
        else:
            vertex.weight += 1
            self.vertices.remove(vertex)
            self.vertices.add(vertex)


def combineFiles():
    with open("src/data/higgs-activity_time.txt") as activity_file, open("src/data/higgs-social_network.edgelist") as social_file:
        activity = csv.reader(activity_file)
        social = csv.reader(social_file)

        tweets = Tweets()
        print("reading activity")
        for i, edge in enumerate(activity):
            edge = edge[0].split(" ")
            tweets.add(Tweet(edge[0], edge[1], edge[2]))                            
            progress(i, 563069, steps=5000)                    
        
        print("reading social")
        for i, edge in enumerate(social):
            edge = edge[0].split(" ")
            tweets.add(Tweet(edge[0], edge[1]))                          
            progress(i, 14855841, steps=10000)                     
        
        filename = f"preprocessed_{int(time.time())}"
        with open(f"src/data/{filename}.csv", "w", newline="") as file:
            data = csv.writer(file)
            print(f"writing edgelist to csv {filename}.csv")
            #data.writerow(["person1", "person2", "weight", "timestamp"])
            for i, tweet in enumerate(tweets.tweets):
                data.writerow([tweet.person1, tweet.person2, tweet.weight, tweet.timestamp])
                progress(i, len(tweets.tweets), steps=1000)       

        generateVertexListFromTweets(tweets.tweets, filename)    

def generateVertexListFromTweets(tweets, filename):
    vertices = Vertices()
    for i, tweet in enumerate(tweets):                
        vertices.add(Vertex(tweet.person1, 1))
        vertices.add(Vertex(tweet.person2, 1))
        progress(i, len(tweets), steps=1000)
    #store vertices in csv
    with open(f"src/data/{filename}_vertexlist.csv", "w", newline="") as file:
        data = csv.writer(file)        
        #write vertices and their weights to csv
        print(f"writing vertexlist to {filename}_vertexlist.csv")
        for i, vertex in enumerate(vertices.vertices):
            data.writerow([vertex.id, vertex.weight])
            progress(i, len(vertices.vertices), steps=1000)



def openFile(file) -> set[Tweet]:
    tweets = set()
    with open(file) as file:
        reader = csv.reader(file)
        for edge in reader:
            tweets.add(Tweet(edge[0], edge[1], edge[2]))
    return tweets

def checkFile(file):
    tweets = openFile(file)
    print("read file")
    count = 0
    for edge in tweets:
        if edge.timestamp != "0": #edge.timestamp is somehow a string...
            count += 1
    print(f"{count=}, {len(tweets)=}")

def fuuuuuuck():
    """
    this function can be used if you fucked up the vertexlist generation
    it allows you to generate the vertexlist from the edgelist csv
    """
    filename = "preprocessed_1652172596"
    with open(f"src/data/{filename}.csv") as file:        
        vertices = set()
        reader = csv.reader(file)
        for i, edge in enumerate(reader):            
            vertices.add(Vertex(edge[0], 1))
            vertices.add(Vertex(edge[1], 1))
            progress(i, 15056958, steps=1000)                           

    #store vertices in csv
    with open(f"src/data/{filename}_vertexlist.csv", "w", newline="") as file:
        data = csv.writer(file)        
        #write vertices and their weights to csv
        print(f"writing vertexlist to {filename}_vertexlist.csv")
        for i, vertex in enumerate(vertices):
            data.writerow([vertex.id, vertex.weight])
            progress(i, len(vertices), steps=1000)


if __name__ == "__main__":
    Config.verbose = True
    #fuuuuuuck()
    print("done")
    combineFiles()

        
        