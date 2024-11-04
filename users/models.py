from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ("customer", "Customer"),
        ("theatre", "Theatre"),
        ("superadmin", "Superadmin"),
    )
    user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=255)
    USERNAME_FIELD = "username"


class CustomerUserProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="customer_profile"
    )
    phone_number = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)


class TheatreUserProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="theatre_profile"
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
