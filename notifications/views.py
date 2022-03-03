from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from accountManagement.models import StudentClass
from .models import Notification


from datetime import datetime
import pytz

from StarHorizonElearning import settings

sgt = pytz.timezone("Asia/Singapore")


@login_required
def viewNotifications(request):
    classes = request.user.classes.all()
    classIds = [i.pk for i in classes]
    notifications = Notification.objects.filter(studentClasses__in=classIds).distinct()

    modified = False
    for i in notifications:
        if i.end < sgt.localize(datetime.now()):
            i.delete()
            modified = True
    
    if modified:
        notifications = Notification.objects.filter(studentClasses__in=classIds).distinct()

    return render(request, 'notifications/view.html', {"notifications": notifications})


@login_required
def manageNotifications(request):
    notifications = Notification.objects.all()

    modified = False
    for i in notifications:
        if i.end < sgt.localize(datetime.now()):
            i.delete()
            modified = True

    if modified:
        notifications = Notification.objects.all()

    return render(request, 'notifications/manage.html', {"notifications": notifications})


@login_required
def createNotification(request):
    if request.user.accountType != 'Teacher':
        return redirect("/")

    # if submitting form
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']

        start = request.POST['start']
        end = request.POST['end']

        newNotification = Notification()
        newNotification.title = title
        newNotification.content = content

        newNotification.start = sgt.localize(datetime.strptime(start, "%b %d, %Y"))
        newNotification.end = sgt.localize(datetime.strptime(end, "%b %d, %Y"))

        newNotification.save()

        if "selectedClasses" in request.POST:
            selectedClasses = request.POST.getlist('selectedClasses')
            for id in selectedClasses:
                sClass = StudentClass.objects.get(id=id)
                newNotification.studentClasses.add(sClass)


        context = {"notification": "Successfully created notification", "notifications": Notification.objects.all()}
        return render(request, 'notifications/manage.html', context)

    else:
        context = {"classObjects": StudentClass.objects.all, }
        return render(request, 'notifications/create.html', context)


# livestream edit page
@login_required
def editNotification(request, NotificationID):
    if request.user.accountType != 'Teacher':
        return redirect("/")

    notification = Notification.objects.get(id=NotificationID)

    # if submitting form
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']

        notification.title = title
        notification.content = content
        notification.save()

        if "selectedClasses" in request.POST:
            selectedClasses = request.POST.getlist('selectedClasses')
            for id in selectedClasses:
                sClass = StudentClass.objects.get(id=id)
                notification.studentClasses.add(sClass)

        context = {"notification": "Successfully edited live lesson", "notifications": Notification.objects.all()}
        return render(request, 'notifications/manage.html', context)

    else:
        start = sgt.normalize(notification.start).strftime("%b %d, %Y")
        end = sgt.normalize(notification.end).strftime("%b %d, %Y")

        classIds = [i.pk for i in notification.studentClasses.all()]

        context = {"classObjects": StudentClass.objects.all, "notif": notification, "start": start, "end": end, "classIds": classIds }
        return render(request, 'notifications/edit.html', context)


def deleteNotification(request, NotificationID):
    if request.user.accountType != 'Teacher':
        return redirect("/")

    notification = Notification.objects.get(id=NotificationID)
    notification.delete()

    return HttpResponse("Success")
