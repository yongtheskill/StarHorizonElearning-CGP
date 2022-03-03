from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('readNotifsConfirm/', views.readNotifications, name='readNotifications'),
    path('addTime/<str:username>', views.addTime, name='addTime'),
    path('dataDemo', views.dataDemo, name='dataDemo'),
    path('whiteboard', views.whiteboard, name='whiteboard'),
]