"""
Author: Sam Bellenchia

03/17/29: Revisied
"""

from multiprocessing.pool import ThreadPool
from multiprocessing import Pool
from functools import lru_cache
from datetime import datetime
import requests
import time
import csv

threads = 2
url = 'https://api.pushshift.io/reddit/search/submission/?q=coronavirus&after={}&before=0s&sort_type=score&sort=desc&size=1000&fields=id,title,created_utc,subreddit'

# Cache data to avoid pickle error
@lru_cache(maxsize=256)

# Retrieve data using get request
def get_docs(url):
    try:
        docs = requests.get(url).json()['data']
        return docs
    except ValueError:
        return "ValueError"

    
# Index data dictionary
def get_attributes(doc):
    with ThreadPool(2) as p:
        results = p.map(lambda x: doc[x], ["id", "created_utc", "title", "subreddit"] )
        return results

    
# Map each document to the attribute function
def get_data(docs):
    with ThreadPool(2) as p:
        results = p.map(get_attributes, docs)
        return results

attributes = [["id", "created_utc", "title", "subreddit"]]

while __name__ == "__main__":


    docs = get_docs(url.format("30s"))

    data = get_data(docs)
    with open("data.csv", "wt") as f:
        writer = csv.writer(f)
        
        for row in data:
            writer.writerow(row)
            
    time.sleep(30)

    print(data)    