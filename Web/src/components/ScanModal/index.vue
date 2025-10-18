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
import {onMounted, onUnmounted} from 'vue'
import {showToast} from 'vant'
import {Html5QrcodeScanner} from 'html5-qrcode'
import {api} from '@/api'
import {useUserStore} from '@/store/user'

const props = defineProps({
  show: Boolean
})

const emit = defineEmits(['update:show'])
const userStore = useUserStore()
let html5QrcodeScanner = null

// 关闭弹窗
const closeDialog = () => {
  if (html5QrcodeScanner) {
    html5QrcodeScanner.clear()
  }
  emit('update:show', false)
}

onMounted(() => {
  if (props.show) {
    initScanner()
  }
})

const initScanner = () => {
  html5QrcodeScanner = new Html5QrcodeScanner(
      'reader',
      {fps: 10, qrbox: {width: 250, height: 250}},
      false
  )

  html5QrcodeScanner.render(onScanSuccess, onScanError)
}

const onScanSuccess = async (qrcodeToken) => {
  try {
    const res = await api.scanClubQrcode({qrcodeToken})
    await userStore.getBingoStatus()
    showToast(`获得${res.addedPoint}点普通积分，${res.addedSpecialPoint}点特殊积分`)
    closeDialog()
  } catch (error) {
    showToast('扫码失败')
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