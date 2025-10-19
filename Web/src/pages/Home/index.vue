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
    // 前端内部使用 0-based 索引，发送给后端时转换为 1-based
    const serverLocation = [location[0] + 1, location[1] + 1]
    await userStore.lightGrid({
      pointType: 'special',
      location: serverLocation
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
/* Home/index.vue 中的 style 部分 */
.home {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.header {
  position: sticky;
  top: 0;
  z-index: 1000;
  backdrop-filter: blur(10px);
  background: rgba(102, 126, 234, 0.95) !important;
}

.game-area {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  gap: 16px;
}

.side-buttons {
  width: 100px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.side-buttons .van-button {
  writing-mode: vertical-rl;
  text-orientation: mixed;
  height: 120px;
  padding: 16px 8px;
  font-size: 14px;
}

.bingo-grid {
  flex: 1;
  max-width: 500px;
}

.rewards {
  padding: 20px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-radius: 20px 20px 0 0;
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.1);
}

.reward-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}

.reward-grid .van-button {
  height: 44px;
  font-size: 14px;
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  color: #2c3e50;
  border: none;
}

.reward-grid .van-button:not(.van-button--disabled):hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.admin-entry {
  text-align: center;
  color: #999;
  font-size: 12px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.admin-entry:hover {
  background: rgba(255, 255, 255, 0.8);
  color: #667eea;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .game-area {
    flex-direction: column;
    padding: 16px;
  }

  .side-buttons {
    width: 100%;
    flex-direction: row;
    justify-content: center;
  }

  .side-buttons .van-button {
    writing-mode: horizontal-tb;
    height: auto;
    padding: 12px 16px;
  }

  .reward-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .reward-grid {
    grid-template-columns: 1fr;
  }

  .game-area {
    padding: 12px;
  }
}
</style>