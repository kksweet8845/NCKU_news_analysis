from newsdb.models import Subject, Brand, Brand_sub, New, Word, Tagger, Aspect
# from ckiptagger import data_utils, construct_dictionary, WS, POS
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import numpy as np
import pandas as pd
import os, re
from django.conf import settings
from .hotword_v1 import Hotword
from datetime import date, timedelta, datetime
import pickle
from tqdm import tqdm
import json


class KeywordToday:
    def __init__(self):
        self.get20Group()
        self.util_path = settings.BASE_DIR + '/analysis/apis/utils/ckiptagger'
        self.util_count_path = settings.BASE_DIR + '/analysis/apis/utils/word_count'
        # self.ws = WS(self.util_path + '/data')
        # self.pos = POS(self.util_path + '/data')

    def get20Group(self):
        self.keywords_group = []

        for i in range(1, 20):
            self.keywords_group.append(New.objects.filter(cluster_day__cluster=i, cluster_day__date=(date.today() - timedelta(days=1)).isoformat()))

    def getWordFreq(self):

        news = New.objects.filter(cluster_day__date=(date.today() - timedelta(days=1)).isoformat() )

        if os.path.isfile(f'{self.util_count_path}/{(date.today() - timedelta(days=1)).isoformat()}.pkl'):
            with open(f'{self.util_count_path}/{(date.today() - timedelta(days=1)).isoformat()}.pkl', 'rb') as file:
                return pickle.load(file)

        # news = New.objects.filter(cluster_day__date='2020-05-30', cluster_day__cluster=1)
        df = self.preprocessing(news)

        # print(len(df))

        # word_ls = self.ws(df['content'])
        word_ls = [ json.loads(dtag.split) for dtag in Tagger.objects.filter(news_id__in=df['id'])]

        ls = []
        for dword in word_ls:
            ls.append(' '.join(word[0] for word in dword))
        # ls = [ self.tagger([content]) for content in tqdm(df['content']) ]

        # print(len(ls))
        vec = CountVectorizer()
        matrix = vec.fit_transform(ls)
        name = vec.get_feature_names()
        row, col = matrix.shape

        count = {}
        for dc in range(col):
            sum = 0
            for dr in range(row):
                sum += matrix[dr, dc]
            count[name[dc]] = sum

        with open(f'{self.util_count_path}/{(date.today() - timedelta(days=1)).isoformat()}.pkl', 'wb') as file:
            pickle.dump(count, file)
        return count

    def getWordFreqToday(self):
        news = New.objects.filter(cluster_day__date=date.today().isoformat() )

        if os.path.isfile(f'{self.util_count_path}/{date.today().isoformat()}.pkl'):
            with open(f'{self.util_count_path}/{date.today().isoformat()}.pkl', 'rb') as file:
                return pickle.load(file)
        # news = New.objects.filter(cluster_day__date='2020-05-30', cluster_day__cluster=1)
        df = self.preprocessing(news)

        # print(len(df))

        # word_ls = self.ws(df['content'])
        word_ls = [ json.loads(dtag.split) for dtag in Tagger.objects.filter(news_id__in=df['id'])]

        ls = []
        for dword in word_ls:
            ls.append(' '.join(word[0] for word in dword))
        # ls = [ self.tagger([content]) for content in tqdm(df['content']) ]

        # print(len(ls))
        vec = CountVectorizer()
        matrix = vec.fit_transform(ls)
        name = vec.get_feature_names()
        row, col = matrix.shape

        count = {}
        for dc in range(col):
            sum = 0
            for dr in range(row):
                sum += matrix[dr, dc]
            count[name[dc]] = sum

        with open(f'{self.util_count_path}/{date.today().isoformat()}.pkl', 'wb') as file:
            pickle.dump(count, file)
        return count


    def getGroupKeywords(self):

        keywords_filename = f"{self.util_path}/group_keywords/keywords-oneDay-{(date.today() - timedelta(days=1)).isoformat()}.pkl"
        relative_filename = f"{self.util_path}/group_keywords/relative-news-oneDay-{(date.today() - timedelta(days=1)).isoformat()}.pkl"

        if os.path.isfile(keywords_filename) and os.path.isfile(relative_filename):

            keywords_file = open(keywords_filename, "rb")
            relative_file = open(relative_filename, "rb")

            return pickle.loads(keywords_file), pickle.loads(relative_file)

        ls = []
        for i, dq in enumerate(self.keywords_group):
            # ls.append((i, json.loads(Tagger.objects.get(id=dq.news_id).split)))
            ls.append(self.preprocessing(dq))

        groupWised_content = []
        for i, dl in enumerate(ls):
            groupWised_content.append(
                (
                    i, self.genCorpus(Tagger.objects.filter(news_id__in=dl['id']))
                ))
            # groupWised_content.append((i, self.tagger(dl['content'])))

        # print(groupWised_content)

        keywords_tuple = self.genTfidf(groupWised_content)

        keywords = [ dk[1][0] for dk in keywords_tuple ]

        df = self.getNewHotword()

        relative_news = self.find_relative_news(keywords, df)

        with open(keywords_filename, "wb") as file:
            pickle.dumps(keywords, file)
        with open(relative_filename, "wb") as file:
            pickle.dumps(relative_news, file)

        return keywords, relative_news

    def text_preprocessing(self, raw):
        text = raw['content']
        tmp = re.sub(r'（.+）','', text)
        tmp = re.sub(r'〔.+〕', '', tmp)
        tmp = re.sub(r'[\r\n]', '', tmp)
        tmp = tmp.strip()
        # tmp = tmp.split(' ')
        if len(tmp) != 0:
            raw['content'] = tmp
        else:
            raw['content'] = None
        return raw

    def value_convert(self, raw):
        date = raw['update_time']
        raw['update_time'] = date.strftime('%Y-%m-%d')
        raw['date'] = raw['date'].strftime('%Y-%m-%d')
        return raw

    def preprocessing(self, querySet):
        df = pd.DataFrame(
            list(querySet.values()),
            columns=['id', 'title', 'content', 'author', 'brand_id', 'sub_id', 'date', 'update_time', 'url']
        )

        pre_df = df \
                    .apply(self.text_preprocessing, axis=1) \
                    .apply(self.value_convert, axis=1) \
                    .dropna()

        return pre_df

    def genCorpus(self, content):
        ls = []

        for dtagger in content:
            tagged_words = json.loads(dtagger.split)
            for dwords_tuple in tagged_words:
                ls.append(dwords_tuple[0])

        rst = ' '.join( [ str(word) for word in ls])
        return rst

    def tagger(self, content):
        words_ls = self.ws(content)
        pos_ls = self.pos(words_ls)


        ls = []

        pos_tag = ['Nb', 'Nc']

        for dwords_ls in words_ls:
            for dword in dwords_ls:
                ls.append(dword)

        rst = ' '.join( [str(word) for word in ls ] )

        return rst


    def genTfidf(self, matrix_tuple):
        vectorizer = TfidfVectorizer()
        # try:
        tfidf_vec = vectorizer.fit_transform([ dl[1] for dl in matrix_tuple])
        # except:
        #     # print(matrix_tuple)
        #     print("error")

        tfidf_arr = tfidf_vec.toarray()
        sort = np.argsort(tfidf_arr, axis=1)[:, -20:]
        names = vectorizer.get_feature_names()
        try:
            keywords = pd.Index(names)[sort].values
        except:
            keywords = pd.Index(names)[sort]
        keywords_tuple = list(zip([dc[0] for dc in matrix_tuple], keywords))

        return keywords_tuple


    def getNewHotword(self):
        """ Calculate all keywords in news today
        """

        # todayNews = New.objects.filter(cluster_day__date__gte=date.today().isoformat())
        threeDayNews = New.objects.filter(date__gte=(date.today() - timedelta(days=3)).isoformat())
        df = pd.DataFrame(
            list(threeDayNews.values()),
            columns=['id', 'title', 'content', 'author', 'brand_id', 'sub_id', 'date', 'update_time', 'url']
        )
        df = df \
            .apply(self.text_preprocessing, axis=1) \
            .apply(self.value_convert, axis=1) \
            .dropna()

        # words = self.ws(df['content'])

        words = [ (dtag.news_id, json.loads(dtag.split))  for dtag in Tagger.objects.filter(news_id__in=df['id'])]
        ll = []
        for i in words:
            if len(i[1]) != 0:
                ll.append(' '.join(word[0] for word in i[1]))
        # assert len(ll) == len(df)
        vectorizer = TfidfVectorizer()
        try:
            tfidf_vec = vectorizer.fit_transform(ll)
        except ValueError:
            print(ll)

        tfidf_arr = tfidf_vec.toarray()
        sort = np.argsort(tfidf_arr, axis=1)[:, -20:]
        names = vectorizer.get_feature_names()
        try:
            keywords = pd.Index(names)[sort].values
        except:
            keywords = pd.Index(names)[sort]

        keywords_tuple = list(zip([dt[0]for dt in words], keywords))

        return keywords_tuple

    def find_relative_news(self, keywords, keywords_tuple):

        ls = {}
        for i in keywords:
            ls[i] = {}

        for news_id, news_keywords in keywords_tuple:
            news = New.objects.get(id=news_id)
            id = news.id
            date = news.date.isoformat()
            for main_keyword in keywords:
                if main_keyword in news_keywords:
                    if date in ls[main_keyword].keys():
                        t = pd.Series(news_keywords)
                        ls[main_keyword]['relative_keywords'].extend(t[ t != main_keyword ].tolist())
                        ls[main_keyword][date][id] = {}
                        ls[main_keyword][date][id]['keywords'] = t[ t != main_keyword ].tolist()
                        ls[main_keyword][date][id]['url'] = news.url
                        ls[main_keyword][date][id]['title'] = news.title
                    else:
                        ls[main_keyword][date] = {}
                        ls[main_keyword]['relative_keywords'] = []
        return ls

    def chooseKeyword(self, uni_key, uni_count):

        # wordFreq = None
        # if os.path.isfile(f'{self.util_count_path}/{(date.today() - timedelta(days=1)).isoformat()}.pkl'):
        #     with open(f'{self.util_count_path}/{date.today().isoformat()}.pkl', 'rb') as file:
        #         wordFreq = pickle.load(file)

        max_index = np.argmax(uni_count)

        return uni_key[max_index]


    def genData(self, keyword, relative_news):
        ls = []
        # print(relative_news[keyword].keys())
        for date in relative_news[keyword].keys():
            if date != 'relative_keywords':
                tmp = {
                    'date': date,
                }
                posLinks = []
                negLinks = []
                n = 0
                # print(relative_news[keyword][date])
                keyword_list = []
                for news_id in relative_news[keyword][date].keys():
                    url = relative_news[keyword][date][news_id]['url']
                    title = relative_news[keyword][date][news_id]['title']
                    keyword_list.extend(relative_news[keyword][date][news_id]['keywords'])
                    if Aspect.objects.filter(new__id=news_id).aspect <= 1:
                        posLinks.append({
                            'title': title,
                            'url' : url
                        })
                    else:
                        negLinks.append({
                            'title': title,
                            'url': url
                        })
                    n += 1
                tmp['posLinks'] = posLinks
                tmp['negLinks'] = negLinks
                uni_keywords, keywords_counts = np.unique(keyword_list)
                tmp['keywords'] = self.chooseKeyword(uni_keywords, keywords_counts)
                ls.append(tmp)

        wordCloud = []
        wordCount = self.getWordFreq()
        for dword in relative_news[keyword]['relative_keywords']:
            try:
                wordCloud.append({
                    'text' : dword,
                    'size' : str(wordCount[dword])
                })
            except KeyError:
                pass

        return ls, wordCloud


