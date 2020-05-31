from django.db import models
from .news_model import New

class Aspect(models.Model):
    new = models.ForeignKey(New, on_delete=models.CASCADE)
    aspect = models.DecimalField(
        max_digits=2,
        decimal_places=0,
        default=0,
        blank=False
    )

    def __str__(self):
        return ""

    class Meta:
        db_table = "aspect"