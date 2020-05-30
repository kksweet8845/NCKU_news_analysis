from simpletransformers.classification import ClassificationModel
from django.db.models import Q
from newsdb.models import New, standpoint

def standpoint_analysis(query_set):
    content_list = []
    model = ClassificationModel('bert', 'standpoint_model/', args={})
    for query in query_set:
        content_list.append(query.content)
    predictions, raw_outputs = model.predict(content_list)


    
news_query = New.objects.filter(Q(sub_id__lt=7))
standpoint(news_query)


