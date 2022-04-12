import csv  
import time
from Helpers import print


class Tweet:
    person1: int
    person2: int
    timestamp: int

    def __init__(self, person1, person2, timestamp=0):
        self.person1 = person1
        self.person2 = person2
        self.timestamp = timestamp


    
    def __eq__(self, other):
        """
        checks if the persons are the same and the tweettype is the same
        """
        return other.person1 == self.person1 and other.person2 == self.person2

    def __hash__(self) -> int:
        return int(str(self.person1) + "0000000000" + str(self.person2))

    def __str__(self) -> str:
        return f"{self.person1=}, {self.person2=}, {self.timestamp=}"
 

def combineFiles():
    with open("src/data/higgs-activity_time.txt") as activity_file, open("src/data/higgs-social_network.edgelist") as social_file:
        activity = csv.reader(activity_file)
        social = csv.reader(social_file)

        tweets = set()

        for edge in activity:
            edge = edge[0].split(" ")
            tweets.add(Tweet(edge[0], edge[1], edge[2]))
        print(f"read activity: {len(tweets)}")

        for edge in social:
            edge = edge[0].split(" ")
            tweets.add(Tweet(edge[0], edge[1]))
        print(f"read social: {len(tweets)}")
        

        with open(f"src/data/preprocessed_{int(time.time())}.csv", "w", newline="") as file:
            data = csv.writer(file)
            data.writerows([i.person1, i.person2, i.timestamp] for i in tweets)


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



#combineFiles()
checkFile("src/data/preprocessed_1648560717.csv") #file is correct

        
        