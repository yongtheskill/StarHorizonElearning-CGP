<template>
  <v-card>
    <v-row class="draggingRow"> <v-icon class="draggingHandle">mdi-drag-horizontal</v-icon></v-row>
    <v-row>
      <v-col sm="12" md="8" style="display: flex; align-items: center">
        <v-text-field label="Question" v-model="text" />
        <v-file-input
          hide-input
          style="
            margin-bottom: 1rem;
            margin-left: 1.4rem;
            flex: none;
            padding-top: none;
            margin-top: none;
          "
          prepend-icon="mdi-image"
          accept="image/*"
          hide-details
          ref="file"
          @change="uploadFile"></v-file-input>
      </v-col>
      <v-col sm="12" md="4">
        <v-select
          :items="qtypes"
          label="Question Type"
          v-model="type"
          outlined
          item-text="label"
          item-value="code"
          :append-icon="
            type === 'cb'
              ? 'mdi-checkbox-marked'
              : type === 'mc'
              ? 'mdi-radiobox-marked'
              : type === 'sa'
              ? 'mdi-text-short'
              : 'mdi-text-long'
          "></v-select>
      </v-col>
    </v-row>
    <v-hover v-slot="{ hover }">
      <div>
        <v-skeleton-loader
          v-if="imageLoading"
          type="image"
          max-width="100%"
          style="margin: 0 2rem; margin-bottom: 2rem"></v-skeleton-loader>
        <v-row
          v-else-if="imageUrl != ''"
          style="margin: 0 2rem; margin-bottom: 2rem; position: relative">
          <img :src="imageUrl" style="object-fit: contain; max-width: 100%" />

          <v-fade-transition>
            <v-overlay
              v-if="hover"
              absolute
              color="#ff0000"
              opacity="0.5"
              style="cursor: pointer"
              @click="deleteImage">
              <v-icon>mdi-delete</v-icon>
            </v-overlay>
          </v-fade-transition>
        </v-row>
      </div></v-hover
    >

    <draggable
      handle=".draggingHandle"
      v-model="options"
      v-bind="dragOptions"
      @start="drag = true"
      @end="drag = false"
      v-if="type === 'mc' || type === 'cb'">
      <transition-group type="transition" :name="!drag ? 'flip-list' : null">
        <v-row
          v-for="(option, index) in options"
          :key="option.id"
          class="optionRowCol"
          @mouseover="hoveredId = option.id"
          @dragenter="hoveredId = -1"
          @dragleave="hoveredId = -1"
          @mouseleave="hoveredId = -1">
          <v-col sm="12" class="optionRowCol optionRow">
            <v-icon
              :class="{
                draggingHandle: true,
                draggingHandleVertical: true,
                hidden: hoveredId !== option.id && !$vuetify.breakpoint.mobile,
              }"
              >mdi-drag-vertical</v-icon
            >
            <v-text-field
              :label="'Option ' + (index + 1).toString()"
              :prepend-icon="type === 'cb' ? 'mdi-checkbox-blank-outline' : 'mdi-radiobox-blank'"
              :value="option.text"
              @input="
                (e) => {
                  optionChanged(option.id, e);
                }
              "
              append-outer-icon="mdi-close-circle-outline"
              @click:append-outer="deleteOption(option.id)" />
          </v-col>
        </v-row>
      </transition-group>
    </draggable>
    <v-row v-if="type === 'mc' || type === 'cb'">
      <v-col sm="12">
        <v-btn color="info" @click="addOption" small text>
          Add Option
          <v-icon right dark>mdi-plus</v-icon>
        </v-btn>
      </v-col>
    </v-row>
    <v-row v-if="validate">
      <div v-if="type === 'mc'">
        <div class="text-h6 answerKeyHeader">Answer Key</div>
        <v-col sm="12" class="validateCol">
          <v-radio-group v-model="mcAnswer" mandatory hide-details>
            <v-radio v-for="option in options" :key="option.id" :value="option.id">
              <template v-slot:label>
                <div class="black--text" :id="'questionOption-' + option.id.toString()">
                  {{ option.text }}
                </div>
              </template>
            </v-radio>
          </v-radio-group>
        </v-col>
      </div>
      <!-- -->
      <div v-if="type === 'cb'">
        <div class="text-h6 answerKeyHeader">Answer Key</div>
        <v-col sm="12" class="validateCol">
          <v-checkbox
            hide-details
            v-for="option in options"
            :key="option.id"
            :value="option.id"
            v-model="cbAnswer">
            <template v-slot:label>
              <div class="black--text" :id="'questionOption-' + option.id.toString()">
                {{ option.text }}
              </div>
            </template>
          </v-checkbox>
        </v-col>
      </div>
      <!-- -->
      <div class="text-h6" style="margin-left: 0.65rem" v-if="type === 'sa'" hide-details>
        Correct Answer
      </div>
      <v-col sm="12" class="" v-if="type === 'sa'">
        <v-text-field label="Answer" v-model="saAnswer" />
      </v-col>
    </v-row>

    <v-divider class="card-divider" />
    <v-card-actions class="v-card-actions">
      <v-row align="center" justify="space-between">
        <v-switch v-model="validate" inset hide-details class="validateSwitch" v-if="type !== 'la'">
          <template v-slot:label>
            <div class="black--text">Auto-grade</div>
          </template>
        </v-switch>
        <div v-else></div>
        <div style="display: flex; align-items: center">
          <div class="text-center">
            <v-menu offset-y>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  v-bind="attrs"
                  v-on="on"
                  class="ma-2"
                  text
                  rounded
                  style="
                    border: 1px solid #ccc;
                    padding-left: 12px !important;
                    padding-right: 8px !important;
                    text-transform: none;
                  ">
                  <v-icon :left="chosenTag !== undefined" color="error"> mdi-tag </v-icon>
                  {{ chosenTag && chosenTag.text }}
                  <v-btn
                    x-small
                    icon
                    v-if="chosenTag"
                    style="margin-left: 8px"
                    @click="changeTag(-1)"
                    ><v-icon>mdi-close-circle-outline</v-icon></v-btn
                  >
                </v-btn>
              </template>
              <v-list>
                <v-list-item v-for="item in tags" :key="item.id" @click="changeTag(item.id)">
                  <v-list-item-title>{{ item.text }}</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </div>

          <v-btn color="error" small icon fab @click="deleteQn">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </div>
      </v-row>
    </v-card-actions>
  </v-card>
