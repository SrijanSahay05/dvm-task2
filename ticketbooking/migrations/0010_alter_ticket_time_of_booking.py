# Generated by Django 5.1.2 on 2024-11-05 14:05

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketbooking', '0009_ticket_time_of_booking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='time_of_booking',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]