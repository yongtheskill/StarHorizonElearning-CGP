import re
import json
from time import sleep
import humanize
import string
import random
from datetime import date, datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from lessons.models import Lesson

from .models import User, Course, StudentClass, Module
from quizzes.models import Quiz
from videoLessons.models import Video
from quizzes.models import Quiz, QuizAttempt
from fileUploads.models import FileUpload
from liveLesson.models import LiveLesson

import pytz
sgt = pytz.timezone('Asia/Singapore')


# Create your views here.

# Login Page

def loginHome(request):

    if request.user.is_authenticated:
        return redirect('/')

    context = {'displayFailMessage': False}
    nextURL = request.GET.get('next')

    if request.POST:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                '''if request.user.passwordChangeRequired:
                    
                    context = {'email': request.user.email, 'phoneNumber': request.user.phoneNumber, "forcePwChange": "yes",}
                    userId = request.user.id
                    user = User.objects.get(id = userId)
                    
                    return render(request, 'core/manageAccount.html', context)'''

                if nextURL is not None:
                    return redirect(nextURL)
                else:
                    return redirect('/')
                #context = {'authStatus': "Log in success",}
                # return render(request, 'projects/home.html', context)

        else:
            context = {'displayFailMessage': True}

    return render(request, 'accountManagement/login.html', context)

# Logout Page


def logoutHome(request):

    if request.POST:
        logout(request)
        return redirect('/')

    return render(request, 'accountManagement/logout.html')

# Manage Account Page


@login_required
def manageAccount(request):
    context = {'email': request.user.email,
               'phoneNumber': request.user.phoneNumber}
    userId = request.user.id
    user = User.objects.get(id=userId)
    if request.POST:
        user.email = request.POST['email']
        user.phoneNumber = request.POST['phoneNumber']
        user.passwordChangeRequired = False
        user.save()
        context = {'email': request.user.email, 'phoneNumber': request.user.phoneNumber,
                   "notification": "Successfully updated details", }
        return render(request, 'accountManagement/manageAccount.html', context)

    return render(request, 'accountManagement/manageAccount.html', context)

# Change password page


@login_required
def changePassword(request):

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accountManagement/changePassword.html', {'form': form})

# View list of students and teachers in class


@login_required
def classView(request, classId):

    studentClass = StudentClass.objects.get(id=classId)
    teachers = list(User.objects.filter(
        classes=classId, accountType="Teacher"))
    students = list(User.objects.filter(
        classes=classId, accountType="Student"))
    courses = list(studentClass.courses.all())

    courses.sort(key=lambda x: x.courseName)
    liveLessonsNew, liveLessonsOld = newnessChecker(
        list(LiveLesson.objects.filter(studentClass=classId)))

    for course in courses:
        course.modules = list(Module.objects.filter(course=course))

    modules = []
    for i in courses:
        modules += list(Module.objects.filter(course=i))

    quizzes = []
    for i in modules:
        quizzes += list(Quiz.objects.filter(module=i))

    quizData = []
    for quiz in quizzes:
        quizData.append({
            "name": quiz.quizName,
            "completed": len([i for i in QuizAttempt.objects.filter(quiz__quizID=quiz.quizID) if i.student.classes.filter(id=classId).exists()]),
            "passed": len([i for i in list(QuizAttempt.objects.filter(quiz__quizID=quiz.quizID)) if i.score >= quiz.passingScore and i.student.classes.filter(id=classId).exists()]),
            "id": quiz.quizID
        })

    context = {"class": studentClass, "teachers": teachers, "students": students, "courses": courses,
               "liveLessonsNew": liveLessonsNew, "liveLessonsOld": liveLessonsOld, "quizData": quizData, "nStudents": len(students), }

    return render(request, 'accountManagement/classView.html', context)

# View list of classes participating in a course, as well as course materials


