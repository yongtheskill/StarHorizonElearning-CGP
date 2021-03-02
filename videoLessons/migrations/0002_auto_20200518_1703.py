# Generated by Django 3.0.5 on 2020-05-18 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoLessons', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='videoURL',
        ),
        migrations.AddField(
            model_name='video',
            name='videoFile',
            field=models.FileField(max_length=1000, null=True, upload_to='', verbose_name='video url'),
        ),
    ]
