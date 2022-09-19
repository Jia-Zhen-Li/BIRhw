from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from hw1.forms import UploadFileForm, Get_Url
#from hw1.models import Url
import os, json, nltk, re
nltk.download('punkt')
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import *
from nltk.stem.snowball import SnowballStemmer
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
#from hw1.functions import handle_uploaded_file
# Create your views here.

def index(request):
    return render(request,'index.html')

def upload_file(request): # 上傳檔案
    error_msg = ''
    file_text=''
    counts={'char':0,'word':0,'sentence':0}
    word_counts={}
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        #print('1')
        if form.is_valid():
            #print('2')
            handle_uploaded_file(request.FILES['file'])
            #print('3')
            file_text=readFile(request.FILES['file'])
            print(file_text)
            if(request.FILES['file'].name[-3:]=='xml'): #判斷是xml檔還是json
                scrape_texts = xml_file_parser(file_text)
            else:
                scrape_texts = json_file_parser(file_text)
            #print(scrape_texts)
            file_text = scrape_texts
            counts = counter(scrape_texts)
            word_counts = prepared_words_counter(scrape_texts)
            file_text=find_keyword(file_text,request.POST['keyword'])
            print(word_counts)
            error_msg='Upload Success'
            return render(request,'upload.html',{'form':form,'error_msg':error_msg,'file_text':file_text,'counts':counts,'word_counts':word_counts})
        #print('4')
        error_msg = "Can't read the file!Please Try again."
    else:
        form = UploadFileForm()
    return render(request,'upload.html',{'form':form,'error_msg':error_msg,'filetext':file_text,'counts':counts,'word_counts':word_counts})

def url_parser(request): #使用url擷取文件
    error_msg = ''
    url_text=''
    counts={'char':0,'word':0,'sentence':0}
    word_counts={}
    if request.method == 'POST':
        form = Get_Url(request.POST)
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
        #print('4')
        error_msg = 'Error!Please Try again.'
    else:
        form = Get_Url()
    return render(request,'url_parser.html',{'url_text':url_text,'form':form,'error_msg':error_msg,'counts':counts,'word_counts':word_counts})

def show_counter(request):
    return None

# functions
def handle_uploaded_file(f): # 儲存檔案
    #print('6')
    save_path = os.path.join(settings.MEDIA_ROOT,'upload_files', f.name)
    print(save_path)
    #print('7')
    fp = open(save_path, 'wb+')
    #print('8')
    for chunk in f.chunks():
        fp.write(chunk)
    fp.close()

def readFile(f): # 讀取檔案
    #print('9')
    read_path = os.path.join(settings.MEDIA_ROOT,'upload_files', f.name)
    #print('10')
    fp = open(read_path,'r+',encoding="utf-8")
    #print('11')
    #print(fp.read())
    file_text = fp.read()
    return file_text


def scrape(url): # 從網頁擷取內容
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
    texts = parser[0]['Text'] # 將text擷取出來
    return texts

def json_url_parser(url_text):
    soup = BeautifulSoup(url_text)
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


def prepared_words_counter(text):
    # (xml)計算words的數量
    stemmer = SnowballStemmer('english') # stemmer
    words_counts = {} # word dictionary
    keyword_counts = []
    title_pre = text_prepare(text) #前處理
    for t in title_pre.split():
        t = stemmer.stem(t)
        if(words_counts.get(t)):
            words_counts[t] += 1
        else:
            words_counts[t] = 1
    words_class=len(words_counts)
    # 印出前十多的words
    common_words = sorted(words_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    #print(common_words)
    for i in range(len(common_words)):
        count=[0]*2
        count[0]=common_words[i][0]
        counts = common_words[i][1]
        count[1] = str(counts)+"("+str(int(counts/words_class*100))+"%)"
        keyword_counts.append(count)
        #print(common_words[i])
        #print(keyword_counts[i])
    print(keyword_counts)
    return keyword_counts


REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))

def text_prepare(text):  # 文字處理(移除標點符號、數字、stopwords)
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
  # 刪除stopwords
  text_split = text.split()
  text=""
  for t in text_split:
    if(not(t in STOPWORDS)):
      text = text+t+' '
  text = text[:-1] #將最後的空格刪除

  return text

def find_keyword(text,key):
    #將keyword tag出來
    matches = list(re.finditer(key.lower(),text.lower()))
    matches.reverse()
    for i in matches:
        text=text[:i.start()]+"<mark style='color:green'>"+ text[i.start():i.end()] + '</mark>' +text[i.end():]
    #將換行符replace成<br>
    char='\n'
    print('no change',text.count(char))
    text=text.replace(char, "<br>")
    print('change',text.count(char))
    return text
    