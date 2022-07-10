from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Lesson
from accountManagement.models import Module, Course, User

import json
import re

import pytz
sgp = pytz.timezone('Asia/Singapore')


# file management page
@login_required
def manageUploads(request):

    context = {"lessonObjects": Lesson.objects.all, }

    return render(request, 'lessons/manage.html', context)


# file creation page
@login_required
def createLesson(request):
    nowTime = datetime.now()
    timestamp = nowTime.strftime("%Y-%m-%d-%H-%M")

    courseObjects = list(Course.objects.all())
    courseIDs = [i.id for i in courseObjects]

    baseContext = {"fileIDtoUse": "lesson%s" % (
        timestamp), "courseObjects": courseObjects, "courseIDs": courseIDs, "moduleObjects": Module.objects.all, "lessonObjects": Lesson.objects.all}

    # if uploadig file
    if request.method == 'POST':

        # get values from submitted form
        lessonName = request.POST["lessonName"]
        fileID = request.POST["fileID"]

        # validate that file name is unique
        if (Lesson.objects.filter(name=lessonName).exists()):
            context = {
                **baseContext, "error": "Sorry, a lesson with this name already exists, please choose a different name for your lesson.", }
            return render(request, 'lessons/manage.html', context)
        else:

            if 'uploadedFile' in request.FILES:
                # get extension
                fileExtension = re.findall(
                    r"\..*", request.POST["fileName"])[-1]

                # handle files
                request.FILES['uploadedFile'].name = "%s%s" % (
                    fileID, fileExtension)
                if (Lesson.objects.filter(uploadedFile=request.FILES['uploadedFile']).exists()):
                    # return error
                    context = {
                        **baseContext, "error": "Error, the lesson ID already exists, please try again", }
                    return render(request, 'lessons/manage.html', context)

            else:
                # return error
                context = {
                    **baseContext, "error": "No file uploaded, please select a file to upload", }
                return render(request, 'lessons/manage.html', context)

            # find matching course
            moduleID = request.POST["moduleID"]
            module = Module.objects.get(pk=moduleID)

            # create project with entered values
            newLesson = Lesson()
            newLesson.name = lessonName
            newLesson.fileID = fileID
            newLesson.uploadedFile = request.FILES['uploadedFile']
            newLesson.module = module
            newLesson.save()
            # return success
            context = {"lessonObjects": Lesson.objects.all,
                       "notification": "Lesson: %s successfully uploaded!" % (lessonName), }
            return render(request, 'lessons/manage.html', context)

    else:
        return render(request, 'lessons/create.html', baseContext)


# file edit page
@login_required
def deleteLesson(request, lessonID):

    # if editing file
    if request.method == 'POST':
        fileToDelete = Lesson.objects.get(fileID=lessonID)
        fileToDelete.uploadedFile.delete()
        fileToDelete.delete()

        context = {"fileObjects": Lesson.objects.all,
                   "notification": "File successfully deleted!", }
        return render(request, 'lessons/manage.html', context)

    else:
        fileToDelete = Lesson.objects.get(fileID=lessonID)
        context = {"fileToDelete": fileToDelete}
        return render(request, 'lessons/delete.html', context)


@login_required
def viewLesson(request, lessonID):
    return render(request, 'lessons/view.html', {'lesson': Lesson.objects.get(fileID=lessonID)})
