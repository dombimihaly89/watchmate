# Generated by Django 4.0.5 on 2022-06-23 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0006_movie_avg_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='number_of_ratings',
            field=models.IntegerField(default=0),
        ),
    ]
