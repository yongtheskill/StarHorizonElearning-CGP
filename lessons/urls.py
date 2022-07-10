from django.urls import path

from . import views

urlpatterns = [
    path('manage/', views.manageUploads, name='manageUploadds'),
    path('create/', views.createLesson, name='Create Lesson'),
    path('delete/<str:lessonID>', views.deleteLesson, name='Delete Lesson'),
    path('view/<str:lessonID>', views.viewLesson, name='View Lesson'),
]
