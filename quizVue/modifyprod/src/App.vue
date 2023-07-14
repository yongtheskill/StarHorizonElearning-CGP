<template>
  <v-app>
    <v-main>
      <HomeComponent />
    </v-main>
  </v-app>
</template>

<script>
import HomeComponent from "./components/HomeComponent";

export default {
  name: "App",

  components: {
    HomeComponent,
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