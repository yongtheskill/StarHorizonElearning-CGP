from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Quiz, Question
from accountManagement.models import Course, Module, User

import json
import re

import base64

import pytz
sgt = pytz.timezone('Asia/Singapore')
from datetime import datetime

from openpyxl import Workbook
from django.http import HttpResponse, JsonResponse





@login_required
def bankGet(request, questionID):
    question = Question.objects.filter(pk=questionID)[0]

    return JsonResponse(json.loads(question.questionData))




@login_required
def bankDelete(request, questionID):
    qtd = Question.objects.filter(pk=questionID)
    try:
        qtd.delete()
    except:
        context = {"questionObjects": Question.objects.all, "error": "Error deleting question, please do not use the back button or refresh the page"}
    context = {"questionObjects": Question.objects.all, "notification": "Successfully deleted question"}

    return render(request, 'quizzes/manageBank.html', context)

#quiz creation page
@login_required
def bankCreate(request):
   
    #if submitting form
    if request.method == 'POST':
        qJSON = request.POST['allQuestionsJSON']
        qJSON = re.sub("_____var__", "", qJSON) #remove js stuff
        qData = json.loads(qJSON)[0]
        questionName = request.POST['questionName']

        if Question.objects.filter(questionName=questionName):
            context = {"questionObjects": Question.objects.all, "error": "This question name is already being used, please choose a new question name."}
            return render(request, 'quizzes/manageBank.html', context)


        newQuestion = Question()
        newQuestion.questionName = questionName
        newQuestion.questionData = json.dumps(qData)
        newQuestion.save()
        
        context = {"questionObjects": Question.objects.all, "notification": "Successfully created questions"}
        return render(request, 'quizzes/manageBank.html', context)


    else:
        
        context = {}
        return render(request, 'quizzes/bankCreate.html', context)









#quiz management page
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
        myCourses.update( i.courses.all() )
        
    myQs = []
    
    for i in allQs:
        if i.module.course in myCourses:
            myQs.append(i)


    context = {"quizObjects": myQs, "selectedId": selectedId}

    return render(request, 'quizzes/download.html', context)



@login_required
def exportQuiz(request):

    wb = Workbook()
    qte = Quiz.objects.get(quizID=request.GET["id"])    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}.xlsx"'.format(qte.quizID)
    quizName = qte.quizName
    passingScore = qte.passingScore

    qte = json.loads(qte.quizData)
    ws = wb.active

    #format header
    baseHeader = ["Class", "Name", "Designation", "Start Date", "QuizName", "Score", "Passing Score", "Competency"]
    quizLen = len(qte)
    qLi = []
    qtLi = []
    qTags = []

    for i in range(quizLen):
        qLi.append("Q"+ str(i+1))
        qtLi.append("Q"+ str(i+1) + "Tag")
        try:
            qTags.append(qte[i]["questionTag"])
        except:
            qTags.append("")
    
    baseHeader += qLi
    baseHeader += qtLi
    
    ws.append(baseHeader)

    allUsers = list(User.objects.all())

    #for user in allUsers:
    for user in allUsers:
        quizResponseJSON = user.quizResponses
        if quizResponseJSON and "__________RESPONSESPLITTER__________" in quizResponseJSON:
            allQuizResponses = quizResponseJSON.split("__________RESPONSESPLITTER__________")[1:]

            for i in allQuizResponses:
                quizData = json.loads(i)
                if quizData[0]["quizName"] == quizName:
                    newLine = []

                    try:
                        newLine.append(str(user.classes.all()[0]))
                    except:
                        newLine.append("")

                    try:
                        newLine.append(user.first_name + " " + user.last_name)
                    except:
                        newLine.append("")
                    
                    try:
                        newLine.append(user.designation)
                    except:
                        newLine.append("")
                    
                    try:
                        newLine.append(str(user.startDate))
                    except:
                        newLine.append("")
                    
                    try:
                        newLine.append(quizName)
                    except:
                        newLine.append("")

                    score = len(re.findall(r'"isCorrect": true', i))
                    try:
                        newLine.append(str(score))
                    except:
                        newLine.append("")
                    try:
                        newLine.append(str(passingScore))
                    except:
                        newLine.append("")
                    if(score >= passingScore):
                        newLine.append("Competent")
                    else:
                        newLine.append("Not Yet Competent")

                    correctData = []
                    for j in quizData[1:]:
                        if j["isCorrect"]:
                            correctData.append("1")
                        else:
                            correctData.append("0")

                    newLine += correctData
                    newLine += qTags

                    ws.append(newLine)
                            

    wb.save(response)
    return response
                

