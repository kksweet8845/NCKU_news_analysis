from django.shortcuts import render
from .apis import Hotword, WordMap
from .apis import get_word_freq
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Max
import json
from multiprocessing import Pool
import pandas as pd
from tqdm import tqdm
import numpy as np
from newsdb.models import Word, Standpoint, Sentiment, Cluster_day, Aspect, Cluster_three_day, New, Brand
from analysis.apis import KeywordToday, KeywordThreeDay
from datetime import date, datetime, timedelta
# Create your views here.

# hd = Hotword()
# hd.fetch_news([Q(date__gte=datetime.today() - timedelta(days=28)) , Q(brand_id=11) , Q(sub_id=2),])
# data = hd.get_hotword(20)
# keyBrand = hd.gen_keyBrand()
# brandKey = hd.gen_branKey()

keywords = None
keywords_analysis = None
relative_wordCloud = None
relative_news = None


def zero(num):
    return f"0{num}" if num < 10 else f"{num}"



def hotword_worker(where):
    """ """
    hd = Hotword()
    hd.fetch_news(*where)
    data = hd.get_hotword(20)
    keyBrand = hd.gen_keyBrand()
    brandKey = hd.gen_branKey()

    return (keyBrand, brandKey)

def hotword(request):
    """ """

    hd = Hotword()
    hd.fetch_news([Q(date__gte=datetime.today() - timedelta(days=1)) & Q(brand_id=11) & Q(sub_id=2),])
    data = hd.get_hotword(20)
    keyBrand = hd.gen_keyBrand()
    brandKey = hd.gen_branKey()
    # pool = Pool(processes=2)
    # scale = 250
    # ls = []
    # keyBrand = []
    # brandKey = []
    # for i in range(2):
    #     ls.append(pool.apply_async(hotword_worker, ([Q(id__gt=20000 + i*scale) & Q(id__lt=20000 + (i+1)*scale -1),])))
    return HttpResponse(json.dumps(brandKey))


def keyword(request):
    """ """
    return HttpResponse(json.dumps(keyBrand))

def pubKeyword(request):
    """ """
    return HttpResponse(json.dumps(brandKey))

def wordmap_worker(where):
    wp = WordMap()
    wp.fetch_news([Q(id__gt=0) & Q(id__lt=20500),])
    data = wp.gen_dict()

    return data


def wordmap(request):
    """ """
    maxid = 6500
    scale = 20
    wp = WordMap()
    word_dict = []
    # for i in tqdm(range(maxid // scale)):
    #     data = wp.fetch_news([Q(id__gt=i*scale) & Q(id__lt=(i+1)*scale -1),])
    #     word_dict.append(wp.gen_dict(data))

    pre_df = wp.fetch_news([Q(id__gt=0),])
    words = wp.gen_dict(pre_df)

    with open('dictionary.txt', 'w') as file:
        for dw in words:
            file.writeline(dw)

    return HttpResponse(True)


def dumpArticle(request):
    """ """
    wp = WordMap()

    df = wp.fetch_news([Q(id__gt=6000) & Q(id__lt=8000),])
    df.to_csv('analysis/src/dump.csv', index=False)

    return HttpResponse(True)


def wordFreq(request):

    keywordToday = KeywordToday()
    # keywordToday.getWordFreq()
    keywords, relative_news = keywordToday.getGroupKeywords()
    # df = keywordToday.getNewHotword()
    keywords_analysis, relative_wordCloud = keywordToday.genData(keywords[0], relative_news)

    return HttpResponse(json.dumps([keywords, keywords_analysis, relative_wordCloud]))

def newsMemory(request):
    keywordToday = KeywordThreeDay()
    keywords, relative_news = keywordToday.getGroupKeywords()


    mem, keyword_ls = keywordToday.genData(keywords, relative_news)


    for i, dm in enumerate(mem):
        rst = get_standpoint(keyword_ls[i]['relative_news'])
        dm.update(rst)

    return HttpResponse(json.dumps(mem))

