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
      <bingo-grid class="bingo-grid" />
    </div>

    <!-- 积分按钮区域 -->
    <div class="points-buttons">
      <van-button
        type="primary"
        :disabled="!userStore.bingoStatus.point"
        @click="useNormalPoint"
        class="point-button"
      >
        使用普通积分 ({{ userStore.bingoStatus.point }})
      </van-button>
      <van-button
        type="primary"
        :disabled="!userStore.bingoStatus.specialPoint"
        @click="useSpecialPoint"
        class="point-button"
      >
        使用特殊积分 ({{ userStore.bingoStatus.specialPoint }})
      </van-button>
    </div>

    <!-- 底部奖励按钮区域 -->
    <div class="rewards">
      <div class="reward-grid">
        <div
          v-for="level in 6"
          :key="level"
          class="reward-item"
          :class="{ unlocked: userStore.bingoStatus.rewards.includes(level) }"
          @click="getReward(level)"
        >
          <van-button
            :disabled="!userStore.bingoStatus.rewards.includes(level)"
            class="reward-button"
          >
            <!-- 按钮仅作为点击容器，内容由 reward-image 控制 -->
          </van-button>
          <div class="reward-image" :class="{ locked: !userStore.bingoStatus.rewards.includes(level) }">
            <img :src="getRewardImage(level)" :alt="`${level}号奖品`" />
            <!-- 未获得时显示锁和提示 -->
            <div v-if="!userStore.bingoStatus.rewards.includes(level)" class="lock-overlay">
              <van-icon name="lock" size="24" />
              <span class="level-text">{{ level }}号奖品</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 管理员入口 -->
      <div class="admin-entry-container">
        <div class="admin-entry" @click="goToAdmin">后台入口</div>
        <div class="admin-entry" @click="showInvite">邀请代码</div>
      </div>
    </div>

    <!-- 登录弹窗 -->
    <login-modal v-model:show="showLoginModal" />

    <!-- 扫码弹窗 -->
    <scan-modal v-model:show="showScanModal" />

    <!-- 特殊积分使用弹窗 -->
    <special-point-modal v-model:show="showSpecialPointModal" @confirm="confirmSpecialPoint" />

    <!-- 奖励二维码弹窗 -->
    <reward-modal v-model:show="showRewardModal" :reward-token="currentRewardToken" />

      <!-- 邀请代码弹窗 -->
      <van-dialog
        v-model:show="showInviteModal"
        title="请输入邀请代码"
        show-cancel-button
        @confirm="submitInvite"
      >
        <van-form @submit="submitInvite">
          <van-field v-model="inviteCode" label="邀请代码" placeholder="请输入邀请代码" />
        </van-form>
      </van-dialog>
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
// 获取奖励图片
const getRewardImage = (level) => {
  // 这里可以根据等级返回不同的图片URL
  // 你可以替换为实际的图片路径
  const imageMap = {
    1: '/image/rewards/level1.png',
    2: '/image/rewards/level2.png',
    3: '/image/rewards/level3.png',
    4: '/image/rewards/level4.png',
    5: '/image/rewards/level5.png',
    6: '/image/rewards/level6.png'
  }
  return imageMap[level] || '/image/rewards/default.png'
}

const router = useRouter()
const userStore = useUserStore()

// 各种弹窗的显示状态
const showLoginModal = ref(false)
const showScanModal = ref(false)
const showSpecialPointModal = ref(false)
const showRewardModal = ref(false)
const currentRewardToken = ref('')
const showInviteModal = ref(false)
const inviteCode = ref('')

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
    const serverLocation = [location[0], location[1]]
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
  // API expects { reward: level }
  const res = await api.getRewardQrcode({ reward: level })
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

// 显示邀请代码输入弹窗
const showInvite = () => {
  if (!userStore.token) {
    showToast('请先登录')
    return
  }
  inviteCode.value = ''
  showInviteModal.value = true
}

// 提交邀请代码
const submitInvite = async () => {
  if (!inviteCode.value || inviteCode.value.trim() === '') {
    showToast('请填写邀请代码')
    return
  }
  try {
    await userStore.verifyInvite(inviteCode.value.trim())
    // 获取成功，重新获取 bingo 状态
    await userStore.getBingoStatus().catch(() => {})
    showInviteModal.value = false
    showToast('验证成功')
    // 如果角色发生变化，为便于站上进入后台
    const role = userStore.userInfo.role
    if (role === 'admin') {
      router.push('/admin').catch(() => {})
    } else if (role === 'club') {
      router.push('/club-admin').catch(() => {})
    }
  } catch (error) {
    console.error(error)
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
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.bingo-grid {
  flex: 1;
  max-width: 500px;
}

/* 积分按钮区域 - 新增样式 */
.points-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
  padding: 16px 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.point-button {
  min-width: 160px;
  height: 44px;
  border-radius: 22px;
  font-size: 14px;
  font-weight: 500;
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

.reward-item {
  position: relative;
  aspect-ratio: 1;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
  min-height: 80px;
}

.reward-button {
  width: 100%;
  height: 100%;
  border: none;
  border-radius: 8px;
  background: transparent;
}

.reward-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  animation: fadeIn 0.5s ease;
}

.reward-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: 8px;
  padding: 4px;
  box-sizing: border-box;
}

.reward-image.locked {
  filter: grayscale(85%) brightness(0.6);
}

.reward-item.unlocked .reward-image {
  filter: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.lock-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  border-radius: 8px;
  padding: 8px;
  box-sizing: border-box;
  text-align: center;
}

.lock-overlay .van-icon {
  margin-bottom: 4px;
  font-size: 20px;
}

.level-text {
  font-size: 12px;
  font-weight: bold;
  line-height: 1.2;
}

.reward-item.unlocked:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
}

.reward-item.unlocked:hover .reward-image img {
  transform: scale(1.05);
  transition: transform 0.3s ease;
}

.reward-item:not(.unlocked) {
  cursor: not-allowed;
}

.reward-item:not(.unlocked) .reward-button {
  cursor: not-allowed;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes unlock {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

.reward-item.unlocked .reward-image {
  animation: fadeIn 0.5s ease, unlock 0.6s ease;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .reward-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }

  .reward-item {
    min-height: 100px;
  }

  .points-buttons {
    flex-direction: row;
    gap: 12px;
    padding: 12px 16px;
  }

  .point-button {
    min-width: 140px;
    height: 40px;
    font-size: 13px;
  }

  .game-area {
    padding: 16px;
  }
}

@media (max-width: 480px) {
  .reward-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
  }

  .reward-item {
    min-height: 90px;
  }

  .points-buttons {
    gap: 8px;
    padding: 10px 12px;
  }

  .point-button {
    min-width: 120px;
    height: 36px;
    font-size: 12px;
    flex: 1;
  }

  .game-area {
    padding: 12px;
  }
}

@media (max-width: 360px) {
  .points-buttons {
    gap: 6px;
    padding: 8px 10px;
  }

  .point-button {
    min-width: 120px;
    height: 34px;
    font-size: 11px;
  }
}

@media (min-width: 769px) {
  .reward-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .reward-item {
    min-height: 120px;
  }
}

.reward-item {
  max-width: 200px;
  margin: 0 auto;
}
</style>