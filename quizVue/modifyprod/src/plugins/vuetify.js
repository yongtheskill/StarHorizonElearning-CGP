import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: '#db3833',
        accent: '#536DFE',
        info: '#db3833',
      },
    },
  },
});
