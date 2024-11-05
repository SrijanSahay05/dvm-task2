from django.db import models
from users.models import TheatreUserProfile, CustomerUserProfile
from movies.models import Movie


class screen(models.Model):
    screen_name = models.CharField(max_length=100, unique=True)
    theatre = models.ForeignKey(TheatreUserProfile, on_delete=models.CASCADE)
    total_seats = models.IntegerField()  # Maximum seats for the screen

    def __str__(self):
        return self.screen_name


class show(models.Model):
    theatre = models.ForeignKey(TheatreUserProfile, on_delete=models.CASCADE, null=True)
    screen = models.ForeignKey(screen, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    show_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.IntegerField(default=0)  # Available seats per show

    def save(self, *args, **kwargs):
        # Initialize available_seats based on screen.total_seats if this is a new instance
        if not self.pk:
            self.available_seats = self.screen.total_seats
        super(show, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.movie.title} - {self.show_time}"


class ticket(models.Model):
    show = models.ForeignKey(show, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomerUserProfile, on_delete=models.CASCADE)
    num_of_seats = models.IntegerField()
    status = models.CharField(max_length=20, default="Booked")

    def __str__(self):
        return f"{self.show.movie.title} - {self.num_of_seats} seats"