def zero(num):
    return f"0{num}" if num < 10 else f"{num}"


class KeywordThreeDay:
    def __init__(self):
        self.get20Group()
        self.util_path = settings.BASE_DIR + '/analysis/apis/utils'
        self.util_count_path = settings.BASE_DIR + '/analysis/apis/utils/word_count'
        # self.ws = WS(self.util_path + '/data')
        # self.pos = POS(self.util_path + '/data')

    def get20Group(self):
        self.keywords_group = []

        base = datetime.today()
        date_list = [ base - timedelta(days=x) for x in range(3)]
        date_list = [ f'{dd.year}-{zero(dd.month)}-{zero(dd.day)}' for dd in date_list]
        for i in range(1, 6):
            self.keywords_group.append(New.objects.filter(cluster_day__cluster=i, cluster_day__date='2020-05-31'))

    def getWordFreq(self):
        news = New.objects.filter(cluster_day__date=date.today().isoformat())

        if os.path.isfile(f'{self.util_count_path}/{date.today().isoformat()}.pkl'):
            with open(f'{self.util_path}/{date.today().isoformat()}.pkl', 'rb') as file:
                return pickle.load(file)
        # news = New.objects.filter(cluster_day__date='2020-05-30', cluster_day__cluster=1)
        df = self.preprocessing(news)

        # print(len(df))

        # word_ls = self.ws(df['content'])
        word_ls = [ json.loads(dtag.split) for dtag in Tagger.objects.filter(news_id__in=df['id'])]

        ls = []
        for dword in word_ls:
            ls.append(' '.join(word[0] for word in dword))
        # ls = [ self.tagger([content]) for content in tqdm(df['content']) ]

        # print(len(ls))
        vec = CountVectorizer()
        matrix = vec.fit_transform(ls)
        name = vec.get_feature_names()
        row, col = matrix.shape

        count = {}
        for dc in range(col):
            sum = 0
            for dr in range(row):
                sum += matrix[dr, dc]
            count[name[dc]] = sum

        with open(f'{self.util_count_path}/{date.today().isoformat()}.pkl', 'wb') as file:
            pickle.dump(count, file)
        return count

    def getGroupKeywords(self):


        keywords_filename = f"{self.util_path}/group_keywords/keywords-threeDay-{(date.today() - timedelta(days=1)).isoformat()}.pkl"
        relative_filename = f"{self.util_path}/group_keywords/relative-news-threeDay-{(date.today() - timedelta(days=1)).isoformat()}.pkl"

        if os.path.isfile(keywords_filename) and \
            os.path.isfile(relative_filename):
            file_keywords = open(keywords_filename, "rb")
            file_relative = open(relative_filename, "rb")

            return pickle.loads(file_keywords), pickle.loads(file_relative)

        ls = []
        for i, dq in enumerate(self.keywords_group):
            # ls.append((i, json.loads(Tagger.objects.get(id=dq.news_id).split)))
            ls.append(self.preprocessing(dq))

        groupWised_content = []
        for i, dl in enumerate(ls):
            groupWised_content.append(
                (
                    i, self.genCorpus(Tagger.objects.filter(news_id__in=dl['id']))
                ))
            # groupWised_content.append((i, self.tagger(dl['content'])))

        # print(groupWised_content)

        keywords_tuple = self.genTfidf(groupWised_content)

        keywords = [ dk[1][0] for dk in keywords_tuple ]

        df = self.getNewHotword()

        relative_news, ids_ls = self.find_relative_news(keywords, df)


        for key in ids_ls.keys():
            sum_i = Summary(ids_ls[key])
            relative_news[key]['summary'] = sum_i.getSummary()

        with open(keywords_filename, "wb") as file:
            pickle.dumps(keywords, file)

        with open(relative_filename, "wb") as file:
            pickle.dumps(relative_news, file)

        return keywords, relative_news

    def text_preprocessing(self, raw):
        text = raw['content']
        tmp = re.sub(r'（.+）','', text)
        tmp = re.sub(r'〔.+〕', '', tmp)
        tmp = re.sub(r'[\r\n]', '', tmp)
        tmp = tmp.strip()
        # tmp = tmp.split(' ')
        if len(tmp) != 0:
            raw['content'] = tmp
        else:
            raw['content'] = None
        return raw

    def value_convert(self, raw):
        date = raw['update_time']
        raw['update_time'] = date.strftime('%Y-%m-%d')
        raw['date'] = raw['date'].strftime('%Y-%m-%d')
        return raw

    def preprocessing(self, querySet):
        df = pd.DataFrame(
            list(querySet.values()),
            columns=['id', 'title', 'content', 'author', 'brand_id', 'sub_id', 'date', 'update_time', 'url']
        )

        pre_df = df \
                    .apply(self.text_preprocessing, axis=1) \
                    .apply(self.value_convert, axis=1) \
                    .dropna()

        return pre_df

    def genCorpus(self, content):
        ls = []

        for dtagger in content:
            tagged_words = json.loads(dtagger.split)
            for dwords_tuple in tagged_words:
                ls.append(dwords_tuple[0])

        rst = ' '.join( [ str(word) for word in ls])
        return rst

    def tagger(self, content):
        words_ls = self.ws(content)
        pos_ls = self.pos(words_ls)


        ls = []

        pos_tag = ['Nb', 'Nc']

        for dwords_ls in words_ls:
            for dword in dwords_ls:
                ls.append(dword)

        rst = ' '.join( [str(word) for word in ls ] )

        return rst


    def genTfidf(self, matrix_tuple):
        vectorizer = TfidfVectorizer()
        try:
            tfidf_vec = vectorizer.fit_transform([ dl[1] for dl in matrix_tuple])
        except:
            print(matrix_tuple)

        tfidf_arr = tfidf_vec.toarray()
        sort = np.argsort(tfidf_arr, axis=1)[:, -20:]
        names = vectorizer.get_feature_names()
        try:
            keywords = pd.Index(names)[sort].values
        except:
            keywords = pd.Index(names)[sort]
        keywords_tuple = list(zip([dc[0] for dc in matrix_tuple], keywords))

        return keywords_tuple


    def getNewHotword(self):
        """ Calculate all keywords in news today
        """

        # todayNews = New.objects.filter(cluster_day__date__gte=date.today().isoformat())
        threeDayNews = New.objects.filter(date__gte='2020-05-29')
        df = pd.DataFrame(
            list(threeDayNews.values()),
            columns=['id', 'title', 'content', 'author', 'brand_id', 'sub_id', 'date', 'update_time', 'url']
        )
        df = df \
            .apply(self.text_preprocessing, axis=1) \
            .apply(self.value_convert, axis=1) \
            .dropna()

        # words = self.ws(df['content'])

        words = [ (dtag.news_id, json.loads(dtag.split))  for dtag in Tagger.objects.filter(news_id__in=df['id'])]
        # TODO need to be done in workflow
        ll = []
        for i in words:
            if len(i[1]) != 0:
                ll.append(' '.join(word[0] for word in i[1]))
        # print(len(ll), len(df))
        # assert len(ll) == len(df)
        vectorizer = TfidfVectorizer()
        try:
            tfidf_vec = vectorizer.fit_transform(ll)
        except ValueError:
            print(ll)

        tfidf_arr = tfidf_vec.toarray()
        sort = np.argsort(tfidf_arr, axis=1)[:, -20:]
        names = vectorizer.get_feature_names()
        try:
            keywords = pd.Index(names)[sort].values
        except:
            keywords = pd.Index(names)[sort]

        keywords_tuple = list(zip([dt[0]for dt in words], keywords))

        return keywords_tuple

    def find_relative_news(self, keywords, keywords_tuple):

        ls = {}
        for i in keywords:
            ls[i] = {}

        ids_ls = {}
        for news_id, news_keywords in tqdm(keywords_tuple):
            news = New.objects.get(id=news_id)
            id = news.id
            date = news.date.isoformat()
            for main_keyword in keywords:
                if main_keyword in ids_ls.keys():
                    ids_ls[main_keyword].append(id)
                else:
                    ids_ls[main_keyword] = []
                    ids_ls[main_keyword].append(id)
                if main_keyword in news_keywords:
                    if date in ls[main_keyword].keys():
                        t = pd.Series(news_keywords)
                        ls[main_keyword]['relative_keywords'].extend(t[ t != main_keyword ].tolist())
                        ls[main_keyword][date][id] = {}
                        ls[main_keyword][date][id]['keywords'] = t[ t != main_keyword ].tolist()
                        ls[main_keyword][date][id]['url'] = news.url
                        ls[main_keyword][date][id]['title'] = news.title
                    else:
                        ls[main_keyword][date] = {}
                        ls[main_keyword]['relative_keywords'] = []
        return ls, ids_ls

    def genData(self, keywords, relative_news):
        ls = []
        keywords_ls = []
        all_brand = Brand.objects.all()
        for keyword in keywords:
            tmp = {
                'keyword' : keyword,
                'summary' : relative_news[keyword]['summary'],
                'reportNum' : [0]*18
            }
            keyword_tmp = {
                'keyword' : keyword,
                'relative_news' : []
            }
            newsNum = 0
            links = []
            for date in relative_news[keyword].keys():
                if date != 'relative_keywords':
                    for id in relative_news[keyword][date].keys():
                        brand_index = New.objects.get(id=id).brand_id - 1
                        links.append({
                            'title' : relative_news[keyword][date][id]['title'],
                            'url' : relative_news[keyword][date][id]['url']
                        })
                        newsNum += 1
                        keyword_tmp['relative_news'].append(str(id))
                        tmp['reportNum'][brand_index] += 1
            tmp['newsNum'] = newsNum
            tmp['links'] = links
            ls.append(tmp)
            keywords_ls.append(keyword_tmp)




        return ls, keywords_ls



