#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np

import unicodedata
import re
import os
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords


import acquire


# Define a function named basic_clean. It should take in a string and apply some basic text cleaning to it:  
#   
# Lowercase everything  
# Normalize unicode characters  
# Replace anything that is not a letter, number, whitespace or a single quote.  

# In[2]:


def basic_clean(string):
    string = string.lower()
    string = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    string = re.sub("[^A-Za-z0-9\s']",'',string)
    return string


# In[3]:


phrase = 'i have having had so much swim swam swimming swum'


# In[4]:


basic_clean(phrase)


# Define a function named tokenize. It should take in a string and tokenize all the words in the string.

# In[5]:


def tokenize(string):
    tokenizer = nltk.tokenize.ToktokTokenizer()
    return tokenizer.tokenize(string,return_str=True)
    


# In[6]:


tokenize(phrase)


# Define a function named stem. It should accept some text and return the text after applying stemming to all the words.

# In[62]:


def stem(string):
    ps = nltk.porter.PorterStemmer()
    stems = [ps.stem(w) for w in string.split()]
    return ' '.join(stems)


# In[49]:


stem(phrase)


# Define a function named lemmatize. It should accept some text and return the text after applying lemmatization to each word.

# In[50]:


def lemmatize(string):
    wnl = nltk.stem.WordNetLemmatizer()
    lems = [wnl.lemmatize(w) for w in string.split()]
    return ' '.join(lems)


# In[51]:


lemmatize(phrase)


# Define a function named remove_stopwords. It should accept some text and return the text after removing all the stopwords.
# 
# This function should define two optional parameters, extra_words and exclude_words. These parameters should define any additional stop words to include, and any words that we don't want to remove.

# In[27]:


def remove_stopwords(string,extra_words=None,exclude_words=None):
    stopword_list = stopwords.words('english')
    if extra_words != None:
        stopword_list.remove(extra_words)
    if exclude_words != None:  
        stopword_list.append(exclude_words)
    words = string.split()
    return ' '.join([w for w in words if w not in stopword_list])


# In[28]:


remove_stopwords(phrase)


# Use your data from the acquire to produce a dataframe of the news articles. Name the dataframe news_df.

# In[39]:


news_df = pd.DataFrame(acquire.scrape_one_page('sports'))


# In[40]:


news_df.head()


# In[70]:


news_df['clean'] = news_df.content.apply(basic_clean)


# In[72]:


news_df['stemmed'] = news_df.content.apply(stem)


# In[73]:


news_df['lemmatized'] = news_df.content.apply(lemmatize)


# In[74]:


news_df.head()


# In[ ]:




