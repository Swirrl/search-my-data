# Search My Data

Demonstration of information retrieval using word embeddings.

Download dataa: GloVe (word embedding) and list of datasets (csv of uri and label) from gss-data.org.uk:

```
make all
```

Install dependencies:

```
pip install -r requirements.txt
sudo python -m nltk.downloader -d /usr/local/share/nltk_data stopwords
```

Run script:

```
python smd.py --query "Booze stats"
```

Results are presented in ascending order of distance from the query (i.e. lowest distance means more relevant).

Since it takes a little while to load up all the embeddings into the search index, instead of calling the script from your shell you might prefer to start an interactive session:

```
python -i smd.py
```

This will execute a search for the default query, "booze", then drop you into a repl where you can explore further by searching the index with your own queries e.g.:

```
index.search('poison')
```

This is powered purely by dataset labels at the moment. Adding descriptions or incorporating labels from the resources involved in the dataset (e.g. dimensions and codelists) would likely improve the relevance of the search results.

The script uses the smallest GloVe embeddings, having 50-dimensions. You can change the `embedding_length` constant to a higher value to get more "accurate" results, but the index will take longer to load. 50-dimensions is sufficient to demonstrate the potential.
