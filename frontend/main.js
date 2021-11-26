// Ref: https://buzz-server.com/tech/vuejs-fastapi/
// Ref: https://nekopachi.net/index.php/2021/01/25/post-121/

import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import AxiosPlugin from '@/plugins/axios/index'

createApp(App).use(VueAxios, axios).use(AxiosPlugin).mount('#app')