@login_required
def courseView(request, courseId):
    user = request.user

    course = Course.objects.get(id=courseId)
    classes = list(StudentClass.objects.filter(courses=courseId))
    ownClasses = [x for x in classes if x in list(user.classes.all())]
    otherClasses = [x for x in classes if not x in list(user.classes.all())]
    modules = list(Module.objects.filter(course=courseId))

    for module in modules:
        allQuizzes = list(Quiz.objects.filter(module=module))

        quizResponseJSON = user.quizResponses
        if quizResponseJSON and "__________RESPONSESPLITTER__________" in quizResponseJSON:
            allQuizResponses = quizResponseJSON.split(
                "__________RESPONSESPLITTER__________")[1:]

            for i in allQuizResponses:
                for j in allQuizzes:
                    if j.quizName == json.loads(i)[0]["quizName"]:
                        # allQuizzes.remove(j)
                        pass

        quizzesNew, quizzesOld = newnessChecker(allQuizzes)
        module.quizzesAll = [{"quiz": q, "new": True} for q in quizzesNew]
        module.quizzesAll.extend([{"quiz": q, "new": False}
                                 for q in quizzesOld])
        module.quizzesAll.sort(key=lambda x: x["quiz"].quizID)

        videoLessonsNew, videoLessonsOld = newnessChecker(
            list(Video.objects.filter(module=module)))
        module.videoLessonsAll = [{"vLesson": v, "new": True}
                                  for v in videoLessonsNew]
        module.videoLessonsAll.extend(
            [{"vLesson": v, "new": False} for v in videoLessonsOld])
        module.videoLessonsAll.sort(key=lambda x: x["vLesson"].videoID)

        fileUploadsNew, fileUploadsOld = newnessChecker(
            list(FileUpload.objects.filter(module=module)))
        module.fileUploadsAll = [{"file": f, "new": True}
                                 for f in fileUploadsNew]
        module.fileUploadsAll.extend(
            [{"file": f, "new": False} for f in fileUploadsOld])
        module.fileUploadsAll.sort(key=lambda x: x["file"].fileID)

        lessonsNew, lessonsOld = newnessChecker(
            list(Lesson.objects.filter(module=module)))
        module.lessonsAll = [{"lesson": l, "new": True}
                             for l in lessonsNew]
        module.lessonsAll.extend(
            [{"lesson": l, "new": False} for l in lessonsOld])
        module.lessonsAll.sort(key=lambda x: x["lesson"].fileID)

    context = {"course": course, "ownClasses": ownClasses,
               "otherClasses": otherClasses, "modules": modules, }

    return render(request, 'accountManagement/courseView.html', context)


@login_required
def individualAccountQuizView(request, userId, quizName):

    user = User.objects.get(id=userId)

    origQuiz = Quiz.objects.get(quizName=quizName)
    origQuizData = json.loads(origQuiz.quizData)

    if user.timeOnline:
        timeOnline = humanize.naturaldelta(user.timeOnline)
    else:
        timeOnline = "0 minutes"

    quizResponseJSON = user.quizResponses
    if quizResponseJSON and "__________RESPONSESPLITTER__________" in quizResponseJSON:
        allQuizResponses = quizResponseJSON.split(
            "__________RESPONSESPLITTER__________")[1:]

        for i in allQuizResponses:
            if(json.loads(i)[0]["quizName"]):
                quiz = json.loads(i)
                break

        questionTypeLookup = {"la": "Long Answer", "sa": "Short Answer",
                              "cb": "Checkboxes", "mc": "Multiple Choice"}

        quizResData = []

        for question in quiz[1:]:
            quizDataElem = {}

            origQuestion = origQuizData[next((index for (index, d) in enumerate(
                origQuizData) if d["questionID"] == question["questionID"]), None)]

            quizDataElem["type"] = questionTypeLookup[question["questionType"]]
            quizDataElem["title"] = origQuestion["questionTitle"]

            if "isAutoGraded" in origQuestion and origQuestion["isAutoGraded"]:
                quizDataElem["correct"] = str(origQuestion["correctAnswer"])
            else:
                quizDataElem["correct"] = "-"

            if question["questionType"] == "cb":
                answers = ""
                for j in question["studentCheckboxValues"]:
                    if question["studentCheckboxValues"][j] == True:
                        answers += "{}, ".format(j)
                answers = answers[:-2]
                quizDataElem["ans"] = answers
            else:
                quizDataElem["ans"] = question["studentResponse"]

            quizResData.append(quizDataElem)

        context = {"tempUser": user, "timeOnline": timeOnline,
                   "qData": quizResData, "qName": quizName}
    else:
        context = {"tempUser": user, "timeOnline": timeOnline}

    return render(request, 'accountManagement/inidvidualAccountQuizView.html', context)


