#!/usr/bin/python
# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect
import nltk, re
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import *
from nltk.stem.snowball import SnowballStemmer
from nltk.metrics.distance import edit_distance
nltk.download('words')
from nltk.corpus import words
from selenium.webdriver.chrome.options import Options
from random import choice
from collections import Counter, OrderedDict
# Create your views here.

covid_cbow=[['major','0.9999517202377319'],['therapy','0.9999486207962036'],['course','0.999937891960144'],['case','0.9999340772628784'],['however','0.999931812286377'],['laboratory','0.9999285936355591'],['outcomes','0.9999274015426636'],['membrane','0.9999233484268188'],['reactions','0.9999217391014099'],['cerebral','0.9999212026596069'],['treatment','0.9999164938926697'],['loss','0.9999141097068787'],['known','0.999912440776825'],['given','0.9999104738235474'],['outbreaks','0.9999096393585205'],['surgical','0.9999033212661743'],['present','0.9999019503593445'],['mucormycosis','0.9999013543128967'],['investigation','0.9998984932899475'],['described','0.9998971223831177'],['following','0.9998964667320251'],['body','0.9998941421508789'],['acid','0.999891996383667'],['outcome','0.9998903870582581'],['multiple','0.9998893737792969'],['although','0.9998874664306641'],['cancer','0.9998867511749268'],['air','0.9998866319656372'],['detection','0.9998856782913208'],['report','0.9998836517333984'],['adverse','0.9998800754547119'],['setting','0.9998795390129089'],['established','0.9998787045478821'],['advanced','0.9998781681060791'],['effectiveness','0.9998781085014343'],['oral','0.9998767375946045'],['pediatric','0.9998753070831299'],['pulmonary','0.9998705983161926'],['emergency','0.9998698234558105'],['remdesivir','0.9998694062232971'],['cytokines','0.9998686909675598'],['chest','0.9998684525489807'],['rna','0.9998681545257568'],['wide','0.9998669624328613'],['cell','0.9998661875724792'],['additional','0.9998643398284912'],['involved','0.9998636841773987'],['order','0.99986332654953'],['rt-pcr','0.9998632669448853'],['highly','0.9998624324798584'],['tuberculosis','0.999861478805542'],['cardiac','0.9998612403869629'],['protective','0.9998611807823181'],['initial','0.9998599290847778'],['confirmed','0.9998589158058167'],['reducing','0.9998588562011719'],['due','0.9998572468757629'],['recommended','0.9998568892478943'],['commonly','0.9998564720153809'],['particularly','0.999855637550354'],['diagnostic','0.9998514652252197'],['inhibitor','0.9998507499694824'],['condition','0.9998506307601929'],['long','0.9998505711555481'],['c','0.9998503923416138'],['might','0.9998501539230347'],['even','0.9998501539230347'],['upper','0.9998496770858765'],['million','0.9998492002487183'],['visual','0.9998489618301392'],['society','0.9998488426208496'],['phase','0.999848484992981'],['skin','0.9998472929000854'],['adult','0.999846339225769'],['association','0.9998462200164795'],['thrombocytopenia','0.9998447895050049'],['subsequent','0.999843955039978'],['testing','0.9998435974121094'],['throughout','0.9998435378074646'],['natural','0.9998435378074646'],['transplantation','0.9998423457145691'],['six','0.999840259552002'],['lungs','0.999839186668396'],['human','0.9998377561569214'],['therapeutics','0.9998376369476318'],['nasal','0.9998371601104736'],['active','0.9998367428779602'],['presented','0.9998337626457214'],['de','0.9998326301574707'],['literature','0.9998321533203125'],['disorders','0.9998300075531006'],['reaction','0.9998295903205872'],['receptor','0.9998294711112976'],['underlying','0.9998258948326111'],['pregnancy','0.9998247027397156'],['increasing','0.9998246431350708'],['result','0.9998245239257812'],['require','0.9998242855072021'],['effective','0.9998239278793335'],['production','0.9998235702514648']]
covid_sg=[['ill','0.9527148008346558'],['delayed','0.9515600204467773'],['cardiac','0.9492279887199402'],['neurological','0.9471701979637146'],['long','0.9467635154724121'],['critically','0.9463145732879639'],['chronic','0.9458582401275635'],['requiring','0.9455441832542419'],['presentations','0.9430776834487915'],['acp','0.9425822496414185'],['neuropsychiatric','0.9414405226707458'],['prolonged','0.9410496950149536'],['manifestations','0.9390771389007568'],['leading','0.9387648105621338'],['renal','0.9382652044296265'],['occurrence','0.9380744695663452'],['suffering','0.9378026723861694'],['long-covid','0.9374372959136963'],['alzheimer','0.9364416599273682'],['syndrome-coronavirus-','0.9348005056381226'],['post-acute','0.9333150386810303'],['presenting','0.9328542947769165'],['disease-','0.9327310919761658'],['sequelae','0.9312055706977844'],['echocardiography','0.9299083352088928'],['common','0.9295570254325867'],['cam','0.9290566444396973'],['onset','0.9284818172454834'],['embolism','0.9282784461975098'],['liver','0.9278910756111145'],['course','0.9278106093406677'],['therapy','0.9274688363075256'],['known','0.9267117381095886'],['fibrillation','0.9258546829223633'],['parallel','0.9256191849708557'],['hypoalbuminemia','0.9254868030548096'],['transplantation','0.9253419637680054'],['underlying','0.924979567527771'],['spectrum','0.9246545433998108'],['prone','0.9242312908172607'],['co-morbidities','0.9240858554840088'],['prognostic','0.9238428473472595'],['aware','0.9236133694648743'],['frequent','0.9232082366943359'],['described','0.9225817322731018'],['magnetic','0.9222750663757324'],['cough','0.9222118258476257'],['dyspnea','0.9219902753829956'],['pneumonia','0.9218971133232117'],['invasive','0.9199457764625549'],['circuits','0.9199436902999878'],['cap','0.9192705154418945'],['pediatric','0.9190207719802856'],['injury','0.9187494516372681'],['serious','0.9183976650238037'],['unknown','0.9182922840118408'],['cause','0.9181758761405945'],['tuberculosis','0.917591392993927'],['targeted','0.9175553321838379'],['pregnancy','0.917363703250885'],['illness','0.9163806438446045'],['organ','0.9160981178283691'],['prognosis','0.9159103035926819'],['cac','0.9151591658592224'],['electrocardiogram','0.9150187969207764'],['hyperoxemia','0.9145718812942505'],['wide','0.9145007133483887'],['term','0.9143098592758179'],['hematological','0.9143080711364746'],['multisystem','0.9139112234115601'],['medication','0.9136938452720642'],['mucormycosis','0.9135861396789551'],['suspected','0.9132466316223145'],['lt','0.9130252599716187'],['fungal','0.9124189615249634'],['parkinson','0.9120838046073914'],['diseases','0.9118502736091614'],['progression','0.9116345047950745'],['evolving','0.9112222790718079'],['accompanied','0.911198079586029'],['present','0.9110128879547119'],['delay','0.9102135300636292'],['ards','0.9098806977272034'],['rhino-orbital','0.9098500609397888'],['pans','0.9088807106018066'],['thrombosis','0.9088427424430847'],['hydroxychloroquine','0.908429741859436'],['ventilated','0.908409059047699'],['hyaluronic','0.9081880450248718'],['surgical','0.9081003069877625'],['coronary','0.9080584645271301'],['complicated','0.9080021381378174'],['rehabilitation','0.907390832901001'],['spinal','0.9072303771972656'],['worsening','0.9069538116455078'],['causes','0.9068868160247803'],['circulatory','0.906753659248352'],['atrial','0.9066084623336792'],['newly','0.9064122438430786'],['metabolic','0.906247079372406']]
mpx_sg=[['spain','0.999600350856781'],['human','0.9995913505554199'],['outsid','0.999568521976471'],['infecti','0.999562680721283'],['korea','0.9995594620704651'],['may','0.9995527863502502'],['report','0.9995443224906921'],['countri','0.9995328187942505'],['measur','0.9995278120040894'],['first','0.9995185732841492'],['june','0.9995070099830627'],['area','0.999506950378418'],['import','0.9995005130767822'],['new','0.9994977712631226'],['fluid','0.9994968175888062'],['control','0.9994944334030151'],['case','0.9994915723800659'],['diagnosi','0.9994897842407227'],['worldwid','0.999488890171051'],['challeng','0.9994831085205078'],['europ','0.9994804263114929'],['outbreak','0.999478816986084'],['infect','0.9994715452194214'],['across','0.9994713068008423'],['factor','0.9994705319404602'],['data','0.9994701147079468'],['respiratori','0.9994680881500244'],['medic','0.9994661808013916'],['republ','0.9994649887084961'],['present','0.9994614124298096'],['becom','0.9994603991508484'],['re-emerg','0.9994600415229797'],['unit','0.999459981918335'],['ongo','0.9994592070579529'],['knowledg','0.9994544982910156'],['potenti','0.9994535446166992'],['america','0.99945068359375'],['pandem','0.9994453191757202'],['taiwan','0.999441385269165'],['epidemiolog','0.9994386434555054'],['travel','0.9994379281997681'],['activ','0.9994367957115173'],['belong','0.9994362592697144'],['transmiss','0.9994362592697144'],['diseas','0.9994354844093323'],['hiv','0.9994348287582397'],['epidem','0.9994334578514099'],['histori','0.9994332194328308'],['anim','0.9994326233863831'],['expand','0.9994306564331055'],['non-endem','0.9994273781776428'],['msm','0.9994266033172607'],['result','0.9994262456893921'],['pain','0.9994254112243652'],['healthcar','0.9994252920150757'],['virus','0.9994248151779175'],['atyp','0.9994246363639832'],['high','0.9994243383407593'],['addit','0.9994224905967712'],['contain','0.999420166015625'],['world','0.9994201064109802'],['pathogen','0.9994199872016907'],['rare','0.9994192123413086'],['identifi','0.9994188547134399'],['signific','0.9994182586669922'],['system','0.9994171261787415'],['western','0.9994156360626221'],['spread','0.9994155764579773'],['awar','0.9994155168533325'],['number','0.9994148015975952'],['occur','0.9994146823883057'],['endem','0.999414324760437'],['sampl','0.9994125962257385'],['year','0.9994120597839355'],['suspect','0.9994120597839355'],['emerg','0.9994116425514221'],['northern','0.9994115233421326'],['confirm','0.9994107484817505'],['cessat','0.9994099736213684'],['day','0.9994099736213684'],['respons','0.9994099140167236'],['multi-countri','0.9994097352027893'],['overal','0.999409556388855'],['virolog','0.999408483505249'],['affect','0.999407172203064'],['region','0.9994069933891296'],['profession','0.9994069337844849'],['surveil','0.9994066953659058'],['isol','0.9994054436683655'],['differ','0.9994053840637207'],['zoonosi','0.9994049072265625'],['west','0.9994046092033386'],['mani','0.9994034767150879'],['rise','0.999403178691864'],['return','0.9994018077850342'],['allow','0.9994003772735596'],['intern','0.9993999004364014'],['sojourn','0.9993999004364014'],['centr','0.9993992447853088'],['inform','0.9993974566459656']]
mpx_cbow=[['case','0.9656734466552734'],['virus','0.9645563364028931'],['outbreak','0.9615261554718018'],['public','0.9544534087181091'],['clinic','0.9526852965354919'],['vaccin','0.9499849081039429'],['infect','0.9466119408607483'],['diseas','0.946216344833374'],['smallpox','0.9445787668228149'],['health','0.9422571063041687'],['patient','0.9409277439117432'],['africa','0.9401131868362427'],['may','0.9387099742889404'],['exposur','0.9329108595848083'],['present','0.9315025806427002'],['human','0.931381106376648'],['confirm','0.9309754371643066'],['current','0.9298739433288574'],['control','0.9291667938232422'],['report','0.9288610219955444'],['transmiss','0.9272884726524353'],['detect','0.9272723197937012'],['includ','0.9271237254142761'],['first','0.9268794059753418'],['identifi','0.9268625974655151'],['infecti','0.9265116453170776'],['prevent','0.925530731678009'],['countri','0.9250656962394714'],['lesion','0.9248021841049194'],['symptom','0.923833966255188'],['-','0.9233891367912292'],['laboratori','0.9229637980461121'],['diagnosi','0.9224929809570312'],['contact','0.9216614961624146'],['mpxv','0.9212676286697388'],['system','0.9208704233169556'],['pcr','0.9200177192687988'],['analysi','0.9186092615127563'],['rapid','0.9182038903236389'],['covid-','0.917532742023468'],['orthopoxvirus','0.9148179292678833'],['rash','0.9135017991065979'],['june','0.9131889343261719'],['knowledg','0.913098931312561'],['variant','0.9126964211463928'],['epidem','0.912026047706604'],['mpx','0.9103207588195801'],['clade','0.9089301228523254'],['popul','0.9075462222099304'],['men','0.9058023691177368'],['test','0.905683159828186'],['measur','0.9049069285392761'],['possibl','0.9044930338859558'],['use','0.9040499329566956'],['area','0.9040035605430603'],['emerg','0.9016085267066956'],['global','0.9009094834327698'],['spain','0.900002658367157'],['earli','0.8996670842170715'],['endem','0.8977223634719849'],['featur','0.896895706653595'],['surveil','0.8953686952590942'],['transmit','0.8949661254882812'],['perform','0.8948466181755066'],['healthcar','0.8935954570770264'],['histori','0.89326012134552'],['risk','0.8915934562683105'],['potenti','0.891061544418335'],['person','0.8907103538513184'],['republ','0.8905496597290039'],['review','0.8895655274391174'],['spread','0.8887601494789124'],['genom','0.8875905275344849'],['region','0.8872594833374023'],['zoonot','0.886165976524353'],['dna','0.8859539031982422'],['caus','0.8858392834663391'],['two','0.8855541944503784'],['recent','0.8853175044059753'],['lineag','0.8850746750831604'],['addit','0.881301760673523'],['pandem','0.8798745274543762'],['vac','0.8781402111053467'],['diagnost','0.8761343955993652'],['specif','0.8755693435668945'],['posit','0.8733273148536682'],['sever','0.87237548828125'],['new','0.8676052689552307'],['respons','0.8673507571220398'],['sinc','0.8668107986450195'],['epidemiolog','0.8663573265075684'],['data','0.8659356832504272'],['develop','0.8643922209739685'],['ro','0.864362359046936'],['n','0.8598856925964355'],['assess','0.8581018447875977'],['europ','0.8580261468887329'],['hcp','0.8575682640075684'],['fever','0.8518397808074951'],['sampl','0.850260853767395']]


