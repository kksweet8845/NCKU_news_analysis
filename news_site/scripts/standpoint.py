from simpletransformers.classification import ClassificationModel
from django.db.models import Q
from newsdb.models import New, standpoint
from datetime import datetime

def standpoint_analysis(query_set):
    model = ClassificationModel('bert', '/home/boldcentaur/Desktop/coding/NCKU_news_analysis/news_site/sentiment_model/', args={}, use_cuda=False)
    i = 0
    content_list = []
    for query in query_set:
        content_list.append(query.content)
    predictions, raw_inputs = model.predict(content_list)
    for prediction in predictions:
        a = standpoint(news=query_set[i], standpoint=int(prediction))
        a.save()
        i += 1
    return prediction

def run():
    news_query = New.objects.filter(Q(date__gte=datetime.today()))
    prediction = standpoint_analysis(news_query)


