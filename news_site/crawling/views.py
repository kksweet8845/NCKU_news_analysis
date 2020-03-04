from django.shortcuts import render
from django.http import HttpResponse
from crawling.apis import ltn_crawling, nowNews_crawling, pts_crawling, udn_crawling, cts_crawling
from newsdb.models import Subject, Brand, Brand_sub
# Create your views here.

def test_ltn_crawling(request):
    c = ltn_crawling()
    # data = c.getNews(date='all')
    data = c.getNewsToday()
    # result = c.insertNews(data)
    return HttpResponse(data)

def test_nowNews_crawling(request):
    c = nowNews_crawling()
    data = c.getNews(date='all')
    result = c.insertNews(data)
    return HttpResponse(data[:500])

def test_pts_crawling(request):
    c = pts_crawling()
    data = c.getNews(date='all')
    return HttpResponse(data)

def test_udn_crawling(request):
    c = udn_crawling()
    data = c.getNews(date='all')
    return HttpResponse(data)

def test_cts_crawling(request):
    c = cts_crawling()
    data = c.getNews(date='all')
    return HttpResponse(data)
