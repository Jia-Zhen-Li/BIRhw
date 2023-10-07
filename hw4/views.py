#!/usr/bin/python
# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from hw4.forms import Query
import nltk, re
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import *
from nltk.stem.snowball import SnowballStemmer
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from sklearn.feature_extraction.text import TfidfVectorizer


corpus=''


def index(request):
    return render(request,'index4.html')


# hw4
def show(request):
    global corpus
    all_results=[[0]*6 for i in range(50)]
    load_file()
    if request.method == 'POST':
        form = Query(request.POST)
        if form.is_valid():
            query = text_prepare(request.POST['query'])
            processed_corpus = [text_prepare(doc) for doc in corpus]
            # initialise TfidfVectorizer
            vectoriser = TfidfVectorizer()
            vectoriser2 = TfidfVectorizer(binary = True)
            vectoriser3 = TfidfVectorizer(sublinear_tf = True)
            # obtain weights of each term to each document in corpus (ie, tf-idf scores)
            tf_idf_scores = vectoriser.fit_transform(processed_corpus)
            feature_names = vectoriser.get_feature_names()
            tf_idf_scores2 = vectoriser2.fit_transform(processed_corpus)
            tf_idf_scores3 = vectoriser3.fit_transform(processed_corpus)
            tf_idf_scores_query = vectoriser.fit_transform([query])
            print(len(feature_names))
            similarity_score1=cosine_similarity(query,feature_names,tf_idf_scores_query,tf_idf_scores)
            similarity_score2=cosine_similarity(query,feature_names,tf_idf_scores_query,tf_idf_scores2)
            similarity_score3=cosine_similarity(query,feature_names,tf_idf_scores_query,tf_idf_scores3)
            for i in range(50):
                all_results[i][0]=similarity_score1[i][0]
                all_results[i][1]=similarity_score1[i][1]
                all_results[i][2]=similarity_score2[i][0]
                all_results[i][3]=similarity_score2[i][1]
                all_results[i][4]=similarity_score3[i][0]
                all_results[i][5]=similarity_score3[i][1]
            print(all_results)
            return render(request,'show.html',{'form':form,'all_results':all_results})
    else:
        form =  Query()
    return render(request,'show.html',{'form':form})


def read_file(path):
    f = open(path, "r", encoding='utf-8')
    file_data = f.read()
    f.close()
    return file_data

def load_file():
    global corpus
    file_data1 = read_file(path = "./hw4/pubmed_Meniere_204.txt")
    #print(file_data1)
    file_data2 = read_file(path = "./hw4/pubmed_depression_200.txt")
    #print(file_data2)
    file_data3 = read_file(path = "./hw4/pubmed_epilepsy_200.txt")
    #print(file_data3)
    corpus = file_data1.split('-'*90)[0:100] + file_data2.split('-'*90)[0:100] + file_data3.split('-'*90)[0:100]
    #print(len(corpus))

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]


REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^a-z #+_]')
STOPWORDS = set(stopwords.words('english'))

def text_prepare(text,stopwords=True,stem=True):  # 文字處理(移除標點符號、數字、stopwords)
  """
      text: a string
        
      return: modified initial string
  """
  # 轉小寫
  #print('yuanlai: ',text)
  text = text.lower()
  #print('lower: ',text)
  # 將REPLACE_BY_SPACE_RE 的符號換成空格號
  text = re.sub(REPLACE_BY_SPACE_RE,' ',text, count=0, flags=0)
  #print('re: ',text)
  # 將非BAD_SYMBOLS_RE的符號移除
  text = re.sub(BAD_SYMBOLS_RE,' ',text, count=0, flags=0)
  #print('bad: ',text)
  # 刪除stopwords & stem
  if(stopwords or stem):
    text_split = text.split()
    text=""
  if stopwords:
    for s in STOPWORDS:
      try:
        text_split=remove_values_from_list(text_split,s)
      except:
        continue
      #print(s,text_split)
    
  stemmer = SnowballStemmer('english') # stemmer
  if stem:
    for t in range(len(text_split)):
            text_split[t] = stemmer.stem(text_split[t])
  
  for t in text_split:
    text = text+t+' '
  #print(text)
  return text

def cosine_similarity(query,feature_names,tfidf_scores_query,tfidf_scores_documents):
    tfidf_doc = tfidf_scores_documents.toarray()
    tfidf_qur = tfidf_scores_query.toarray()
    length = len(tfidf_doc)
    score = {}
    for i in range(length):
        score[i] = 0
        for j in range(len(query.split())):
            item = query.split()[j]
            #print(item)
            try:
                index = feature_names.index(item)
                #print(feature_names.index(item))
            except:
                continue
            else:
                score[i] += tfidf_qur[0][j]*tfidf_doc[i][index]
    output = sorted(score.items(), key=lambda x:x[1],reverse=True)
    print(output)
    return output