from django.db import models
from .news_model import New

class tagger(models.Model):
    news = models.ForeignKey(New, on_delete=models.CASCADE)
    split = models.CharField(max_length=6000)

    def __str__(self):
        return ""
    class Meta:
        db_table = "tagger"