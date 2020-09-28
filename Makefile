data:
	mkdir $@

data/glove.6B.50d.txt: data
	curl -L https://nlp.stanford.edu/data/glove.6B.zip -o data/glove.6B.zip
	unzip data/glove.6B.zip -d data/

data/resources.csv: data
	curl -H 'Accept: text/csv' --data-urlencode "query@data/select-labels.sparql" http://gss-data.org.uk/sparql -o $@

all: data/glove.6B.50d.txt data/resources.csv 
