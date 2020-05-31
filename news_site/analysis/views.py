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
from newsdb.models import Word, standpoint, sentiment, cluster_day, Aspect
from datetime import datetime, timedelta
# Create your views here.

# hd = Hotword()
# hd.fetch_news([Q(date__gte=datetime.today() - timedelta(days=28)) , Q(brand_id=11) , Q(sub_id=2),])
# data = hd.get_hotword(20)
# keyBrand = hd.gen_keyBrand()
# brandKey = hd.gen_branKey()

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

    keywords, relative_news = get_word_freq([Q(date__lt='2020-05-21'), Q(date__gt='2020-05-13'), Q(brand_id=10) | Q(brand_id=18)])

    return HttpResponse(json.dumps(relative_news))

def get_sentiment(request):
    news_query = sentiment.objects.filter(Q(date__gte='2020-05-30'))
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

def get_standpoint(request, relative_news):
    news_query = standpoint.objects.filter(Q(news__in=relative_news))
    china = 0
    setn = 0
    for i in news_query:
        if i.standpoint == 1:
            china += 1
        else:
            setn += 1
    
    news_query2 = Aspect.objects.filter(Q(news__in=relative_news))
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

    return HttpResponse(json.dumps(return_dict))
    
def get_cluster(request):
    
    pass


        