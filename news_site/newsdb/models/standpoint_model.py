from django.db import models
from .news_model import New

class Standpoint(models.Model):
    news = models.ForeignKey(New, on_delete=models.CASCADE)
    standpoint = models.DecimalField(
        max_digits=2,
        decimal_places=0,
        default=0,
        blank=False
    )

    def __str__(self):
        return ""
    class Meta:
        db_table = "standpoint"