# Generated by Django 2.2.9 on 2022-03-03 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountManagement', '0020_user_notificationaccess'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='notificationAccess',
            field=models.BooleanField(default=False, help_text='Designates whether the user can send notifications', verbose_name='Notification Access'),
        ),
    ]