def get_sentiment(request):
    news_query = Sentiment.objects.filter(Q(date__gte='2020-05-30'))
    good_q = news_query.order_by('-good')[0]
    surprise_q = news_query.order_by('-surprise')[0]
    sad_q = news_query.order_by('-sad')[0]
    fear_q = news_query.order_by('-fear')[0]
    disgust_q = news_query.order_by('-disgust')[0]
    happy_q = news_query.order_by('-happy')[0]
    anger_q = news_query.order_by('-anger')[0]

    alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    tmp = {}
    for da in alpha:
        for dq in [good_q, surprise_q, sad_q, fear_q, disgust_q, happy_q, anger_q]:
            tmp[da] = {
                        'title': dq.news.title,
                        'url'  : dq.news.url,
                        'score': [str(dq.good), str(dq.surprise), str(dq.sad), str(dq.fear),
                                  str(dq.disgust), str(dq.happy), str(dq.anger)]
                      }
    return HttpResponse(json.dumps(tmp))

def get_standpoint(relative_news):


    news_query = Standpoint.objects.filter(Q(news__in=relative_news))
    china = 0
    setn = 0
    for i in news_query:
        if i.standpoint == 1:
            china += 1
        else:
            setn += 1

    news_query2 = Aspect.objects.filter(Q(new_id__in=relative_news))
    pos = 0
    middle = 0
    neg = 0
    for j in news_query2:
        if j.aspect == 0:
            pos += 1
        elif j.aspect == 1:
            middle += 1
        else:
            neg += 1

    return_dict = {
        'sentiment': [pos, middle, neg],
        'standpoint': [china, setn],
        'newsNum': len(relative_news)
    }

    return return_dict
    
def get_cluster(request):
    dt = {}

    all_news = New.objects.all()
    all_brands = Brand.objects.all()
    
    for i in range(17):
        news_no = []
        news_query = Cluster_three_day.objects.filter(Q(cluster__lte=10)
                     & Q(date_today=date.today().isoformat()))
        for query in news_query:
            if query.news.brand_id == i+1:
                news_no.append(query.news_id)
        if len(news_no) == 0:
            continue

        news_query2 = New.objects.filter(Q(brand_id=i+1) & Q(date__gt=(date.today()-timedelta(days=3)).isoformat()))
        news_no2 = []
        for query in news_query2:
            news_no2.append(query.id)
        standpoint_query = Standpoint.objects.filter(Q(news__in=news_no2))
        china = 0
        setn = 0
        for k in standpoint_query:
            if k.standpoint == 1:
                china += 1
            else:
                setn += 1

        aspect_query = Aspect.objects.filter(Q(new_id__in=news_no2))
        pos = 0
        middle = 0
        neg = 0
        for j in aspect_query:
            if j.aspect == 0:
                pos += 1
            elif j.aspect == 1:
                middle += 1
            else:
                neg += 1
        focus_news = []
        for x in range(10):
            temp_list = []
            for y in news_no:
                y = Cluster_three_day.objects.get(news__id=y)
                if y.cluster == x+1:
                    temp_list.append({'title': all_news.get(id=y.news_id).title, 'url': all_news.get(id=y.news_id).url})
            focus_news.append(temp_list)

        brand = all_brands.get(id=all_news.get(id=y.news_id).brand_id)
        dt[i+1] = {
            'names': brand.brand_name,
            'news_number': len(news_no2),
            'sentiment': [pos, middle, neg],
            'standpoint': [china, setn],
            'focus_news': focus_news
            }

    return HttpResponse(json.dumps(dt))


