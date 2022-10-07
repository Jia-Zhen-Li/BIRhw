from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from hw2.forms import UploadFileForm_zipf, Get_Url_zipf
import os, json, nltk, re
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import *
from nltk.stem.snowball import SnowballStemmer
from nltk.metrics.distance import edit_distance
from nltk.util import ngrams
nltk.download('words')
from nltk.corpus import words
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from random import choice
# Create your views here.

def index(request):
    return render(request,'index.html')


# hw2
def uploadfile_zipf(request):
    error_msg = ''
    keyword_msg = ''
    file_text=''
    pre_word_counts={}
    all_word_counts={}
    pre_freq_list = []
    all_freq_list = []
    if request.method == 'POST':
        form = UploadFileForm_zipf(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            file_text=readFile(request.FILES['file'])
            #print(file_text)
            if(request.FILES['file'].name[-3:]=='xml'): #判斷是xml檔還是json
                scrape_texts = xml_file_parser(file_text)
            else:
                scrape_texts = json_file_parser(file_text)
            #print(scrape_texts)
            file_text = scrape_texts
            word_counts = prepared_words_counter(scrape_texts,stopwords=False,stem=False)        # bag_of_words
            all_word_counts = top_n_words(word_counts,n=request.POST['ranks']) # 前n個關鍵字(未刪除stopwords)
            all_freq_list = word_freq_list(word_counts)
            word_counts = prepared_words_counter(scrape_texts) 
            pre_word_counts = top_n_words(word_counts,n=request.POST['ranks'])  # 前n個關鍵字(前處理)
            pre_freq_list = word_freq_list(word_counts)
            keyword = textCheck(request.POST['keyword'],[x[0] for x in prepared_words_counter(scrape_texts,stopwords=True,stem=False)]) #使用刪除stopwords、未stem的，偵錯輸入的keywords
            #print(keyword)
            #print(request.POST['keyword'])
            file_text=find_keyword(file_text,keyword) # 在文本搜尋關鍵字
            print(word_counts)
            error_msg='Upload Success'
            keyword_msg = keywordCheck(keyword,request.POST['keyword'])
            #print(keyword_msg)
            return render(request,'upload_zipf.html',{'form':form,'error_msg':error_msg,'keyword_msg':keyword_msg,'file_text':file_text,'pre_word_counts':pre_word_counts ,'all_word_counts':all_word_counts ,'pre_freq_list':pre_freq_list,'all_freq_list':all_freq_list,"ranks":str(int(request.POST['ranks'])+1)})
        error_msg = "Can't read the file!Please Try again."
    else:
        form = UploadFileForm_zipf()
    return render(request,'upload_zipf.html',{'form':form,'error_msg':error_msg,'keyword_msg':keyword_msg})

def url_zipf(request):
    error_msg = ''
    keyword_msg = ''
    file_text=''
    pre_word_counts={}
    all_word_counts={}
    pre_freq_list = []
    all_freq_list = []
    if request.method == 'POST':
        web_type = request.POST['webtype']
        form = Get_Url_zipf(request.POST)
        term = request.POST['term']
        size = request.POST['size']
        keyword=request.POST['keyword']
        #print('url',get_url )
        if web_type = 'PUBMED':
            scrape_texts=
            file_text = scrape_texts
            word_counts = prepared_words_counter(scrape_texts,stopwords=False,stem=False)        # bag_of_words
            all_word_counts = top_n_words(word_counts,n=request.POST['ranks']) # 前n個關鍵字(未刪除stopwords)
            all_freq_list = word_freq_list(word_counts)
            word_counts = prepared_words_counter(scrape_texts) 
            pre_word_counts = top_n_words(word_counts,n=request.POST['ranks'])  # 前n個關鍵字(前處理)
            pre_freq_list = word_freq_list(word_counts)
            keyword = textCheck(request.POST['keyword'],[x[0] for x in prepared_words_counter(scrape_texts,stopwords=True,stem=False)]) #使用刪除stopwords、未stem的，偵錯輸入的keywords
            #print(keyword)
            #print(request.POST['keyword'])
            file_text=find_keyword(file_text,keyword) # 在文本搜尋關鍵字
            #print(word_counts)
            error_msg='Upload Success'
            keyword_msg = keywordCheck(keyword,request.POST['keyword'])
            #print(keyword_msg)
            return render(request,'url_zipf.html',{'form':form,'error_msg':error_msg,'keyword_msg':keyword_msg,'file_text':file_text,'pre_word_counts':pre_word_counts ,'all_word_counts':all_word_counts ,'pre_freq_list':pre_freq_list,'all_freq_list':all_freq_list,"ranks":str(int(request.POST['ranks'])+1)})
    else:
        form = Get_Url_zipf()
    return render(request,'url_zipf.html',{'form':form,'error_msg':error_msg,'keyword_msg':keyword_msg})

def test(request):
    return render(request,'test.html')


#function

def handle_uploaded_file(f): # 儲存檔案
    save_path = os.path.join(settings.MEDIA_ROOT,'upload_files', f.name)
    #print(save_path)
    fp = open(save_path, 'wb+')
    for chunk in f.chunks():
        fp.write(chunk)
    fp.close()

def readFile(f): # 讀取檔案
    read_path = os.path.join(settings.MEDIA_ROOT,'upload_files', f.name)
    fp = open(read_path,'r+',encoding="utf-8")
    #print(fp.read())
    file_text = fp.read()
    fp.close()
    return file_text


def scrape(url,sleep = 0.001): # 從網頁擷取內容
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications") # 取消網頁中的彈出視窗
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driverPath=os.path.join(settings.BASE_DIR,'chromedrive','chromedriver.exe') #存放chromedriver的路徑
    #driverPath='chromedriver'
    chrome = webdriver.Chrome(executable_path=driverPath,chrome_options=options) 
    #建立webdriver物件，(executable_path=瀏覽器驅動程式路徑，chrome_options=瀏覽器設定)。
    chrome.get(url)   # 前往要爬取的網頁網址
    time.sleep(sleep)     # 等頁面加載完成
    return chrome.page_source

def json_file_parser(file_text): # 分析json檔內容
    parser=''
    while(1):
        try:
            parser = json.loads(file_text)
            #print('try')
        except: # 把多餘的逗號濾掉，避免error
            index = file_text.rfind(',')
            file_text = file_text[:index]+file_text[index+1:]
            #print('except')
        else:
            break
            #print('break')
    try:
        texts = parser[0]['Text'] # 將text擷取出來
    except:
        texts = parser[0]['tweet_text'] # 將text擷取出來

    return texts

def json_url_parser(url_text):
    text_list=[]
    tweet={'user':'','id':'','text':'','time':''}
    soup = BeautifulSoup(url_text,'lxml')
    tweetText = soup.find_all('div',{'data-testid':'tweetText'})
    tweetUser = soup.find_all('span',{'class':'css-901oao css-16my406 css-1hf3ou5 r-poiln3 r-bcqeeo r-qvutc0'})
    tweetID = soup.find_all('div',{'class':'css-901oao css-1hf3ou5 r-14j79pv r-18u37iz r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0'})
    tweetTime = soup.find_all('time')
    for i in range(len(tweetText)):
        tweet['user']=tweetUser[i].text
        print(tweetID[i].text)
        tweet['id']=tweetID[i].text
        tweet['text']=tweetText[i].text
        print(tweetTime[i])
        tweet['time']=tweetTime[i]['datetime']
        text_list.append(tweet)
    return text_list


def xml_file_parser(file_text):
    soup = BeautifulSoup(file_text,'xml')
    #print('====this:')
    #print(file_text)
    #print('13')
    #article_title = soup.find('ArticleTitle') #文章標題
    #print(article_title)
    abstract = soup.find_all('Abstract') #文章的Abstract
    texts=''
    #texts = (article_title.text) +'\n'
    #print(title.text)
    for a in abstract:
        if(a.text):
            texts += a.text+'\n'
        #print(a.text) 
    return texts

def xml_url_parser(url_text):
    soup = BeautifulSoup(url_text)
    #title = soup.find('h1',{'class':'heading-title'})
    abstract = soup.find_all('div',{'class':'abstract'})
    texts=''
    #texts = title.text+'\n'
    #print(title.text)
    for a in abstract:
        if(a.text):
            texts += a.text+'\n'
        #print(a.text) 
    return texts

def pubmed_search_scraper(term,size): #抓取pubmed搜尋到的文本
    page=1
    data_ids=''
    text_list=[]
    while(size>len(data_ids.split(','))):
        url='https://pubmed.ncbi.nlm.nih.gov/?term='+term+'&size=200&page='+str(page)
        search_page=scrape(url)
        soup = BeautifulSoup(search_page)
        data_ids += soup.find('div',{'class':'search-results-chunk results-chunk'})['data-chunk-ids']
        if(size<len(data_ids.split(','))):
            break
        data_ids += ','
        page += 1
    
    for i in range(size):
        id=data_ids.split(',')[i]
        url='https://pubmed.ncbi.nlm.nih.gov/'+id
        print(url)
        url_text = scrape(url)
        texts = xml_url_parser(url_text)
        text_list.append(texts)
        #print(texts) 
        #print('-----------------')
    return text_list

def twitter_search_scraper(term,size):
    text_list=[]
    url='https://twitter.com/search?q='+term
    #set the chrome_options
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-notifications')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driverPath=os.path.join('chromedrive','chromedriver.exe')
    #driverPath='chromedriver'
    # open the browser with chrome driver
    chrome = webdriver.Chrome(executable_path=driverPath,chrome_options=options) 
    chrome.get(url)
    time.sleep(1)

    while(size>len(text_list)):
        html_source = chrome.page_source
        tweet = json_url_parser(html_source,'lxml')
        text_list += tweet
        #scroll down until "size == len(text_list)"
        last_height = chrome.execute_script("return document.body.scrollHeight")
        chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(1)
        # Calculate new scroll height and compare with last scroll height
        new_height = chrome.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        if size<=len(text_list):
            break
        last_height = new_height
    return text_list

def prepared_words_counter(text,stopwords=True,stem=True):   # 計算所有單字出現次數及機率
    # (xml)計算words的數量
    stemmer = SnowballStemmer('english') # stemmer
    words_counts = {} # word dictionary
    title_pre = text_prepare(text,stopwords) # 前處理
    for t in title_pre.split():    # bag_of_words
        if stem:
            t = stemmer.stem(t)
        if(words_counts.get(t)):
            words_counts[t] += 1
        else:
            words_counts[t] = 1
    common_words = sorted(words_counts.items(), key=lambda x: x[1], reverse=True)
    return common_words


def find_keyword(text,keyword):
    #將keyword tag出來
    for key in keyword.split():
        color = "".join([choice("0123456789ABCDEF") for k in range(6)])
        matches = list(re.finditer(key.lower(),text.lower()))
        matches.reverse()
        for i in matches:
            text=text[:i.start()]+"<mark style='color:#"+ color +"'>"+ text[i.start():i.end()] + '</mark>' +text[i.end():]
    
    #將換行符replace成<br>
    char='\n'
    #print('no change',text.count(char))
    text=text.replace(char, "<br>")
    #print('change',text.count(char))
    return text

def top_n_words(common_words,n=10):        # 印出前10多單字
    keyword_counts = []
    #print(keyword_counts)
    words_class=sum(c[1] for c in common_words)
    if int(n) < len(common_words):
        #print('n= ',n)
        #print('len= ',len(common_words[0]),len(common_words))
        common_words = common_words[:int(n)]
    for i in range(len(common_words)):
        count=[0]*2
        count[0]=common_words[i][0]
        counts = common_words[i][1]
        count[1] = str(counts)+"("+str(int(counts/words_class*100))+"%)"
        keyword_counts.append(count)
        #print(common_words[i])
        #print(keyword_counts[i])
    return keyword_counts


def word_freq_list(common_words): # freq_counts:[times,frequence]
    freq_counts=[[(i+1) for i in range(len(common_words))]]
    times=[]
    freq=[]
    all_counts=sum(c[1] for c in common_words)
    #print("words")
    for cw in common_words:
        #print(cw[0])
        times.append(cw[1])
        freq.append(cw[1]/all_counts)
    #print(freq_counts)
    freq_counts.append(times)
    freq_counts.append(freq)
    #print(freq_counts)
    return freq_counts


# 不計算的字元與單字
REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_-]')
STOPWORDS = set(stopwords.words('english'))