def index(request):
    return render(request,'index3.html')


def covid(request):
        covid = [[covid_cbow[i][0],covid_cbow[i][1],covid_sg[i][0],covid_sg[i][1]] for i in range(100)]
        #file_text=''
        scrape_texts=''
        #show_texts=''
        pre_word_counts={}
        all_word_counts={}
        pre_freq_list = []
        all_freq_list = []
        ranks = 30
        #keyword=['anaphylaxis','socioeconomic','contrary','afraid','intensive','amplified','covid-positive','ipv','04-0','symptoms','covid-19']
        #print('url',get_url )
        scrape_texts = read_file1() 
        #show_texts = scrape_texts.split(','*90)[0]
        #file_text = scrape_texts
        word_counts = prepared_words_counter(scrape_texts,stopwords=False,stem=False)        # bag_of_words
        all_word_counts = top_n_words(word_counts,n=ranks) # 前n個關鍵字(未刪除stopwords)
        all_freq_list = word_freq_list(word_counts)
        word_counts = prepared_words_counter(scrape_texts) 
        pre_word_counts = top_n_words(word_counts,n=ranks)  # 前n個關鍵字(前處理)
        pre_freq_list = word_freq_list(word_counts)
        #keyword = textCheck(keywords,[x[0] for x in prepared_words_counter(scrape_texts,stopwords=True,stem=False)])
        #print(keyword)
        #print(request.POST['keyword'])
        #file_text=find_keyword(show_texts,keyword) # 在文本搜尋關鍵字
        #print(word_counts)
        #keyword_msg = keywordCheck(keyword,keywords)
        #print(keyword_msg)
        return render(request,'covid.html',{'pre_word_counts':pre_word_counts[:100] ,'all_word_counts':all_word_counts[:100] ,'pre_freq_list':pre_freq_list[:100],'all_freq_list':all_freq_list[:100],"ranks":ranks+1,"cov":covid})

    
