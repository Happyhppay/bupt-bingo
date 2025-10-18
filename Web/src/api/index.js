import axios from 'axios'
import { showToast } from 'vant'
import router from '../router'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 5000
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    const { code, message, data } = response.data

    if (code === 200) {
      return data
    }

    showToast(message || '请求失败')
    return Promise.reject(new Error(message || '请求失败'))
  },
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      router.push('/')
    }
    showToast(error.message || '网络错误')
    return Promise.reject(error)
  }
)

export const api = {
  // 用户相关
  login: (data) => request.post('/users/login', data),
  verifyInvite: (data) => request.post('/users/verify', data),

  // Bingo 相关
  getBingoStatus: () => request.get('/bingo/status'),
  lightGrid: (data) => request.post('/bingo/light', data),

  // 社团相关
  getClubQrcode: () => request.get('/clubs/qrcode'),
  scanClubQrcode: (data) => request.post('/clubs/scan', data),

  // 奖励相关
  getRewardQrcode: (data) => request.post('/reward/qrcode', data),
  verifyReward: (data) => request.post('/reward/verify', data)
}

export default request