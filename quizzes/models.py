from datetime import datetime
from django.db import models
from model_clone import CloneMixin

from StarHorizonElearning.storage_backends import QuizImageStorage

from accountManagement.models import Course, Module, User

import pytz

sgt = pytz.timezone("Asia/Singapore")


# Create your models here.


class Quiz(CloneMixin, models.Model):

    quizName = models.CharField(max_length=200, verbose_name="quiz name")
    quizID = models.CharField(max_length=200, verbose_name="quiz id")
    quizDueDate = models.DateTimeField(blank=True, null=True)
    creationDate = models.DateTimeField(auto_now_add=True)

    passingScore = models.IntegerField(
        verbose_name="passing score", blank=True, null=True, default=0
    )

    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True)

    repeatNumber = models.IntegerField(verbose_name="repeat number", default=0)

    questionOrder = models.CharField(
        max_length=9999, verbose_name="Question Order", default="[]"
    )

    randomOptions = models.IntegerField(
        verbose_name="randomise options", default=False)
    randomQuestions = models.IntegerField(
        verbose_name="randomise questions", default=False
    )
    allowRetries = models.IntegerField(
        verbose_name="allow retries", default=False
    )

    _clone_m2o_or_o2m_fields = ["questions"]

    class Meta:
        verbose_name_plural = "Quizzes"

    @property
    def isDue(self):
        try:
            return sgt.localize(datetime.now()) > self.quizDueDate
        except:
            return False

    def __str__(self):
        return self.quizName

    def toDict(self):
        try:
            modId = self.module.id
            cId = self.module.course.id
        except:
            modId = None
            cId = -1
        return {
            "questions": [i.toDict() for i in self.questions.all()],
            "quizName": self.quizName,
            "quizID": self.quizID,
            "quizDueDate": self.quizDueDate,
            "passingScore": self.passingScore,
            "moduleId": modId,
            "courseId": cId,
            "randomOptions": self.randomOptions,
            "randomQuestions": self.randomQuestions,
            "allowRetries": self.allowRetries,
            "questionOrder": self.questionOrder,
        }

    def doToDict(self):
        return {
            "questions": [i.doToDict() for i in self.questions.all()],
            "quizName": self.quizName,
            "quizID": self.quizID,
            "randomOptions": self.randomOptions,
            "randomQuestions": self.randomQuestions,
            "questionOrder": self.questionOrder,
        }


class QuestionTag(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="questionTags"
    )
    text = models.CharField(
        max_length=999,
    )

    def toDict(self):
        return {
            "courseId": self.course.id,
            "text": self.text,
            "id": self.id
        }

class QuizImage(models.Model):
    imageFile = models.FileField(storage=QuizImageStorage()) 
    
    def __str__(self):
         return self.id

class Question(CloneMixin, models.Model):
    text = models.CharField(
        max_length=999, verbose_name="Question Text", null=True)
    autoGrade = models.BooleanField(default=False)
    optionOrder = models.CharField(
        max_length=9999, verbose_name="Option Order", default="[]"
    )

    image = models.ForeignKey(
        QuizImage, on_delete=models.SET_NULL, related_name="question", null=True
    )

    type = models.CharField(
        max_length=8,
        choices=[
            ("cb", "Checkboxes"),
            ("mc", "Multiple Choice"),
            ("sa", "Short Answer"),
            ("la", "Long Answer"),
        ],
        default="cb",
    )
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="questions", null=True)
    saAnswer = models.CharField(max_length=999, default="")
    mcAnswer = models.IntegerField(default=-1)
    cbAnswer = models.CharField(max_length=999, default="[]")

    questionTag = models.ForeignKey(
        QuestionTag, on_delete=models.CASCADE, related_name="questions", null=True)

    name = models.CharField(
        max_length=999, verbose_name="Question Name", default="")
    isBankQuestion = models.BooleanField(default=False)

    _clone_m2o_or_o2m_fields = ["options"]

    def toDict(self):
        qtag = None
        imageUrl = None
        if self.image != None:
            imageUrl = self.image.imageFile.url
        if self.questionTag != None:
            qtag = self.questionTag.toDict()
        return {
            "id": self.id,
            "text": self.text,
            "autoGrade": self.autoGrade,
            "type": self.type,
            "options": [i.toDict() for i in self.options.all()],
            "optionOrder": self.optionOrder,
            "saAnswer": self.saAnswer,
            "mcAnswer": self.mcAnswer,
            "cbAnswer": self.cbAnswer,
            "questionTag": qtag,
            "questionName": self.name,
            "imageUrl": imageUrl
        }

    def doToDict(self):
        imageUrl = None
        if self.image != None:
            imageUrl = self.image.imageFile.url
        return {
            "id": self.id,
            "text": self.text,
            "type": self.type,
            "options": [i.toDict() for i in self.options.all()],
            "optionOrder": self.optionOrder,
            "imageUrl": imageUrl
        }

    def __str__(self) -> str:
        return str(self.text)


class Option(models.Model):
    text = models.CharField(
        max_length=999, verbose_name="Option text", null=True)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="options"
    )

    def toDict(self):
        return {"id": self.id, "text": self.text}


class QuizAttempt(models.Model):
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="quizAttempts"
    )
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="attempts")
    score = models.IntegerField(default=0)

    timestamp = models.CharField(max_length=500, null=True)

    def toDict(self):
        return {
            "id": self.id,
            "quizName": self.quiz.quizName,
            "questionOrder": self.quiz.questionOrder,
            "questionAttempts": [i.toDict() for i in self.questionAttempts.all()],
        }

    def __str__(self):
        return f"{self.quiz.quizName}: {self.student.username}"


class QuestionAttempt(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="questionAttempts"
    )
    quizAttempt = models.ForeignKey(
        QuizAttempt, on_delete=models.CASCADE, related_name="questionAttempts"
    )
    type = models.CharField(
        max_length=8,
        choices=[
            ("cb", "Checkboxes"),
            ("mc", "Multiple Choice"),
            ("sa", "Short Answer"),
            ("la", "Long Answer"),
        ],
        default="cb",
    )
    saAnswer = models.CharField(max_length=999999, default="")
    mcAnswer = models.IntegerField(default=-1)
    cbAnswer = models.CharField(max_length=999, default="[]")
    isCorrect = models.BooleanField(default=False, verbose_name="Is Correct")

    def toDict(self):
        return {
            "question": self.question.toDict(),
            "type": self.type,
            "saAnswer": self.saAnswer,
            "mcAnswer": self.mcAnswer,
            "cbAnswer": self.cbAnswer,
            "isCorrect": self.isCorrect,
        }



