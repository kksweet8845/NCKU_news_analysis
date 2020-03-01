from django.db import models

class Subject(models.Model):
    sub_name = models.CharField(
        max_length=10,
        blank=False,
        default=''
    )

    def __str__(self):
        return "sub_ID: {}\nsub_name : {}".format(self.id, self.sub_name)

    class Meta:
        db_table = "subjects"