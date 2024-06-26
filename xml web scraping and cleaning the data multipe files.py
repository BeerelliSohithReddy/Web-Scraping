import os
import pandas as pd
import numpy as np
import bs4 as bs
import urllib.request
import re
import spacy
import re,string,unicodedata
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

lem=WordNetLemmatizer()

os.chdir(r'D:\data science class\AI\xml web scraping\xml_many articles')

from glob import glob

path=r'D:\data science class\AI\xml web scraping\xml_many articles'
files = glob(os.path.join(path, "*.xml"))

import xml.etree.ElementTree as ET

clean_files=[]

for filename in files:
    tree = ET.parse(filename)
    root=tree.getroot()
    root=ET.tostring(root,encoding="utf8").decode("utf8")
    clean_files.append(root)

import bs4 as bs
import urllib.request
import re


    
def data_parsing(each_file):
    parsed_article = bs.BeautifulSoup(each_file,'xml')
    paragraphs = parsed_article.find_all('para')
    
    article_text=""
    
    for p in paragraphs:
        article_text+=p.text
        print(p.text)
        
    return article_text
data=[data_parsing(each_file) for each_file in clean_files]

# combining all data
from bs4 import BeautifulSoup
soup =BeautifulSoup(clean_files[0],'html.parser')
print(soup.prettify())
parsed_article=bs.BeautifulSoup(clean_files[0],'xml')
paragraphs=parsed_article.find_all('para')

def remove_stop_words(file):
    nlp=spacy.load("en_core_web_sm")
    punctuations = string.punctuation
    from nltk.corpus import stopwords
    stopwords = stopwords.words('english')
    SYMBOLS = " ".join(string.punctuation).split(" ") + ["-", "...", "”", "”"]
    stopwords = nltk.corpus.stopwords.words('english')+SYMBOLS
    
    doc = nlp(file, disable=['parser', 'ner'])
    tokens = [tok.lemma_.lower().strip() for tok in doc if tok.lemma_ != '-PRON-']
    tokens = [tok for tok in tokens if tok not in stopwords and tok not in punctuations]
    s=[lem.lemmatize(word) for word in tokens]
    tokens = ' '.join(s)
    
    article_text = re.sub(r'\[[0-9]*\]', ' ',tokens)
    article_text = re.sub(r'\s+', ' ', article_text)
        
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
    formatted_article_text = re.sub(r'\W*\b\w{1,3}\b', "",formatted_article_text)
  
    return formatted_article_text
    
clean_data=[remove_stop_words(file) for file in data]
all_words=' '.join(clean_data)

from wordcloud import WordCloud
import matplotlib.pyplot as plt
wordcloud=WordCloud(width=480,height=480,margin=0).generate(all_words)
plt.imshow(wordcloud,interpolation='bilinear')
plt.axis("off")
plt.margins(x=0,y=0)
plt.show()
