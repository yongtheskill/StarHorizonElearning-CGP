# Generated by Django 2.2.9 on 2022-05-27 16:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0006_auto_20220527_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='end',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 28, 0, 55, 51, 923296)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 28, 0, 55, 51, 923296)),
        ),
    ]
