from django.db import models
from .news_model import New

class Position(models.Model):
    new = models.ForeignKey(New, on_delete=models.CASCADE)

    position = models.ForeignKey(New, on_delete=models.CASCADE)

    def __str__(self):
        return ""

    class Meta:
        db_table = "positions"