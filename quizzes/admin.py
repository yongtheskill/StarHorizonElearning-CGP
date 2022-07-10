from django.contrib import admin

from django.utils.html import format_html

from .models import Quiz

# Register your models here.


class QuizAdmin(admin.ModelAdmin):
    list_display = list(admin.ModelAdmin.list_display)
    list_display.append("download_link")

    def download_link(self, obj):
        return format_html("<a href='/quizzes/dl/?id={id}'>Download</a>", id=obj.quizID)

    def __str__(self):
        return super().__str__()


admin.site.register(Quiz, QuizAdmin)
