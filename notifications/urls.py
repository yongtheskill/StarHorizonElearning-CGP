from django.urls import path

from . import views

urlpatterns = [
    path('', views.viewNotifications, name='viewNotifications'),
    path('manage/', views.manageNotifications, name='manageNotifications'),
    path('create/', views.createNotification, name='createNotification'),
    path('edit/<int:NotificationID>',
         views.editNotification, name='editNotification'),
    path('delete/<int:NotificationID>',
         views.deleteNotification, name='deleteNotification'),

]
