from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    genre = models.CharField(max_length=100)
    release_date = models.DateField()
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Rating must be between 0 and 10",
    )
    duration = models.IntegerField()
    director = models.CharField(max_length=100)

    def __str__(self):
        return self.title
