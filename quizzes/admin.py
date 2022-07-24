
from django.contrib import admin

from django.utils.html import format_html

from .models import Question, QuestionAttempt, QuestionTag, Quiz, QuizAttempt

# Register your models here.


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = list(admin.ModelAdmin.list_display)
    list_display.append("download_link")

    fields = ('quizName', 'quizDueDate', 'passingScore', 'module')
    readonly_fields = ('quizID')

    def download_link(self, obj):
        return format_html("<a href='/quizzes/dl/?id={id}'>Download</a>", id=obj.quizID)

    def __str__(self):
        return super().__str__()


class QuestionAttemptInline(admin.TabularInline):
    fields = ('question', 'type', 'isCorrect')
    model = QuestionAttempt
    readonly_fields = ('question', 'type')
    exclude = ('saAnswer', 'mcAnswer', 'cbAnswer')
    can_delete = False


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = list(admin.ModelAdmin.list_display)
    list_display.append("quiz")
    list_display.append("student")
    list_display.append("score")

    inlines = [QuestionAttemptInline]

    def __str__(self):
        return super().__str__()