@login_required
def individualAccountView(request, userId):

    user = User.objects.get(id=userId)

    if request.method == "POST":
        user.quizResponses = ""
        user.save()

    classes = list(user.classes.all())

    if user.timeOnline:
        timeOnline = humanize.naturaldelta(user.timeOnline)
    else:
        timeOnline = "0 minutes"

    print(user.attempts.all())

    context = {"tempUser": user, "classes": classes,
               "timeOnline": timeOnline, "attempts": user.attempts.all()}

    return render(request, 'accountManagement/individualAccountView.html', context)


@login_required
def classListView(request):

    classes = list(request.user.classes.all())

    outstandingQuizzes = []
    outstandingLivelessons = []

    for studentClass in classes:

        outstandingLivelessons += list(LiveLesson.objects.filter(
            studentClass=studentClass, streamTime__contains=date.today()))

        for course in studentClass.courses.all():
            modules = list(Module.objects.filter(course=course))

            for module in modules:
                outstandingQuizzes += list(Quiz.objects.filter(
                    module=module, quizDueDate__contains=date.today()))

    context = {"classes": classes, "outstandingQuizzes": outstandingQuizzes,
               "outstandingLivelessons": outstandingLivelessons, }

    return render(request, 'accountManagement/classListView.html', context)


def courseListView(request):

    classes = list(request.user.classes.all())

    courseList = []

    for studentClass in classes:

        courses = list(Course.objects.filter(studentclass=studentClass))

        courses.sort(key=lambda x: x.courseName)

        for entry in courses:
            if entry not in courseList:
                courseList.append(entry)
            else:
                pass

    for course in courseList:
        course.modules = list(Module.objects.filter(course=course))

    context = {"courses": courseList, }

    return render(request, 'accountManagement/courseListView.html', context)


def newnessChecker(materialList):
    # Used in courseview page
    # Detects what course materials are new (within 2 days), places them on top of the list
    today = sgt.localize(datetime.today())

    timeLimit = today-timedelta(hours=48)

    oldMaterials = []
    newMaterials = []

    for material in materialList:
        if material.creationDate > timeLimit:
            newMaterials.append(material)
        else:
            oldMaterials.append(material)

    return newMaterials, oldMaterials


@login_required
def createClass(request):
    courseObjects = list(Course.objects.all())
    courseIDs = [i.id for i in courseObjects]

    if request.method == 'POST':

        # find matching course
        courseIDs = request.POST.getlist("courseSelector")
        courseList = []
        for courseID in courseIDs:
            courseList.append(Course.objects.get(pk=courseID))

        # create project with entered values
        newClass = StudentClass()
        newClass.className = request.POST["className"]
        newClass.institution = request.POST["institution"]
        newClass.save()
        newClass.courses.add(*courseList)
        newClass.save()

        request.user.classes.add(newClass)

        # return success
        classes = list(request.user.classes.all())
        for studentClass in classes:
            outstandingLivelessons = list(LiveLesson.objects.filter(
                studentClass=studentClass, streamTime__contains=date.today()))
            livelessonObjs = [
                i for i in outstandingLivelessons if i.studentClass in classes]
            for course in studentClass.courses.all():
                modules = list(Module.objects.filter(course=course))
                for module in modules:
                    outstandingQuizzes = list(Quiz.objects.filter(
                        module=module, quizDueDate__contains=date.today()))

        context = {"classes": classes, "outstandingQuizzes": outstandingQuizzes,
                   "outstandingLivelessons": outstandingLivelessons, "notification": "Class successfully uploaded!", }

        return render(request, 'accountManagement/classListView.html', context)

    else:
        return render(request, 'accountManagement/createClass.html', {"courseObjects": courseObjects, "courseIDs": courseIDs, })


