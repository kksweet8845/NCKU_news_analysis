from simpletransformers.classification import ClassificationModel
from django.db.models import Q
from newsdb.models import New, Standpoint
from datetime import datetime
from news_site import settings


def standpoint_analysis(query_set):
    model = ClassificationModel('bert', settings.BASE_DIR + '/sentiment_model/', args={}, use_cuda=False)
    i = 0
    content_list = []
    for query in query_set:
        content_list.append(query.content)
    predictions, raw_inputs = model.predict(content_list)
    for prediction in predictions:
        a = Standpoint(news=query_set[i], standpoint=int(prediction))
        a.save()
        i += 1
    return prediction