def sentimentWeek(request):

    base = datetime.today()

    seventWeekAgoDate = base - timedelta(days=7)

    news_query = Sentiment.objects.filter(Q(date__gte=f'{seventWeekAgoDate.year}-{zero(seventWeekAgoDate.month)}-{zero(seventWeekAgoDate.day)}'))

    good_q = news_query.order_by('-good')[0]
    surprise_q = news_query.order_by('-surprise')[0]
    sad_q = news_query.order_by('-sad')[0]
    fear_q = news_query.order_by('-fear')[0]
    disgust_q = news_query.order_by('-disgust')[0]
    happy_q = news_query.order_by('-happy')[0]
    anger_q = news_query.order_by('-anger')[0]

    alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    tmp = {}
    for da, dq in zip(alpha, [good_q, surprise_q, sad_q, fear_q, disgust_q, happy_q, anger_q]):
        tmp[da] = {
                    'title': dq.news.title,
                    'url'  : dq.news.url,
                    'data': [str(dq.good), str(dq.surprise), str(dq.sad), str(dq.fear),
                                str(dq.disgust), str(dq.happy), str(dq.anger)]
                    }

    print(tmp)
    return HttpResponse(json.dumps(tmp))


def newsReview(request):
    keywordToday = KeywordThreeDay()
    keywords, relative_news = keywordToday.getGroupKeywords()

    mem, keyword_ls = keywordToday.genData(keywords, relative_news)

    for i, dm in enumerate(mem):
        rst = get_standpoint(keyword_ls[i]['relative_news'])
        dm.update(rst)

    return HttpResponse(json.dumps(mem))


def mediaReport(request):

    all_brands = Brand.objects.all()

    mediaName = []
    mediaNum = []
    for dbrand in all_brands:
        mediaName.append(dbrand.brand_name)
        mediaNum.append(New.objects.filter(brand_id=dbrand.id).count())

    return HttpResponse(json.dumps({
        'labels' : mediaName,
        'series' : mediaNum
    }))

def top20Keywords(request):
    global keywords
    global keywords_analysis
    global relative_wordCloud
    global relative_news
    keywordToday = KeywordToday()
    if keywords == None:
        # keywordToday.getWordFreq()
        keywords, relative_news = keywordToday.getGroupKeywords()
        # df = keywordToday.getNewHotword()

    return HttpResponse(json.dumps(keywords))


def keywordAnalysis(request, word):
    global keywords_analysis
    global relative_wordCloud
    global keywords
    global relative_news
    print(word)
    keywordToday = KeywordToday()
    if keywords_analysis == None:
        # keywordToday.getWordFreq()
        keywords, relative_news = keywordToday.getGroupKeywords()
        # df = keywordToday.getNewHotword()
    keywords_analysis, relative_wordCloud = keywordToday.genData(word, relative_news)

    return HttpResponse(json.dumps(keywords_analysis))

def relativeKeyword(request, word):
    global relative_wordCloud
    global keywords_analysis
    global keywords
    global relative_news
    keywordToday = KeywordToday()
    if relative_wordCloud == None:
        
        # keywordToday.getWordFreq()
        keywords, relative_news = keywordToday.getGroupKeywords()
        # df = keywordToday.getNewHotword()
    keywords_analysis, relative_wordCloud = keywordToday.genData(word, relative_news)

    return HttpResponse(json.dumps(relative_wordCloud))

def mediaAnalysis(requeset):
    print('mediaAnalysis')
    dt = {}

    all_news = New.objects.filter(date__gte='2020-05-01')
    all_brands = Brand.objects.all()
    for i in range(17):
        news_no = []
        news_query = Cluster_three_day.objects.filter(Q(cluster__lte=10)
                     & Q(date_today='2020-05-31'))
        for query in news_query:
            if query.news.brand_id == i+1:
                news_no.append(query.news_id)
        if len(news_no) == 0:
            continue
        news_query2 = Standpoint.objects.filter(Q(news__in=news_no))
        china = 0
        setn = 0
        for k in news_query2:
            if k.standpoint == 1:
                china += 1
            else:
                setn += 1

        news_query3 = Aspect.objects.filter(Q(new_id__in=news_no))
        pos = 0
        middle = 0
        neg = 0
        for j in news_query3:
            if j.aspect == 0:
                pos += 1
            elif j.aspect == 1:
                middle += 1
            else:
                neg += 1
        focus_news = []
        for x in range(10):
            temp_list = []
            for y in news_no:
                y = Cluster_three_day.objects.get(news__id=y)
                if y.cluster == x+1:
                    temp_list.append({'title': all_news.get(id=y.news_id).title, 'url': all_news.get(id=y.news_id).url})
            focus_news.append(temp_list)

        brand = all_brands.get(id=all_news.get(id=y.news_id).brand_id)
        dt[i+1] = {
            'names': brand.brand_name,
            'news_number': len(news_no),
            'sentiment': [pos, middle, neg],
            'standpoint': [china, setn],
            'focus_news': focus_news
            }
    
    return HttpResponse(json.dumps(dt))
        
