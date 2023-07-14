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
              {{ attempt.quizName }}
            </div>
            <div class="text-subtitle-1" style="margin-left: 0.8rem">
              Quiz review
            </div>
          </v-card>
        </v-col>
      </v-row>

      <div v-for="(question, i) in questionAttempts" :key="question.id">
        <v-row>
          <v-col>
            <QuestionReview
              :questionAttempt="question"
              :questionNumber="i + 1"
            />
          </v-col>
        </v-row>
      </div>

      <v-row>
        <v-col
          xs="12"
          class="justify-end d-flex"
          style="padding-bottom: 3rem; cursor: not-allowed"
        >
          <v-btn color="primary" disabled>already submitted</v-btn>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
import QuestionReview from "./QuestionReview.vue";

export default {
  components: {
    QuestionReview,
  },
  props: {
    attempt: Object,
  },
  data() {
    return {
      questionAttempts: Object,
    };
  },
  methods: {
    backButton() {
      history.back();
    },
  },
  mounted() {
    console.log(this.attempt);

    const orderData = JSON.parse(this.attempt.questionOrder);
    const questions = [];

    const unorderedQuestions = this.attempt.questionAttempts.filter(
      (q) => !orderData.includes(q.question.id)
    );

    for (const i of orderData) {
      const nextQn = this.attempt.questionAttempts.find(
        (q) => q.question.id === i
      );
      if (nextQn !== undefined) {
        questions.push(nextQn);
      }
    }

    this.questionAttempts = questions.concat(unorderedQuestions);
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