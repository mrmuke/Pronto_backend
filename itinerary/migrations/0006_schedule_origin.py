# Generated by Django 3.1.7 on 2021-04-02 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itinerary', '0005_auto_20210331_2321'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='origin',
            field=models.CharField(default='SIN', max_length=100),
        ),
    ]
