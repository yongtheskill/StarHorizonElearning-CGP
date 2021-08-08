from django.db import models

from accountManagement.models import Module

import pytz
sgt = pytz.timezone('Asia/Singapore')

from datetime import datetime

# Create your models here.
class Quiz(models.Model):
    
    quizName = models.CharField(max_length=200, verbose_name="quiz name")
    quizID = models.CharField(max_length=200, verbose_name="quiz id")
    quizDueDate = models.DateTimeField(blank=True, null=True)
    creationDate = models.DateTimeField(auto_now_add=True)

    passingScore = models.IntegerField(verbose_name="passing score", blank=True, null=True)

    quizData = models.CharField(max_length=10000000, verbose_name="quiz data")

    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    repeatNumber = models.IntegerField(verbose_name="repeat number")

    randomOptions = models.IntegerField(verbose_name="randomise options")
    randomQuestions = models.IntegerField(verbose_name="randomise questions")

    class Meta:
        verbose_name_plural = "Quizzes"

    @property
    def isDue(self):
        return sgt.localize(datetime.now()) > self.quizDueDate

    def __str__(self):
         return self.quizName






class Question(models.Model):
    questionId = models.BigAutoField(primary_key=True)
    questionName = models.CharField(max_length=200, verbose_name="question name")
    questionTitle = models.CharField(max_length=2000, verbose_name="question title")
    creationDate = models.DateTimeField(auto_now_add=True)

    questionData = models.CharField(max_length=10000000, verbose_name="question data")

    class Meta:
        verbose_name_plural = "Question bank questions"

    def __str__(self):
         return self.questionName
