# Generated by Django 2.2.27 on 2022-06-06 06:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0017_auto_20220606_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='end',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 6, 14, 25, 8, 966082)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 6, 14, 25, 8, 966082)),
        ),
    ]
