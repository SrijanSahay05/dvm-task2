# Generated by Django 5.1.2 on 2024-11-05 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketbooking', '0008_show_food_allowed'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='time_of_booking',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
