from multiprocessing.pool import ThreadPool
from functools import lru_cache
from datetime import datetime
import requests
import time
import csv
"""
Author: Sam Bellenchia
Github: github.com/schlam/sentiment-mining-tool


"""

# Cache data to avoid pickle error
#@lru_cache(maxsize=256)

# Format url for specific query
def get_url(topic,content="submission",after="60s",before="0s",sort_type="score",sort_how='desc',size=1000,features=("title","created_utc", "permalink", "score")):
    base = 'https://api.pushshift.io/reddit/search/{}/?q={}'.format(content,topic)
    query = '&after={}&before={}'.format(after, before)
    sort = '&sort_type={}&sort={}&size={}'.format(sort_type,sort_how,size)
    fields = '%s,'*len(features) % tuple(features)
    fields = '&fields={}'.format(fields[:-1])
    url = base + query + sort + fields
    return url

# Retrieve data using get request
def get_docs(url):
    try:
        docs = requests.get(url).json()['data']
        return docs
    except ValueError:
        return "ValueError"
    
# Index data dictionary
def get_attributes(doc):
    features=("title","created_utc", "permalink", "score")
    with ThreadPool(2) as p:
        results = p.map(lambda x: doc[x],features)
        return results
    
# Map each document to the attribute function
def get_data(docs):
    if docs==[]:
        return "null"
    with ThreadPool(2) as p:
        results = p.map(get_attributes, docs)
        return results

# Write data to file
def write_data(data, fname):
    if data=="null":
        return "Query returned no results. No data written to csv"
    with open(fname, "wt") as f:
        writer = csv.writer(f)
        writer.writerow(["title","created_utc", "permalink", "score"])
        for row in data:
            writer.writerow(row)
        f.close()
        return "Wrote data to {}".format(fname)