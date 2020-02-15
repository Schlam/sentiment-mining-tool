from time import sleep
import pandas as pd
import requests
from datetime import datetime
import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as SIA
import re

analyzer = SIA()

KEYWORD = "bitcoin"
SUBREDDITS = ['wallstreetbets', 'algotrading','thewallstreet','cryptocurrency','bitcoin']

#base query url
#maximum size is 1000, increasing will not change number of comments returned
#score threshold set to greater than 1 to avoid problems with normalizing sentiment
base_url = "https://api.pushshift.io/reddit/search/comment/" + \
            "?q={}&" + \
            "{}" + \
            "after={}&" + \
            "before={}&" + \
            "score=>1&" + \
            "sort_type=score&" + \
            "sort=desc&" + \
            "size=1000"

base_POST_url = "https://api.pushshift.io/reddit/search/submission/" + \
                "?q={}&" + \
                "{}" + \
                "after={}&" + \
                "before={}&" + \
                "score=>1&" + \
                "sort_type=score&" + \
                "sort=desc&" + \
                "size=1000"

#formats the desired subreddits to match REST query
def format_subreddit(sub):
    if sub == "all":
        return ""
    return "subreddit={}&".format(sub)

#converts unix time to string
def utc_to_str(utc_time):
    utc_time = int(utc_time)
    return datetime.utcfromtimestamp(utc_time).strftime('%Y/%m/%d')

#returns sentiment normalized by the posts score
def get_normalized_sentiment(comments):
    if len(comments) < 5:
        return 0 #ignore weeks with less than 10 mentions
    total_score, total_sent = 0, 0
    for comment in comments:
        body = comment.get('body', '')
        score = comment.get('score', 1)
        total_score += score
        total_sent += analyzer.polarity_scores(body)['compound'] * score
    #Normalized sentiment formula: total_sentiment / (total_comments * total_score)
    normalized_sentiment = total_sent / (len(comments) or 1) / (total_score or 1)
    return normalized_sentiment
#count the occurance of a keyword in each comment
def get_term_frequency(submissions):
  for submission in submissions:
    body = submission.get('body', '')
    return body.lower().count(KEYWORD)

#makes appropriate headers for given subreddits
def make_header(subreddits):
    header = ["Date"]
    header += ["/r/{}".format(sub) for sub in subreddits]
    return header

line = "_______________________________________________________________________"
if __name__ == "__main__":
    print(line+"\n\nThis program uses pushshift.io and vaderSentiment to mine relevant data from reddit.com\n")
    print("The chosen topic is {}, and the following subreddits are queried:\n  {}\n".format(KEYWORD,SUBREDDITS)+line)

    sub_queries = list(map(format_subreddit, SUBREDDITS))
    start_time = int(datetime(2014, 1, 1).strftime("%s"))
    max_time = int(datetime(2020, 1, 14).strftime("%s"))
    increment = 24 * 60 * 60 #Increment in 1 day intervals
    header = make_header(SUBREDDITS)
    full_data1 = [header]
    full_data2 = [header]

    while start_time < max_time:

        curr_row = [utc_to_str(start_time)]
        curr_row2 = [utc_to_str(start_time)]

        print("\n\nQuerying each subreddit for {} data on {}\n".format(KEYWORD,utc_to_str(start_time)))
        
        for subreddit in sub_queries:
            sleep(1)
            end_time = start_time + increment
            curr_url = base_url.format(KEYWORD, subreddit, start_time, end_time)
            try:
              if(requests.get(curr_url).json()['data'] == ([] or None)):
                print('    r/{} data unavailable'.format(subreddit[10:-1]))
                curr_row.append(0)
                curr_row2.append(0)
              else:
                print("    r/{} data AVAILABLE".format(subreddit[10:-1]))
                comments = requests.get(curr_url).json()['data']
                curr_row.append(get_normalized_sentiment(comments))
                curr_row2.append(get_term_frequency(comments))
            except ValueError:
              print('    ValueError')
              curr_row.append(0)
              curr_row2.append(0)

        full_data1.append(curr_row)
        full_data2.append(curr_row2)
        
        start_time = end_time
    
    fname1 = "./{}-sentiment14-20.csv".format(KEYWORD)
    with open(fname1, "wt") as f:
        writer = csv.writer(f)
        for row in full_data1:
            writer.writerow(row)


    fname2 = "./{}-count14-20.csv".format(KEYWORD)
    with open(fname2, "wt") as f:
        writer = csv.writer(f)
        for row in full_data2:
            writer.writerow(row)

print(line+'\nData aquisition was successful.\nThe following files have been writtem:\n\n{}\n{}'.format(fname1,fname2))


df1 = pd.read_csv('./bitcoin-sentiment14-20.csv')
df2 = pd.read_csv('./bitcoin-count14-20.csv')

print(line+'\n',df1.head(len(df1)),'\n'+line)
print(line+'\n',df2.head(len(df2)),'\n'+line)
