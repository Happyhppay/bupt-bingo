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

// 启动时尝试从本地恢复并刷新用户 bingo 状态
import { useUserStore } from './store/user'
const userStore = useUserStore(pinia)
if (localStorage.getItem('token')) {
  // 异步调用，不阻塞挂载
  userStore.getBingoStatus().catch(err => {
    console.warn('获取 bingo 状态失败', err)
  })
}

// 注册 Vant 组件
;[Button, Dialog, Field, Form, NavBar, Toast].forEach(component => {
  app.use(component)
})

app.mount('#app')