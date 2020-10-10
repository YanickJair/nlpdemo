import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify';

Vue.config.productionTip = true;

if (!Vue.config.productionTip)
  Vue.prototype.$hostname = 'http://localhost:5000';
else
  Vue.prototype.$hostname = 'https://nlpdemoapi.yandrade.dev';

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
