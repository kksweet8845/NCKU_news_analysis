from newsdb.models import New, Subject, Brand
import pandas as pd
import os
from tqdm import tqdm
# from django.db.transaction import commit_on_success

# @commit_on_success
def upload(filename):
    df = pd.read_csv('../dump/' + filename)

    for row in tqdm(df.iterrows(), total=len(df)):
        row = row[1]
        # if len(New.objects.filter(url=row['url'])) == 0:
        a = New(**{
            'title' : row['title'],
            'content': row['content'],
            'author': row['author'],
            'date': row['date'],
            'brand' : Brand.objects.get(id=row['brand_id']),
            'sub': Subject.objects.get(id=row['sub_id']),
            'url': row['url'],
        })
        a.save()



def run():
    for (dirpath, dirnames, filenames) in os.walk('../dump/'):
        for filename in tqdm(filenames):
            upload(filename)