def tryAppend(l, data):
    try:
        l.append(data)
    except:
        l.append("")


#quiz management page
@login_required
def manageQuizzes(request):

    anyDue = False
    for i in Quiz.objects.all():
        if i.isDue:
            anyDue = True

    context = {"quizObjects": Quiz.objects.all, "anyDue": anyDue}

    return render(request, 'quizzes/manage.html', context)



#quiz management page
@login_required
def manageBank(request):


    context = {"questionObjects": Question.objects.all,}

    return render(request, 'quizzes/manageBank.html', context)
    



#quiz view page
@login_required
def repeatQuiz(request, quizID):

    newQuiz = Quiz.objects.get(quizID=quizID)
    
    newQuiz.pk = None
    if newQuiz.repeatNumber > 3:
        anyDue = False
        for i in Quiz.objects.all():
            if i.isDue:
                anyDue = True
        context = {"quizObjects": Quiz.objects.all, "anyDue": anyDue, "error": "You cannot repeat a quiz more than 3 times."}
        return render(request, 'quizzes/manage.html', context)
    elif newQuiz.repeatNumber > 0:
        newQuiz.repeatNumber += 1
        newQuiz.quizName = newQuiz.quizName[:-1] + str(newQuiz.repeatNumber)
    else:
        newQuiz.repeatNumber = 1
        newQuiz.quizName += " repeat 1"

    if request.method == 'POST':
        
        dueDate = request.POST['dueDate']
        dueTime = request.POST['dueTime']

        dueDate += dueTime
        dueDateTime = datetime.strptime(dueDate, "%b %d, %Y%I:%M %p")
        
        newQuiz.quizDueDate = sgt.localize(dueDateTime)
        newQuiz.quizID += "r"
        newQuiz.save()
        

        anyDue = False
        for i in Quiz.objects.all():
            if i.isDue:
                anyDue = True
        context = {"quizObjects": Quiz.objects.all, "anyDue": anyDue, "notification": "Successfully repeated quiz"}
        return render(request, 'quizzes/manage.html', context)

    else:
        context = {"newQuizName": newQuiz.quizName}
        return render(request, 'quizzes/repeat.html', context)





#quiz creation page
@login_required
def createQuiz(request):
    nowTime = datetime.now()
    timestamp = nowTime.strftime("%Y-%m-%d-%H-%M")


    modules = Module.objects.all()
    for module in modules:
        module.tags = list(set(list(module.course.quizTags.split(","))))



    courseObjects = list(Course.objects.all())
    courseIDs = [i.id for i in courseObjects]

    context = {"qbank": Question.objects.all, "quizIDtoUse": "quiz%s" % (timestamp), "courseObjects": courseObjects, "courseIDs": courseIDs ,"moduleObjects": modules, }
    
    #if submitting form
    if request.method == 'POST':
        if Quiz.objects.filter(quizID=request.POST['quizID']):
            context = {"quizObjects": Quiz.objects.all, "error": "This quiz ID is already being used, please avoid refreshing the page."}
            return render(request, 'quizzes/manage.html', context)


        questionsJSON = request.POST['allQuestionsJSON']
        questionsJSON = re.sub("_____var__", "", questionsJSON) #remove js stuff
        

        questionsJSON = json.loads(questionsJSON)

        questionsJSON[0]["quizName"] = request.POST['quizName']
        
        questionsJSON = json.dumps(questionsJSON)
        
        if not "assignedModule" in request.POST or not (request.POST['dueDate']!='' and request.POST['dueTime']!='' and request.POST["assignedModule"] and request.POST["assignedModule"]!='' and request.POST['quizName']!=''):
            context = {"quizObjects": Quiz.objects.all, "error": "Please fill in all fields."}
            return render(request, 'quizzes/manage.html', context)

        dueDate = request.POST['dueDate']
        dueTime = request.POST['dueTime']

        dueDate += dueTime
        dueDateTime = datetime.strptime(dueDate, "%b %d, %Y%I:%M %p")

        #find matching course
        assignedModuleID = request.POST["assignedModule"]
        assignedModule = Module.objects.get(pk=assignedModuleID)




        newQuiz = Quiz()
        newQuiz.quizName = request.POST['quizName']
        newQuiz.quizID = request.POST['quizID']
        if 'passingScore' in request.POST and request.POST['passingScore'] != '':
            newQuiz.passingScore = int(request.POST['passingScore'])
        else:
            newQuiz.passingScore = 0

        if 'ranQn' in request.POST:
            newQuiz.randomQuestions = 1
        else:
            newQuiz.randomQuestions = 0

        if 'ranOp' in request.POST:
            newQuiz.randomOptions = 1
        else:
            newQuiz.randomOptions = 0

        newQuiz.quizDueDate = sgt.localize(dueDateTime)
        newQuiz.module = assignedModule
        newQuiz.quizData = questionsJSON
        newQuiz.repeatNumber = 0
        newQuiz.save()
        
        context = {"quizObjects": Quiz.objects.all, "notification": "Successfully created quiz"}
        return render(request, 'quizzes/manage.html', context)


    else:
        return render(request, 'quizzes/create.html', context)



