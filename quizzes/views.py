from datetime import datetime
from dateutil import parser
import json
from django.http import HttpResponse, JsonResponse
from openpyxl import Workbook
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from accountManagement.models import Course, Module, User

from quizzes.models import Option, Question, QuestionAttempt, QuestionTag, Quiz, QuizAttempt, QuizImage

import json

import pytz

sgt = pytz.timezone("Asia/Singapore")


@login_required
def manageQuizzes(request):
    messageCode = request.GET.get("m", "")
    context = {"quizObjects": Quiz.objects.all}
    if messageCode == "qd":
        context = {
            "quizObjects": Quiz.objects.all,
            "notification": "Quiz successfully deleted",
        }

    return render(request, "manage.html", context)


@login_required
def createQuiz(request):

    if request.method == "POST":
        newQuiz = Quiz()

        newQuiz.quizName = request.POST["quizName"]

        quizID = "quiz" + datetime.now().strftime("%Y-%m-%d-%H-%M")
        newQuizID = quizID
        addDigit = 0
        while Quiz.objects.filter(quizID=newQuizID):
            newQuizID = quizID + str(addDigit)
            addDigit += 1

        newQuiz.quizID = newQuizID

        newQuiz.save()
        return redirect(f"/quizzes/{newQuizID}/edit/")

    return render(request, "create.html")


@login_required
def editQuiz(request, quizID):
    return render(request, "edit.html")


@login_required
def doQuiz(request, quizID):
    return render(request, "do.html")


@login_required
def editQuizSettings(request, quizID):
    if request.method == "POST":
        quizObj = Quiz.objects.get(quizID=quizID)

        data = json.loads(request.body)
        quizObj.quizName = data["quizName"]
        quizObj.passingScore = data["passingScore"]
        quizObj.randomOptions = data["randomOptions"]
        quizObj.randomQuestions = data["randomQuestions"]
        quizObj.questionOrder = data["questionOrder"]
        try:
            quizObj.quizDueDate = parser.parse(data["dueDate"])
        except:
            pass
        try:
            mod = Module.objects.get(id=data["moduleId"])
            quizObj.module = mod
        except:
            pass
        quizObj.save()

        return JsonResponse({"success": True})
    return JsonResponse({"error": "POST only"})


@login_required
def getQuiz(request, quizID):
    quizObj = Quiz.objects.get(quizID=quizID)
    return JsonResponse(quizObj.toDict())


@login_required
def getQuizDo(request, quizID):
    quizObj = Quiz.objects.get(quizID=quizID)
    return JsonResponse(quizObj.doToDict())


@login_required
def getCourses(request):
    courses = list(Course.objects.all())
    return JsonResponse({"courses": [i.toDict() for i in courses]})


@login_required
def getModules(request):
    modules = Module.objects.filter(course_id=request.GET.get("courseId", -1))

    return JsonResponse({"modules": [i.toDict() for i in modules]})


@login_required
def addQuestion(request, quizID):
    if request.method == "POST":
        quizObj = Quiz.objects.get(quizID=quizID)

        newQuestion = Question()
        newQuestion.quiz = quizObj

        newQuestion.save()
        return JsonResponse({"success": True})

    return JsonResponse({"error": "POST only"})


@login_required
def addBank(request, quizID, questionID):
    if request.method == "POST":
        quizObj = Quiz.objects.get(quizID=quizID)
        questionObj = Question.objects.get(id=questionID)

        qClone = questionObj.make_clone()
        qClone.quiz = quizObj
        qClone.isBankQuestion = False

        oldCbAnswer = json.loads(qClone.cbAnswer)
        newCbAnswer = []
        for id in oldCbAnswer:
            oldOption = Option.objects.get(id=id)
            newCbAnswer.append(qClone.options.get(text=oldOption.text).id)
        qClone.cbAnswer = json.dumps(newCbAnswer)

        if qClone.mcAnswer != -1:
            oldOption = Option.objects.get(id=qClone.mcAnswer)
            qClone.mcAnswer = qClone.options.get(text=oldOption.text).id

        qClone.save()
        return JsonResponse({"success": True})

    return JsonResponse({"error": "POST only"})


@login_required
def getQuestions(request, quizID):
    questions = Question.objects.filter(
        quiz_id=Quiz.objects.get(quizID=quizID).id)

    return JsonResponse({"questions": [i.toDict() for i in questions]})


@login_required
def getQuestion(request, questionID):
    return JsonResponse(Question.objects.get(id=questionID).toDict())


@login_required
def deleteQuestion(request):
    if request.method == "POST":
        data = json.loads(request.body)
        questionToDelete = Question.objects.get(id=data["questionId"])
        questionToDelete.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"error": "POST only"})


@login_required
def deleteQuestionBank(request, questionID):
    questionToDelete = Question.objects.get(id=questionID)
    questionToDelete.delete()
    return redirect("/quizzes/bank/")