def mpx(request):
        mpx = [[mpx_cbow[i][0],mpx_cbow[i][1],mpx_sg[i][0],mpx_sg[i][1]] for i in range(100)]
        #file_text=''
        scrape_texts=''
        #show_texts=''
        pre_word_counts={}
        pre_freq_list = []
        ranks = 30
        #keyword=['anaphylaxis','socioeconomic','contrary','afraid','intensive','amplified','covid-positive','ipv','04-0','symptoms','covid-19']
        #print('url',get_url )
        scrape_texts = read_file2() 
        #show_texts = scrape_texts.split(','*90)[0]
        #file_text = scrape_texts
        word_counts = prepared_words_counter(scrape_texts,stopwords=False,stem=False)        # bag_of_words
        word_counts = prepared_words_counter(scrape_texts) 
        pre_word_counts = top_n_words(word_counts,n=ranks)  # 前n個關鍵字(前處理)
        pre_freq_list = word_freq_list(word_counts)
        #keyword = textCheck(keywords,[x[0] for x in prepared_words_counter(scrape_texts,stopwords=True,stem=False)])
        #print(keyword)
        #print(request.POST['keyword'])
        #file_text=find_keyword(show_texts,keyword) # 在文本搜尋關鍵字
        #print(word_counts)
        #keyword_msg = keywordCheck(keyword,keywords)
        #print(keyword_msg)
        return render(request,'monkeypox.html',{'pre_word_counts':pre_word_counts[:100] ,'pre_freq_list':pre_freq_list[:100],"ranks":ranks+1,"mpx":mpx})


