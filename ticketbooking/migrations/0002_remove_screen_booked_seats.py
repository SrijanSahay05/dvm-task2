# Generated by Django 5.1.2 on 2024-11-04 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketbooking', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='screen',
            name='booked_seats',
        ),
    ]