@login_required
def editQuestion(request):
    if request.method == "POST":
        data = json.loads(request.body)

        questionObj = Question.objects.get(id=data["id"])

        questionObj.text = data["text"]
        questionObj.type = data["type"]
        questionObj.optionOrder = data["optionOrder"]
        questionObj.autoGrade = data["validate"]
        questionObj.mcAnswer = data["mcAnswer"]
        questionObj.cbAnswer = data["cbAnswer"]
        questionObj.saAnswer = data["saAnswer"]

        try:
            questionObj.name = data["questionName"]
        except:
            pass

        try:
            tag = QuestionTag.objects.get(id=data["tagId"])
        except:
            tag = None
        questionObj.questionTag = tag

        questionObj.save()

        return JsonResponse({"success": True})
    return JsonResponse({"error": "POST only"})


@login_required
def addOption(request):
    if request.method == "POST":
        data = json.loads(request.body)

        questionObj = Question.objects.get(id=data["questionId"])

        newOption = Option()
        newOption.question = questionObj

        newOption.save()
        return JsonResponse({"success": True})

    return JsonResponse({"error": "POST only"})

@login_required
def setImage(request):
    if request.method == "POST":
        questionObj = Question.objects.get(id=request.POST["questionId"])
        newImage = QuizImage.objects.create(imageFile = request.FILES["image"])

        if questionObj.image != None:
            questionObj.image.imageFile.delete(save=False)
            questionObj.image.delete()
        questionObj.image = newImage
        questionObj.save()
        return JsonResponse({"success": True, "imageUrl": newImage.imageFile.url})
    return JsonResponse({"error": "POST only"})

@login_required
def deleteImage(request):
    if request.method == "POST":
        data = json.loads(request.body)
        imageToDelete = Question.objects.get(id=data["questionId"]).image
        imageToDelete.imageFile.delete(save=False)
        imageToDelete.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"error": "POST only"})

@login_required
def getOptions(request):
    options = Option.objects.filter(
        question_id=request.GET.get("questionId", -1))
    return JsonResponse({"options": [i.toDict() for i in options]})


@login_required
def editOption(request):
    if request.method == "POST":
        data = json.loads(request.body)

        optionObj = Option.objects.get(id=data["id"])
        optionObj.text = data["text"]
        optionObj.save()

        return JsonResponse({"success": True})
    return JsonResponse({"error": "POST only"})


@login_required
def deleteOption(request):
    if request.method == "POST":
        data = json.loads(request.body)
        optionToDelete = Option.objects.get(id=data["id"])
        optionToDelete.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"error": "POST only"})


@login_required
def cbValidation(request):
    if request.method == "POST":
        data = json.loads(request.body)

        questionObj = Question.objects.get(id=data["questionId"])
        questionObj.mcAnswer = data["correctOption"]
        questionObj.save()

        return JsonResponse({"success": True})
    return JsonResponse({"error": "POST only"})


@login_required
def deleteQuiz(request, quizID):
    Quiz.objects.filter(quizID=quizID)[0].delete()
    return redirect("/quizzes/manage/?m=qd")


@login_required
def duplicateQuiz(request, quizID):
    quizObj = Quiz.objects.get(quizID=quizID)
    qClone = quizObj.make_clone()
    qClone.quizName += " copy"
    qClone.quizID += "r"
    while Quiz.objects.filter(quizID=qClone.quizID).exists():
        qClone.quizID += "r"
    qClone.save()
    for qn in qClone.questions.all():
        if qn.type == 'cb' and qn.autoGrade:
            oldIds = json.loads(qn.cbAnswer)
            newIds = []
            for oldId in oldIds:
                qtext = Option.objects.get(id=oldId).text
                newId = qn.options.get(text=qtext).id
                newIds.append(newId)
            qn.cbAnswer = json.dumps(newIds)
            qn.save()

    return redirect("/quizzes/" + qClone.quizID + "/edit/")


@login_required
def clearCbOptions(request, quizID):
    if request.user.username != 'YonkTeacher':
        return JsonResponse({'failure': 'not authorised'})
    quiz = Quiz.objects.get(quizID=quizID)
    for qn in quiz.questions.all():
        if qn.type == 'cb':
            qn.cbAnswer = '[]'
            qn.save()
    return JsonResponse({'success': True})


