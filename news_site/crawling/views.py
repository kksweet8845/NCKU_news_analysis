# local Django
from newsdb.models import Subject, Brand, Brand_sub, New

# Django
from django.shortcuts import render
from django.http import HttpResponse

# foregin media
#from crawling.foreign_news_apis import *

# dimestic media
from crawling.dimestic_news_apis import *

from crawling.apis import ltn_crawling, nowNews_crawling, pts_crawling, udn_crawling, cts_crawling, ftvnews_crawling
from newsdb.models import Subject, Brand, Brand_sub
from multiprocessing import Pool
from newsdb.serializers import NewSerializer

from datetime import date
'''
def get_foreign_news_today(request):
    apis = [
        AljazeeraCrawler,
        RFICrawler,
        BBCCrawler,
        NYTCrawler,
        FTCrawler,
        AsahiCrawler,
        SputniknewsCrawler,
        JoongAngCrawler,
        EpochTimesCrawler,
        HuanqiuCrawler
    ]

    for api in apis:
        try:
            crawler = api()
            news_today = crawler.get_news_today()
            result = crawler.insert_news(news_today)
            crawler.get_news_headline()
        except Exception as e:
            print(e)
            print('error in crawler')
            continue

    return HttpResponse(True)

def get_dimestic_news_today(request):
    apis = [
        SETNCrawler,
        CNACrawler,
        EBCCrawler,
        NewtalkCrawler,
        TVBSCrawler,
        UpmediaCrawler,
        StormCrawler,
        ChinatimesCrawler,
    ]

    for api in apis:
        try:
            crawler = api()
            news_today = crawler.get_news_today()
            result = crawler.insert_news(news_today)

            print('successful')
        except Exception as e:
            print(e)
            print('error in crawler')
            continue

    return HttpResponse(True)
'''
def test_ltn_crawling(request):
    c = ltn_crawling()
    print(date.today().isoformat())
    data = c.getNews(date=[date.today().isoformat()])
    # data = c.getNewsToday()
    errors = []
    for j in data:
            n = NewSerializer(data=j)
            try:
                if not n.is_valid():
                    raise ValueError
                # n.save()
            except ValueError:
                errors.append({'error': n.errors, 'data': n.data})
                pass
    # result = c.insertNews(data)
    return HttpResponse([errors, data])

def test_nowNews_crawling(request):
    c = nowNews_crawling()
    data = c.getNews(date=[date.today().isoformat()])
    errors = []
    for j in data:
            n = NewSerializer(data=j)
            try:
                if not n.is_valid():
                    raise ValueError
            except ValueError:
                errors.append({'error': n.errors, 'data': n.data})
                pass
    # result = c.insertNews(data)
    return HttpResponse([data, errors])

def test_pts_crawling(request):
    c = pts_crawling()
    data = c.getNews(date=['2020-06-01', '2020-05-31', '2020-05-30', '2020-05-29'])
    errors = []
    for j in data:
            n = NewSerializer(data=j)
            try:
                if not n.is_valid():
                    raise ValueError
            except ValueError:
                errors.append({'error': n.errors, 'data': n.data})
                pass
    # result = c.insertNews(data)
    return HttpResponse([data])

def test_udn_crawling(request):
    c = udn_crawling()
    data = c.getNews(date=['2020-04-24'])
    errors = []
    for j in data:
            n = NewSerializer(data=j)
            try:
                if not n.is_valid():
                    raise ValueError
            except ValueError:
                errors.append({'error': n.errors, 'data': n.data})
                pass
    # result = c.insertNews(data)
    return HttpResponse([data, errors])

def test_cts_crawling(request):
    c = cts_crawling()
    data = c.getNews(date=['2020-04-24'])
    errors = []
    for j in data:
            n = NewSerializer(data=j)
            try:
                if not n.is_valid():
                    raise ValueError
            except ValueError:
                errors.append({'error': n.errors, 'data': n.data})
                pass
    # result = c.insertNews(data)
    return HttpResponse([data, errors])

def test_chinatimes_crawling(request):
    c = TVBSCrawler()
    # data = c.get_news_today()
    data = c.get_news_by_date(date_list=['2020-03-26'])
    result = c.insert_news(data)
    # data = c.get_news_headline()
    return HttpResponse(data)

def test_ftvnews_crawling(request):
    c = ftvnews_crawling()
    data = c.getNews(date=['2020-04-24'])
    errors = []
    for j in data:
            n = NewSerializer(data=j)
            try:
                if not n.is_valid():
                    raise ValueError
            except ValueError:
                errors.append({'error': n.errors, 'data': n.data})
                pass
    # result = c.insertNews(data)
    return HttpResponse([data, errors])

def todayNews_crawling(request):
    ls = [
        ltn_crawling(),
        nowNews_crawling(),
        udn_crawling(),
        ftvnews_crawling(),
        pts_crawling(),
        cts_crawling()
    ]
    errors = []
    for i in ls:
        print('='*150)
        data = i.getNews(date=[date.today().isoformat()])
        for j in data:
            n = NewSerializer(data=j)
            try:
                if not n.is_valid():
                    raise ValueError
            except ValueError:
                errors.append({'error': n.errors, 'data': n.data})
                pass
        # result = i.insertNews(data)
    return HttpResponse(errors)
