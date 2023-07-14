<template>
  <v-card
    :class="{ qCard: true, highlightCard: highlightUndone && !attempted }"
  >
    <v-row>
      <v-col sm="12" class="text-h5 questionText">
        {{ questionNumber }}. {{ question.text }}
      </v-col>
    </v-row>
    <v-row style="margin: 2rem; margin-bottom: 1.2rem" v-if="question.imageUrl">
      <img
        :src="question.imageUrl"
        style="object-fit: contain; max-width: 100%"
      />
    </v-row>

    <v-row>
      <div v-if="question.type === 'mc'">
        <v-col sm="12" class="inputCol mcCol">
          <v-radio-group v-model="mcAnswer" hide-details>
            <v-radio
              v-for="option in options"
              :key="option.id"
              :value="option.id"
            >
              <template v-slot:label>
                <div
                  class="black--text"
                  :id="'questionOption-' + option.id.toString()"
                >
                  {{ option.text }}
                </div>
              </template>
            </v-radio>
          </v-radio-group>
        </v-col>
      </div>
      <!-- -->
      <v-col sm="12" class="inputCol" v-if="question.type === 'cb'">
        <v-checkbox
          hide-details
          v-for="option in options"
          :key="option.id"
          :value="option.id"
          v-model="cbAnswer"
          class="cbRow"
        >
          <template v-slot:label>
            <div
              class="black--text"
              :id="'questionOption-' + option.id.toString()"
            >
              {{ option.text }}
            </div>
          </template>
        </v-checkbox>
      </v-col>
      <!-- -->
      <v-col sm="12" class="saCol" v-if="question.type === 'sa'">
        <v-text-field label="Answer" v-model="tAnswer" />
      </v-col>
      <v-col sm="12" v-if="question.type === 'la'">
        <v-textarea filled label="Answer" v-model="tAnswer" />
      </v-col>
    </v-row>
    <v-row
      class="text-caption questionText d-flex justify-end"
      v-if="highlightUndone && !attempted"
    >
      Please attempt this question
    </v-row>
  </v-card>
</template>

<script>
import responseStore from "../responseStore";
import _ from "lodash";

export default {
  props: {
    question: Object,
    getIsRandomOptions: Function,
    highlightUndone: Boolean,
    questionNumber: Number,
  },
  data: () => ({
    options: [],
    cbAnswer: [],
    mcAnswer: -1,
    tAnswer: "",
    attempted: false,
  }),
  watch: {
    mcAnswer() {
      this.attempted = true;
      responseStore.setResponse(this.question.id, this.mcAnswer);
    },
    cbAnswer() {
      this.attempted = true;
      responseStore.setResponse(this.question.id, this.cbAnswer);
    },
    tAnswer() {
      this.attempted = true;
      responseStore.setResponse(this.question.id, this.tAnswer);
    },
  },
  mounted() {
    const orderData = JSON.parse(this.question.optionOrder);
    const options = [];

    const unorderedOptions = this.question.options.filter(
      (q) => !orderData.includes(q.id)
    );

    for (const i of orderData) {
      const nextQn = this.question.options.find((q) => q.id === i);
      if (nextQn !== undefined) {
        options.push(nextQn);
      }
    }

    this.options = options.concat(unorderedOptions);

    if (this.getIsRandomOptions()) {
      this.options = _.shuffle(this.options);
    }
  },
};
</script>

<style scoped>
.qCard {
  border: 1px solid #fff;
}
.highlightCard {
  border: 1px solid #db3833 !important;
}
.saCol {
  padding-top: 4px;
}
.mcCol {
  padding-top: 0.4rem;
}
.questionText {
  padding-bottom: 0;
}
.v-input--selection-controls {
  margin: 0;
}
.cbRow {
  margin-bottom: 8px;
}
.draggingHandle {
  cursor: grab;
}
.draggingHandle:active {
  cursor: grabbing;
}
.draggingHandleVertical {
  padding-bottom: 0.4rem;
}
.v-card-actions {
  margin: 0.6rem 0.5rem 0 0.5rem;
}
.card-divider {
  margin-top: 2rem;
}
.addOptionButton {
  margin-left: 1rem;
}
.optionRowCol {
  margin-top: 0 !important;
  margin-bottom: 0 !important;
  padding-top: 0 !important;
  padding-bottom: 0 !important;
}
.optionRow {
  display: flex;
  align-items: center;
}
.hidden {
  opacity: 0 !important;
}
.validateSwitch {
  margin-left: 0.8rem;
  margin-bottom: 0.2rem;
}
.validateCol {
  margin: 0 0.7rem;
  padding-top: 0;
  padding-bottom: 0.4rem;
}
.v-input--radio-group {
  margin-top: 0.3rem;
}
.answerKeyHeader {
  margin-top: 0;
  margin-left: 1rem;
}
.draggingRow {
  display: flex;
  justify-content: center;
}
</style>