# 關鍵字選擇頁面
def testChoose(request):
    data = [f"test{i}" for i in range(20)]

    return JsonResponse(data, safe=False)

# 關鍵字頁面文字雲
def testRelativeKeyword(request, word):
    data = [{
            'text': '罷韓',
            'size': 67,
        },{
            'text': '罷免',
            'size': 54,
        },{
            'text': '時中',
            'size': 81,
        },{
            'text': '罷韓',
            'size': 61,
        },{
            'text': '罷免',
            'size': 92,
        },{
            'text': '時中',
            'size': 61,
        },{
            'text': '罷韓',
            'size': 80,
        },{
            'text': '罷免',
            'size': 61,
        },{
            'text': '時中',
            'size': 90,
        },{
            'text': '罷韓',
            'size': 60,
        },{
            'text': '罷免',
            'size': 81,
        },{
            'text': '時中',
            'size': 65,
        },{
            'text': '罷韓',
            'size': 48,
        },{
            'text': '罷免',
            'size': 55,
        },{
            'text': '時中',
            'size': 66,
        },{
            'text': '罷韓',
            'size': 56,
        },{
            'text': '罷免',
            'size': 71,
        },{
            'text': '時中',
            'size': 65,
        },{
            'text': '罷韓',
            'size': 89,
        },{
            'text': '罷免',
            'size': 67,
        },{
            'text': '時中',
            'size': 75,
        },{
            'text': '罷韓',
            'size': 61,
        },{
            'text': '罷免',
            'size': 55,
        },{
            'text': '時中',
            'size': 70,
        },{
            'text': '罷韓',
            'size': 60,
        },{
            'text': '罷免',
            'size': 50,
        },{
            'text': '時中',
            'size': 40,
        }]
    return JsonResponse(data, safe=False)

# 關鍵字頁面時間軸
def testKeywordAnalysis(request, word):
    data = [{
            'date': '2020-02-21',
            'keyword': '口罩',
            'posLinks': [
                {
                    'title':'疾管署召開「因應中國不明原因肺炎疫情專家諮詢會議」POS',
                    'url': 'https://google.com',
                },{
                    'title':'政府派專家赴陸訪查 POS',
                    'url': 'https://google.com',
                },{
                    'title':'疾管署召開「因應中國不明原因肺炎疫情專家諮詢會議」POS',
                    'url': 'https://google.com',
                },{
                    'title':'政府派專家赴陸訪查 POS',
                    'url': 'https://google.com',
                },
            ],
            'negLinks': [
                {
                    'title':'疾管署召開「因應中國不明原因肺炎疫情專家諮詢會議」POS',
                    'url': 'https://google.com',
                },{
                    'title':'政府派專家赴陸訪查 POS',
                    'url': 'https://google.com',
                },{
                    'title':'疾管署召開「因應中國不明原因肺炎疫情專家諮詢會議」POS',
                    'url': 'https://google.com',
                },
            ]
        }, {
            'date': '2020-03-01',
            'keyword': '鑽石公主號',
            'posLinks': [],
            'negLinks': [
                {
                    'title':'疾管署召開「因應中國不明原因肺炎疫情專家諮詢會議」POS',
                    'url': 'https://google.com',
                },{
                    'title':'政府派專家赴陸訪查 POS',
                    'url': 'https://google.com',
                },
            ]
        }, {
            'date': '2020-03-13',
            'keyword': '美國',
            'posLinks': [],
            'negLinks': [
                {
                    'title':'疾管署召開「因應中國不明原因肺炎疫情專家諮詢會議」POS',
                    'url': 'https://google.com',
                },{
                    'title':'政府派專家赴陸訪查 POS',
                    'url': 'https://google.com',
                },
            ]
        }, {
            'date': '2020-03-24',
            'keyword': '義大利',
            'posLinks': [
                {
                    'title':'疾管署召開「因應中國不明原因肺炎疫情專家諮詢會議」POS',
                    'url': 'https://google.com',
                },{
                    'title':'政府派專家赴陸訪查 POS',
                    'url': 'https://google.com',
                },
            ],
            'negLinks': []
        }, {
            'date': '2020-03-28',
            'keyword': '疫苗',
            'posLinks': [
                {
                    'title':'疾管署召開「因應中國不明原因肺炎疫情專家諮詢會議」POS',
                    'url': 'https://google.com',
                },{
                    'title':'政府派專家赴陸訪查 POS',
                    'url': 'https://google.com',
                },
            ],
            'negLinks': [
                {
                    'title':'疾管署召開「因應中國不明原因肺炎疫情專家諮詢會議」POS',
                    'url': 'https://google.com',
                },{
                    'title':'政府派專家赴陸訪查 POS',
                    'url': 'https://google.com',
                },
            ]
        }]

    return JsonResponse(data, safe=False)

