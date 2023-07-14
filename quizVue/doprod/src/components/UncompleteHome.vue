<template>
  <div id="hcom" class="hide">
    <div class="container">
      <v-row>
        <v-col sm="12" style="display: flex; justify-content: left">
          <v-btn plain @click="backButton">
            <v-icon left> mdi-chevron-left </v-icon>
            Back
          </v-btn>
        </v-col>
      </v-row>

      <v-row>
        <v-col sm="12">
          <v-card>
            <div class="text-h4" style="font-weight: 700">
              {{ quizName }}
            </div>
          </v-card>
        </v-col>
      </v-row>

      <div v-for="(question, i) in questions" :key="question.id">
        <v-row>
          <v-col>
            <QuestionView
              :question="question"
              :getIsRandomOptions="getIsRandomOptions"
              :highlightUndone="highlightUndone"
              :questionNumber="i + 1"
            />
          </v-col>
        </v-row>
      </div>

      <v-row>
        <v-col xs="12" class="justify-end d-flex" style="padding-bottom: 0">
          <v-btn color="primary" @click="submitQuiz"
            >Submit <v-icon right dark> mdi-send </v-icon></v-btn
          >
        </v-col>
      </v-row>
      <v-row style="margin-bottom: 3rem">
        <v-col
          xs="12"
          :class="{
            'd-flex': true,
            'justify-end': true,
            transparent: !highlightUndone,
          }"
          style="padding-top: 8px; font-weight: 700"
        >
          Please attempt all questions
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
import _ from "lodash";
import axios from "axios";
import QuestionView from "./QuestionView.vue";
import responseStore from "../responseStore.js";

export default {
  components: {
    QuestionView,
  },
  data() {
    return {
      quizName: "",
      randomOptions: true,
      randomQuestions: true,
      questions: [],
      questionOrder: "",
      highlightUndone: false,
    };
  },
  methods: {
    backButton() {
      history.back();
    },
    getIsRandomOptions() {
      return this.randomOptions;
    },
    submitQuiz() {
      console.log(responseStore.getLength());
      if (responseStore.getLength() !== this.questions.length) {
        this.highlightUndone = true;
        return;
      }
      this.highlightUndone = false;
      axios
        .post("../submit/", responseStore.responses, {
          withCredentials: true,
          headers: {
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
              .value,
          },
        })
        .then(() => {
          window.location.replace(window.location.href);
        });
    },
  },
  mounted() {
    responseStore.clearResponses();
    axios.get("../doGet/").then((r) => {
      _.extend(this, r.data);
      this.randomOptions = this.randomOptions === 1;
      this.randomQuestions = this.randomQuestions === 1;

      const qorder = JSON.parse(this.questionOrder);
      const questions = [];

      const unorderedQuestions = this.questions.filter(
        (q) => !qorder.includes(q.id)
      );

      for (const i of qorder) {
        const nextQn = this.questions.find((q) => q.id === i);
        if (nextQn !== undefined) {
          questions.push(nextQn);
        }
      }

      this.questions = questions.concat(unorderedQuestions);

      if (this.randomQuestions) {
        this.questions = _.shuffle(this.questions);
      }

      document.getElementById("hcom").classList.remove("hide");
    });
  },
};
</script>

<style>
.transparent {
  opacity: 0;
}
.v-input--switch {
  margin: 0;
}
.v-card {
  padding: 1.5rem 2rem;
}
.addButton {
  margin-top: 1rem;
  margin-bottom: 2rem;
  float: right;
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