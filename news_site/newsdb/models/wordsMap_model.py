from django.db import models


class Word(models.Model):
    word = models.CharField(
        max_length=20,
        blank=False
    )

    def __str__(self):
        return "\nword: {}".format(self.word)

    class Meta:
        db_table = "wordsMap"


