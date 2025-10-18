import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../pages/Home/index.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/club-admin',
    name: 'ClubAdmin',
    component: () => import('../pages/ClubAdmin/index.vue'),
    meta: { requiresAuth: true, requiresClub: true }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('../pages/Admin/index.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const userRole = localStorage.getItem('userRole')

  if (to.meta.requiresAuth && !token) {
    next('/')
    return
  }

  if (to.meta.requiresClub && userRole !== 'club') {
    next('/')
    return
  }

  if (to.meta.requiresAdmin && userRole !== 'admin') {
    next('/')
    return
  }

  // 防止无限重定向
  if (to.path === '/' || !to.meta.requiresAuth) {
    next()
    return
  }

  next()
})

export default router