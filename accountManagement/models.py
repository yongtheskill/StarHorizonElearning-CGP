from django.db import models
from django.contrib.auth.models import AbstractUser
from StarHorizonElearning.storage_backends import MediaStorage

import json


# Create your models here.


class Course(models.Model):
    courseName = models.CharField(max_length=200, verbose_name="course name")
    courseInstitution = models.CharField(
        max_length=200, verbose_name="institution", null=True
    )
    courseDescription = models.CharField(
        max_length=5000, verbose_name="course description", null=True, default=None
    )

    courseCode = models.CharField(max_length=200, verbose_name="course code", null=True)

    def setTags(self, x):
        self.quizTags = json.dumps(x)

    def getTags(self):
        return json.loads(self.quizTags)

    def __str__(self):
        return self.courseName

    def toDict(self):
        return {"name": self.courseName, "id": self.id}


class StudentClass(models.Model):
    className = models.CharField(max_length=200, verbose_name="class name")
    classInstitution = models.CharField(
        max_length=200, verbose_name="institution", null=True
    )
    courses = models.ManyToManyField(Course, blank=True)

    class Meta:
        verbose_name_plural = "Classes"

    def __str__(self):
        return self.className


class Module(models.Model):
    moduleName = models.CharField(max_length=200, verbose_name="module name")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.moduleName

    def toDict(self):
        return {"name": self.moduleName, "id": self.id, "courseId": self.course.id}


class User(AbstractUser):
    institution = models.CharField(max_length=200, blank=True, null=True)
    phoneNumber = models.CharField(
        verbose_name="phone number", max_length=20, blank=True, null=True, default=None
    )
    profilePic = models.ImageField(
        storage=MediaStorage(), verbose_name="Profile picture", blank=True
    )

    ACC_TYPES = [
        ("Teacher", "Teacher"),
        ("Student", "Student"),
    ]
    accountType = models.CharField(
        verbose_name="account type",
        max_length=16,
        choices=ACC_TYPES,
        default="Administrator",
    )
    classes = models.ManyToManyField(StudentClass, blank=True, related_name="users")

    quizResponses = models.CharField(
        max_length=1000000, verbose_name="quizResponses", null=True, blank=True
    )

    timeOnline = models.DurationField(verbose_name="timeOnline", blank=True, null=True)

    startDate = models.DateField(blank=True, null=True, verbose_name="Start date")
    unit = models.CharField(max_length=500, blank=True, null=True)
    designation = models.CharField(max_length=500, blank=True, null=True)

    notificationAccess = models.BooleanField(
        default=False,
        verbose_name="Notification Access",
        help_text="Designates whether the user can send notifications",
    )

    notificationsSeen = models.ManyToManyField("notifications.Notification")

    pwResetCode = models.CharField(max_length=256, default="none")
    pwResetTime = models.DateTimeField(null=True)

    def __str__(self):
        return self.username
