<template>
  <div class="club-admin">
    <van-nav-bar
      title="社团后台"
      left-arrow
      @click-left="onBack"
      class="club-navbar"
    />

    <div class="content">
      <div class="action-section">
        <div class="action-card card-shadow">
          <van-button
            type="primary"
            block
            @click="refreshQrcode"
            class="refresh-btn"
            icon="replay"
            :loading="loading"
          >
            {{ loading ? '生成中...' : '刷新二维码' }}
          </van-button>
        </div>

        <div class="tip-card card-shadow" v-if="qrcodeToken">
          <div class="tip-header">
            <span class="tip-icon">💡</span>
            <span class="tip-title">使用说明</span>
          </div>
          <p class="tip-content">请让参与者扫描下方二维码进行签到，每次扫码可获得积分<br>参与者扫码后原二维码将失效，需要重新刷新二维码</p>
        </div>
      </div>

      <div class="qrcode-section" v-if="qrcodeToken">
        <div class="qrcode-card card-shadow">
          <div class="qrcode-header">
            <h3>社团二维码</h3>
            <p class="qrcode-subtitle">有效时间：5分钟</p>
          </div>
          <div class="qrcode-container">
            <qrcode-vue
              :value="qrcodeToken"
              :size="qrcodeSize"
              level="H"
              class="qrcode"
            />
          </div>
        </div>
      </div>

      <div class="empty-state" v-else>
        <div class="empty-illustration">
          <div class="empty-icon">🎯</div>
          <h3 class="empty-title">欢迎使用社团后台</h3>
          <p class="empty-text">点击上方按钮生成签到二维码</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import QrcodeVue from 'qrcode.vue'
import { api } from '@/api'

const router = useRouter()
const qrcodeToken = ref('')
const loading = ref(false)

const qrcodeSize = computed(() => {
  return window.innerWidth < 400 ? 200 : 250
})

const onBack = () => {
  router.push('/')
}

const refreshQrcode = async () => {
  try {
    loading.value = true
    const res = await api.getClubQrcode()
    qrcodeToken.value = res.qrcodeToken
    showToast('二维码已更新')
  } catch (error) {
    showToast('获取二维码失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const downloadQrcode = () => {
  showToast('下载功能开发中...')
  // 实际实现需要将二维码转换为图片下载
}

const shareQrcode = () => {
  showToast('分享功能开发中...')
  // 实际实现需要调用分享API
}
</script>

<style scoped>
.club-admin {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.club-navbar {
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
}

.content {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.action-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.action-card {
  background: white;
  padding: 20px;
  border-radius: 20px;
}

.refresh-btn {
  height: 50px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 12px;
}

.tip-card {
  background: linear-gradient(135deg, #ffeaa7, #fab1a0);
  padding: 16px;
  border-radius: 16px;
  border-left: 4px solid #e17055;
}

.tip-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.tip-icon {
  font-size: 18px;
}

.tip-title {
  font-weight: 600;
  color: #2d3436;
}

.tip-content {
  margin: 0;
  font-size: 14px;
  color: #636e72;
  line-height: 1.5;
}

.qrcode-section {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.qrcode-card {
  background: white;
  padding: 24px;
  border-radius: 20px;
  text-align: center;
  max-width: 300px;
  width: 100%;
  animation: scaleIn 0.5s ease;
}

.qrcode-header {
  margin-bottom: 20px;
}

.qrcode-header h3 {
  margin: 0 0 8px 0;
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
}

.qrcode-subtitle {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.qrcode-container {
  padding: 16px;
  background: #f8f9fa;
  border-radius: 12px;
  margin-bottom: 20px;
}

.qrcode {
  border-radius: 8px;
}

.qrcode-footer {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.qrcode-footer .van-button {
  border-radius: 20px;
  flex: 1;
  max-width: 120px;
}

.empty-state {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.empty-illustration {
  text-align: center;
  padding: 40px 20px;
}

.empty-icon {
  font-size: 80px;
  margin-bottom: 20px;
  opacity: 0.7;
}

.empty-title {
  margin: 0 0 12px 0;
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
}

.empty-text {
  margin: 0;
  color: #666;
  font-size: 16px;
}

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* 响应式设计 */
@media (max-width: 480px) {
  .content {
    padding: 16px;
    gap: 16px;
  }

  .action-card {
    padding: 16px;
  }

  .qrcode-card {
    padding: 20px;
  }

  .qrcode-container {
    padding: 12px;
  }
}

@media (max-width: 360px) {
  .qrcode-footer {
    flex-direction: column;
    gap: 8px;
  }

  .qrcode-footer .van-button {
    max-width: none;
  }
}
</style>