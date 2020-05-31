from django.db import models
from .news_model import New

class Sentiment(models.Model):
    news = models.ForeignKey(New, on_delete=models.CASCADE)
    date = models.DateField(
        auto_now=False,
        auto_now_add=False
    )
    happy = models.DecimalField(max_digits=5, decimal_places=0, default=0)
    good = models.DecimalField(max_digits=5, decimal_places=0, default=0)
    surprise = models.DecimalField(max_digits=5, decimal_places=0, default=0)
    anger = models.DecimalField(max_digits=5, decimal_places=0, default=0)
    sad = models.DecimalField(max_digits=5, decimal_places=0, default=0)
    fear = models.DecimalField(max_digits=5, decimal_places=0, default=0)
    disgust = models.DecimalField(max_digits=5, decimal_places=0, default=0)
    length = models.DecimalField(max_digits=5, decimal_places=0, default=0)

    def __str__(self):
        return ""
    class Meta:
        db_table = "sentiment"