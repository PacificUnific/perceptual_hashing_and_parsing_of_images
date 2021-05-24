from django.db import models

# Create your models here.


class Image(models.Model):
    label = models.CharField(max_length=256)
    date = models.DateField()
    top = models.IntegerField(null=True)
    request = models.CharField(max_length=64)
    title = models.CharField(null=True, max_length=256)
    domain = models.CharField(null=True, max_length=64)
    origin = models.CharField(null=True, max_length=256)
    image = models.CharField(null=True, max_length=256)
    history = models.TextField(null=True)
    rating = models.TextField(null=True)

    def __str__(self):
        return f'{self.request} ' \
               f'image with id {self.id} ' \
               f'was found at {self.date} last time'
