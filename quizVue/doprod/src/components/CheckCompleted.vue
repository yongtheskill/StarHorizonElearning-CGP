<template>
  <div v-if="loaded">
    <UncompleteHome v-if="!attempted" />
    <CompleteHome v-else :attempt="attempt" />
  </div>
</template>

<script>
import axios from "axios";
import UncompleteHome from "./UncompleteHome.vue";
import CompleteHome from "./CompleteHome.vue";

export default {
  components: {
    UncompleteHome,
    CompleteHome,
  },
  data() {
    return {
      attempted: false,
      attempt: {},
      loaded: false,
    };
  },
  created() {
    axios.get("../getAttempt/").then((r) => {
      this.attempted = r.data.attempted;
      if (this.attempted) {
        this.attempt = r.data.attempt;
      }
      this.loaded = true;
    });
  },
};
</script>

<style>
</style>