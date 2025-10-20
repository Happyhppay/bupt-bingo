<template>
  <div class="admin">
    <van-nav-bar
      title="管理员后台"
      left-arrow
      @click-left="onBack"
      class="admin-navbar"
    />

    <div class="content">
      <div class="action-card card-shadow">
        <van-button
          type="primary"
          block
          @click="startScan"
          class="scan-btn"
          icon="scan"
        >
          扫描领奖二维码
        </van-button>
      </div>

      <div class="result-card card-shadow" v-if="verifyResult">
        <h3 class="result-title">🎉 验证成功</h3>
        <div class="user-info">
          <div class="info-item">
            <span class="label">学号</span>
            <span class="value">{{ verifyResult.userInfo.studentId }}</span>
          </div>
          <div class="info-item">
            <span class="label">姓名</span>
            <span class="value">{{ verifyResult.userInfo.name }}</span>
          </div>
          <div class="info-item">
            <span class="label">奖励等级</span>
            <span class="value reward-level">第 {{ verifyResult.rewardLevel }} 级</span>
          </div>
        </div>
        <van-button
          type="success"
          block
          @click="verifyResult = null"
          class="clear-btn"
        >
          清除结果
        </van-button>
      </div>

      <div class="empty-state" v-else>
        <div class="empty-icon">📱</div>
        <p class="empty-text">点击上方按钮开始扫码验证</p>
      </div>
    </div>

    <!-- 复用 ScanModal 组件（手动模式） -->
    <scan-modal v-model:show="showScanner" :manual="true" @decoded="onAdminDecoded" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import { api } from '@/api'
import ScanModal from '@/components/ScanModal/index.vue'

const router = useRouter()
const showScanner = ref(false)
const verifyResult = ref(null)

const onBack = () => {
  router.push('/')
}

const startScan = () => {
  showScanner.value = true
  verifyResult.value = null
}

const stopScan = () => {
  showScanner.value = false
}

const onAdminDecoded = async (decodedText) => {
  try {
    stopScan()
    const res = await api.verifyReward({ rewardToken: decodedText })
    verifyResult.value = res
    showToast('验证成功')
  } catch (error) {
    showToast('验证失败')
    console.error(error)
  }
}
</script>

<style scoped>
.admin {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.admin-navbar {
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
}

.content {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.action-card {
  background: white;
  padding: 20px;
  border-radius: 20px;
}

.scan-btn {
  height: 50px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 12px;
}

.result-card {
  background: white;
  padding: 24px;
  border-radius: 20px;
  animation: slideInUp 0.5s ease;
}

.result-title {
  text-align: center;
  margin: 0 0 20px 0;
  font-size: 20px;
  font-weight: 600;
  color: #27ae60;
  background: linear-gradient(135deg, #27ae60, #2ecc71);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 20px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #f8f9fa;
  border-radius: 12px;
  border-left: 4px solid #667eea;
}

.label {
  font-weight: 500;
  color: #666;
}

.value {
  font-weight: 600;
  color: #2c3e50;
}

.reward-level {
  color: #e74c3c;
  font-weight: 700;
}

.clear-btn {
  height: 44px;
  border-radius: 12px;
  background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
  border: none;
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.6;
}

.empty-text {
  color: #666;
  font-size: 16px;
  margin: 0;
}

.scanner-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.9);
  z-index: 2000;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.scanner-container {
  background: white;
  border-radius: 20px;
  padding: 24px;
  width: 100%;
  max-width: 400px;
  text-align: center;
}

.scanner-header {
  margin-bottom: 20px;
}

.scanner-header h3 {
  margin: 0 0 8px 0;
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
}

.scanner-header p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.scanner {
  width: 100%;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 20px;
}

.close-scanner-btn {
  width: 100%;
  height: 44px;
  border-radius: 12px;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式设计 */
@media (max-width: 480px) {
  .content {
    padding: 16px;
    gap: 16px;
  }

  .action-card,
  .result-card {
    padding: 16px;
  }

  .info-item {
    padding: 10px 12px;
  }
}
</style>