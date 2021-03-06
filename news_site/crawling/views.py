from django.shortcuts import render
from django.http import HttpResponse
from crawling.apis import ltn_crawling, nowNews_crawling, pts_crawling, udn_crawling, cts_crawling, ftvnews_crawling
from newsdb.models import Subject, Brand, Brand_sub
from multiprocessing import Pool
from newsdb.serializers import NewSerializer
# Create your views here.

def test_ltn_crawling(request):
    c = ltn_crawling()
    # data = c.getNews(date='all')
    data = c.getNewsToday()
    result = c.insertNews(data)
    return HttpResponse(data)

def test_nowNews_crawling(request):
    c = nowNews_crawling()
    # data = c.getNews(date=)
    data = c.getNewsToday()
    result = c.insertNews(data)
    return HttpResponse(data[:500])

def test_pts_crawling(request):
    c = pts_crawling()
    data = c.getNews(date='all')
    result = c.insertNews(data)
    return HttpResponse(data)

def test_udn_crawling(request):
    c = udn_crawling()
    data = c.getNews(date=['2020-03-05', '2020-03-06', '2020-03-07'])
    # data = c.getNewsToday()
    # result = c.insertNews(data)
    return HttpResponse(data)

def test_cts_crawling(request):
    c = cts_crawling()
    data = c.getNews(date=['2020-03-05', '2020-03-06', '2020-03-07'])
    result = c.insertNews(data)
    return HttpResponse(data)

def test_ftvnews_crawling(request):
    c = ftvnews_crawling()
    data = c.getNews(date=['2020-03-05', '2020-03-06', '2020-03-07'])
    result = c.insertNews(data)
    return HttpResponse(data)

def todayNews_crawling(request):
    ls = [
        ltn_crawling(),
        nowNews_crawling(),
        pts_crawling(),
        udn_crawling(),
        ftvnews_crawling()
    ]

    for i in ls:
        data = i.getNewsToday()
        for j in data:
            n = NewSerializer(data=j)
            try:
                if not n.is_valid():
                    raise ValueError
            except ValueError:
                print(n.errors)
                pass
        # result = i.insertNews(data)

    return HttpResponse(True)
