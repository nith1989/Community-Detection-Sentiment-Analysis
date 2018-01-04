"""
collect.py
"""
# The program exracts 500 tweets that mention PM of India @narendramodi using the search/tweets API. 
# From these tweets, the program extracts 15 tweeters & information about their friends using the friends/ids API
# For these 15 users, the program extracts tweets from their timelines
# The tweets & friends data is stored into files

# Time taken: 30-40 seconds

# Required imports
from collections import Counter
from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx
import sys
import time
import re, os
from TwitterAPI import TwitterAPI
import pickle

# Authentication
consumer_key='FexaKBoJvI4PkwVRoneeJTqAX'
consumer_secret='QcbQ5fOHteRQrmZXmieqft7bdUBVZOK8xYuNmWQhnYzrzHsveG'
access_token='93624770-UyEh1gNxUd9bqNaDLfhkS5xmyni8U2H4poNIKLbi5'
access_token_secret='WeidtkZVk97BZXXAqKZhHyEs7QHlsYLCTNKgkQeX4dUEC'

# Function for connecting to Twitter with required credentials
def get_twitter():
    return TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)

# Function to sleep if rate limit error happens
def robust_request(twitter, resource, params, max_tries=5):
    for i in range(max_tries):
        request = twitter.request(resource, params)
        if request.status_code == 200:
            return request
        else:
            print('Rate limited %s \n will pause for 15 minutes before extracting again.' % request.text)
            sys.stderr.flush()
            time.sleep(61 * 15)

# Get Tweets about Indian PM Narendra Modi (500 tweets)
def get_mentions(twitter):
    mentions = []
    n_tweets=500
    while True:
        for r in robust_request(twitter, "search/tweets", {"q":'@narendramodi', "count": 100, "lang":'en'}):
            mentions.append(r)
            if len(mentions) % 100 == 0:
                print('%d tweets' % len(mentions))
            if len(mentions) >= n_tweets:
                break
        if len(mentions) >= n_tweets:
                break
    print('Fetched %d tweets' % len(mentions))
    return mentions          

# Get tweets of 15 users across 20 pages and add to a Pickle file
def get_tweets(twitter, users):
    tweets=[]
    loop_range = 20
    for user in range(len(users)):
        for i in range(1, loop_range):
            request = twitter.request('statuses/user_timeline',
                                      {'screen_name': users[user]['screen_name'], 'count': 200, 'include_rts': 'false', 'page':i})
            tweets.append(request)
    pickle.dump(tweets, open('nmodi_tweets.pkl', 'wb'))

# Get friends of the above 15 users
def get_friends(twitter, user):
    request = robust_request(twitter, "friends/ids", {"screen_name": user, "count": 500})
    friends = [friend for friend in request]
    return (sorted(friends))

# Get friends and add to a Pickle file
def add_all_friends(twitter, users, num):
    for user in range(len(users)):
        users[user]['friends'] = get_friends(twitter, users[user]['screen_name'])
        num += len(users[user]['friends'])
        pickle.dump(users, open('nmodi_frnds.pkl', 'wb'))
    return num

# Get information of 15 users (screen name)
def get_users(users_object):
    users = []
    temp_users=[]
    for tweet in range(len(users_object)):
        new_user = users_object[tweet]['user']['screen_name']
        if new_user not in temp_users and len(temp_users)<15:
            temp_users.append(new_user)
            user_list = {}
            user_list['screen_name'] = new_user
            users.append(user_list)
    return users

# Read the saved file
def read_file():
    return pickle.load(open('nmodi_tweets.pkl', 'rb'))

# Save each tweet as a separate text file
def create_files(tweets):
    directory='Tweets Data'
    if not os.path.exists(directory):
        os.makedirs(directory)
    val=0
    for i in tweets:
        for tweet in i:
            file = open(("Tweets Data/NarendaModi_" + str(val) + ".txt"), "w", encoding='utf8')
            file.write(tweet['text'])
            file.close
            val+=1
    return val

def main():
    
    # Get twitter connection
    twitter = get_twitter()
    
    # Get tweets object
    tweets_obj = get_mentions(twitter)
    
    # Get top users who post the above tweets
    users = get_users(tweets_obj)
    
    # Get these users friends
    num=0
    num_of_friends=len(users)
    num_of_friends += add_all_friends(twitter, users, num)
    
    # Get tweets of these users
    get_tweets(twitter, users)
    
    # Read the saved file & store it as object for further usage
    tweets = read_file()
    
    # Create different files for each tweet object
    num_of_tweets = create_files(tweets)
    
    # Summary of the files collected
    file = open("Collection Summary.txt", "w")
    file.write("Number of users collected: " + str(num_of_friends))
    file.write("\nNumber of messages collected: " + str(num_of_tweets))
    file.close()

if __name__=='__main__':
    main()