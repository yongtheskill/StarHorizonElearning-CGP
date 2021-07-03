# Generated by Django 2.2.9 on 2021-07-03 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0024_delete_choice'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='randomOptions',
            field=models.IntegerField(default=0, verbose_name='randomise options'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='randomQuestions',
            field=models.IntegerField(default=0, verbose_name='randomise questions'),
            preserve_default=False,
        ),
    ]
