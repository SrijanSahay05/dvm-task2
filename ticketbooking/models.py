from django.db import models
from users.models import TheatreUserProfile, CustomerUserProfile
from movies.models import Movie


class screen(models.Model):
    screen_name = models.CharField(max_length=100, unique=True)
    theatre = models.ForeignKey(TheatreUserProfile, on_delete=models.CASCADE)
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the object is new (not yet saved to the database)
            self.available_seats = self.total_seats
        super(screen, self).save(*args, **kwargs)

    def __str__(self):
        return self.screen_name


class show(models.Model):
    theatre = models.ForeignKey(TheatreUserProfile, on_delete=models.CASCADE, null=True)
    screen = models.ForeignKey(screen, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    show_time = models.DateTimeField()
    # show_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.movie.title + " " + str(self.show_time)


class ticket(models.Model):
    show = models.ForeignKey(show, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomerUserProfile, on_delete=models.CASCADE)
    num_of_seats = models.IntegerField()
    status = models.CharField(max_length=20, default="Booked")

    def __str__(self):
        return self.show.show_name + " " + str(self.seat_number)
