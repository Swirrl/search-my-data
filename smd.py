import numpy as np
import pandas as pd
from scipy import linalg
from scipy.spatial import distance
from nltk.corpus import stopwords
import argparse
import re

# number of dimensions in word embedding vectors
embedding_length = 50 # see data/glove.6B.* for the options

class Index:
    """Builds a search index"""

    def __init__(self, embeddings, resources):
      self.embeddings = embeddings
      self.resources = resources
      self.r_vectors = list(map(self.calculate_vector, resources['label']))

    def tokenize(self, string, remove_stopwords = True):
      text = re.sub("[^a-zA-Z]"," ", string)
      words = text.lower().split()
      if remove_stopwords:
        stops = set(stopwords.words("english"))
        words = [w for w in words if not w in stops]
      return words
      
    def calculate_vector(self, string):
      v = np.zeros(embedding_length)
      for w in self.tokenize(string):
        if w.lower() in self.embeddings and w.lower() not in stopwords.words("english"):
          v += self.embeddings[w.lower()]
      v = v / linalg.norm(v)
      return v
      
    def distances(self, q_v):
      distances = map(lambda r_v: distance.cosine(q_v, r_v), self.r_vectors)
      return(list(distances))

    def search(self, query):
      query_v = self.calculate_vector(query)
      results = self.resources.copy()
      results['distance'] = self.distances(query_v)
      return(results.sort_values(by=['distance']))


if __name__ == '__main__':
  # parsing input arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('--query', type=str, default='booze', help='search query')
  parser.add_argument('--resources', type=str, default='data/resources.csv', help='resources to search through (csv with uri and label)')
  parser.add_argument('--embeddings', type=str, default="data/glove.6B." + str(embedding_length) + "d.txt", help='word embeddings')
  args = parser.parse_args()

  # read resources
  resources = pd.read_csv(args.resources)

  # read glove
  embeddings = {}
  with open(args.embeddings) as f:
    for line in f:    
      l = line.split()
      embeddings[l[0]] = list(map(float, l[1:]))
  
  # build search index
  index = Index(embeddings, resources)
  
  # calculate search results
  results = index.search(args.query)
  print(results)
  
