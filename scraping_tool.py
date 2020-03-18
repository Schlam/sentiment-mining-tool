'''
Author: Sam Bellenchia
Last Revised: 03/12/20

-- The following code searches reddit for comments/submissions containing a specified keyword
-- and analyzes the sentiment intensity of the containing text, then writes that data to a 
-- specified .csv file  

NOTE: !pip install vaderSentiment to run this code

'''
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
from datetime import datetime
import numpy as np
import requests
import time
import csv
import sys

FILENAME       =   "_sentiment.csv"     # Designate filename to write data into
CONTENT_TYPE   =   "submission"         # Choose "submission" or "comment"
KEYWORD        =   "tesla"              # Choose keyword to filter text by
DIRECTORY      =   "./"                 # Set directory to write file into
RANGE          =   365                  # How many days to extend the query
SUBREDDITS     =   []                   # Leave empty to search all subreddits
SLEEP_TIME     =   0                    # Time to pause between requests

# Lambda function to contain long if/else construct
date_format = lambda a: "{}-0{}-0{}".format(a.year, a.month, a.day) if( a.month < 10 and a.day < 10) else "{}-0{}-{}".format(a.year, a.month, a.day) if( a.month < 10 and a.day >= 10) else "{}-{}-0{}".format(a.year, a.month, a.day) if( a.month >= 10 and a.day < 10) else "{}-{}-{}".format(a.year, a.month, a.day)

# Convert UTC time to YYYY-MM-DD format
def format_date(item):

  a = datetime.date(datetime.fromtimestamp(item))
  return date_format(a)

# Analyzes sentiment values from each document and returns a daily total
def aggregate(documents, content, subreddit):
    frequency = len(documents) 
    total = np.zeros(4)    
    attribute = 'body' if content == 'comment' else 'selftext'
    for doc in documents:
        if doc['selftext'] == "":
            frequency -= 1
        else:
            text, utc = doc[attribute], doc['created_utc']
            sent = analyzer.polarity_scores(text)     
            formatted_date = format_date(utc) 
            total += np.array([sent['pos'],sent['neg'],sent['neu'],sent['compound']])

    data = [formatted_date, frequency] + [val for val in total]
    
    if subreddit:
        data += [subreddit]
    
    return data


f = open(DIRECTORY+KEYWORD+FILENAME, "wt")
writer = csv.writer(f)
attribute = 'body' if CONTENT_TYPE == 'comment' else 'selftext'
for day in range(1,RANGE):
    time.sleep(SLEEP_TIME)
    if SUBREDDITS == []:
        
        # Format the pushshift url according to the query 
        base = '{}/?q={}&after={}d&before={}d'.format(CONTENT_TYPE, KEYWORD, RANGE - day, RANGE - day - 1)        
        URL = 'https://api.pushshift.io/reddit/search/{}&sort_type=score&sort=desc&size=1000&fields=selftext,created_utc'.format(base)
        docs = requests.get(URL).json()['data']
        
        # Write data to file
        row = aggregate(docs, CONTENT_TYPE, subreddit=None)
        writer.writerow(row)

    else:  
        for SUB in SUBREDDITS:
            base = '{}/?q={}&subreddit={}&after={}d&before={}d'.format(CONTENT_TYPE, KEYWORD, SUB, RANGE - day, RANGE - day - 1)        
            URL = 'https://api.pushshift.io/reddit/search/{}&sort_type=score&sort=desc&size=1000&fields=selftext,created_utc'.format(base)
            docs = requests.get(URL).json()['data']
            row = aggregate(docs, CONTENT_TYPE, SUB)
            writer.writerow(row)

    print("Day {}/{}, {} {}s".format(day, RANGE, len(docs), CONTENT_TYPE))
