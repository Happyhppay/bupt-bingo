<template>
  <van-dialog
    :show="show"
    title="扫描二维码"
    :show-confirm-button="false"
    @update:show="$emit('update:show', $event)"
  >
    <div class="scanner-container">
      <div id="reader"></div>
      <div class="dialog-actions">
        <van-button type="default" @click="closeDialog" class="close-btn">
          关闭扫码
        </van-button>
      </div>
    </div>
  </van-dialog>
</template>

<script setup>
import { onUnmounted, watch, nextTick } from 'vue'
import { showToast } from 'vant'
import { Html5Qrcode } from 'html5-qrcode'
import { api } from '@/api'
import { useUserStore } from '@/store/user'

const props = defineProps({
  show: Boolean
})

const emit = defineEmits(['update:show'])
const userStore = useUserStore()
let html5Qrcode = null

// 关闭弹窗
const closeDialog = () => {
  stopScanner()
  emit('update:show', false)
}

const startScanner = () => {
  // 防止重复初始化
  if (html5Qrcode && html5Qrcode.isScanning) {
    return
  }
  html5Qrcode = new Html5Qrcode('reader')
  const config = { fps: 10, qrbox: { width: 250, height: 250 } }
  html5Qrcode.start({ facingMode: 'environment' }, config, onScanSuccess, onScanError).catch((err) => {
    console.error('无法启动扫描器', err)
    showToast('无法启动扫描器，请检查摄像头权限')
  })
}

const stopScanner = () => {
  if (html5Qrcode && html5Qrcode.isScanning) {
    html5Qrcode.stop().catch((err) => {
      console.error('停止扫描器失败', err)
    })
  }
  html5Qrcode = null
}

watch(
  () => props.show,
  (newValue) => {
    if (newValue) {
      nextTick(() => {
        startScanner()
      })
    } else {
      stopScanner()
    }
  }
)

const onScanSuccess = async (decodedText, decodedResult) => {
  // 成功扫描后停止扫描器
  stopScanner()
  try {
    const res = await api.scanClubQrcode({ qrcodeToken: decodedText })
    await userStore.getBingoStatus()
    showToast(`获得${res.addedPoint}点普通积分，${res.addedSpecialPoint}点特殊积分`)
    emit('update:show', false) // 关闭弹窗
  } catch (error) {
    showToast(error.message || '扫码失败')
    console.error(error)
    emit('update:show', false) // 出错也关闭弹窗
  }
}

const onScanError = (error) => {
  // onScanError 会被频繁调用，这里不做过多处理
  // console.warn(`扫码错误: ${error}`)
}

onUnmounted(() => {
  stopScanner()
})
</script>

<style scoped>
.scanner-container {
  padding: 16px;
}

#reader {
  width: 100%;
  margin-bottom: 16px;
}

.dialog-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
}

.close-btn {
  min-width: 120px;
  border-radius: 20px;
}
</style>