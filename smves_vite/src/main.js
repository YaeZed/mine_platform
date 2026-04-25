import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import Particles from 'vue3-particles'
// element-plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
// pinia
import { createPinia } from 'pinia'
// 配置 Axios 的基础 URL
axios.defaults.baseURL = 'http://localhost:8000/api/'
// 注册持久化存储
import piniaPluginPersistedstate from 'pinia-plugin-persist'

import api from '@/api/api.js'

// 创建 Vue 应用
const app = createApp(App)
// 注册全局api
app.config.globalProperties.$api = api
// 创建 Pinia 实例
const pinia = createPinia()
// 使用持久化插件
pinia.use(piniaPluginPersistedstate)
app.use(pinia)
// 挂载插件
app.use(ElementPlus).use(router).use(Particles)

// 将 axios 挂载为全局变量
app.config.globalProperties.$axios = axios

// 挂载应用
app.mount('#app')

//注册@element-plus/icons-vue图标
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
