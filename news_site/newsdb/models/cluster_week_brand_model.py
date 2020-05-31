from django.db import models
from .news_model import New

class cluster_week_brand(models.Model):
    news = models.ForeignKey(New, on_delete=models.CASCADE)
    date = models.DateField(
        auto_now=False,
        auto_now_add=False
    )
    date_from = models.DateField(
        auto_now=False,
        auto_now_add=False
    )
    date_to = models.DateField(
        auto_now=False,
        auto_now_add=False
    )
    brand = models.IntegerField()
    cluster = models.IntegerField()

    def __str__(self):
        return ""
    class Meta:
        db_table = "cluster_week_brand"