#function

def prepared_words_counter(text,stopwords=True,stem=True):  # 計算所有單字出現次數及機率
    stemmer = SnowballStemmer('english') # stemmer
    words_counts = {} # word dictionary
    title_pre = text_prepare(text,stopwords)# 前處理
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
    freq_counts=[]
    words=[]
    times=[]
    freq=[]
    all_counts=sum(c[1] for c in common_words)
    #print("words")
    for cw in common_words:
        #print(cw[0])
        words.append(cw[0])
        times.append(cw[1])
        freq.append(cw[1]/all_counts)
    #print(freq_counts)
    freq_counts.append(words)
    freq_counts.append(times)
    freq_counts.append(freq)
    #print(freq_counts)
    return freq_counts


# 不計算的字元與單字
REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^a-z #+_-]')
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
  # �NREPLACE_BY_SPACE_RE的符號換成空格號
  text = re.sub(REPLACE_BY_SPACE_RE,' ',text, count=0, flags=0)
  #print('re: ',text)
  # �NBAD_SYMBOLS_RE的符號移除
  text = re.sub(BAD_SYMBOLS_RE,'',text, count=0, flags=0)
  #print('bad: ',text)
  # �R��stopwords
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
    output = output[:-1]#去掉最後的' ' 
    return output


def keywordCheck(keywords,insert):
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

def read_file1():
    path ="./hw3/pubmed_covid_1000.txt"
    f = open(path, "r", encoding='utf-8')
    file_data = f.read()
    f.close()
    return file_data

def read_file2():
    path ="./hw3/pubmed_monkeypox_1000.txt"
    f = open(path, "r", encoding='utf-8')
    file_data = f.read()
    f.close()
    return file_data
