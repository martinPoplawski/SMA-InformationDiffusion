# SMA-InformationDiffusion
Social Media Analytics Project

## Tasks
Todo issue list in Project

Project structure can be adapted however you see fit. 

## Requirements
* pip install networkx 
* pip install matplotlib


* [Neo4j](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-neo4j-on-ubuntu-20-04)


## How to run Program
You have to run the program in the 'src' folder. 


*Preprocessing*: Add the multiple graphs and calculate edge weights. 



* python Main.py -loadAll 


*Sampling*: Sample the graph and create Communities: 



* python Main.py -sample [numberOfSampledNodes]


*Run* the program on a community (Number is the file number in src/data/Comms)

* python Main.py -c 8 -o loss 5 0 


*Possible optimization*


* loss - Stops once max Starting nodes or the improvement by adding nodes is too small 
  * -o loss [MaxNumberStartingNodes] [minLossImprovement]
* lossfast - Stops once max Starting nodes or the improvement by adding nodes is too small (only 1 iteration step in LTM) 
  * -o lossfast [MaxNumberStartingNodes] [minLossImprovement]
* costandgain - Stops once cost of adding node is bigger than gain of activating node 
  * -o costandgain [costOfAddingNodeToStartingSet] [GainOfActivatingNode] 
* percentage - Stops once x-percent of people have seen the tweet | -o percentage [percentToSeeTweet]"
