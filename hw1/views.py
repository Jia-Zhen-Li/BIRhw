from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from hw1.forms import UploadFileForm_counter, Get_Url_counter
from hw1.forms import UploadFileForm_zipf, Get_Url_zipf
import os, json, nltk, re
nltk.download('punkt')
from nltk.tokenize import sent_tokenize, RegexpTokenizer
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
#from hw1.functions import handle_uploaded_file
# Create your views here.

def index(request):
    return render(request,'index.html')

# hw1
def upload_file_counter(request): # 上傳檔案
    error_msg = ''
    file_text=''
    counts={'char':0,'word':0,'sentence':0}
    word_counts={}
    if request.method == 'POST':
        form = UploadFileForm_counter(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            file_text=readFile(request.FILES['file'])
            print(file_text)
            if(request.FILES['file'].name[-3:]=='xml'): #判斷是xml檔還是json
                scrape_texts = xml_file_parser(file_text)
            else:
                scrape_texts = json_file_parser(file_text)
            #print(scrape_texts)
            file_text = scrape_texts
            counts = counter(scrape_texts) 
            word_counts = prepared_words_counter(scrape_texts)        # bag_of_words
            word_counts = top_n_words(word_counts)                   # 前10多關鍵字
            file_text=find_keyword(file_text,request.POST['keyword']) # 在文本搜尋關鍵字
            #print(word_counts)
            error_msg='Upload Success'
            return render(request,'upload.html',{'form':form,'error_msg':error_msg,'file_text':file_text,'counts':counts,'word_counts':word_counts})
        error_msg = "Can't read the file!Please Try again."
    else:
        form = UploadFileForm_counter()
    return render(request,'upload.html',{'form':form,'error_msg':error_msg,'filetext':file_text,'counts':counts,'word_counts':word_counts})

def url_parser_counter(request): #使用url擷取文件
    error_msg = ''
    url_text=''
    counts={'char':0,'word':0,'sentence':0}
    word_counts={}
    if request.method == 'POST':
        form = Get_Url_counter(request.POST)
        get_url = request.POST['url']
        keyword=request.POST['keyword']
        #print('url',get_url )
        try:
            url_text=scrape(get_url)
        except:
            error_msg = "Can't find this url!Please Try again."
            return render(request,'url_parser.html',{'url_text':url_text,'form':form,'error_msg':error_msg,'counts':counts,'word_counts':word_counts})
        else:
            if(get_url.find('pubmed')!=-1): #判斷是pubmed還是twitter
                scrape_texts = xml_url_parser(url_text)
            else:
                scrape_texts = json_url_parser(url_text)
            counts=counter(scrape_texts)
            word_counts=prepared_words_counter(scrape_texts)
            url_text=scrape_texts
            url_text=find_keyword(scrape_texts,keyword)
            
        return render(request,'url_parser.html',{'url_text':url_text,'form':form,'error_msg':error_msg,'counts':counts,'word_counts':word_counts})
    else:
        form = Get_Url_counter()
    return render(request,'url_parser.html',{'url_text':url_text,'form':form,'error_msg':error_msg,'counts':counts,'word_counts':word_counts})


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
            print(file_text)
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
            keyword = textCheck(request.POST['keyword'],[x[0] for x in word_counts])
            print(keyword)
            print(request.POST['keyword'])
            file_text=find_keyword(file_text,keyword) # 在文本搜尋關鍵字
            #print(word_counts)
            error_msg='Upload Success'
            if(keyword != request.POST['keyword']):
                keyword_msg = 'Showing results for the following terms: '+'<b style=\"color:red\">' +keyword +'</b>'
            print(keyword_msg)
            return render(request,'test.html',{'form':form,'error_msg':error_msg,'keyword_msg':keyword_msg,'file_text':file_text,'pre_word_counts':pre_word_counts ,'all_word_counts':all_word_counts ,'pre_freq_list':pre_freq_list,'all_freq_list':all_freq_list,"ranks":str(int(request.POST['ranks'])+1)})
        error_msg = "Can't read the file!Please Try again."
    else:
        form = UploadFileForm_zipf()
    return render(request,'test.html',{'form':form,'error_msg':error_msg,'keyword_msg':keyword_msg})


def test(request):
    return render(request,'test.html')


# functions
# hw1
def handle_uploaded_file(f): # 儲存檔案
    save_path = os.path.join(settings.MEDIA_ROOT,'upload_files', f.name)
    print(save_path)
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


def scrape(url): # 從網頁擷取內容
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications") # 取消網頁中的彈出視窗
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    #driverPath=os.path.join(settings.BASE_DIR,'chromedrive','chromedriver.exe') #存放chromedriver的路徑
    driverPath='chromedriver'
    chrome = webdriver.Chrome(executable_path=driverPath,chrome_options=options) 
    #建立webdriver物件，(executable_path=瀏覽器驅動程式路徑，chrome_options=瀏覽器設定)。
    chrome.get(url)   # 前往要爬取的網頁網址
    time.sleep(2)
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
    soup = BeautifulSoup(url_text,'lxml')
    tweetText = soup.find_all('div',{'data-testid':'tweetText'})
    texts = ''
    for tt in tweetText:
        texts += tt.text+'\n'
        #print(tt.text)
        #print('==')
    return texts


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
    

def counter(text):
    counts={'char':0,'word':0,'sentence':0}
    #計算所有字元數、單字數、句子數
    #計算title字元數
    counts['char'] = 0
    counts['char']  += len(text)
    counts['char']  -= (text).count('\n')

    #計算title單字數
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    counts['word'] = len(tokens)

    #計算title句子數
    sentence = sent_tokenize(text)
    counts['sentence']= len(sentence)


    #print('chars number: ',char_num)  
    #print('words number: ',word_num)  
    #print('sentences number: ',sentence_num)  

    #print('sentence: ')
    #for sen in sentence:
        #print('==')
        #print(sen)

    return counts


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


# 不計算的字元與單字
REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
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
    print('no change',text.count(char))
    text=text.replace(char, "<br>")
    print('change',text.count(char))
    return text

# hw2
    
def text_prepare_have_stopwords(text):  # 文字處理(移除標點符號、數字、stopwords)
  """
      text: a string
        
      return: modified initial string
  """
  # 轉小寫
  text = text.lower()
  # 將REPLACE_BY_SPACE_RE 的符號換成空格號
  text = re.sub(REPLACE_BY_SPACE_RE,' ',text, count=0, flags=0)
  # 將BAD_SYMBOLS_RE的符號移除
  text = re.sub(BAD_SYMBOLS_RE,'',text, count=0, flags=0)

  return text

def word_freq_list(common_words): # freq_counts:[times,frequence]
    freq_counts=[[(i+1) for i in range(len(common_words))]]
    times=[]
    freq=[]
    all_counts=sum(c[1] for c in common_words)
    print("words")
    for cw in common_words:
        print(cw[0])
        times.append(cw[1])
        freq.append(cw[1]/all_counts)
    #print(freq_counts)
    freq_counts.append(times)
    freq_counts.append(freq)
    #print(freq_counts)
    return freq_counts

def textCheck(sentence,words_list):
    print(words_list)
    correct_words = sorted(words.words()+list(words_list))
    output=''
    for word in sentence.split():
        temp = [(edit_distance(word,w),w)
                for w in correct_words if w[0]==word[0]]
        #print(sorted(temp, key = lambda val:val[0])[0][1])
        print(sorted(temp, key = lambda val:val[0])[0][:10])
        output += sorted(temp, key = lambda val:val[0])[0][1] + ' '
    output = output[:-1] #去掉最後的' ' 
    return output