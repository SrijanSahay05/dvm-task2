# Generated by Django 5.1.2 on 2024-11-02 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_theatreuserprofile_location_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customeruserprofile',
            name='city',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='customeruserprofile',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
        migrations.AddField(
            model_name='customeruserprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='theatreuserprofile',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='theatreuserprofile',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]