@login_required
def createCourse(request, classId):

    if request.method == 'POST':

        # find matching course
        courseIDs = request.POST.getlist("courseSelector")
        courseList = []
        for courseID in courseIDs:
            courseList.append(Course.objects.get(pk=courseID))

        # create project with entered values
        newCourse = Course()
        newCourse.courseName = request.POST["courseName"]
        newCourse.courseInstitution = request.POST["institution"]
        newCourse.desc = request.POST["desc"]
        newCourse.quizTags = "[]"
        newCourse.save()

        studentClass = StudentClass.objects.get(id=classId)
        studentClass.courses.add(newCourse)

        return courseView(request, newCourse.pk)

    else:
        return render(request, 'accountManagement/createCourse.html', {})


@login_required
def createModule(request, courseId):

    if request.method == 'POST':

        # find matching course
        course = Course.objects.get(pk=courseId)

        # create project with entered values
        newModule = Module()
        newModule.moduleName = request.POST["moduleName"]
        newModule.course = course
        newModule.save()

        return courseView(request, courseId)

    else:
        return render(request, 'accountManagement/createModule.html', {})


def forgotPassword(request):

    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.POST["username"])
        except:
            sleep(1+random.random()*2)
            return render(request, 'accountManagement/resetNotification.html', {"mainText": "Please check your email to reset your password.", "secText": "The email will only be sent if an account corresponding to your username exists."})

        user.pwResetCode = ''.join(random.choice(
            string.ascii_letters) for i in range(64))

        user.pwResetTime = sgt.localize(
            datetime.now()) + timedelta(minutes=15)

        user.save()

        resetUrl = f'http://cgpsdotraining.com/pwr/{user.pwResetCode}'

        html_message = render_to_string('accountManagement/pwreset.html', {
                                        'firstName': user.first_name, 'lastName': user.last_name, 'resetUrl': resetUrl})
        plain_message = f'''Hi {user.first_name} {user.last_name},

You requested a password reset for the CGPSDOTRAINING website.
Please click on the following link to reset your password.
{resetUrl}
Note: the link will expire in 15 minutes.

Thank you.'''

        send_mail(
            'Password Reset - CGP SDO Training',
            plain_message,
            'CGP SDO Training <noreply@cgpsdotraining.com>',
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )

        return render(request, 'accountManagement/resetNotification.html', {"mainText": "Please check your email to reset your password.", "secText": "The email will only be sent if an account corresponding to your username exists."})

    else:
        return render(request, 'accountManagement/forgotPassword.html')


def forgotPasswordReset(request, passwordCode):
    try:
        user = User.objects.get(pwResetCode=passwordCode)
    except:
        return render(request, 'accountManagement/resetNotification.html', {"mainText": "Password reset link is invalid."})

    if sgt.localize(datetime.now()) > user.pwResetTime:
        return render(request, 'accountManagement/resetNotification.html', {"mainText": "Password reset link has expired."})

    if request.method == 'POST':

        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            user.pwResetTime = user.pwResetTime - timedelta(hours=1)
            user.save()
            return render(request, 'accountManagement/resetNotification.html', {"mainText": "Password successfully reset."})
        else:
            messages.error(request, 'Password does not meet requirements.')
    else:
        list(messages.get_messages(request))
        form = PasswordChangeForm(user)
    return render(request, 'accountManagement/passwordReset.html', {'form': form})
