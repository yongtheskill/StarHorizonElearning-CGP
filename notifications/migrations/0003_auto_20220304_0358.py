# Generated by Django 2.2.9 on 2022-03-03 19:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_auto_20220304_0209'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='end',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 4, 3, 58, 14, 768930)),
        ),
        migrations.AddField(
            model_name='notification',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 4, 3, 58, 14, 768930)),
        ),
    ]
