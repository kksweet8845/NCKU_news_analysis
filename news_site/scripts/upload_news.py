from newsdb.models import New, Subject, Brand
import pandas as pd
import os

def upload(filename):
    df = pd.read_csv('../dump/' + filename)

    for row in df.iterrows():
        row = row[1]
        a = New(**{
            'title' : row['title'],
            'content': row['content'],
            'author': row['author'],
            'date': row['date'],
            'update_time': row['update_time'],
            'brand' : Brand.objects.get(id=row['brand_id']),
            'sub': Subject.objects.get(id=row['sub_id']),
            'url': row['url'],
        })
        if len(New.objects.filter(url=row['url'])) == 0:
            a.save()



def run():
    print(123)
    for (dirpath, dirnames, filenames) in os.walk('../dump/'):
        for filename in filenames:
            upload(filename)