class Summary:
    def __init__(self, ids):
        self.ids = ids
        self.util_count_path = settings.BASE_DIR + '/analysis/apis/utils/word_count'
        with open(f"{self.util_count_path}/{(date.today() - timedelta(days=1)).isoformat()}.pkl", "rb") as file:
            self.freq_table = pickle.loads(file)


    def fetchNews(self):
        news = New.Objects.filter(id__in=self.ids)
        all_sents = [  ( dtag.news_id, json.loads(dtag.sents_split)) for dtag in Tagger.Objects.filter(id__in=self.ids)]

        self.all_sents = all_sents


    def sentence_scores(self):

        sent_weight = []
        cand_sents = []
        for news_id, data in self.all_sents:
            for raw_sent, splitted_sent in data:
                sent_wordcount_without_stop_words = 0
                sent_word_weight = 0
                for word, flag in splitted_sent:
                    if word in self.freq_table:
                        sent_wordcount_without_stop_words += 1
                        sent_word_weight += self.freq_table[word]
                if sent_wordcount_without_stop_words != 0:
                    sent_word_weight = sent_word_weight / sent_wordcount_without_stop_words
                sent_weight.append(sent_word_weight)
                cand_sents.append(raw_sent)

        sum = 0
        for score in sent_weight:
            sum += score

        avg_score = sum / len(sent_weight)

        assert len(cand_sents) == len(sent_weight)
        return list(zip(cand_sents, sent_weight)), avg_score


    def article_summary(self, sents_tuple, treshold):
        tmp = ""
        for cand_sent, sent_weight in sents_tuple:
            if sent_weight > treshold:
                tmp += " " + cand_sent

        return tmp


    def getSummary(self):
        self.fetchNews()
        sents_tuple, treshold = self.sentence_scores()
        return self.article_summary(sents_tuple, treshold)

