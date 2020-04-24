from django.shortcuts import render
from django.http import HttpResponse
from crawling.apis import ltn_crawling, nowNews_crawling, pts_crawling, udn_crawling, cts_crawling, ftvnews_crawling
from newsdb.models import Subject, Brand, Brand_sub
from multiprocessing import Pool
from newsdb.serializers import NewSerializer
from datetime import datetime, date
# Create your views here.

def test_ltn_crawling(request):
    c = ltn_crawling()
    data = c.getNews(date=['2020-04-22'])
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
    return HttpResponse([errors])

def test_nowNews_crawling(request):
    c = nowNews_crawling()
    data = c.getNews(date=['2020-04-22'])
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
    data = c.getNews(date=['2020-03-29',
                           '2020-03-30',
                           '2020-03-31',
                           '2020-04-01',
                           '2020-04-02',
                           '2020-04-03',
                           '2020-04-04',
                           '2020-04-05',
                           '2020-04-06',
                           '2020-04-07',
                           '2020-04-08',
                           '2020-04-09',
                           '2020-04-10',
                           '2020-04-11',
                           '2020-04-12',
                           '2020-04-13',
                           '2020-04-14',
                           '2020-04-15',
                           '2020-04-16',
                           '2020-04-17',
                           '2020-04-18',
                           '2020-04-19',
                           '2020-04-20'])
    # errors = []
    # for j in data:
    #         n = NewSerializer(data=j)
    #         try:
    #             if not n.is_valid():
    #                 raise ValueError
    #         except ValueError:
    #             errors.append({'error': n.errors, 'data': n.data})
    #             pass
    result = c.insertNews(data)
    return HttpResponse([data])

def test_udn_crawling(request):
    c = udn_crawling()
    data = c.getNews(date=['2020-03-29',
                           '2020-03-30',
                           '2020-03-31',
                           '2020-04-01',
                           '2020-04-02',
                           '2020-04-03',
                           '2020-04-04',
                           '2020-04-05',
                           '2020-04-06',
                           '2020-04-07',
                           '2020-04-08',
                           '2020-04-09',
                           '2020-04-10',
                           '2020-04-11',
                           '2020-04-12',
                           '2020-04-13',
                           '2020-04-14',
                           '2020-04-15',
                           '2020-04-16',
                           '2020-04-17',
                           '2020-04-18',
                           '2020-04-19',
                           '2020-04-20'])
    errors = []
    # for j in data:
    #         n = NewSerializer(data=j)
    #         try:
    #             if not n.is_valid():
    #                 raise ValueError
    #         except ValueError:
    #             errors.append({'error': n.errors, 'data': n.data})
    #             pass
    result = c.insertNews(data)
    return HttpResponse([data, errors])

def test_cts_crawling(request):
    c = cts_crawling()
    data = c.getNews(date=['2020-03-29',
                           '2020-03-30',
                           '2020-03-31',
                           '2020-04-01',
                           '2020-04-02',
                           '2020-04-03',
                           '2020-04-04',
                           '2020-04-05',
                           '2020-04-06',
                           '2020-04-07',
                           '2020-04-08',
                           '2020-04-09',
                           '2020-04-10',
                           '2020-04-11',
                           '2020-04-12',
                           '2020-04-13',
                           '2020-04-14',
                           '2020-04-15',
                           '2020-04-16',
                           '2020-04-17',
                           '2020-04-18',
                           '2020-04-19',
                           '2020-04-20'])
    errors = []
    # for j in data:
    #         n = NewSerializer(data=j)
    #         try:
    #             if not n.is_valid():
    #                 raise ValueError
    #         except ValueError:
    #             errors.append({'error': n.errors, 'data': n.data})
    #             pass
    result = c.insertNews(data)
    return HttpResponse([data, errors])

def test_ftvnews_crawling(request):
    c = ftvnews_crawling()
    data = c.getNews(date=['2020-03-29',
                           '2020-03-30',
                           '2020-03-31',
                           '2020-04-01',
                           '2020-04-02',
                           '2020-04-03',
                           '2020-04-04',
                           '2020-04-05',
                           '2020-04-06',
                           '2020-04-07',
                           '2020-04-08',
                           '2020-04-09',
                           '2020-04-10',
                           '2020-04-11',
                           '2020-04-12',
                           '2020-04-13',
                           '2020-04-14',
                           '2020-04-15',
                           '2020-04-16',
                           '2020-04-17',
                           '2020-04-18',
                           '2020-04-19',
                           '2020-04-20'])
    errors = []
    # for j in data:
    #         n = NewSerializer(data=j)
    #         try:
    #             if not n.is_valid():
    #                 raise ValueError
    #         except ValueError:
    #             errors.append({'error': n.errors, 'data': n.data})
    #             pass
    result = c.insertNews(data)
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
