# Generated by Django 2.2.27 on 2022-06-06 03:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0014_auto_20220605_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='end',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 6, 11, 54, 35, 506474)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 6, 11, 54, 35, 506474)),
        ),
    ]