from django.shortcuts import render
from .apis import Hotword, WordMap
from .apis import get_word_freq
from django.http import HttpResponse
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
            news_no2.append(query.news_id)
        standpoint_query = Standpoint.objects.filter(Q(new_id__in=news_no2))
        china = 0
        setn = 0
        for i in standpoint_query:
            if i.standpoint == 1:
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
    for da in alpha:
        for dq in [good_q, surprise_q, sad_q, fear_q, disgust_q, happy_q, anger_q]:
            tmp[da] = {
                        'title': dq.news.title,
                        'url'  : dq.news.url,
                        'score': [str(dq.good), str(dq.surprise), str(dq.sad), str(dq.fear),
                                  str(dq.disgust), str(dq.happy), str(dq.anger)]
                      }
    return HttpResponse(json.dumps(tmp))


def newsReview(request):
    keywordToday = KeywordThreeDay()
    keywords, relative_news = keywordToday.getGroupKeywords()

    mem, keyword_ls = keywordToday.genData(keywords, relative_news)

    for i, dm in enumerate(mem):
        rst = get_standpoint(keyword_ls[i]['relative_news'])
        dm.update(rst)

    return HttpResponse(json.dumps(mem))


def top20Keywords(request):
    global keywords
    global keywords_analysis
    global relative_wordCloud
    global relative_news
    if keywords == None:
        keywordToday = KeywordToday()
        # keywordToday.getWordFreq()
        keywords, relative_news = keywordToday.getGroupKeywords()
        # df = keywordToday.getNewHotword()

    return HttpResponse(json.dumps(keywords))


def keywordAnalysis(request, word):
    global keywords_analysis
    global relative_wordCloud
    global keywords
    global relative_news
    if keywords_analysis == None:
        keywordToday = KeywordToday()
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
    if relative_wordCloud == None:
        keywordToday = KeywordToday()
        # keywordToday.getWordFreq()
        keywords, relative_news = keywordToday.getGroupKeywords()
        # df = keywordToday.getNewHotword()
    keywords_analysis, relative_wordCloud = keywordToday.genData(word, relative_news)

    return HttpResponse(json.dumps(relative_wordCloud))

def mediaAnalysis(requeset):
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
        news_query2 = Standpoint.objects.filter(Q(news__in=news_no))
        china = 0
        setn = 0
        for i in news_query2:
            if i.standpoint == 1:
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