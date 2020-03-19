UPDATE 03/2020: merged the optimized querying functions with original program, all fucntions moved to pyshift.py. This allows for cool stuff like:

```
import pyshift as ps

url = ps.get_url(
    topic="coronavirus", 
    after="2d", 
    before="1d", 
    fields = ('created_utc','subreddit','selftext','title'))

docs = ps.get_docs(url)

data = get_data(docs)

write_data(data, "data.csv")


```


UPDATE 03/2020: threadpooling.py runs in about a quarter of the time by utilizing the multiprocessing capability of ThreadPool, working on integrating into main program

UPDATE 03/2020: Added verbosity, made tool more flexible, and now writes preprocessed data to the .csv file.  

