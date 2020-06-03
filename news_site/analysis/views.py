from django.shortcuts import render
from .apis import Hotword, WordMap
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q
import json
from multiprocessing import Pool
import pandas as pd
from tqdm import tqdm
import numpy as np
from newsdb.models import Word
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
            'title': '屏榮高中陳守心錄取醫學系 盼未來結合興趣回饋部落',
            'score': [400, 430, 448, 470, 540, 1200, 1380],
        },
        'b': {
            'title': '北市助攻都會農友 讓農業變有趣又吸睛',
            'score': [400, 430, 448, 470, 540, 200, 1380],
        },
        'c': {
            'title': '新冠肺炎燒三個月 來台觀光收益損近千億元',
            'score': [400, 430, 448, 1470, 540, 1200, 380],
        },
        'e': {
            'title': '50公斤「世界最胖山貓」大叔照爆紅 因心臟病死亡',
            'score': [400, 430, 448, 470, 540, 1200, 1380],
        },
        'f': {
            'title': '屏榮高中陳守心錄取醫學系 盼未來結合興趣回饋部落',
            'score': [1400, 430, 448, 470, 540, 200, 380],
        },
        'g': {
            'title': '屏榮高中陳守心錄取醫學系 盼未來結合興趣回饋部落',
            'score': [400, 430, 1048, 470, 540, 100, 130],
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