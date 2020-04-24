from newsdb.models import New, Subject, Brand, Brand_sub
import requests
from bs4 import BeautifulSoup as bs
import json, os, re
from datetime import date, datetime
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
            a_tag = x.select('a')[0]
            title = a_tag.get_text()
            time = x.select('div.sweet-info span:last-child')[0]
            return (a_tag.attrs['href'], title, time.get_text())
        except AttributeError:
            print('error')
            return (None, None, None)
            # return (x.attrs['href'], x.get_text())


    def request_newsUrl(self, url, type_cn, date):
        ls = []
        res = requests.get(url)
        soup = bs(res.text, 'html.parser')
        contents = soup.select('div.news-right-list')
        contents = list(map(self.fn, contents))
        for i in contents:
            time = datetime.strptime(i[2], '%Y-%m-%d')
            if time < date[0]:
                break
            if date == 'all':
                ls.append({
                        'url': i[0],
                        'title': i[1],
                        'date': i[2],
                        'sub': self.sub.get(sub_name=type_cn)
                    })
            else:
                for dt in date:
                    if dt.year == time.year and dt.month == time.month and dt.day == time.day:
                        ls.append({
                            'url': i[0],
                            'title': i[1],
                            'date': i[2],
                            'sub': self.sub.get(sub_name=type_cn)
                        })
                        break
        return ls

    def request_subCategory(self, url):
        res = requests.get(url)
        soup = bs(res.text, 'html.parser')
        contents = soup.select('div.more > a')
        contents = list(map(lambda x: x.attrs['href'], contents))
        return contents

    def aux_request_ajax(self, cid, type_cn, i, date):
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
                time = datetime.strptime(dn['news_date'], '%Y-%m-%d')
                if time < date[0]:
                    break
                if date == 'all':
                    ls.append({
                            'url': 'https://news.pts.org.tw/article/'+dn['news_id'],
                            'title': dn['subject'],
                            'date': dn['news_date'],
                            'sub': self.sub.get(sub_name=type_cn)
                        })
                else:
                    for dt in date:
                        if dt.year == time.year and dt.month == time.month and dt.day == time.day:
                            ls.append({
                                'url': 'https://news.pts.org.tw/article/'+dn['news_id'],
                                'title': dn['subject'],
                                'date': dn['news_date'],
                                'sub': self.sub.get(sub_name=type_cn)
                            })
                            break
        except:
            return None
        return ls

    def request_ajax(self, cid, type_cn, date):
        ls = []
        result = []
        pool = ThreadPool(processes=4)
        for i in range(1, 10):
            ls.append(pool.apply_async(self.aux_request_ajax, (cid, type_cn, i, date)))

        for i in ls:
            tmp = i.get()
            if tmp != None:
                result.extend(tmp)
        return result


    def crawl_newsUrl(self, date, type_cn=''):
        """ """
        newsUrl = []
        ls = []
        pool = Pool(processes=12)
        if date != 'all':
            print(date)
            date_obj = [datetime.strptime(i, '%Y-%m-%d') for i in date]
        else:
            date_obj = date
        for dm in tqdm(self.menuList, total=len(self.menuList), desc="L1"):
            try:
                links = dm['link']
            except:
                links = dm['sub_link']
            for index_url in tqdm(links, total=len(links), desc="L2"):
                sub_category = self.request_subCategory(index_url)
                for dnewsUrl in tqdm(sub_category, total=len(sub_category), desc="L3"):
                    cid = dnewsUrl.split('/')[-1]
                    ls.append(pool.apply_async(self.request_newsUrl, (dnewsUrl, dm['name'], date_obj)))
                    ls.append(pool.apply_async(self.request_ajax, (cid, dm['name'], date_obj)))
        for i in tqdm(ls, total=len(ls)):
            newsUrl.extend(i.get())
        self.newsUrl = newsUrl


    def request_newsContent(self, data):
        """ """
        dn = data
        news = requests.get(dn['url'])
        news_soup = bs(news.content, 'html.parser')
        article = news_soup.select('div.article_content')[0].get_text()
        author = news_soup.select('div.subtype-sort')[0].get_text()
        return {
            'title': dn['title'],
            'content': article,
            'author': author if len(author) != 0 else "None",
            'brand': self.brand,
            'sub': dn['sub'],
            'date': dn['date'],
            'url': dn['url']
        }

    def crawl_newsContent(self, date=[date.today().isoformat()]):
        """ """
        pool = Pool(processes=8)
        final_news = []
        ls = []
        for dn in tqdm(self.newsUrl, total=len(self.newsUrl)):
            if date =='all' or dn['date'] in date:
                ls.append(pool.apply_async(self.request_newsContent, (dn, )))

        for i in tqdm(ls, total=len(ls)):
            tmp = i.get()
            final_news.append(tmp)
        return final_news

    def getNews(self, date=[date.today().isoformat()]):
        """ """
        self.crawl_newsUrl(date)
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