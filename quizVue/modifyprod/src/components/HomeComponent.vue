<template>
  <div id="hcom" class="hide">
    <div class="container">
      <v-row>
        <v-col sm="12" style="display: flex; justify-content: space-between">
          <v-btn plain @click="backButton">
            <v-icon left> mdi-chevron-left </v-icon>
            Back
          </v-btn>
          <div v-if="updatingIDs.length > 0" style="display: flex; align-items: center">
            <div style="padding-right: 0.5rem; padding-bottom: 0.1rem">
              <v-progress-circular indeterminate :size="20" :width="2"></v-progress-circular>
            </div>
            Saving Changes
          </div>
          <div v-else style="padding-top: 0.4rem">All changes saved</div>
        </v-col>
      </v-row>

      <v-row>
        <v-col sm="12">
          <v-card>
            <v-list-item>
              <v-list-item-content>
                <div class="text-h4">Quiz Setttings</div>
              </v-list-item-content>
            </v-list-item>
            <v-card-text>
              <v-row>
                <v-col sm="12">
                  <v-text-field label="Quiz Name" v-model="quizName" />
                </v-col>
              </v-row>
              <v-row>
                <v-col sm="12" md="4">
                  <v-dialog
                    ref="dialog"
                    v-model="modal"
                    :return-value.sync="pickerDate"
                    persistent
                    width="290px">
                    <template v-slot:activator="{ on, attrs }">
                      <v-text-field
                        v-model="pickerDate"
                        label="Due Date"
                        readonly
                        v-bind="attrs"
                        v-on="on"></v-text-field>
                    </template>
                    <v-date-picker v-model="pickerDate" scrollable>
                      <v-spacer></v-spacer>
                      <v-btn text color="primary" @click="modal = false">Cancel</v-btn>
                      <v-btn text color="primary" @click="$refs.dialog.save(pickerDate)">OK</v-btn>
                    </v-date-picker>
                  </v-dialog>
                </v-col>
                <v-col sm="12" md="4">
                  <v-dialog
                    ref="dialog2"
                    v-model="modal2"
                    :return-value.sync="pickerTime"
                    persistent
                    width="290px">
                    <template v-slot:activator="{ on, attrs }">
                      <v-text-field
                        v-model="pickerTime"
                        label="Due Time"
                        readonly
                        v-bind="attrs"
                        v-on="on"></v-text-field>
                    </template>
                    <v-time-picker v-if="modal2" v-model="pickerTime" full-width>
                      <v-spacer></v-spacer>
                      <v-btn text color="primary" @click="modal2 = false">Cancel</v-btn>
                      <v-btn text color="primary" @click="$refs.dialog2.save(pickerTime)">OK</v-btn>
                    </v-time-picker>
                  </v-dialog>
                </v-col>
                <v-col sm="12" md="4">
                  <v-text-field
                    label="Passing Score"
                    step="1"
                    min="0"
                    v-model="passingScore"
                    type="number" />
                </v-col>
              </v-row>
              <v-row>
                <v-col sm="12" md="6">
                  <v-select
                    :items="courses"
                    v-model="courseId"
                    item-text="name"
                    item-value="id"
                    label="Course" />
                </v-col>
                <v-col sm="12" md="6">
                  <v-select
                    :items="moduleOptions"
                    v-model="moduleId"
                    item-text="name"
                    item-value="id"
                    label="Module" />
                </v-col>
              </v-row>
              <v-row>
                <v-col sm="12" md="6">
                  <v-switch v-model="randomQuestions" inset>
                    <template v-slot:label>
                      <div class="black--text">Randomise questions</div>
                    </template>
                  </v-switch>
                </v-col>
                <v-col sm="12" md="6">
                  <v-switch v-model="randomOptions" inset>
                    <template v-slot:label>
                      <div class="black--text">Randomise options</div>
                    </template>
                  </v-switch>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <draggable
        handle=".draggingHandle"
        v-model="questions"
        v-bind="dragOptions"
        @start="drag = true"
        @end="drag = false">
        <transition-group type="transition" :name="!drag ? 'flip-list' : null">
          <div v-for="question in questions" :key="question.id">
            <v-row>
              <v-col>
                <QuestionView
                  :question="question"
                  :getQuestions="getQuestions"
                  :addUpdatingID="addUpdatingID"
                  :removeUpdatingID="removeUpdatingID"
                  :tags="tags" />
              </v-col>
            </v-row>
          </div>
        </transition-group>
      </draggable>
      <div style="display: flex; justify-content: flex-end">
        <v-dialog v-model="dialog" scrollable max-width="300px">
          <template v-slot:activator="{ on, attrs }">
            <v-btn color="warning" class="addButton addButtonBank" v-bind="attrs" v-on="on">
              Bank Question
              <v-icon right dark>mdi-plus</v-icon>
            </v-btn>
          </template>
          <v-card>
            <v-card-title>Add Bank Question</v-card-title>
            <v-divider></v-divider>
            <v-card-text style="height: 300px">
              <v-radio-group v-model="questionToAdd" column>
                <v-radio
                  :label="question.questionName"
                  :value="question.id"
                  v-for="question in bankQuestions"
                  :key="question.id"></v-radio>
              </v-radio-group>
            </v-card-text>
            <v-divider></v-divider>
            <v-card-actions>
              <div style="display: flex; justify-content: flex-end; width: 100%">
                <v-btn color="#aaa" text @click="dialog = false"> Close </v-btn>
                <v-btn color="error" text @click="addBank" style="font-weight: 700"> Add </v-btn>
              </div>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <v-btn color="info" class="addButton" @click="addQuestion">
          New Question
          <v-icon right dark>mdi-plus</v-icon>
        </v-btn>
      </div>
    </div>
  </div>
