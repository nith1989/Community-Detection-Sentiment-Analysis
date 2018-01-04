"""
classify.py
"""

# The program uses lexicon based approach to classify the sentiments of the tweets collected earlier

# Time taken: 30-40 seconds

# Loading required libraries
import re
import numpy as np
import pickle
import os

# Read previously loaded file with tweets
def read_file():
    return pickle.load(open('nmodi_tweets.pkl', 'rb'))

# Tokenization for tweets
def tokenize(t):
    # Remove mentions, URLs & convert to words
    text = t.lower()
    text = re.sub('@\S+', ' ', text)  
    text = re.sub('http\S+', ' ', text) 
    return re.findall('[A-Za-z]+', text) 

# Download the AFINN lexicon
def download_afinn():
    from collections import defaultdict
    from io import BytesIO
    from zipfile import ZipFile
    from urllib.request import urlopen

    url = urlopen('http://www2.compute.dtu.dk/~faan/data/AFINN.zip')
    zipfile = ZipFile(BytesIO(url.read()))
    afinn_file = zipfile.open('AFINN/AFINN-111.txt')
    afinn = dict()

    for line in afinn_file:
        parts = line.strip().split()
        if len(parts) == 2:
            afinn[parts[0].decode("utf-8")] = int(parts[1])
    return afinn

# Classify sentiment as positive or negative
def afinn_sentiment2(terms, afinn, verbose=False):
    pos = 0
    neg = 0
    for t in terms:
        if t in afinn:
            if afinn[t] > 0:
                pos += afinn[t]
            else:
                neg += -1 * afinn[t]
    return pos, neg

# Get all files from a specific path
def get_files(path):
    text_files = [os.path.join(path,file) for file in os.listdir(path) if file.endswith('.txt')]
    return sorted(text_files)

# Read and tokenize each document
def read_n_tokenize(train_docs):
    if (isinstance(train_docs, list) == False):
        train_docs = train_docs.tolist()
    new_list = []
    tweets = []
    for e in train_docs:
        file = open(e, 'r', encoding='utf8')
        new_tweet = str(file.read())
        tweets.append(new_tweet)
        new_list.append(tokenize(new_tweet))

    return new_list, tweets

# Classify the sentiment in these tweets
def classify(new_list, tweets):
    positives = []
    negatives = []
    new_path = 'Classified'
    afinn=download_afinn()
    val = 0
    for token_list, tweet in zip(new_list, tweets):
        pos, neg = afinn_sentiment2(token_list, afinn)
        if pos > neg:
            positives.append((tweet, pos, neg))
        elif neg > pos:
            negatives.append((tweet, pos, neg))
    file = open("Classification Summary.txt", "w", encoding='utf8')
    file.write("Number of instances per class found: ")
    file.write("\nPositive Class: "+ str(len(positives)))
    file.write("\nNegative Class: "+ str(len(negatives)))
    file.write("\n\nOne example from each class:")
    file.write("\nPositive Class: \n"+ str(sorted(positives, key=lambda x: x[1], reverse=True)[:1]))
    file.write("\nNegative Class: \n"+ str(sorted(negatives, key=lambda x: x[2], reverse=True)[:1]))
    file.close

def main():
    path = 'Tweets Data/'
    train_docs = get_files(path)
    new_list, tweets = read_n_tokenize(train_docs)
    classify(new_list, tweets)

if __name__=='__main__':
    main()   
 