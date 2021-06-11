from django.urls import path

from . import views

urlpatterns = [
    path('manage/', views.manageQuizzes, name='manageQuizzes'),
    path('create/', views.createQuiz, name='createQuizzes'),
    path('view/<str:quizID>/', views.viewQuiz, name='viewQuiz'),
    path('viewAns/<str:quizNameEncoded>/<int:userId>/', views.viewQuizAns, name='viewQuizAns'),
    path('edit/<str:quizID>/', views.editQuiz, name='editQuiz'),
    path('do/<str:quizID>/', views.doQuiz, name='doQuiz'),
    path('repeat/<str:quizID>/', views.repeatQuiz, name='repeatQuiz'),
    path('deleteQuiz/', views.deleteQuiz, name='deleteQuiz'),
    path('download/', views.downloadQuiz, name='downloadQuiz'),
    path('dl/', views.exportQuiz, name='downloadQuiz'),
    path('bank/', views.manageBank, name='quizBank'),
    path('bank/create/', views.bankCreate, name='createBankQuestion'),
    path('bank/delete/<int:questionID>', views.bankDelete, name='deleteBankQuestion'),
    path('bank/get/<int:questionID>', views.bankGet, name='getBankQuestion'),
]