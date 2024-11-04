from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    genre = models.CharField(max_length=100)
    release_date = models.DateField()
    rating = models.FloatField()
    duration = models.IntegerField()
    director = models.CharField(max_length=100)

    def __str__(self):
        return self.title
