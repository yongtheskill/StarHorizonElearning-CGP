# Generated by Django 2.2.27 on 2023-07-14 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileUploads', '0004_fileupload_creationdate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fileupload',
            name='id',
        ),
        migrations.AlterField(
            model_name='fileupload',
            name='fileID',
            field=models.CharField(max_length=200, primary_key=True, serialize=False, verbose_name='file id'),
        ),
    ]
