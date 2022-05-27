# SMA-InformationDiffusion
Social Media Analytics Project by Dana, Marco and Martin

## Requirements
* First you need to get the 'higgs-social_network.edgelist' file from [here](https://snap.stanford.edu/data/higgs-twitter.html) and save it in 'src/data' folder. 
This file was too big to upload it to git. 
* pip install networkx 
* pip install matplotlib
* pip install numpy
* pip install neo4j and [Neo4j](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-neo4j-on-ubuntu-20-04)
* [Gephi](https://gephi.org/users/download/)

## Steps to follow

On the github the preprocessed files are already available. Therefore for testing it isn't necessary to run -loadAll and -sample. The sample on the github is a random sample of 100k nodes and 900k edges. 

For testing just use -optimization and -visualization


## How to run Program
You have to run the program in the 'src' folder. Preprocessing is not necessary if you pull from this repository because the preprocessed graphs and communities are saved in csv files in src/data or src/data/Comms respectively 


*Preprocessing*: Add the multiple graphs and calculate edge weights. 



* python Main.py -loadAll 


*Sampling*: Sample the graph and create Communities: 



* python Main.py -sample [numberOfSampledNodes]


*Run* the program on a community (Number is the file number in src/data/Comms)

* python Main.py -c 8 -o loss 5 0 


*Possible optimization*


* loss - Stops once max Starting nodes or the improvement by adding nodes is too small 
  * -o loss [MaxNumberStartingNodes] [minLossImprovement]
  * proposed values: -o loss 5 0 
* lossfast - Stops once max Starting nodes or the improvement by adding nodes is too small (only 1 iteration step in LTM) 
  * -o lossfast [MaxNumberStartingNodes] [minLossImprovement]
  * proposed values: -o lossfast 5 0 
* costandgain - Stops once cost of adding node is bigger than gain of activating node 
  * -o costandgain [costOfAddingNodeToStartingSet] [GainOfActivatingNode] 
  * proposed values: -o costandgain 10 5
* percentage - Stops once x-percent of people have seen the tweet | -o percentage [percentToSeeTweet]"
  * proposed values: -o percentage 0.7


*Visualization* choose a second community for comparison (Number is the file number in src/data/Comms)

* python Main.py -visualization 15
