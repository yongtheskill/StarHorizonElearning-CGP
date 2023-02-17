# Generated by Django 2.2.27 on 2022-09-16 14:28

import StarHorizonElearning.storage_backends
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imageFile', models.FileField(storage=StarHorizonElearning.storage_backends.QuizImageStorage(), upload_to='')),
            ],
        ),
        migrations.AlterField(
            model_name='questionattempt',
            name='isCorrect',
            field=models.BooleanField(default=False, verbose_name='Is Correct'),
        ),
        migrations.AddField(
            model_name='question',
            name='image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question', to='quizzes.QuizImage'),
        ),
    ]