</template>

<script>
import axios from 'axios';
import debounce from '../debounce.js';
import draggable from 'vuedraggable';

export default {
  components: {
    draggable,
  },
  props: {
    question: Object,
    getQuestions: Function,
    addUpdatingID: Function,
    removeUpdatingID: Function,
    tags: Array,
  },
  data: () => ({
    qtypes: [
      { label: 'Checkboxes', code: 'cb' },
      { label: 'Multiple Choice', code: 'mc' },
      { label: 'Short Answer', code: 'sa' },
      { label: 'Long Answer', code: 'la' },
    ],
    type: 'cb',
    text: '',
    options: [],
    orderData: '[]',
    hoveredId: -1,

    validate: false,
    drag: false,

    mcAnswer: -1,
    cbAnswer: [],
    saAnswer: '',

    tagId: -1,
    currentImage: null,
    imageLoading: false,
    imageUrl: '',
  }),
  methods: {
    deleteImage() {
      this.imageLoading = true;
      axios
        .post(
          '/quizzes/deleteImage/',
          {
            questionId: this.question.id,
          },
          {
            withCredentials: true,
            headers: {
              'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
          }
        )
        .then((r) => {
          this.imageLoading = false;
          if (r.data.success) {
            this.imageUrl = '';
          }
        });
    },
    uploadFile(f) {
      const formData = new FormData();
      formData.append('image', f);
      formData.append('questionId', this.question.id);
      this.imageLoading = true;
      axios
        .post('/quizzes/setImage/', formData, {
          withCredentials: true,
          headers: {
            'Content-Type': 'multipart/form-data',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
          },
        })
        .then((r) => {
          this.imageLoading = false;
          if (r.data.success) {
            this.imageUrl = r.data.imageUrl;
          }
        });
    },
    changeTag(id) {
      this.tagId = id;
      this.addUpdatingID(this.question.id);
      this.doQnUpdate(this.question.id, this);
    },
    optionChanged(id, e) {
      this.options.find((o) => o.id === id).text = e;
      try {
        document.getElementById('questionOption-' + id.toString()).innerText = e;
      } catch {
        //pass
      }

      this.addUpdatingID(id.toString() + 'q');
      this.doOptionUpdate(id.toString() + 'q', id, e, this);
    },
    deleteQn() {
      axios
        .post(
          '/quizzes/deleteQuestion/',
          {
            questionId: this.question.id,
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
            this.getQuestions();
          }
        });
    },
    deleteOption(id) {
      axios
        .post(
          '/quizzes/deleteOption/',
          { id },
          {
            withCredentials: true,
            headers: {
              'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
          }
        )
        .then((r) => {
          if (r.data.success) {
            this.getOptions();
          }
        });
    },
    qnUpdated() {
      this.addUpdatingID(this.question.id);
      this.doQnUpdate(this.question.id, this);
    },
    addOption() {
      axios
        .post(
          '/quizzes/addOption/',
          { questionId: this.question.id },
          {
            withCredentials: true,
            headers: {
              'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
          }
        )
        .then((r) => {
          if (r.data.success) {
            this.getOptions();
          }
        });
    },
    doOptionUpdate: debounce((id, text, th) => {
      axios
        .post(
          '/quizzes/editOption/',
          { id, text },
          {
            withCredentials: true,
            headers: {
              'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
          }
        )
        .then((r) => {
          if (r.data.success) {
            th.removeUpdatingID(id.toString() + 'q');
          }
        });
    }, 1000),
    getOptions() {
      axios
        .get('/quizzes/getOptions/', {
          params: { questionId: this.question.id },
        })
        .then((r) => {
          this.options = r.data.options;

          const orderData = JSON.parse(this.optionOrder);

          const options = [];

          const unorderedOptions = this.options.filter((q) => !orderData.includes(q.id));

          for (const i of orderData) {
            const nextQn = this.options.find((q) => q.id === i);
            if (nextQn !== undefined) {
              options.push(nextQn);
            }
          }

          this.options = options.concat(unorderedOptions);
        });
    },
    doQnUpdate: debounce((th) => {
      axios
        .post(
          '/quizzes/editQuestion/',
          {
            id: th.question.id,
            text: th.text,
            type: th.type,
            optionOrder: th.orderData,
            validate: th.validate,
            mcAnswer: th.mcAnswer,
            cbAnswer: JSON.stringify(th.cbAnswer),
            saAnswer: th.saAnswer,
            tagId: th.tagId,
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
            th.removeUpdatingID(th.question.id);
          }
        });
    }, 500),
  },
  watch: {
    text() {
      this.qnUpdated();
    },
    type() {
      this.qnUpdated();
    },
    validate() {
      this.qnUpdated();
    },
    mcAnswer() {
      this.qnUpdated();
    },
    cbAnswer() {
      this.qnUpdated();
    },
    saAnswer() {
      this.qnUpdated();
    },
    options(n) {
      const optionOrder = [];
      for (const option of n) {
        optionOrder.push(option.id);
      }
      this.orderData = JSON.stringify(optionOrder);
      this.qnUpdated();
    },
  },
  mounted() {
    this.type = this.question.type;
    this.text = this.question.text;
    this.options = this.question.options;
    this.optionOrder = this.question.optionOrder;
    this.validate = this.question.autoGrade;
    this.mcAnswer = this.question.mcAnswer;
    this.cbAnswer = JSON.parse(this.question.cbAnswer);
    this.saAnswer = this.question.saAnswer;
    this.imageUrl = this.question.imageUrl || '';
    if (this.question.questionTag !== null) {
      this.tagId = this.question.questionTag.id;
    }

    const orderData = JSON.parse(this.optionOrder);

    const options = [];

    const unorderedOptions = this.options.filter((q) => !orderData.includes(q.id));

    for (const i of orderData) {
      const nextQn = this.options.find((q) => q.id === i);
      if (nextQn !== undefined) {
        options.push(nextQn);
      }
    }

    this.options = options.concat(unorderedOptions);
  },
  computed: {
    chosenTag() {
      return this.tags.find((t) => t.id === this.tagId);
    },
    dragOptions() {
      return {
        animation: 200,
        group: 'Options' + this.question.id,
        disabled: false,
        ghostClass: 'ghost',
        forceFallback: true,
        scrollSensitivity: 100,
      };
    },
  },
};
</script>

<style scoped>
.v-list-item {
  cursor: pointer;
  transition: 300ms;
}
.v-list-item:hover {
  background-color: #eee;
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
