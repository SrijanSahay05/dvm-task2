# Generated by Django 5.1.2 on 2024-11-05 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketbooking', '0007_remove_screen_available_seats_show_available_seats'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='food_allowed',
            field=models.BooleanField(default=True),
        ),
    ]