</template>

<script>
import _ from 'lodash';
import axios from 'axios';
import { DateTime } from 'luxon';
import QuestionView from './QuestionView.vue';
import draggable from 'vuedraggable';

const formatTime = (time) => {
  return (
    String(time.getHours()).padStart(2, '0') + ':' + String(time.getMinutes()).padStart(2, '0')
  );
};

const formatDate = (date) => {
  return (
    String(date.getFullYear()).padStart(4, '0') +
    '-' +
    String(date.getMonth() + 1).padStart(2, '0') +
    '-' +
    String(date.getDate()).padStart(2, '0')
  );
};

export default {
  components: {
    QuestionView,
    draggable,
  },
  data() {
    return {
      modal: false,
      modal2: false,
      pickerDate: formatDate(new Date()),
      pickerTime: formatTime(new Date()),

      updatingIDs: [],
      quizName: '',
      module: null,
      passingScore: 0,
      quizDueDate: null,
      randomOptions: false,
      randomQuestions: false,
      moduleOptions: [],
      courses: [],
      courseId: -1,
      moduleId: -1,
      questions: [],
      tags: [],

      orderData: '[]',

      drag: false,
      dialog: false,

      questionToAdd: -1,
      bankQuestions: [],
    };
  },
  computed: {
    dragOptions() {
      return {
        animation: 200,
        group: 'Questions',
        disabled: false,
        ghostClass: 'ghost',
        forceFallback: true,
        scrollSensitivity: 200,
      };
    },
  },
  methods: {
    addBank() {
      this.dialog = false;
      axios
        .post(
          '../addBank/' + this.questionToAdd + '/',
          {},
          {
            withCredentials: true,
            headers: {
              'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
          }
        )
        .then((r) => {
          if (r.data.success) {
            this.getQuestions();
          }
        });
    },
    backButton() {
      window.location.href = '/quizzes/manage/';
    },
    settingUpdated() {
      this.updatingIDs.push(-1);
      this.doSettingsUpdate(this);
    },
    addUpdatingID(id) {
      this.updatingIDs.push(id);
    },
    removeUpdatingID(id) {
      this.updatingIDs = this.updatingIDs.filter((i) => i != id);
    },
    doSettingsUpdate: _.debounce((th) => {
      axios
        .post(
          'settings/',
          {
            quizName: th.quizName,
            dueDate: th.quizDueDate,
            moduleId: th.moduleId,
            passingScore: th.passingScore,
            randomOptions: th.randomOptions ? 1 : 0,
            randomQuestions: th.randomQuestions ? 1 : 0,
            questionOrder: th.orderData,
          },
          {
            withCredentials: true,
            headers: {
              'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
          }
        )
        .then((r) => {
          if (r.data.success) {
            th.removeUpdatingID(-1);
          }
        });
    }, 1000),
    loadModules(n) {
      this.moduleOptions = [];
      axios.get('/quizzes/getModules', { params: { courseId: n } }).then((r) => {
        this.moduleOptions = r.data.modules;
      });
    },
    addQuestion() {
      axios
        .post(
          '../addQuestion/',
          {},
          {
            withCredentials: true,
            headers: {
              'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
          }
        )
        .then((r) => {
          if (r.data.success) {
            this.getQuestions();
          }
        });
    },
    getQuestions() {
      axios.get('../getQuestions').then((r) => {
        this.questions = r.data.questions;

        const qorder = JSON.parse(this.questionOrder);
        const questions = [];

        const unorderedQuestions = this.questions.filter((q) => !qorder.includes(q.id));

        for (const i of qorder) {
          const nextQn = this.questions.find((q) => q.id === i);
          if (nextQn !== undefined) {
            questions.push(nextQn);
          }
        }

        this.questions = questions.concat(unorderedQuestions);
      });
    },
  },
  watch: {
    quizName() {
      this.settingUpdated();
    },
    passingScore() {
      this.settingUpdated();
    },
    randomOptions() {
      this.settingUpdated();
    },
    randomQuestions() {
      this.settingUpdated();
    },
    updatingIDs(n) {
      if (n.length > 0) {
        window.onbeforeunload = function () {
          return true;
        };
      } else {
        window.onbeforeunload = null;
      }
    },
    pickerDate(n) {
      this.quizDueDate = DateTime.fromFormat(n + ' ' + this.pickerTime, 'yyyy-MM-dd HH:mm');
      this.settingUpdated();
    },
    pickerTime(n) {
      this.quizDueDate = DateTime.fromFormat(this.pickerDate + ' ' + n, 'yyyy-MM-dd HH:mm');
      this.settingUpdated();
    },
    courseId(n) {
      this.courseId = n;
      axios
        .get('/quizzes/getTags/', {
          params: { courseId: n },
        })
        .then((r) => {
          this.tags = r.data.tags;
        });
      this.loadModules(this.courseId);
    },
    moduleId() {
      this.settingUpdated();
    },
    questions(n) {
      const questionOrder = [];
      for (const question of n) {
        questionOrder.push(question.id);
      }
      this.orderData = JSON.stringify(questionOrder);
      this.settingUpdated();
    },
  },
  mounted() {
    axios.get('../get').then((r) => {
      _.extend(this, r.data);
      this.randomOptions = this.randomOptions === 1;
      this.randomQuestions = this.randomQuestions === 1;
      this.loadModules(r.data.courseId);

      const qorder = JSON.parse(this.questionOrder);
      const questions = [];

      const unorderedQuestions = this.questions.filter((q) => !qorder.includes(q.id));

      for (const i of qorder) {
        const nextQn = this.questions.find((q) => q.id === i);
        if (nextQn !== undefined) {
          questions.push(nextQn);
        }
      }

      this.questions = questions.concat(unorderedQuestions);

      document.getElementById('hcom').classList.remove('hide');

      if (r.data.quizDueDate !== null) {
        this.pickerDate = formatDate(new Date(r.data.quizDueDate));
        this.pickerTime = formatTime(new Date(r.data.quizDueDate));
      }
    });
    axios.get('/quizzes/getCourses/').then((r) => {
      this.courses = r.data.courses;
    });

    axios.get('/quizzes/bank/getBank/').then((r) => {
      this.bankQuestions = r.data.questions;
    });
  },
  updated() {},
};
</script>

<style>
.v-input--switch {
  margin: 0;
}
.v-card {
  padding: 0.75rem 1.5rem;
}
.addButton {
  margin-top: 1rem;
  margin-bottom: 2rem;
  float: right;
}
.addButtonBank {
  margin-right: 1rem;
}
.flip-list-move {
  transition: transform 0.5s;
}
.no-move {
  transition: transform 0s;
}
.ghost {
  opacity: 0.5;
  background: #c8ebfb;
}
.list-group {
  min-height: 20px;
}
.list-group-item {
  cursor: move;
}
.list-group-item i {
  cursor: pointer;
}

.container {
  margin: 0 auto;
  max-width: 1280px;
  width: 90%;
}

@media only screen and (min-width: 601px) {
  .container {
    width: 85%;
  }
}

@media only screen and (min-width: 993px) {
  .container {
    width: 70%;
  }
}

html {
  background-color: #fbebeb;
}
#app {
  background: #ffffff00;
}

.v-dialog > .v-card {
  padding: 0;
}
</style>
