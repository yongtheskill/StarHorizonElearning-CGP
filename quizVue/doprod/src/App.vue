<template>
  <v-app>
    <v-main>
      <check-completed />
    </v-main>
  </v-app>
</template>

<script>
import CheckCompleted from "./components/CheckCompleted.vue";

export default {
  name: "App",

  components: {
    CheckCompleted,
  },

  data: () => ({
    //
  }),
};
</script>

<style>
* {
  font-family: "Montserrat", "Roboto" !important;
}
</style>