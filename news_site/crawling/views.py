# local Django
from newsdb.models import Subject, Brand, Brand_sub, New

# Django
from django.shortcuts import render
from django.http import HttpResponse

# foregin media
from crawling.foreign_news_apis import *

# dimestic media
from crawling.dimestic_news_apis import *

from crawling.apis import ltn_crawling, nowNews_crawling, pts_crawling, udn_crawling, cts_crawling, ftvnews_crawling
from newsdb.models import Subject, Brand, Brand_sub
from multiprocessing import Pool
from newsdb.serializers import NewSerializer

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

def test_chinatimes_crawling(request):
    c = TVBSCrawler()
    # data = c.get_news_today()
    data = c.get_news_by_date(date_list=['2020-03-26'])
    result = c.insert_news(data)
    # data = c.get_news_headline()
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
