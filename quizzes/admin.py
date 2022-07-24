
from django.contrib import admin

from django.utils.html import format_html

from .models import Question, QuestionAttempt, QuestionTag, Quiz, QuizAttempt

# Register your models here.


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = list(admin.ModelAdmin.list_display)
    list_display.append("download_link")

    def download_link(self, obj):
        return format_html("<a href='/quizzes/dl/?id={id}'>Download</a>", id=obj.quizID)

    def __str__(self):
        return super().__str__()


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = list(admin.ModelAdmin.list_display)
    list_display.append("quiz")
    list_display.append("student")
    list_display.append("score")

    def __str__(self):
        return super().__str__()


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass
