UPDATE 03/2020: merged the optimized querying functions with original program, all fucntions moved to pyshift.py. This allows for cool stuff like:

```
import pyshift as ps

# Generate api.pushshift url to query data from 
url = ps.get_url(
    topic="coronavirus", 
    after="2d", before="1d", 
    fields=('created_utc','subreddit','selftext','title'))

# Load documents from url
docs = ps.get_docs(url)

# Extract data from documents
data = ps.get_data(docs)

# Write data to 'data.csv'
write_data(data, "data.csv")


```


