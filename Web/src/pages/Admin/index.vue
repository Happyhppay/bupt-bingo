<template>
  <div class="admin">
    <van-nav-bar
      title="管理员后台"
      left-arrow
      @click-left="onBack"
    />

    <div class="content">
      <van-button type="primary" block @click="startScan">
        扫描领奖二维码
      </van-button>

      <div class="result" v-if="verifyResult">
        <h3>验证结果</h3>
        <p>学号：{{ verifyResult.userInfo.studentId }}</p>
        <p>姓名：{{ verifyResult.userInfo.name }}</p>
        <p>奖励等级：{{ verifyResult.rewardLevel }}</p>
      </div>
    </div>

    <!-- 扫码组件 -->
    <div class="scanner" v-show="showScanner">
      <div id="reader"></div>
      <van-button type="default" @click="stopScan">关闭扫码</van-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import { Html5QrcodeScanner } from 'html5-qrcode'
import { api } from '@/api'

const router = useRouter()
const showScanner = ref(false)
const verifyResult = ref(null)
let html5QrcodeScanner = null

const onBack = () => {
  router.push('/')
}

const startScan = () => {
  showScanner.value = true
  verifyResult.value = null

  // 初始化扫码器
  html5QrcodeScanner = new Html5QrcodeScanner(
    'reader',
    { fps: 10, qrbox: { width: 250, height: 250 } },
    false
  )

  html5QrcodeScanner.render(onScanSuccess, onScanError)
}

const stopScan = () => {
  if (html5QrcodeScanner) {
    html5QrcodeScanner.clear()
  }
  showScanner.value = false
}

const onScanSuccess = async (rewardToken) => {
  try {
    stopScan()
    const res = await api.verifyReward({ rewardToken })
    verifyResult.value = res
    showToast('验证成功')
  } catch (error) {
    showToast('验证失败')
    console.error(error)
  }
}

const onScanError = (error) => {
  console.warn(error)
}

onUnmounted(() => {
  if (html5QrcodeScanner) {
    html5QrcodeScanner.clear()
  }
})
</script>

<style scoped>
.admin {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.content {
  flex: 1;
  padding: 16px;
}

.result {
  margin-top: 32px;
  padding: 16px;
  background: #fff;
  border-radius: 8px;
}

.result h3 {
  margin: 0 0 16px;
  font-size: 18px;
}

.result p {
  margin: 8px 0;
  color: #666;
}

.scanner {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #fff;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px;
}

#reader {
  width: 100%;
  max-width: 600px;
}
</style>