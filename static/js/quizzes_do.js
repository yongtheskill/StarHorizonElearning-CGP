class QuestionResponse {
    constructor(qType, qID){
        //short ans, long ans, multiple choice, checkbox
        //sa, la, mc, cb 
        this._____var__questionType = qType;

        this._____var__questionID = qID;
    }

    get questionType(){
        return this._____var__questionType;
    }
    set questionType(x){
        this._____var__questionType = x;
    }

    get checkboxValues(){
        return this._____var__checkboxValues;
    }
    set checkboxValues(x){
        this._____var__checkboxValues = x;
    }

    get stuedntCheckboxValues(){
        return this._____var__stuedntCheckboxValues;
    }
    set stuedntCheckboxValues(x){
        this._____var__stuedntCheckboxValues = x;
    }

    get isAutoGraded(){
        return this._____var__isAutoGraded;
    }
    set isAutoGraded(x){
        this._____var__isAutoGraded = x;
    }

    get studentResponse(){
        return this._____var__studentResponse;
    }
    set studentResponse(x){
        this._____var__studentResponse = x;
    }

    get checkboxValues(){
        return this._____var__checkboxValues;
    }
    set checkboxValues(x){
        this._____var__checkboxValues = x;
    }

    get questionID(){
        return this._____var__questionID;
    }
    set questionID(x){
        this._____var__questionID = x;
    }

    get correctAnswer(){
        return this._____var__correctAnswer;
    }
    set correctAnswer(x){
        this._____var__correctAnswer = x;
    }

    get isCorrect(){
        return this._____var__isCorrect;
    }
    set isCorrect(x){
        this._____var__isCorrect = x;
    }



}


var questionResponses = []

var rqn = false;
var rop = false;

function rq(){
    rqn = true;

}
function ro(){
    rop = true;
}

function saAnsChanged(qID) {
    let question = questionResponses.find((o, i) => {
        if (o.questionID === qID) {
            questionResponses[i].studentResponse = $(`#answerField${qID}`).val();
            if (questionResponses[i].isAutoGraded === true && questionResponses[i].studentResponse === questionResponses[i].correctAnswer){
                questionResponses[i].isCorrect = true;
            } else if (questionResponses[i].isAutoGraded === true){
                questionResponses[i].isCorrect = false;
            }
            return true; // stop searching
        }
    });
}

function cbAnsChanged(qID, checkboxIndex) {
    let question = questionResponses.find((o, i) => {
        if (o.questionID === qID) {
            var currentCheckboxValues = questionResponses[i].studentCheckboxValues;
            var optionChanged = questionResponses[i].questionOptions[checkboxIndex];
            currentCheckboxValues[optionChanged] = !currentCheckboxValues[optionChanged];
            questionResponses[i].studentCheckboxValues = currentCheckboxValues;
            var responses = [];
            for (j = 0; j < Object.keys(currentCheckboxValues).length; j++) {
                if (currentCheckboxValues[Object.keys(currentCheckboxValues)[j]] === true) {
                    responses.push(Object.keys(currentCheckboxValues)[j]);
                }
            }
            if (questionResponses[i].isAutoGraded === true && JSON.stringify(questionResponses[i].studentCheckboxValues) === JSON.stringify(questionResponses[i].checkboxValues)){
                questionResponses[i].isCorrect = true;
            } else if (questionResponses[i].isAutoGraded === true){
                questionResponses[i].isCorrect = false;
            }
            
            if(responses.length == 0){
                document.getElementById(`checkbox-question${qID}`).value = "";
            }
            else{
                document.getElementById(`checkbox-question${qID}`).value = "filled";
            }

            return true; // stop searching
        }
    });
}



function setQuizName(quizName){
    questionResponses.push({"quizName": quizName});
}