def testSevenSemantic(request):
    data = {
        'a': {
            'topic': '正向',
            'title': '屏榮高中陳守心錄取醫學系 盼未來結合興趣回饋部落',
            'data': [400, 430, 448, 470, 540, 1200, 1380],
        },
        'b': {
            'topic': '驚奇',
            'title': '北市助攻都會農友 讓農業變有趣又吸睛',
            'data': [400, 430, 448, 470, 540, 200, 1380],
        },
        'c': {
            'topic': '哀傷',
            'title': '新冠肺炎燒三個月 來台觀光收益損近千億元',
            'data': [400, 430, 448, 1470, 540, 1200, 380],
        },
        'e': {
            'topic': '負面',
            'title': '48公斤「世界最胖山貓」大叔照爆紅 因心臟病死亡',
            'data': [400, 430, 448, 470, 540, 1200, 1380],
        },
        'f': {
            'topic': '快樂',
            'title': '屏榮高中陳守心錄取醫學系 盼未來結合興趣回饋部落',
            'data': [1400, 430, 448, 470, 540, 200, 380],
        },
        'g': {
            'topic': '憤怒',
            'title': '屏榮高中陳守心錄取醫學系 盼未來結合興趣回饋部落',
            'data': [400, 430, 1048, 470, 540, 100, 130],
        },
    }
    return JsonResponse(data, safe=False)

