# Generated by Django 5.1.2 on 2024-11-04 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketbooking', '0002_remove_screen_booked_seats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screen',
            name='screen_name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]