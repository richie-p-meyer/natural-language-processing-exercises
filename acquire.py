#!/usr/bin/env python
# coding: utf-8

# In[117]:


import pandas as pd
import numpy as np

import requests
from bs4 import BeautifulSoup

import os
import json


# In[25]:


urls = ['https://codeup.com/tips-for-prospective-students/coding-bootcamp-or-self-learning/',  
'https://codeup.com/data-science/become-a-data-scientist/',  
'https://codeup.com/employers/hiring-tech-talent/',  
'https://codeup.com/cloud-administration/cap-funding-options/',  
'https://codeup.com/dallas-info/it-professionals-dallas/']  

headers = {'User-Agent': 'Codeup Data Science'} 


# In[32]:


response = requests.get(urls[2],headers=headers)


# In[33]:


soup = BeautifulSoup(response.text,'html.parser')


# In[34]:


soup.title.string


# In[23]:


soup.prettify()


# In[36]:


url = 'https://codeup.com/blog/'
response = requests.get(url,headers=headers)
soup = BeautifulSoup(response.text,'html.parser')


# In[45]:


read_more = soup.select('.more-link')


# In[56]:


hrefs = [a['href'] for a in read_more]


# In[57]:


hrefs


# In[58]:


url = hrefs[0]
response = requests.get(url,headers=headers)
soup = BeautifulSoup(response.text,'html.parser')


# In[60]:


soup.title.string


# In[89]:


soup.find_all('span')


# In[68]:


a = soup.find_all('p')


# In[75]:


a[4].text


# In[83]:


soup.p


# In[100]:



#Define headers
headers = {'User-Agent': 'Codeup Data Science'}


# In[106]:


#Scrape blog homepage for links
url = 'https://codeup.com/blog/'

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.content, 'html.parser')

more_links = soup.find_all('a', class_='more-link')

more_links


# In[107]:


#Extract the links into something I can use
links_list = [link['href'] for link in more_links]

links_list


# In[109]:


#Make a request
response = requests.get('https://codeup.com/codeup-news/panelist-spotlight-4/', headers=headers)


# In[110]:


#Create the soup and investigate
soup = BeautifulSoup(response.content, 'html.parser')
example = soup.find('h1')
example.text


# In[111]:


#Access the date published
example2 = soup.find('span', class_='published')
example2.text


# In[112]:


#Access the article content
example3 = soup.find('div', class_='entry-content')
example3.text


# In[114]:


#Loop through the links to collect the relevant information from the blog posts
article_info = []

for link in links_list:
    
    response = requests.get(link, headers=headers)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    info_dict = {'title': soup.find('h1').text,
                 'link': link,
                 'date_published': soup.find('span', class_='published').text,
                 'content': soup.find('div', class_='entry-content').text.strip()}
    
    article_info.append(info_dict)
    
article_info[0]   


# In[ ]:





# In[125]:


#Create a function to collect the information and cache it as a json file
def get_blog_articles(article_list):
    
    file = 'blog_posts.json'
    
#     if os.path.exists(file):
        
#         with open(file) as f:
        
#             return json.load(f)
    
    headers = {'User-Agent': 'Codeup Data Science'}
    
    article_info = []
    
    for article in article_list:
        
        response = requests.get(article, headers=headers)
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        info_dict = {'title': soup.find('h1').text,
                     'link': article,
                     'date_published': soup.find('span', class_='published').text,
                     'content': soup.find('div', class_='entry-content').text}
    
        article_info.append(info_dict)
        
    with open(file, 'w') as f:
        
        json.dump(article_info, f)
        
    return article_info    


# In[126]:


#Run my function to make sure it works!
article_info = get_blog_articles(links_list)


# In[127]:


article_info[0]


# In[130]:


#Define a function to scrape articles from one topic
def scrape_one_page(topic):
    
    base_url = 'https://inshorts.com/en/read/'
    
    response = requests.get(base_url + topic)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    titles = soup.find_all('span', itemprop='headline')
    
    summaries = soup.find_all('div', itemprop='articleBody')
    
    summary_list = []
    
    for i in range(len(titles)):
        
        temp_dict = {'category': topic,
                     'title': titles[i].text,
                     'content': summaries[i].text}
        
        summary_list.append(temp_dict)
        
    return summary_list   


# In[131]:


#Test my function on the business page
business_test = scrape_one_page('business')
business_test[0]


# In[132]:


#Define a function that will scrape information about an array of topics
def get_news_articles(topic_list):
    
    file = 'news_articles.json'
    
    if os.path.exists(file):
        
        with open(file) as f:
            
            return json.load(f)
    
    final_list = []
    
    for topic in topic_list:
        
        final_list.extend(scrape_one_page(topic))
        
    with open(file, 'w') as f:
        
        json.dump(final_list, f)
        
    return final_list    


# In[133]:


#Test my function!
topics = ['business', 'sports', 'technology', 'entertainment']

final_list = get_news_articles(topics)
final_list[0]


# In[134]:


#Turn it into a dataframe!
final_df = pd.DataFrame(final_list)
final_df.head()


# In[ ]:




