import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import 'vant/lib/index.css'
import { Button, Dialog, Field, Form, NavBar, Toast } from 'vant'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// 注册 Vant 组件
;[Button, Dialog, Field, Form, NavBar, Toast].forEach(component => {
  app.use(component)
})

app.mount('#app')