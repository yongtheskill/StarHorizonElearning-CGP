from django.db import models
from accountManagement.models import StudentClass
import datetime

# Create your models here.


class Notification(models.Model):
    title = models.CharField(max_length=200, verbose_name="title")
    content = models.CharField(max_length=1000000, verbose_name="content")

    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(auto_now_add=True)

    studentClasses = models.ManyToManyField(StudentClass)

    def __str__(self):
        return self.title
