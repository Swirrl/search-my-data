# Search My Data

Demonstration of information retrieval using word embeddings.

> Word “embeddings” are numerical representations of words or phrases. They are created by a machine-learning process that seeks to predict the probability of a certain word occurring given the context of other co-occurring words. Thus the vectors embed a representation of the contexts in which a word arises. This means they also encode semantic and syntactic patterns. It works a bit like a form of compression. Instead of words being arbitrarily long sequences of letters, they become fixed-length sequences of decimal numbers.

Taken from my blog post: [the mechanical poetry of semantic embeddings](http://www.infonomics.ltd.uk/blog/2017/10/18/mechanical-poetry/).

Embeddings that are closer together tend to share similar meanings. You can use the distance between embedding vectors as a measure of semantic similarity.

I've created a search index by calculating "sentence embeddings" for the dataset title, this is then compared against another embedding for the search query to retrieve the "closest" datasets.

## Demonstration

Along with traditional keyword matches, you can search via synonym. Although the term "booze" doesn't appear in any dataset titles it may be used to retreive relevant results.

```
>>> index.search('booze')
                                                   uri                                              label  distance
12   http://gss-data.org.uk/data/gss_data/health/hm...                                       Alcohol Duty  0.516165
187  http://gss-data.org.uk/data/gss_data/trade/hmr...                                   Alcohol Bulletin  0.555721
35   http://gss-data.org.uk/data/gss_data/health/nh...                              Alcohol Affordability  0.568875
195  http://gss-data.org.uk/data/gss_data/trade/hmr...                            HMRC Alcohol Duty Rates  0.581527
34   http://gss-data.org.uk/data/gss_data/health/df...              Reported drinking and driving (RAS51)  0.611130
```

Our use of language also captures some domain knowledge. Economic terminology can be understood:

```
>>> index.search('trade deficit')
                                                   uri                                              label  distance
14   http://gss-data.org.uk/data/gss_data/trade/ons...   Quarterly Balance of Payments: Trade in services  0.198862
193  http://gss-data.org.uk/data/gss_data/trade/ons...  Balance of Payments: Transactions with non-EU ...  0.199645
17   http://gss-data.org.uk/data/gss_data/trade/ons...  Trade in goods: country-by-commodity imports a...  0.200713
50   http://gss-data.org.uk/data/gss_data/trade/ons...  Trade in goods: all countries, seasonally adju...  0.202547
192  http://gss-data.org.uk/data/gss_data/trade/ons...   Balance of Payments: Trade in goods and services  0.212595

>>> index.search('value added')
                                                   uri                                              label  distance
184  http://gss-data.org.uk/data/gss_data/trade/ons...  GDP at current prices – real-time database (YBHA)  0.137355
178  http://gss-data.org.uk/data/gss_data/trade/ons...  Quarterly National Accounts, GDP – data tables...  0.167208
47   http://gss-data.org.uk/data/gss_data/trade/ons...  Individual country data (goods) on a monthly b...  0.171243
111  http://gss-data.org.uk/data/gss_data/disabilit...  Family Resources Survey: financial year 2017/1...  0.177647
52   http://gss-data.org.uk/data/gss_data/disabilit...  Family Resources Survey: financial year 2017/1...  0.177647
```

Or mental health terminology:

```
>>> index.search('depression')
                                                   uri                                              label  distance
97   http://gss-data.org.uk/data/gss_data/disabilit...  Co-occurring substance misuse and mental healt...  0.328545
75   http://gss-data.org.uk/data/gss_data/disabilit...  Co-occurring substance misuse and mental healt...  0.328545
90   http://gss-data.org.uk/data/gss_data/disabilit...  Co-occurring substance misuse and mental healt...  0.341216
68   http://gss-data.org.uk/data/gss_data/disabilit...  Co-occurring substance misuse and mental healt...  0.341216
89   http://gss-data.org.uk/data/gss_data/disabilit...  Co-occurring substance misuse and mental healt...  0.350118
```

The terms are combined naively. We're treating them as a so-called "bag of words" - i.e. the order and syntax are ignored.

```
>>> index.search('not migration')
                                                   uri                                              label  distance
1    http://gss-data.org.uk/data/gss_data/migration...            Migration between Scotland and Overseas  0.287836
9    http://gss-data.org.uk/data/gss_data/migration...  International Passenger Survey 4.02, main reas...  0.326788
2    http://gss-data.org.uk/data/gss_data/migration...                Local area migration indicators, UK  0.327138
4    http://gss-data.org.uk/data/gss_data/migration...  Long-term international migration 2.06, area o...  0.336822
7    http://gss-data.org.uk/data/gss_data/migration...  Long-term international migration 2.05, usual ...  0.369048
```

It's also possible to get results that might suggest a political opinion or normative judgements (which it does, in the sense that our use of language embodies these things).

```
>>> index.search('idiots')
                                                   uri                                              label  distance
83   http://gss-data.org.uk/data/gss_data/disabilit...  Homelessness in Scotland: Identified Support N...  0.805401
82   http://gss-data.org.uk/data/gss_data/disabilit...  Homelessness in Scotland: Applications: Suppor...  0.839132
126  http://gss-data.org.uk/data/gss_data/disabilit...                 Number of Starts, by age by gender  0.851695
134  http://gss-data.org.uk/data/gss_data/affordabl...           Live tables on affordable housing supply  0.851823
61   http://gss-data.org.uk/data/gss_data/disabilit...  Children living in long-term workless househol...  0.856884

>>> index.search('geniuses')
                                                   uri                                              label  distance
45   http://gss-data.org.uk/data/gss_data/housing/w...                           Social housing vacancies  0.837857
100  http://gss-data.org.uk/data/gss_data/disabilit...  Co-occurring substance misuse and mental healt...  0.849336
78   http://gss-data.org.uk/data/gss_data/disabilit...  Co-occurring substance misuse and mental healt...  0.849336
132  http://gss-data.org.uk/data/gss_data/disabilit...  Health state life expectancy, all ages, UK - H...  0.849851
77   http://gss-data.org.uk/data/gss_data/disabilit...  Co-occurring substance misuse and mental healt...  0.851486
```

Note that the results aren't particularly "close" to the search terms.

This is mostly a consequence of it being possible to calculate distance between any combination of terms in the vocabulary. All results are always returned, even if they're irrelevant. It might be possible to introduce a maximum distance threshold (so that completely irrelevant resources aren't included).


## Evaluation

This is powered purely by dataset labels at the moment. Adding descriptions or incorporating labels from the resources involved in the dataset (e.g. dimensions and codelists) would likely improve the relevance of the search results because there would be more context.

The script uses the smallest GloVe embeddings, having 50-dimensions. You can change the `embedding_length` constant to a higher value to get more "accurate" results, but the index will take longer to load. 50-dimensions is sufficient to demonstrate the potential.

## Installation

Download data: [GloVe](https://nlp.stanford.edu/projects/glove/) (word embeddings) and list of datasets (csv of uri and label) from gss-data.org.uk:

```
make all
```

Install python dependencies:

```
pip install -r requirements.txt
sudo python -m nltk.downloader -d /usr/local/share/nltk_data stopwords
```

## Usage

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
