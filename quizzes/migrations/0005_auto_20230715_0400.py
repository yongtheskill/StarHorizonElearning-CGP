# Generated by Django 2.2.27 on 2023-07-14 20:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0004_quiz_allowretries'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizattempt',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2023, 7, 14, 20, 0, 27, 561158, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
