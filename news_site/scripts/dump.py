from newsdb.models import Subject, Brand, Brand_sub, New
from news_site import settings
import pickle
import json
import pandas as pd
from datetime import date

def run():
    news = New.objects.all()
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
    df.to_csv(f"{settings.BASE_DIR}/../dump/{date.today().isoformat()}_dump.csv")