#quiz view page
@login_required
def viewQuiz(request, quizID):
    quizObj = Quiz.objects.get(quizID=quizID)

    context = {"quizObject": quizObj, "rop": quizObj.randomOptions == 1, "rqn": quizObj.randomQuestions == 1}

    return render(request, 'quizzes/view.html', context)



#quiz view page
@login_required
def doQuiz(request, quizID):
    #if submitting form
    if request.method == 'POST':
        responsesJSON = request.POST['submissionData']
        responsesJSON = re.sub("_____var__", "", responsesJSON) #remove js stuff

        score = len(re.findall(r'"isCorrect":true', responsesJSON))

        responsesJSON = json.loads(responsesJSON)
        
        quizObj = Quiz.objects.get(quizName=responsesJSON[0]["quizName"])
        passingScore = quizObj.passingScore
        if score >= int(passingScore):
            responsesJSON[0]["isPassed"] = True
        else:
            responsesJSON[0]["isPassed"] = False
        
        responsesJSON = json.dumps(responsesJSON)

        userId = request.user.id
        user = User.objects.get(id = userId)
        currentQuizResponses = user.quizResponses

        if currentQuizResponses and "__________RESPONSESPLITTER__________" in currentQuizResponses:
            allQuizResponses = currentQuizResponses.split("__________RESPONSESPLITTER__________")[1:]
            for i in allQuizResponses:
                quizName = ""
                try:
                    quizName = json.loads(i)[0]["quizName"]
                    if quizName == quizObj.quizName:
                        return redirect("./")
                except:
                    pass

        if currentQuizResponses != None:
            currentQuizResponses = str(user.quizResponses)
        else:
            currentQuizResponses = ""
        user.quizResponses = currentQuizResponses + "__________RESPONSESPLITTER__________" + responsesJSON


        user.save()
        

        return redirect("./")






    quizObj = Quiz.objects.get(quizID=quizID)

    #if quizObj.quizDueDate > sgt.localize(datetime.now()):
    context = {"quizObject": Quiz.objects.get(quizID=quizID), "rop": quizObj.randomOptions == 1, "rqn": quizObj.randomQuestions == 1}

    user = request.user
    quizResponseJSON = user.quizResponses
    if quizResponseJSON and "__________RESPONSESPLITTER__________" in quizResponseJSON:
        allQuizResponses = quizResponseJSON.split("__________RESPONSESPLITTER__________")[1:]
        for i in allQuizResponses:
            if quizObj.quizName == json.loads(i)[0]["quizName"]:
                #quiz done already

                
                def searchForQn(questions, questionID):
                    for i in questions:
                        if i["questionID"] == questionID:
                            return i


                quizObjToCombine = json.loads(Quiz.objects.get(quizID=quizID).quizData)

                quizResponsesToCombine = json.loads(i)[1:]

                for j in quizObjToCombine:
                    j.update(searchForQn(quizResponsesToCombine, j["questionID"]))


                context = {"quizObject": Quiz.objects.get(quizID=quizID), "responsesObject": json.dumps(quizObjToCombine), }
                return render(request, 'quizzes/viewAns.html', context)
    return render(request, 'quizzes/do.html', context)
