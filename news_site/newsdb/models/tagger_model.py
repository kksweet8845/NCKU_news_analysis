from django.db import models
from .news_model import New
from datetime import date
class Tagger(models.Model):
    news = models.ForeignKey(New, on_delete=models.CASCADE)
    split = models.TextField()
    sents_split = models.TextField()
    date = models.DateField(
        auto_now=False,
        auto_now_add=False,
        default=date.today().isoformat()
    )
    def __str__(self):
        return ""
    class Meta:
        db_table = "tagger"