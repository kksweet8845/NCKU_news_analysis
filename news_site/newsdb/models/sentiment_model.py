from django.db import models
from .news_model import New

class sentiment(models.Model):
    news = models.ForeignKey(New, on_delete=models.CASCADE)
    date = models.DateField(
        auto_now=False,
        auto_now_add=False
    )
    happy = models.DecimalField(max_digits=5, decimal_places=2)
    good = models.DecimalField(max_digits=5, decimal_places=2)
    surprise = models.DecimalField(max_digits=5, decimal_places=2)
    anger = models.DecimalField(max_digits=5, decimal_places=2)
    sad = models.DecimalField(max_digits=5, decimal_places=2)
    fear = models.DecimalField(max_digits=5, decimal_places=2)
    disgust = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return ""
    class Meta:
        db_table = "sentiment"