import { defineStore } from 'pinia'
import { api } from '@/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userInfo: JSON.parse(localStorage.getItem('userInfo') || '{}'),
    // 从 localStorage 尝试恢复 bingoStatus，若无则使用默认值
    bingoStatus: JSON.parse(localStorage.getItem('bingoStatus') || 'null') || {
      point: 0,
      specialPoint: 0,
      bingoGrid: Array(5).fill(Array(5).fill(0)),
      bingo: 0
    }
  }),

  actions: {
    async login(data) {
      const res = await api.login(data)
      this.token = res.userToken
      this.userInfo = res.userInfo
      localStorage.setItem('token', res.userToken)
      localStorage.setItem('userInfo', JSON.stringify(res.userInfo))
      // 保存角色供路由守卫使用
      if (res.userInfo?.role) {
        localStorage.setItem('userRole', res.userInfo.role)
      }
    },

    async verifyInvite(code) {
      const res = await api.verifyInvite({ inviteCode: code })
      this.token = res.newToken
      this.userInfo.role = res.role
      localStorage.setItem('token', res.newToken)
      localStorage.setItem('userInfo', JSON.stringify(this.userInfo))
      if (res.role) {
        localStorage.setItem('userRole', res.role)
      }
    },

    async getBingoStatus() {
      const res = await api.getBingoStatus()
      this.bingoStatus = res
      // 持久化 bingoStatus，以便刷新后立即显示
      try {
        localStorage.setItem('bingoStatus', JSON.stringify(this.bingoStatus))
      } catch (e) {
        console.warn('保存 bingoStatus 失败', e)
      }
    },

    async lightGrid(data) {
      const res = await api.lightGrid(data)
      this.bingoStatus = res
      try {
        localStorage.setItem('bingoStatus', JSON.stringify(this.bingoStatus))
      } catch (e) {
        console.warn('保存 bingoStatus 失败', e)
      }
    },

    logout() {
      this.token = ''
      this.userInfo = {}
      this.bingoStatus = {
        point: 0,
        specialPoint: 0,
        bingoGrid: Array(5).fill(Array(5).fill(0)),
        bingo: 0
      }
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
      localStorage.removeItem('bingoStatus')
      localStorage.removeItem('userRole')
    }
  }
})