# Generated by Django 3.1.7 on 2021-03-29 15:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('itinerary', '0003_auto_20210319_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='arrival',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='schedule',
            name='departure',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='schedule',
            name='length',
            field=models.PositiveSmallIntegerField(default=3),
        ),
    ]