def text_prepare(text,stopwords=True):  # 文字處理(移除標點符號、數字、stopwords)
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
  # 將BAD_SYMBOLS_RE的符號移除
  text = re.sub(BAD_SYMBOLS_RE,'',text, count=0, flags=0)
  #print('bad: ',text)
  # 刪除stopwords
  if stopwords:
    text_split = text.split()
    text=""
    for t in text_split:
        if(not(t in STOPWORDS)):
            text = text+t+' '
    text = text[:-1] #將最後的空格刪除
  #print(text)
  return text

def textCheck(sentence,words_list):
    #print(words_list)
    correct_words = sorted(words.words()+list(words_list))
    output=''
    for word in sentence.split():
        temp = [(edit_distance(word,w),w)
                for w in correct_words if w[0]==word[0]]
        #print(sorted(temp, key = lambda val:val[0])[0][1])
        #print(sorted(temp, key = lambda val:val[0])[0][:10])
        output += sorted(temp, key = lambda val:val[0])[0][1] + ' '
    output = output[:-1] #去掉最後的' ' 
    return output


def keywordCheck(keywords,insert):   # 若user輸入有誤，紅標提醒錯誤字。
    keyword_msg = 'Showing results for the following terms: '
    key = keywords.split()
    ins = insert.split()
    f=0
    for i in range(len(key)):
        if(key[i] != ins[i]):
            keyword_msg += '<b style=\"color:red\"> ' + key[i] +'</b>'
            f +=1
        else:
            keyword_msg += '<font style=\"color:gray\"> ' + key[i] +'</font>'
    if f==0:
        keyword_msg = ''
    return keyword_msg