function renderQuizQuestions(quizJSON) {
    
    var questionsData = JSON.parse(quizJSON);
    
    var finalHTML = "";
    for (k=0; k < questionsData.length; k++) {
        finalHTML += generateQuesionHTML(questionsData[k], k);
        newQuestionResponse = new QuestionResponse(questionsData[k].questionType, questionsData[k].questionID);

        if (questionsData[k].questionType == "cb"){
            newQuestionResponse.checkboxValues = questionsData[k].checkboxValues;
            newQuestionResponse.studentCheckboxValues = questionsData[k].studentCheckboxValues;
            newQuestionResponse.questionOptions = questionsData[k].questionOptions;
        }

        newQuestionResponse.isAutoGraded = questionsData[k].isAutoGraded;
        newQuestionResponse.correctAnswer = questionsData[k].correctAnswer;

        questionResponses.push(newQuestionResponse);
    }



    function generateQuesionHTML (question, index) {
        //actual question
        var generatedHTML = `
        <div class="row questionWrapper z-depth-2 question-div-identifier-id-${question.questionID}">
            <div class="questionContainer">
                <div class="row  noPadding valign-wrapper">
                    <div class="input-field col s12 quesionInput">
                        <h6 style="margin: 0px;" id="questionNumberLabel${question.questionID}"><span class="qNumLabel">${index + 1}</span>. ${question.questionTitle}</h4>
                    </div>
                </div>`;

        if (question.questionType === "mc") {
            generatedHTML += `
            <div class="row answerInputContainer">
                <div class="input-field col s12 m6">
                    <select id="answerField${question.questionID}" class="fillValidation shuffle"  onchange="saAnsChanged(${question.questionID})">
                        <option value="" disabled selected>Select correct option</option><div style="display:inline-block">
                        `
            question.questionOptions.forEach(function (option, index) {
                generatedHTML += `
                        <option value="${option}">${option}</option>\n`
            });
            generatedHTML += `
                    </div>
                    </select>
                    <label>Correct Option</label>
                </div>
            </div>`;
            
        }

        if (question.questionType === "cb") {
            generatedHTML += `
            <div class="row answerInputContainer">
                <div style="margin-top: 10px; margin-bottom: 0px;" class="input-field col s12 m6">
                    <p style="margin-top: 0px;">Select Correct Options</p>
                    <input hidden class="fillValidation" id="checkbox-question${question.questionID}"><div style="display:inline-block" class="shuffle">`;
            question.questionOptions.forEach(function (option, index) {
                generatedHTML += `
                    <p>
                        <label>
                            <input type="checkbox" id="checkbox-question${question.questionID}-index${index}" oninput="cbAnsChanged(${question.questionID}, ${index})"/>
                            <span>${option}</span>
                        </label>
                    </p>`;
            });
            generatedHTML += `
                </div>
                </div>
            </div>`;
        }

        if (question.questionType === "sa") {
            generatedHTML += `
            <div class="row answerInputContainer">
                <div class="input-field col s12 m6">
                    <input id="answerField${question.questionID}" class="fillValidation" type="text" class="validate" onfocusout="saAnsChanged(${question.questionID})">
                    <label for="answerField${question.questionID}">Your answer</label>
                </div>
            </div>`;
        }

        if (question.questionType === "la") {
            generatedHTML += `
            <div class="row answerInputContainer">
                <div class="input-field col s12">
                    <textarea  id="answerField${question.questionID}" class="fillValidation materialize-textarea"  type="text" onfocusout="saAnsChanged(${question.questionID})"></textarea>
                    <label for="answerField${question.questionID}">Your answer</label>
                </div>
            </div>`;
        }


        generatedHTML += `
            </div>
        </div>`;

        return generatedHTML;
    }

    return finalHTML;
}





function convertToJSON(quizID) {
    questionResponses["QuizID"] = quizID;
    var jsonQuestions = JSON.stringify(questionResponses);
    $("#submissionDataJSON").val(jsonQuestions);
}

function submitForm(quizID) {
    convertToJSON(quizID);
    const inputs = document.getElementsByClassName("fillValidation");
    for(var i=0; i<inputs.length; i++) {
        if (!inputs[i].value.trim()){
            const successNotification = window.createNotification({
            theme: 'warning',
            showDuration: 10000,
            });
            // Invoke success notification
            successNotification({ 
                message: 'please complete the quiz before submitting' 
            });
            return;
        }
    }
    $("#quizDataForm").submit();
}