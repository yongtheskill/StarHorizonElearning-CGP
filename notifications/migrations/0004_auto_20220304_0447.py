# Generated by Django 2.2.9 on 2022-03-03 20:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_auto_20220304_0358'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='studentClass',
            new_name='studentClasses',
        ),
        migrations.AlterField(
            model_name='notification',
            name='end',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 4, 4, 47, 3, 393274)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 4, 4, 47, 3, 393274)),
        ),
    ]