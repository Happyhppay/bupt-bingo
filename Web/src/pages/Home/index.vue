<template>
  <div class="home">
    <!-- 顶部栏 - 两行布局 -->
    <div class="custom-header">
      <!-- 第一行：标题 -->
      <div class="header-title-row">
        <div class="header-title">百社游园，邮你绘梦</div>
      </div>

      <!-- 第二行：用户信息和功能按钮 -->
      <div class="header-action-row">
        <div class="header-left">
          <user-info v-if="userStore.token" />
          <van-button v-else type="primary" size="small" icon="user" @click="showLogin">登录</van-button>
        </div>
        <div class="header-right">
          <van-button type="primary" size="small" icon="scan" @click="showScan">扫码</van-button>
        </div>
      </div>
    </div>

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
      <!-- 新增游戏规则按钮 -->
      <van-button
        type="info"
        @click="showGameRules"
        class="point-button"
      >
        游戏规则
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
      <!-- 修改奖励网格布局 -->
      <div class="reward-grid">
        <!-- 前6个奖励放在第一行 -->
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

        <!-- 第7个奖励单独放在第二行中间，未激活时隐藏 -->
        <div
          v-if="userStore.bingoStatus.rewards.includes(7)"
          class="reward-item reward-item-special"
          :class="{ unlocked: userStore.bingoStatus.rewards.includes(7) }"
          @click="getReward(7)"
        >
          <van-button
            :disabled="!userStore.bingoStatus.rewards.includes(7)"
            class="reward-button"
          >
            <!-- 按钮仅作为点击容器，内容由 reward-image 控制 -->
          </van-button>
          <div class="reward-image" :class="{ locked: !userStore.bingoStatus.rewards.includes(7) }">
            <img :src="getRewardImage(7)" :alt="`神秘奖品`" />
            <!-- 未获得时显示锁和提示 -->
            <div v-if="!userStore.bingoStatus.rewards.includes(7)" class="lock-overlay">
              <van-icon name="lock" size="24" />
              <span class="level-text">神秘奖品</span>
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

    <!-- 游戏规则弹窗 -->
    <van-dialog
      v-model:show="showGameRulesModal"
      title="游戏规则"
      show-cancel-button
      cancel-button-text="关闭"
      :show-confirm-button="false"
    >
      <div class="game-rules-content">
        <h3>Bingo 游戏规则</h3>
        <div class="rule-item">
          <strong>1. 游戏目标</strong>
          <p>完成 Bingo 卡片上的连线任务，获得对应的奖励。</p>
        </div>
        <div class="rule-item">
          <strong>2. 连线规则</strong>
          <p>横线、竖线、对角线连成一条直线即可完成一次Bingo连线。</p>
        </div>
        <div class="rule-item">
          <strong>3. 奖励获取</strong>
          <p>完成一次Bingo连线可随机点亮一个奖励（每个奖励只能点亮一次）。</p>
        </div>
        <div class="rule-item">
          <strong>4. 积分获得</strong>
          <p>完成各个社团的活动后，扫描该社团的动态签到码获得。</p>
        </div>
        <div class="rule-item">
          <strong>5. 积分使用</strong>
          <p>- 普通积分：随机点亮一个格子。</p>
          <p>- 特殊积分：指定点亮任意一个格子。</p>
        </div>
        <div class="rule-item">
          <strong>6. 奖励兑换</strong>
          <p>点击想要兑换的奖励会出现一个兑奖二维码，由社团工作部兑奖处的工作人员扫码后，出示学生证或校园卡获取（一个二维码只能用一次）。</p>
        </div>
        <div class="rule-item">
          <strong>7. 彩蛋</strong>
		  <p>提示1："五佳十优"社团的签到码似乎有点特别？！</p>
          <p>提示2：尝试点亮全部25个格子会有惊喜吗？</p>
        </div>
      </div>
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
  const imageMap = {
    1: '/image/rewards/level1.png',
    2: '/image/rewards/level2.png',
    3: '/image/rewards/level3.png',
    4: '/image/rewards/level4.png',
    5: '/image/rewards/level5.png',
    6: '/image/rewards/level6.png',
    7: '/image/rewards/level7.png'
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
const showGameRulesModal = ref(false)

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

// 显示游戏规则弹窗
const showGameRules = () => {
  showGameRulesModal.value = true
}

// 使用普通积分
const useNormalPoint = async () => {
  try {
    await userStore.lightGrid({pointType: 'normal'})
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
    const res = await api.getRewardQrcode({reward: level})
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
    await userStore.getBingoStatus().catch(() => {})
    showInviteModal.value = false
    showToast('验证成功')
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
.home {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* 新的顶部栏样式 */
.custom-header {
  position: sticky;
  top: 0;
  z-index: 1000;
  backdrop-filter: blur(10px);
  background: rgba(102, 126, 234, 0.95);
  padding: 12px 16px 8px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.header-title-row {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 8px;
}

.header-title {
  color: white;
  font-size: 18px;
  font-weight: bold;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.header-action-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left,
.header-right {
  flex: 1;
  display: flex;
  align-items: center;
}

.header-left {
  justify-content: flex-start;
}

.header-right {
  justify-content: flex-end;
}

.game-area {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 16px 20px;
}

.bingo-grid {
  flex: 1;
  max-width: 500px;
}

/* 积分按钮区域 */
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
  position: relative;
  min-height: auto;
  transition: all 0.3s ease;
}

/* 当第7个奖励显示时的特殊样式 */
.reward-item-special {
  grid-column: 2 / 3;
  justify-self: center;
  margin-top: 12px;
  animation: fadeIn 0.5s ease;
}

.admin-entry-container {
  display: flex;
  justify-content: center;
  gap: 16px;
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
  min-width: 80px;
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
  max-width: 200px;
  margin: 0 auto;
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

/* 游戏规则内容样式 */
.game-rules-content {
  padding: 16px;
  max-height: 60vh;
  overflow-y: auto;
}

.game-rules-content h3 {
  text-align: center;
  margin-bottom: 16px;
  color: #1989fa;
}

.rule-item {
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f0f0f0;
}

.rule-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.rule-item strong {
  display: block;
  margin-bottom: 4px;
  color: #333;
}

.rule-item p {
  margin: 4px 0;
  color: #666;
  font-size: 14px;
  line-height: 1.4;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.8) translateY(-10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
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
  .custom-header {
    padding: 10px 12px 6px;
  }

  .header-title {
    font-size: 16px;
  }

  .header-title-row {
    margin-bottom: 6px;
  }

  .reward-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }

  .reward-item-special {
    grid-column: 1 / -1;
    justify-self: center;
    max-width: 120px;
    margin-top: 8px;
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
  .custom-header {
    padding: 8px 10px 6px;
  }

  .header-title {
    font-size: 15px;
  }

  .header-title-row {
    margin-bottom: 6px;
  }

  .reward-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
  }

  .reward-item-special {
    grid-column: 1 / -1;
    justify-self: center;
    max-width: 100px;
    margin-top: 6px;
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
  .custom-header {
    padding: 6px 8px 4px;
  }

  .header-title {
    font-size: 14px;
  }

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
</style>