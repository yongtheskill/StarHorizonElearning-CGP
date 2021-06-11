# Generated by Django 2.2.9 on 2021-06-11 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0021_delete_quiz2'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name_plural': 'Question bank questions'},
        ),
        migrations.RemoveField(
            model_name='question',
            name='id',
        ),
        migrations.AddField(
            model_name='question',
            name='questionId',
            field=models.BigAutoField(default=0, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='creationDate',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
