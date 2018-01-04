# Exploring community detection & sentiment analysis
Performing community detection and clustering using real-time social network data

The program extracts 500 tweets that mention PM of India @narendramodi using the search/tweets API. From these tweets, the program extracts 15 tweeters & information about their friends using the friends/ids API. 
For these 15 users, the program extracts tweets from their timelines.

## Community Detection
Using the data of PM Modi's 1st degree friends and 2nd degree friends, the program creates a social graph. The original graph is reduced to keep only friends who have a significant "friend" overlap with PM Modi (overlap is defined using Jaccard scores). A Jaccard threshhold of 0.1 is applied to the original graph and this reduces the number of nodes.

Community detection using Girvan Newmann algorithm is performed on the reduced graph. 

## Sentiment Analysis
The program downloads the AFINN lexicon to perform sentiment analysis of the tweets collected earlier. 
