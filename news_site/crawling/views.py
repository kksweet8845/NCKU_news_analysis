from django.shortcuts import render
from django.http import HttpResponse
from .api import ltn_crawling
from .api_SETN import SETNCrawler
from .api_EBC import EBCCrawler
from .api_TVBS import TVBSCrawler
from .api_asahi import AsahiCrawler
from .api_CNA import CNACrawler
from .api_upmedia import UpmediaCrawler
from newsdb.models import Subject, Brand, Brand_sub
# Create your views here.

def test_ltn_crawling(request):
    c = ltn_crawling()
    data = c.getNews(date='all')
    result = c.insertNews(data)
    return HttpResponse(data)

def test_SETN_craling(request):
    crawler = SETNCrawler()
    subURL = crawler.getSubjectUrl()
    newsToday = crawler.getNewsToday(subURL)
    result = crawler.insertNews(newsToday)
    return HttpResponse(newsToday)

def test_EBC_craling(request):
    crawler = EBCCrawler()
    news_today = crawler.get_news_today()
    result = crawler.insert_news(news_today)
    return HttpResponse(news_today)

def test_Asahi_craling(request):
    crawler = AsahiCrawler()
    news_today = crawler.get_news_today()
    result = crawler.insert_news(news_today)
    return HttpResponse(news_today)

def test_TVBS_craling(request):
    crawler = TVBSCrawler()
    news_today = crawler.get_news_today()
    result = crawler.insert_news(news_today)
    return HttpResponse(news_today)

def test_Upmedia_craling(request):
    crawler = UpmediaCrawler()
    news_today = crawler.get_news_today()
    result = crawler.insert_news(news_today)
    return HttpResponse(news_today)