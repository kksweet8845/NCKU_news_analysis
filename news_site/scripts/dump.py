from newsdb.models import Subject, Brand, Brand_sub, New
from news_site import settings
import pickle
import json
import pandas as pd
from datetime import date
import re
from tqdm import tqdm
import csv

def run():
    news = New.objects.all()
    # for dnews in tqdm(news):
    #     dnews.content = re.sub(r'[,]', ' ', dnews.content)
    #     dnews.title = re.sub(r'[,]', ' ', dnews.title)
        # dnews.content = re.sub(r'[,]+', '', dnews.content)

    df = pd.DataFrame(
            list(news.values()),
            columns=['id',
                     'title',
                     'content',
                     'author',
                     'brand_id',
                     'sub_id',
                     'date',
                     'update_time',
                     'url']
    )

    def fn(row):
        row['content'] = re.sub(r'[\r]', ' ', row['content'])
        row['title'] = re.sub(r'[\r]', ' ', row['title'])
        return row

    df = df.apply(fn, axis=1 )
    # for row in df.iterrows():
    #     print(row)
    #     break
    #     row = row[1]
    #     row['content'] = re.sub(r'[，\r]', ' ', row['content'])
    #     row['title'] = re.sub(r'[，\r]', ' ', row['title'])

    dump_json = []

    for row in df.iterrows():
        row = row[1]
        # print(row['date'])
        obj = {
            'title' : row['title'],
            'content' : row['content'],
            'author' : row['author'],
            'brand_id' : row['brand_id'],
            'date' : str(row['date']),
            'url' : row['url'],
        }
        dump_json.append(obj)

    json_str = json.dumps(dump_json, indent=4, ensure_ascii=False)

    with open(f"{settings.BASE_DIR}/../dump/{date.today().isoformat()}_dump.json", 'w', encoding='utf8') as file:
        file.write(json_str)
    file.close()


    # df.to_csv(f"{settings.BASE_DIR}/../dump/{date.today().isoformat()}_dump.csv", index=False)


    # read_df = pd.read_csv(f"{settings.BASE_DIR}/../dump/{date.today().isoformat()}_dump.csv")

    # print(len(df), len(read_df))
    # assert len(read_df) == len(df)