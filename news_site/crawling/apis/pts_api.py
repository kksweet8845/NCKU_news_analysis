from newsdb.models import New, Subject, Brand, Brand_sub
import requests
from bs4 import BeautifulSoup as bs
import json, os, re
from datetime import date
from tqdm import tqdm
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool


class pts_crawling:
    brand_name = "公視"
    brand_url = "https://news.pts.org.tw/"
    brand_ID = 10
    menuList = [
        {
            'name': '政治',
            'link': [
                'https://news.pts.org.tw/category/2'
            ]
        },
        {
            'name': '國際',
            'link': [
                'https://news.pts.org.tw/category/4',
            ]
        },
        {
            'name': '生活',
            'link': [
                'https://news.pts.org.tw/category/5'
            ]
        },
        {
            'name': '社會',
            'link': [
                'https://news.pts.org.tw/category/7'
            ]
        },
        {
            'name': '體育',
            'sub_link':[
                'https://news.pts.org.tw/subcategory/154'
            ]
        }
    ]

    def __init__(self):
        self.brand = Brand.objects.get(id=self.brand_ID)
        self.sub = Subject.objects.all()
        pass

    def insertSubjectUrl(self):
        """ """
        for di in self.menuList:
            tmp_sub = self.sub.get(sub_name=di['name'])
            try:
                links = di['link']
            except:
                links = di['sub_link']
            for dl in links:
                data = {
                    'sub': tmp_sub,
                    'brand': self.brand,
                    'index_href': dl,
                    'ajax_href': dl
                }
                try:
                    bs = Brand_sub(**data)
                    bs.save()
                except:
                    print(bs)
                    return False
        return True


    def fn(self, x):
        try:
            return (x.attrs['href'], x.span.get_text())
        except AttributeError:
            return (x.attrs['href'], x.get_text())


    def request_newsUrl(self, url, type_cn):
        ls = []
        res = requests.get(url)
        soup = bs(res.text, 'html.parser')
        contents = soup.select('div.text-title > a')
        contents = list(map(self.fn, contents))
        for i in contents:
            ls.append({
                'url': i[0],
                'title': i[1],
                'sub': self.sub.get(sub_name=type_cn)
            })
        return ls

    def request_subCategory(self, url):
        res = requests.get(url)
        soup = bs(res.text, 'html.parser')
        contents = soup.select('div.more > a')
        contents = list(map(lambda x: x.attrs['href'], contents))
        return contents

    def aux_request_ajax(self, cid, type_cn, i):
        ls = []
        url = "https://news.pts.org.tw/subcategory/category_more.php"
        res = requests.post(url, data={
                'cid': cid,
                'page': i
            })
        try:
            res_json = json.loads(res.text)
            if len(res_json) == 0:
                return None
            for dn in res_json:
                ls.append({
                    'url': 'https://news.pts.org.tw/article/'+dn['news_id'],
                    'title': dn['subject'],
                    'sub': self.sub.get(sub_name=type_cn)
                })
        except:
            return None
        return ls

    def request_ajax(self, cid, type_cn):
        ls = []
        result = []
        pool = ThreadPool(processes=4)
        for i in range(1, 51):
            ls.append(pool.apply_async(self.aux_request_ajax, (cid, type_cn, i)))

        for i in ls:
            tmp = i.get()
            if tmp != None:
                result.extend(tmp)
        return result


    def crawl_newsUrl(self, type_cn=''):
        """ """
        newsUrl = []
        ls = []
        pool = Pool(processes=8)
        for dm in tqdm(self.menuList, total=len(self.menuList), desc="L1"):
            try:
                links = dm['link']
            except:
                links = dm['sub_link']
            for index_url in tqdm(links, total=len(links), desc="L2"):
                sub_category = self.request_subCategory(index_url)
                for dnewsUrl in tqdm(sub_category, total=len(sub_category), desc="L3"):
                    cid = dnewsUrl.split('/')[-1]
                    ls.append(pool.apply_async(self.request_newsUrl, (dnewsUrl, dm['name'])))
                    ls.append(pool.apply_async(self.request_ajax, (cid, dm['name'])))
        for i in tqdm(ls, total=len(ls)):
            newsUrl.extend(i.get())
        self.newsUrl = newsUrl


    def request_newsContent(self, data, date):
        """ """
        dn = data
        news = requests.get(dn['url'])
        news_soup = bs(news.content, 'html.parser')
        time = news_soup.select('div.maintype-wapper > h2')[0].get_text()
        time = re.sub(r'[年月]','-', time )
        time = re.sub(r'日','', time)
        if date == 'all' or time in date:
            article = news_soup.select('div.article_content')[0].get_text()
            author = news_soup.select('div.subtype-sort')[0].get_text()
            return {
                'title': dn['title'],
                'content': article,
                'author': author,
                'brand': self.brand,
                'sub': dn['sub'],
                'date': time,
                'url': dn['url']
            }
        else:
            return None

    def crawl_newsContent(self, date=[date.today().isoformat()]):
        """ """
        pool = Pool(processes=8)
        final_news = []
        ls = []
        for dn in tqdm(self.newsUrl, total=len(self.newsUrl)):
            ls.append(pool.apply_async(self.request_newsContent, (dn, date)))

        for i in tqdm(ls, total=len(ls)):
            tmp = i.get()
            if tmp != None:
                final_news.append(tmp)
        return final_news

    def getNews(self, date=[date.today().isoformat()]):
        """ """
        self.crawl_newsUrl()
        return self.crawl_newsContent(date=date)

    def getNewsToday(self):
        """ """
        return self.getNews(date=[date.today().isoformat()])

    def insertNews(self, news):
        """ """
        for dn in news:
            try:
                tmp = New(**dn)
                tmp.save()
            except:
                print(tmp)
        return True