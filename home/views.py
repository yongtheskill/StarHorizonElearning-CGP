from notifications.models import Notification
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from accountManagement.models import User

import datetime
import pytz

sgt = pytz.timezone("Asia/Singapore")


# home page
def home(request):
    context = {"isHome": True}
    if request.user.is_authenticated:
        if not request.user.notificationAccess:
            classes = request.user.classes.all()
            classIds = [i.pk for i in classes]
            notifications = Notification.objects.filter(
                studentClasses__in=classIds).distinct()

            notificationsSeen = request.user.notificationsSeen.all()

            notificationsUnseen = notifications.difference(notificationsSeen)
            context = {"isHome": True,
                       "notificationsUnseen": notificationsUnseen}

    return render(request, 'home/home.html', context)

# acknowledge notifs


@login_required
def readNotifications(request):
    classes = request.user.classes.all()
    classIds = [i.pk for i in classes]
    notifications = Notification.objects.filter(
        studentClasses__in=classIds).distinct()

    modified = False
    for i in notifications:
        if i.end < sgt.localize(datetime.datetime.now()):
            i.delete()
            modified = True

    if modified:
        notifications = Notification.objects.filter(
            studentClasses__in=classIds).distinct()

    request.user.notificationsSeen.clear()
    request.user.notificationsSeen.add(*notifications)
    return HttpResponse("Ok")


# timer
def addTime(request, username):
    try:
        userObject = User.objects.get(username=username)

        if not userObject.timeOnline:
            userObject.timeOnline = datetime.timedelta(seconds=0)

        userObject.timeOnline += datetime.timedelta(seconds=10)
        userObject.save()
    except:
        return HttpResponse("Not Available")

    return HttpResponse("Done")


def whiteboard(request):
    return render(request, 'home/whiteboard.html', {})


# data demo
def dataDemo(request):
    return render(request, 'home/dataDemo.html', {})
