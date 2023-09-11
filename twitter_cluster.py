# -*- coding: utf-8 -*-
"""Twitter cluster.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18aJZQNjCMYO_JoUnsV1kmhKBy3XCKbaF
"""

pip install datasets gensim

from datasets import list_datasets

available_datasets = list_datasets()
twitter_datasets = [ds for ds in available_datasets if "twitter" in ds.lower()]

print(twitter_datasets)

from datasets import load_dataset

try:
    btc_dataset = load_dataset('strombergnlp/broad_twitter_corpus')
    print("Broad Twitter Corpus dataset loaded successfully!")
except FileNotFoundError:
    print("Broad Twitter Corpus dataset not found!")

from datasets import load_dataset
from gensim import corpora, models
from gensim.parsing.preprocessing import STOPWORDS, strip_punctuation
from collections import defaultdict
import re

# Load Broad Twitter Corpus dataset
def load_btc_dataset():
    dataset = load_dataset('strombergnlp/broad_twitter_corpus')
    return [' '.join(tokens) for tokens in dataset["train"]["tokens"]]

# Preprocess the data
def preprocess_data(data):
    # Remove URLs
    data = [re.sub(r'http\S+', '', text) for text in data]

    # Remove words of length 2 or less, which will handle the short placeholders
    texts = [[word for word in strip_punctuation(document.lower()).split() if word not in STOPWORDS and len(word) > 2]
             for document in data]

    # Remove words that only appear once
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    texts = [[token for token in text if frequency[token] > 1]
             for text in texts]

    return texts

# Cluster data using LDA
def cluster_data(data):
    texts = preprocess_data(data)

    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    # Increase the number of passes
    lda = models.LdaModel(corpus, id2word=dictionary, num_topics=10, passes=15)
    return lda.print_topics(num_words=5)

# Load data
tweets = load_btc_dataset()

# Cluster and print topics
topics = cluster_data(tweets)
for topic in topics:
    print(topic)