def testReview(request):
    data = [{
            'keyword': '武漢肺炎',
            'summary': '新冠肺炎疫情從1月底開始爆發，迄今已延燒近四個月，據內政部移民署最新統計顯示，今年2、3、4月疫情嚴重的時候，來台旅客量逐月驟減，4月份來台旅客數僅2,559人，創下歷史新低量，而三個月來台旅客量較去年同期狂減260.9萬人次，觀光收益減損多達969.3億元。',
            'newsNum': 60,
            'reportNum': [44, 55, 41, 67, 22, 43, 44, 55, 41, 67, 22, 43],
            'sentiment': [4.51, 1, 2.18],
            'standpoint': [3.51, 2],
            'links': [
                {
                    'title': '新冠肺炎燒三個月 來台觀光收益損近千億元',
                    'url':   'https://www.google.com',
                },
                {
                    'title': '蘆洲驚見核能燃料棒輻射量爆表？原能會到場鬆了一口氣',
                    'url':   'https://www.google.com',
                },
                {
                    'title': '陳時中：樂活長照都顧到 防疫才算成功',
                    'url': 'https://www.google.com'
                }
            ]
        },{
            'keyword': '美國',
            'summary': '新冠肺炎疫情從1月底開始爆發，迄今已延燒近四個月，據內政部移民署最新統計顯示，今年2、3、4月疫情嚴重的時候，來台旅客量逐月驟減，4月份來台旅客數僅2,559人，創下歷史新低量，而三個月來台旅客量較去年同期狂減260.9萬人次，觀光收益減損多達969.3億元。',
            'newsNum': 55,
            'reportNum': [44, 55, 41, 67, 22, 43, 44, 55, 41, 67, 22, 43],
            'sentiment': [4.51, 1, 2.18],
            'standpoint': [3.51, 2],
            'links': [
                {
                    'title': '新冠肺炎燒三個月 來台觀光收益損近千億元',
                    'url':   'https://www.google.com',
                },
                {
                    'title': '蘆洲驚見核能燃料棒輻射量爆表？原能會到場鬆了一口氣',
                    'url':   'https://www.google.com',
                },
                {
                    'title': '陳時中：樂活長照都顧到 防疫才算成功',
                    'url': 'https://www.google.com'
                }
            ]
        },{
            'keyword': '義大利',
            'summary': '新冠肺炎疫情從1月底開始爆發，迄今已延燒近四個月，據內政部移民署最新統計顯示，今年2、3、4月疫情嚴重的時候，來台旅客量逐月驟減，4月份來台旅客數僅2,559人，創下歷史新低量，而三個月來台旅客量較去年同期狂減260.9萬人次，觀光收益減損多達969.3億元。',
            'newsNum': 45,
            'reportNum': [44, 55, 41, 67, 22, 43, 44, 55, 41, 67, 22, 43],
            'sentiment': [4.51, 1, 2.18],
            'standpoint': [3.51, 2],
            'links': [
                {
                    'title': '新冠肺炎燒三個月 來台觀光收益損近千億元',
                    'url':   'https://www.google.com',
                },
                {
                    'title': '蘆洲驚見核能燃料棒輻射量爆表？原能會到場鬆了一口氣',
                    'url':   'https://www.google.com',
                },
                {
                    'title': '陳時中：樂活長照都顧到 防疫才算成功',
                    'url': 'https://www.google.com'
                }
            ]
        },{
            'keyword': '中國',
            'summary': '新冠肺炎疫情從1月底開始爆發，迄今已延燒近四個月，據內政部移民署最新統計顯示，今年2、3、4月疫情嚴重的時候，來台旅客量逐月驟減，4月份來台旅客數僅2,559人，創下歷史新低量，而三個月來台旅客量較去年同期狂減260.9萬人次，觀光收益減損多達969.3億元。',
            'newsNum': 44,
            'reportNum': [44, 55, 41, 67, 22, 43, 44, 55, 41, 67, 22, 43],
            'sentiment': [4.51, 1, 2.18],
            'standpoint': [3.51, 2],
            'links': [],
        },{
            'keyword': '蔡英文',
            'summary': '新冠肺炎疫情從1月底開始爆發，迄今已延燒近四個月，據內政部移民署最新統計顯示，今年2、3、4月疫情嚴重的時候，來台旅客量逐月驟減，4月份來台旅客數僅2,559人，創下歷史新低量，而三個月來台旅客量較去年同期狂減260.9萬人次，觀光收益減損多達969.3億元。',
            'newsNum': 40,
            'reportNum': [44, 55, 41, 67, 22, 43, 44, 55, 41, 67, 22, 43],
            'sentiment': [4.51, 1, 2.18],
            'standpoint': [3.51, 2],
            'links': [],
        },{
            'keyword': '香港',
            'summary': '新冠肺炎疫情從1月底開始爆發，迄今已延燒近四個月，據內政部移民署最新統計顯示，今年2、3、4月疫情嚴重的時候，來台旅客量逐月驟減，4月份來台旅客數僅2,559人，創下歷史新低量，而三個月來台旅客量較去年同期狂減260.9萬人次，觀光收益減損多達969.3億元。',
            'newsNum': 35,
            'reportNum': [44, 55, 41, 67, 22, 43, 44, 55, 41, 67, 22, 43],
            'sentiment': [4.51, 1, 2.18],
            'standpoint': [3.51, 2],
            'links': [],
        },
    ]

    return JsonResponse(data, safe=False)
