<template>
  <div v-if="loaded">
    <UncompleteHome v-if="!attempted" />
    <div v-else>
      <div id="hcom" class="hide" v-if="!decided">
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
                  Not yet competent, do you want to retry?
                </div>
                <div style="display: flex; padding-top: 1rem; padding-left: 0.8rem">
                  <v-btn color="primary" @click="selectReattempt(true)">Retry</v-btn>
                  <v-btn color="primary" style="margin-left: 1rem" @click="selectReattempt(false)"
                    >Review attempt</v-btn
                  >
                </div>
              </v-card>
            </v-col>
          </v-row>
        </div>
      </div>
      <CompleteHome :attempt="attempt" v-else />
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import UncompleteHome from './UncompleteHome.vue';
import CompleteHome from './CompleteHome.vue';

export default {
  components: {
    UncompleteHome,
    CompleteHome,
  },
  methods: {
    selectReattempt(doReattempt) {
      if (doReattempt) {
        this.attempted = false;
        return;
      }
      this.decided = true;
    },
    backButton() {
      history.back();
    },
  },
  data() {
    return {
      attempted: false,
      attempt: {},
      loaded: false,
      decided: false,
    };
  },
  created() {
    axios.get('../getAttempt/').then((r) => {
      this.attempted = r.data.attempted;
      if (this.attempted) {
        this.attempt = r.data.attempt;
        this.decided = !r.data.allowRetries;
      }
      this.loaded = true;
    });
  },
};
</script>

<style></style>
