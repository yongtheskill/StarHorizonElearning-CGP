# Generated by Django 2.2.9 on 2020-09-06 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accountManagement', '0014_course_coursecode'),
    ]

    operations = [
        migrations.RenameField(
            model_name='module',
            old_name='courses',
            new_name='course',
        ),
    ]
