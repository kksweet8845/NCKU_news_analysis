from django.db import models
from .news_model import New

class tagger(models.Model):
    news = models.ForeignKey(New, on_delete=models.CASCADE)
    split = models.TextField()
    date = models.DateField(
        auto_now=False,
        auto_now_add=False
    )
    def __str__(self):
        return ""
    class Meta:
        db_table = "tagger"