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

def testMedia(request):
    obj = {
        '1': {'name': 'TVBS', 
            'news_number': 3000,
            'sentiment': [44, 55, 41],
            'standpoint': [44, 55],
            'focus_news': [[{'title': '發票沒中卻爽拿2千獎金　真相驚呆眾人：竟還有此招', 'href': 'https://news.tvbs.com.tw/life/1331355?from=Popular_txt_click'},
                            {'title': '隔35天IG再發文！羅志祥「特別致謝2人」讚數破萬', 'href': 'https://news.tvbs.com.tw/entertainment/1331806?from=Popular_txt_click'},
                            {'title': '又是QR818班機！　83乘客16人染新冠肺炎', 'href': 'https://news.tvbs.com.tw/world/1332213?from=Popular_txt_click'}],
                            [{'title': '拒出席罷韓說明會！韓國瑜勘農損、跑市政對抗', 'href': 'https://news.tvbs.com.tw/politics/1331974'},
                            {'title': '謝立功將接民眾黨秘書長　國民黨：不排除開除黨籍', 'href': 'https://news.tvbs.com.tw/politics/1332139'},
                            {'title': '罷韓倒數「冷處理」　韓國瑜曝心境：相信市民', 'href': 'https://news.tvbs.com.tw/politics/1332298'}]]
        },
        '4': {'name': '三立',
            'news_number': 2000,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{'title': '1發票沒中卻爽拿2千獎金　真相驚呆眾人：竟還有此招', 'href': 'https://news.tvbs.com.tw/life/1331355?from=Popular_txt_click'},
                            {'title': '1隔35天IG再發文！羅志祥「特別致謝2人」讚數破萬', 'href': 'https://news.tvbs.com.tw/entertainment/1331806?from=Popular_txt_click'},
                            {'title': '1又是QR818班機！　83乘客16人染新冠肺炎', 'href': 'https://news.tvbs.com.tw/world/1332213?from=Popular_txt_click'}],
                            [{'title': '1拒出席罷韓說明會！韓國瑜勘農損、跑市政對抗', 'href': 'https://news.tvbs.com.tw/politics/1331974'},
                            {'title': '1謝立功將接民眾黨秘書長　國民黨：不排除開除黨籍', 'href': 'https://news.tvbs.com.tw/politics/1332139'},
                            {'title': '1罷韓倒數「冷處理」　韓國瑜曝心境：相信市民', 'href': 'https://news.tvbs.com.tw/politics/1332298'}]]
        },
        '5': {'name': '上報',
            'news_number': 1000,
            'sentiment': [91, 25, 11],
            'standpoint': [25, 74],
            'focus_news': [[{'title': '2發票沒中卻爽拿2千獎金　真相驚呆眾人：竟還有此招', 'href': 'https://news.tvbs.com.tw/life/1331355?from=Popular_txt_click'},
                            {'title': '2隔35天IG再發文！羅志祥「特別致謝2人」讚數破萬', 'href': 'https://news.tvbs.com.tw/entertainment/1331806?from=Popular_txt_click'},
                            {'title': '2又是QR818班機！　83乘客16人染新冠肺炎', 'href': 'https://news.tvbs.com.tw/world/1332213?from=Popular_txt_click'}],
                            [{'title': '2拒出席罷韓說明會！韓國瑜勘農損、跑市政對抗', 'href': 'https://news.tvbs.com.tw/politics/1331974'},
                            {'title': '2謝立功將接民眾黨秘書長　國民黨：不排除開除黨籍', 'href': 'https://news.tvbs.com.tw/politics/1332139'},
                            {'title': '2罷韓倒數「冷處理」　韓國瑜曝心境：相信市民', 'href': 'https://news.tvbs.com.tw/politics/1332298'}]]
        },
        '7': {'name': '三立',
            'news_number': 7,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{'title': '發票沒中卻爽拿2千獎金　真相驚呆眾人：竟還有此招', 'href': 'https://news.tvbs.com.tw/life/1331355?from=Popular_txt_click'},
                            {'title': '隔35天IG再發文！羅志祥「特別致謝2人」讚數破萬', 'href': 'https://news.tvbs.com.tw/entertainment/1331806?from=Popular_txt_click'},
                            {'title': '又是QR818班機！　83乘客16人染新冠肺炎', 'href': 'https://news.tvbs.com.tw/world/1332213?from=Popular_txt_click'}],
                            [{'title': '拒出席罷韓說明會！韓國瑜勘農損、跑市政對抗', 'href': 'https://news.tvbs.com.tw/politics/1331974'},
                            {'title': '謝立功將接民眾黨秘書長　國民黨：不排除開除黨籍', 'href': 'https://news.tvbs.com.tw/politics/1332139'},
                            {'title': '罷韓倒數「冷處理」　韓國瑜曝心境：相信市民', 'href': 'https://news.tvbs.com.tw/politics/1332298'}]]
        },
        '8': {'name': '三立',
            'news_number': 8,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{'title': '發票沒中卻爽拿2千獎金　真相驚呆眾人：竟還有此招', 'href': 'https://news.tvbs.com.tw/life/1331355?from=Popular_txt_click'},
                            {'title': '隔35天IG再發文！羅志祥「特別致謝2人」讚數破萬', 'href': 'https://news.tvbs.com.tw/entertainment/1331806?from=Popular_txt_click'},
                            {'title': '又是QR818班機！　83乘客16人染新冠肺炎', 'href': 'https://news.tvbs.com.tw/world/1332213?from=Popular_txt_click'}],
                            [{'title': '拒出席罷韓說明會！韓國瑜勘農損、跑市政對抗', 'href': 'https://news.tvbs.com.tw/politics/1331974'},
                            {'title': '謝立功將接民眾黨秘書長　國民黨：不排除開除黨籍', 'href': 'https://news.tvbs.com.tw/politics/1332139'},
                            {'title': '罷韓倒數「冷處理」　韓國瑜曝心境：相信市民', 'href': 'https://news.tvbs.com.tw/politics/1332298'}]]
        },
        '9': {'name': '三立',
            'news_number': 9,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{'title': '發票沒中卻爽拿2千獎金　真相驚呆眾人：竟還有此招', 'href': 'https://news.tvbs.com.tw/life/1331355?from=Popular_txt_click'},
                            {'title': '隔35天IG再發文！羅志祥「特別致謝2人」讚數破萬', 'href': 'https://news.tvbs.com.tw/entertainment/1331806?from=Popular_txt_click'},
                            {'title': '又是QR818班機！　83乘客16人染新冠肺炎', 'href': 'https://news.tvbs.com.tw/world/1332213?from=Popular_txt_click'}],
                            [{'title': '拒出席罷韓說明會！韓國瑜勘農損、跑市政對抗', 'href': 'https://news.tvbs.com.tw/politics/1331974'},
                            {'title': '謝立功將接民眾黨秘書長　國民黨：不排除開除黨籍', 'href': 'https://news.tvbs.com.tw/politics/1332139'},
                            {'title': '罷韓倒數「冷處理」　韓國瑜曝心境：相信市民', 'href': 'https://news.tvbs.com.tw/politics/1332298'}]]
        },
        '11': {'name': '三立',
            'news_number': 11,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{'title': '發票沒中卻爽拿2千獎金　真相驚呆眾人：竟還有此招', 'href': 'https://news.tvbs.com.tw/life/1331355?from=Popular_txt_click'},
                            {'title': '隔35天IG再發文！羅志祥「特別致謝2人」讚數破萬', 'href': 'https://news.tvbs.com.tw/entertainment/1331806?from=Popular_txt_click'},
                            {'title': '又是QR818班機！　83乘客16人染新冠肺炎', 'href': 'https://news.tvbs.com.tw/world/1332213?from=Popular_txt_click'}],
                            [{'title': '拒出席罷韓說明會！韓國瑜勘農損、跑市政對抗', 'href': 'https://news.tvbs.com.tw/politics/1331974'},
                            {'title': '謝立功將接民眾黨秘書長　國民黨：不排除開除黨籍', 'href': 'https://news.tvbs.com.tw/politics/1332139'},
                            {'title': '罷韓倒數「冷處理」　韓國瑜曝心境：相信市民', 'href': 'https://news.tvbs.com.tw/politics/1332298'}]]
        },
        '12': {'name': '三立',
            'news_number': 12,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{'title': '發票沒中卻爽拿2千獎金　真相驚呆眾人：竟還有此招', 'href': 'https://news.tvbs.com.tw/life/1331355?from=Popular_txt_click'},
                            {'title': '隔35天IG再發文！羅志祥「特別致謝2人」讚數破萬', 'href': 'https://news.tvbs.com.tw/entertainment/1331806?from=Popular_txt_click'},
                            {'title': '又是QR818班機！　83乘客16人染新冠肺炎', 'href': 'https://news.tvbs.com.tw/world/1332213?from=Popular_txt_click'}],
                            [{'title': '拒出席罷韓說明會！韓國瑜勘農損、跑市政對抗', 'href': 'https://news.tvbs.com.tw/politics/1331974'},
                            {'title': '謝立功將接民眾黨秘書長　國民黨：不排除開除黨籍', 'href': 'https://news.tvbs.com.tw/politics/1332139'},
                            {'title': '罷韓倒數「冷處理」　韓國瑜曝心境：相信市民', 'href': 'https://news.tvbs.com.tw/politics/1332298'}]]
        },
        '13': {'name': '三立',
            'news_number': 13,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{'title': '發票沒中卻爽拿2千獎金　真相驚呆眾人：竟還有此招', 'href': 'https://news.tvbs.com.tw/life/1331355?from=Popular_txt_click'},
                            {'title': '隔35天IG再發文！羅志祥「特別致謝2人」讚數破萬', 'href': 'https://news.tvbs.com.tw/entertainment/1331806?from=Popular_txt_click'},
                            {'title': '又是QR818班機！　83乘客16人染新冠肺炎', 'href': 'https://news.tvbs.com.tw/world/1332213?from=Popular_txt_click'}],
                            [{'title': '拒出席罷韓說明會！韓國瑜勘農損、跑市政對抗', 'href': 'https://news.tvbs.com.tw/politics/1331974'},
                            {'title': '謝立功將接民眾黨秘書長　國民黨：不排除開除黨籍', 'href': 'https://news.tvbs.com.tw/politics/1332139'},
                            {'title': '罷韓倒數「冷處理」　韓國瑜曝心境：相信市民', 'href': 'https://news.tvbs.com.tw/politics/1332298'}]]
        },
        '14': {'name': '三立',
            'news_number': 14,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{'title': '發票沒中卻爽拿2千獎金　真相驚呆眾人：竟還有此招', 'href': 'https://news.tvbs.com.tw/life/1331355?from=Popular_txt_click'},
                            {'title': '隔35天IG再發文！羅志祥「特別致謝2人」讚數破萬', 'href': 'https://news.tvbs.com.tw/entertainment/1331806?from=Popular_txt_click'},
                            {'title': '又是QR818班機！　83乘客16人染新冠肺炎', 'href': 'https://news.tvbs.com.tw/world/1332213?from=Popular_txt_click'}],
                            [{'title': '拒出席罷韓說明會！韓國瑜勘農損、跑市政對抗', 'href': 'https://news.tvbs.com.tw/politics/1331974'},
                            {'title': '謝立功將接民眾黨秘書長　國民黨：不排除開除黨籍', 'href': 'https://news.tvbs.com.tw/politics/1332139'},
                            {'title': '罷韓倒數「冷處理」　韓國瑜曝心境：相信市民', 'href': 'https://news.tvbs.com.tw/politics/1332298'}]]
        },
        '15': {'name': '三立',
            'news_number': 15,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{'title': '發票沒中卻爽拿2千獎金　真相驚呆眾人：竟還有此招', 'href': 'https://news.tvbs.com.tw/life/1331355?from=Popular_txt_click'},
                            {'title': '隔35天IG再發文！羅志祥「特別致謝2人」讚數破萬', 'href': 'https://news.tvbs.com.tw/entertainment/1331806?from=Popular_txt_click'},
                            {'title': '又是QR818班機！　83乘客16人染新冠肺炎', 'href': 'https://news.tvbs.com.tw/world/1332213?from=Popular_txt_click'}],
                            [{'title': '拒出席罷韓說明會！韓國瑜勘農損、跑市政對抗', 'href': 'https://news.tvbs.com.tw/politics/1331974'},
                            {'title': '謝立功將接民眾黨秘書長　國民黨：不排除開除黨籍', 'href': 'https://news.tvbs.com.tw/politics/1332139'},
                            {'title': '罷韓倒數「冷處理」　韓國瑜曝心境：相信市民', 'href': 'https://news.tvbs.com.tw/politics/1332298'}]]
        },
        '16': {'name': '三立',
            'news_number': 16,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{'title': '發票沒中卻爽拿2千獎金　真相驚呆眾人：竟還有此招', 'href': 'https://news.tvbs.com.tw/life/1331355?from=Popular_txt_click'},
                            {'title': '隔35天IG再發文！羅志祥「特別致謝2人」讚數破萬', 'href': 'https://news.tvbs.com.tw/entertainment/1331806?from=Popular_txt_click'},
                            {'title': '又是QR818班機！　83乘客16人染新冠肺炎', 'href': 'https://news.tvbs.com.tw/world/1332213?from=Popular_txt_click'}],
                            [{'title': '拒出席罷韓說明會！韓國瑜勘農損、跑市政對抗', 'href': 'https://news.tvbs.com.tw/politics/1331974'},
                            {'title': '謝立功將接民眾黨秘書長　國民黨：不排除開除黨籍', 'href': 'https://news.tvbs.com.tw/politics/1332139'},
                            {'title': '罷韓倒數「冷處理」　韓國瑜曝心境：相信市民', 'href': 'https://news.tvbs.com.tw/politics/1332298'}]]
        },
        '18': {'name': '三立',
            'news_number': 18,
            'sentiment': [14, 85, 41],
            'standpoint': [90, 15],
            'focus_news': [[{'title': '發票沒中卻爽拿2千獎金　真相驚呆眾人：竟還有此招', 'href': 'https://news.tvbs.com.tw/life/1331355?from=Popular_txt_click'},
                            {'title': '隔35天IG再發文！羅志祥「特別致謝2人」讚數破萬', 'href': 'https://news.tvbs.com.tw/entertainment/1331806?from=Popular_txt_click'},
                            {'title': '又是QR818班機！　83乘客16人染新冠肺炎', 'href': 'https://news.tvbs.com.tw/world/1332213?from=Popular_txt_click'}],
                            [{'title': '拒出席罷韓說明會！韓國瑜勘農損、跑市政對抗', 'href': 'https://news.tvbs.com.tw/politics/1331974'},
                            {'title': '謝立功將接民眾黨秘書長　國民黨：不排除開除黨籍', 'href': 'https://news.tvbs.com.tw/politics/1332139'},
                            {'title': '罷韓倒數「冷處理」　韓國瑜曝心境：相信市民', 'href': 'https://news.tvbs.com.tw/politics/1332298'}]]
        },        
    }

    return JsonResponse(obj, safe=False)

def testMediaReport(request):
    obj = {
        'labels': ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        'series': [44, 55, 41, 67, 22, 43, 44, 55, 41, 67, 22, 43],
    }

    return JsonResponse(obj, safe=False)