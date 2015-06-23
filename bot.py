#!/usr/bin/python
from twython import Twython
import sys
import csv
import random

#input is a file generated from:
#http://www.ncbi.nlm.nih.gov/pubmed?term=%22PloS%20one%22%5BJournal%5D
#exported as .csv
#easy to modify for any other journal

traindict={}
startingwords=[]

twitter = Twython("API KEY",
                  "API SECRET",
                  "ACCESS TOKEN",
                  "YOUR ACCESS TOKEN SECRET")

def makedict(file):
  with open(file, 'rt',encoding="utf-8") as csvfile:
     spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
     for row in spamreader:
         words=row[0].split(sep=" ")
         if len(words)<4:
             continue
         for wordindex in range(len(words)-2):
             if (words[wordindex],words[wordindex+1]) not in traindict:
                    traindict[(words[wordindex],words[wordindex+1])] = list()
             traindict[(words[wordindex],words[wordindex+1])].append(words[wordindex+2])
         if (words[-2],words[-1]) not in traindict:
             traindict[(words[-2],words[-1])] = list()
         traindict[(words[-2],words[-1])].append(False)
         startingwords.append((words[0],words[1]))
  return(traindict,startingwords)


def maketweet(dicttouse,startingwords):
    sentence=[]
    chosen = random.choice(startingwords)
    while chosen[1]:
        sentence = sentence + [chosen[0]]
        chosen = (chosen[1],random.choice(dicttouse[chosen]))
    sentence=sentence+[chosen[0]]
    return(" ".join(sentence))


a, b = makedict(sys.argv[1])

tweeted=0
while tweeted==0:
    totweet=maketweet(a,b)
    if len(totweet)<141:
        twitter.update_status(status=totweet)
        print(totweet)
        tweeted=1