"""
    else:

        classes = list(request.user.classes.all())
        context = {"classes": classes, "error": "Quiz is over.", }
        return render(request, 'accountManagement/classListView.html', context)
        """









@login_required
def viewQuizAns(request, quizNameEncoded, userId):   
    quizName = base64.b64decode(quizNameEncoded).decode('utf-8')

    quizObj = Quiz.objects.get(quizName=quizName)

    user = User.objects.get(id = userId)
    quizResponseJSON = user.quizResponses
    if quizResponseJSON and "__________RESPONSESPLITTER__________" in quizResponseJSON:
        allQuizResponses = quizResponseJSON.split("__________RESPONSESPLITTER__________")[1:]
        for i in allQuizResponses:
            if quizObj.quizName == json.loads(i)[0]["quizName"]:
                #quiz done already

                
                def searchForQn(questions, questionID):
                    for i in questions:
                        if i["questionID"] == questionID:
                            return i


                quizObjToCombine = json.loads(quizObj.quizData)

                quizResponsesToCombine = json.loads(i)[1:]

                for j in quizObjToCombine:
                    j.update(searchForQn(quizResponsesToCombine, j["questionID"]))


                context = {"quizObject": quizObj, "responsesObject": json.dumps(quizObjToCombine), }
                return render(request, 'quizzes/viewAns.html', context)
    else:
        return doQuiz(request, quizObj.quizID)













#quiz edit page
@login_required
def editQuiz(request, quizID):
    
    #if submitting form
    if request.method == 'POST':
        questionsJSON = request.POST['allQuestionsJSON']
        questionsJSON = re.sub("_____var__", "", questionsJSON) #remove js stuff
        
        dueDate = request.POST['dueDate']
        dueTime = request.POST['dueTime']

        dueDate += dueTime
        dueDateTime = datetime.strptime(dueDate, "%b %d, %Y%I:%M %p")


        #find matching course

        newQuiz = Quiz.objects.get(quizID=request.POST['quizID'])
        if 'passingScore' in request.POST and request.POST['passingScore'] != '':
            newQuiz.passingScore = int(request.POST['passingScore'])
        else:
            newQuiz.passingScore = 0
        newQuiz.quizName = request.POST['quizName']

        if 'ranQn' in request.POST:
            newQuiz.randomQuestions = 1
        else:
            newQuiz.randomQuestions = 0

        if 'ranOp' in request.POST:
            newQuiz.randomOptions = 1
        else:
            newQuiz.randomOptions = 0

        newQuiz.quizDueDate = sgt.localize(dueDateTime)
        newQuiz.quizData = questionsJSON
        newQuiz.save()
        
        context = {"quizObjects": Quiz.objects.all, "notification": "Successfully edited quiz", }
        return render(request, 'quizzes/manage.html', context)


    else:
        quizObj = Quiz.objects.get(quizID=quizID)

        dueDate = sgt.normalize(quizObj.quizDueDate).strftime("%b %d, %Y")
        dueTime = sgt.normalize(quizObj.quizDueDate).strftime("%I:%M %p")

        passingScore = quizObj.passingScore

        module = quizObj.module
        availableTags = ", ".join( ['"{}"'.format(x) for x in list(set(list(module.course.quizTags.split(","))))] )

        
        courseObjects = list(Course.objects.all())
        courseIDs = [i.id for i in courseObjects]

        context = {"qbank": Question.objects.all, "courseObjects": courseObjects, "courseIDs": courseIDs ,"modObjects": Module.objects.all, "quizObject": quizObj, "dueDate": dueDate, "dueTime": dueTime, "passingScore": passingScore, "availableTags": availableTags, "module": module}
        return render(request, 'quizzes/edit.html', context)
    

def deleteQuiz(request):
    if request.method == 'POST':
        
        quizID = request.POST['quizID']
        quiz = Quiz.objects.get(quizID = quizID)

        quiz.delete()


        context = {"quizObjects": Quiz.objects.all, "notification": "Deleted quiz", }

        return render(request, 'quizzes/manage.html', context)

    else:
        context = {"quizObjects": Quiz.objects.all, "error": "unable to delete quiz", }

        return render(request, 'quizzes/manage.html', context)