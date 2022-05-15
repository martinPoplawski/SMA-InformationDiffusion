import csv  
import time
import Config 
from Helpers import print, progress


class Tweet:
    person1: int
    person2: int
    timestamp: int
    weight = 1

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
        print(f"read activity: {len(tweets.tweets)}")
        
        print("reading social")
        for i, edge in enumerate(social):
            edge = edge[0].split(" ")
            tweets.add(Tweet(edge[0], edge[1]))                          
            progress(i, 14855841, steps=10000) 
        print(f"read social: {len(tweets.tweets)}")
        
        filename = f"preprocessed_{int(time.time())}.csv"
        with open(f"src/data/{filename}", "w", newline="") as file:
            data = csv.writer(file)
            print(f"writing to csv {filename}")
            data.writerow(["person1", "person2", "weight", "timestamp"])
            for i, tweet in enumerate(tweets.tweets):
                data.writerow([tweet.person1, tweet.person2, tweet.weight, tweet.timestamp])
                progress(i, len(tweets.tweets), steps=1000)            



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


if __name__ == "__main__":
    Config.verbose = True
    combineFiles()

#combineFiles()
#checkFile("src/data/preprocessed_1648560717.csv") #file is correct

        
        