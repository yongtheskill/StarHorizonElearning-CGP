from django.db import models
from accountManagement.models import StudentClass
import datetime

# Create your models here.


class Notification(models.Model):

    title = models.CharField(max_length=200, verbose_name="title")
    content = models.CharField(max_length=999999999, verbose_name="content")
    
    start = models.DateTimeField(default=datetime.datetime.now())
    end = models.DateTimeField(default=datetime.datetime.now())

    studentClasses = models.ManyToManyField(StudentClass)

    def __str__(self):
        return self.title
