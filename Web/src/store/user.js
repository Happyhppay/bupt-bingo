import { defineStore } from 'pinia'
import { api } from '@/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userInfo: JSON.parse(localStorage.getItem('userInfo') || '{}'),
    bingoStatus: {
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
    },

    async verifyInvite(code) {
      const res = await api.verifyInvite({ inviteCode: code })
      this.token = res.newToken
      this.userInfo.role = res.role
      localStorage.setItem('token', res.newToken)
      localStorage.setItem('userInfo', JSON.stringify(this.userInfo))
    },

    async getBingoStatus() {
      const res = await api.getBingoStatus()
      this.bingoStatus = res
    },

    async lightGrid(data) {
      const res = await api.lightGrid(data)
      this.bingoStatus = res
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
    }
  }
})