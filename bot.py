#!/usr/bin/python
from twython import Twython
import sys
import csv
import random
import pandas as pd

#input is a file generated from:
#http://www.ncbi.nlm.nih.gov/pubmed?term=%22PloS%20one%22%5BJournal%5D
#exported as .csv
#easy to modify for any other journal

twitter = Twython("API KEY",
                  "API SECRET",
                  "ACCESS TOKEN",
                  "YOUR ACCESS TOKEN SECRET")

def onetitle(x,traindict, startingwords):
    words = x.split(' ')
    if len(words) < 4:
        return
    else:
        for wordindex in range(len(words)-2):
            if (words[wordindex],words[wordindex+1]) not in traindict:
                traindict[(words[wordindex],words[wordindex+1])] = [words[wordindex+2]]
            else:
                traindict[(words[wordindex],words[wordindex+1])].append(words[wordindex+2])
        if (words[-2],words[-1]) not in traindict:
            traindict[(words[-2],words[-1])] = [False]
        else:
            traindict[(words[-2],words[-1])].append(False)
        startingwords.append((words[0],words[1]))
        return
    
def makedict(file):
    x = pd.read_csv(file, error_bad_lines=False, usecols = ['Title'])
    x.reset_index(level=0,inplace=True)
    traindict={}
    startingwords=[]
    [onetitle(i, traindict, startingwords) for i in x['index']]
    return traindict,startingwords


def maketweet(dicttouse,startingwords):
    sentence=[]
    chosen = random.choice(startingwords)
    while chosen[1]:
        sentence = sentence + [chosen[0]]
        chosen = (chosen[1],random.choice(dicttouse[chosen]))
    sentence=sentence+[chosen[0]]
    return(" ".join(sentence))

if __name__ == "__main__":
    a, b = makedict(sys.argv[1])

    tweeted=0
    while tweeted==0:
        totweet=maketweet(a,b)
        if len(totweet)<141:
            twitter.update_status(status=totweet)
            print(totweet)
            tweeted=1
