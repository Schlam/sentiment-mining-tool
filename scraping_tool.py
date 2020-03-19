from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from multiprocessing.pool import ThreadPool
import pyshift as ps
import numpy as np
import requests
import csv
'''
Author: Sam Bellenchia
Last Revised: 03/18/20

~~~
This tool relies heavily on the Pushshift API and vaderSentiment analysis tools

API documentation found here: 
github.com/pushshift/api

Original code was based on a repo found here:
github.com/ckw017/pushshift-nlp

Sentiment analyser found here:
github.com/vaderSentiment

'''


KEYWORD = "coronavirus"
RANGE = 7

def get_sentiment(docs):
    analyzer = SentimentIntensityAnalyzer()
    with ThreadPool(4) as tp:
        results = tp.map(analyzer.polarity_scores, docs)
        return results

text_data = []
for i in range(1,RANGE):
    query_url = ps.get_url(
        topic = KEYWORD, 
        before = "{}d".format(i-1), 
        after = "{}d".format(i),
        features = ("created_utc","selftext", "title", "score"))

    docs = ps.get_docs(query_url)
    text_data.extend(ps.get_data(docs))

ps.write_data(data, KEYWORK+"_raw_data.csv")

sent_data = get_sentiment(text_data)

ps.write_data(data, KEYWORK+"_sentiment_data.csv")
