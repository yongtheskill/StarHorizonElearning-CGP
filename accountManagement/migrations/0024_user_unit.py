# Generated by Django 2.2.27 on 2023-08-08 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountManagement', '0023_auto_20220710_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='unit',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]