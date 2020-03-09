# local Django
from newsdb.models import Subject, Brand, Brand_sub
from django.shortcuts import render
from django.http import HttpResponse

# foregin media
from .api_aljazeera import AljazeeraCrawler
from .api_RFI       import RFICrawler
from .api_BBC       import BBCCrawler
from .api_NYT       import NYTCrawler
from .api_FT        import FTCrawler
from .api_asahi       import AsahiCrawler
from .api_sputniknews import SputniknewsCrawler
from .api_JoongAng    import JoongAngCrawler
from .api_huanqiu     import HuanqiuCrawler
from .api_epochtimes  import EpochTimesCrawler

# dimestic media
from .api import ltn_crawling
from .api_SETN import SETNCrawler
from .api_EBC import EBCCrawler
from .api_TVBS import TVBSCrawler
from .api_CNA import CNACrawler
from .api_upmedia import UpmediaCrawler

def get_foregin_news_today(request):
    apis = [
        EpochTimesCrawler,
        AljazeeraCrawler,
        RFICrawler,
        BBCCrawler,
        NYTCrawler,
        FTCrawler,
        AsahiCrawler,
        SputniknewsCrawler,
        JoongAngCrawler,
        HuanqiuCrawler
    ]

    for api in apis:
        try:
            crawler = api()
            news_today = crawler.get_news_today()
            result = crawler.insert_news(news_today)
        except Exception as e:
            print(e)
            print('error in crawler')
            continue

    return HttpResponse(True)

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

def test_Sputniknews_craling(request):
    crawler = SputniknewsCrawler()
    news_today = crawler.get_news_today()
    result = crawler.insert_news(news_today)
    return HttpResponse(news_today)

def test_JoongAng_craling(request):
    crawler = JoongAngCrawler()
    news_today = crawler.get_news_today()
    result = crawler.insert_news(news_today)
    return HttpResponse(news_today)

def test_Huanqiu_craling(request):
    crawler = HuanqiuCrawler()
    news_today = crawler.get_news_today()
    result = crawler.insert_news(news_today)
    return HttpResponse(news_today)