# Generated by Django 2.2.9 on 2022-05-27 17:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0008_auto_20220528_0123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='end',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 28, 1, 23, 44, 129598)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 28, 1, 23, 44, 129598)),
        ),
    ]
