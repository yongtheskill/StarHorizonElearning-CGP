# Generated by Django 2.2.9 on 2022-03-03 18:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("notifications", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notification",
            name="content",
            field=models.CharField(max_length=1000000, verbose_name="content"),
        ),
    ]
