# Generated by Django 5.1.2 on 2024-11-04 10:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_movie_description'),
        ('ticketbooking', '0003_alter_screen_screen_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='show',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show_time', models.DateTimeField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
                ('screen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticketbooking.screen')),
            ],
        ),
    ]