@login_required
def submit(request, quizID):
    if request.method == "POST":
        if QuizAttempt.objects.filter(quiz__quizID=quizID, student_id=request.user.id).exists():
            return redirect("/quizzes/" + quizID + "/do/")

        quizObj = Quiz.objects.get(quizID=quizID)
        data = json.loads(request.body)

        questions = list(quizObj.questions.all())

        attempt = QuizAttempt()
        attempt.quiz = quizObj
        attempt.student = User.objects.get(id=request.user.id)
        attempt.timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        att = attempt.save()

        score = 0
        for question in questions:
            questionAttempt = QuestionAttempt()
            questionAttempt.question = question
            questionAttempt.quizAttempt = attempt
            questionAttempt.type = question.type
            res = data[str(question.id)]["response"]
            if question.type == "cb":
                questionAttempt.cbAnswer = json.dumps(res)
                if question.autoGrade:
                    questionAttempt.isCorrect = set(res) == set(
                        json.loads(question.cbAnswer)
                    )
                    if questionAttempt.isCorrect:
                        score += 1
            if question.type == "mc":
                questionAttempt.mcAnswer = res
                if question.autoGrade:
                    questionAttempt.isCorrect = res == question.mcAnswer
                    if questionAttempt.isCorrect:
                        score += 1
            if question.type == "sa":
                questionAttempt.saAnswer = res
                if question.autoGrade:
                    questionAttempt.isCorrect = res == question.saAnswer
                    if questionAttempt.isCorrect:
                        score += 1
            if question.type == "la":
                questionAttempt.saAnswer = res
            questionAttempt.save()

        attempt.score = score
        attempt.save()

        return JsonResponse({"success": True})

    return JsonResponse({"error": "POST only"})


@login_required
def getAttempt(request, quizID):
    try:
        attempt = QuizAttempt.objects.get(
            quiz__quizID=quizID, student_id=request.user.id)

        return JsonResponse({"attempted": True, "attempt": attempt.toDict()})
    except:
        return JsonResponse({"attempted": False})


# quiz management page
@login_required
def downloadQuiz(request):
    try:
        selectedId = request.GET["id"]
    except:
        selectedId = ""

    allQs = list(Quiz.objects.all())

    myClasses = request.user.classes.all()
    myCourses = set()
    for i in myClasses:
        myCourses.update(i.courses.all())

    myQs = []

    for i in allQs:
        if i.module.course in myCourses:
            myQs.append(i)

    context = {"quizObjects": myQs, "selectedId": selectedId}

    return render(request, 'download.html', context)


@login_required
def exportQuiz(request):

    wb = Workbook()
    qte = Quiz.objects.get(quizID=request.GET["id"])
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}.xlsx"'.format(
        qte.quizID)

    quizName = qte.quizName
    passingScore = qte.passingScore

    ws = wb.active

    # format header
    baseHeader = ["Class", "Name", "Designation", "Start Date",
                  "QuizName", "Timestamp", "Score", "Passing Score", "Competency"]

    questions = list(Question.objects.filter(quiz_id=qte.id))

    baseHeader += [f'Q{n+1} {i.text}' for n, i in enumerate(questions)]

    ws.append(baseHeader)

    for attempt in list(QuizAttempt.objects.filter(quiz_id=qte.id)):
        user = attempt.student
        newLine = []

        timestamp = "-"
        if attempt.timestamp:
            timestamp = attempt.timestamp

        tryAppend(newLine, str(user.classes.first()))
        tryAppend(newLine, str(user.first_name + " " + user.last_name))
        tryAppend(newLine, user.designation)
        tryAppend(newLine, str(user.startDate))
        tryAppend(newLine, qte.quizName)
        tryAppend(newLine, timestamp)
        tryAppend(newLine, attempt.score)
        tryAppend(newLine, qte.passingScore)
        if attempt.score >= qte.passingScore:
            tryAppend(newLine, "Competent")
        else:
            tryAppend(newLine, "Not yet competent")

        for question in questions:
            try:
                questionAttempt = attempt.questionAttempts.get(
                    question_id=question.id)
                if question.autoGrade:
                    if questionAttempt.isCorrect:
                        tryAppend(newLine, "1")
                    else:
                        tryAppend(newLine, "0")
                else:
                    tryAppend(newLine, "-")
            except: 
                tryAppend(newLine, "DNA")

        ws.append(newLine)

    wb.save(response)
    return response


def tryAppend(l, data):
    try:
        l.append(data)
    except:
        l.append("")


def createTag(request, courseID):
    if request.method == "POST":
        newTag = QuestionTag()
        newTag.text = request.POST["text"]
        course = Course.objects.get(id=courseID)
        newTag.course = course

        newTag.save()
        return redirect("/courses/")
    return JsonResponse({"error": "POST only"})


def deleteTag(request, tagID):
    if request.method == "POST":
        tag = QuestionTag.objects.get(id=tagID)
        tag.delete()
        return redirect("/courses/")
    return JsonResponse({"error": "POST only"})


def getTags(request):
    tags = QuestionTag.objects.filter(course_id=request.GET.get("courseId"))
    return JsonResponse({"tags": [tag.toDict() for tag in tags]})


def questionBank(request):
    context = {"questions": Question.objects.filter(isBankQuestion=True)}
    return render(request, "bank.html", context)


def createBank(request):
    newQuestion = Question()
    newQuestion.isBankQuestion = True
    newQuestion.save()

    return redirect("/quizzes/bank/" + str(newQuestion.id) + "/edit/")


def editBank(request, questionID):
    return render(request, "editBank.html")


def getBank(request):
    questions = Question.objects.filter(isBankQuestion=True)
    return JsonResponse({"questions": [question.toDict() for question in questions]})
