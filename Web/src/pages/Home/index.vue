<template>
  <div class="home">
    <!-- 顶部栏 -->
    <van-nav-bar class="header">
      <template #left>
        <user-info v-if="userStore.token" />
        <van-button v-else type="primary" size="small" @click="showLogin">登录</van-button>
      </template>
      <template #right>
        <van-button type="primary" size="small" icon="scan" @click="showScan">扫码</van-button>
      </template>
    </van-nav-bar>

    <!-- Bingo 游戏区域 -->
    <div class="game-area">
      <div class="side-buttons left">
        <van-button 
          type="primary" 
          :disabled="!userStore.bingoStatus.point"
          @click="useNormalPoint"
        >
          使用普通积分 ({{ userStore.bingoStatus.point }})
        </van-button>
      </div>

      <bingo-grid class="bingo-grid" />

      <div class="side-buttons right">
        <van-button 
          type="primary" 
          :disabled="!userStore.bingoStatus.specialPoint"
          @click="useSpecialPoint"
        >
          使用特殊积分 ({{ userStore.bingoStatus.specialPoint }})
        </van-button>
      </div>
    </div>

    <!-- 底部奖励按钮区域 -->
    <div class="rewards">
      <div class="reward-grid">
        <van-button 
          v-for="level in 6" 
          :key="level"
          :disabled="userStore.bingoStatus.bingo < level"
          @click="getReward(level)"
        >
          {{ level }}级奖励
        </van-button>
      </div>
      <div class="admin-entry" @click="goToAdmin">后台入口</div>
    </div>

    <!-- 登录弹窗 -->
    <login-modal v-model:show="showLoginModal" />

    <!-- 扫码弹窗 -->
    <scan-modal v-model:show="showScanModal" />

    <!-- 特殊积分使用弹窗 -->
    <special-point-modal v-model:show="showSpecialPointModal" @confirm="confirmSpecialPoint" />

    <!-- 奖励二维码弹窗 -->
    <reward-modal v-model:show="showRewardModal" :reward-token="currentRewardToken" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { api } from '@/api'
import { showToast } from 'vant'
import UserInfo from '@/components/UserInfo/index.vue'
import BingoGrid from '@/components/BingoGrid/index.vue'
import LoginModal from '@/components/LoginModal/index.vue'
import ScanModal from '@/components/ScanModal/index.vue'
import SpecialPointModal from '@/components/SpecialPointModal/index.vue'
import RewardModal from '@/components/RewardModal/index.vue'

const router = useRouter()
const userStore = useUserStore()

// 各种弹窗的显示状态
const showLoginModal = ref(false)
const showScanModal = ref(false)
const showSpecialPointModal = ref(false)
const showRewardModal = ref(false)
const currentRewardToken = ref('')

// 显示登录弹窗
const showLogin = () => {
  showLoginModal.value = true
}

// 显示扫码弹窗
const showScan = () => {
  if (!userStore.token) {
    showToast('请先登录')
    return
  }
  showScanModal.value = true
}

// 使用普通积分
const useNormalPoint = async () => {
  try {
    await userStore.lightGrid({ pointType: 'normal' })
    showToast('使用成功')
  } catch (error) {
    console.error(error)
  }
}

// 使用特殊积分
const useSpecialPoint = () => {
  showSpecialPointModal.value = true
}

// 确认使用特殊积分
const confirmSpecialPoint = async (location) => {
  try {
    await userStore.lightGrid({ 
      pointType: 'special',
      location 
    })
    showToast('使用成功')
    showSpecialPointModal.value = false
  } catch (error) {
    console.error(error)
  }
}

// 获取奖励
const getReward = async (level) => {
  try {
    const res = await api.getRewardQrcode({ rewardLevel: level })
    currentRewardToken.value = res.rewardToken
    showRewardModal.value = true
  } catch (error) {
    console.error(error)
  }
}

// 进入后台
const goToAdmin = () => {
  const role = userStore.userInfo.role
  if (role === 'admin') {
    router.push('/admin')
  } else if (role === 'club') {
    router.push('/club-admin')
  } else {
    showToast('权限不足')
  }
}
</script>

<style scoped>
.home {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  position: sticky;
  top: 0;
  z-index: 100;
}

.game-area {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
}

.side-buttons {
  width: 80px;
}

.bingo-grid {
  flex: 1;
  margin: 0 16px;
}

.rewards {
  padding: 16px;
}

.reward-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  margin-bottom: 16px;
}

.admin-entry {
  text-align: center;
  color: #999;
  font-size: 12px;
  padding: 8px;
}
</style>