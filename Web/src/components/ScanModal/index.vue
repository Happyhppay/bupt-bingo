<template>
  <van-dialog
    :show="show"
    title="扫描二维码"
    :show-confirm-button="false"
    @update:show="$emit('update:show', $event)"
  >
    <div class="scanner-container">
      <div id="reader"></div>
    </div>
  </van-dialog>
</template>

<script setup>
import { onMounted, onUnmounted, watch } from 'vue'
import { showToast } from 'vant'
import { Html5QrcodeScanner } from 'html5-qrcode'
import { api } from '@/api'
import { useUserStore } from '@/store/user'

const props = defineProps({
  show: Boolean
})

const emit = defineEmits(['update:show'])
const userStore = useUserStore()
let html5QrcodeScanner = null

watch(() => props.show, (newVal) => {
  if (newVal) {
    // Use nextTick to ensure the DOM is ready
    // And a small timeout for the dialog animation
    setTimeout(() => {
      initScanner()
    }, 200)
  } else {
    clearScanner()
  }
})

const initScanner = () => {
  if (!document.getElementById('reader')) {
    console.error("Element with id 'reader' not found.");
    return;
  }
  // Prevent re-initialization
  if (html5QrcodeScanner && html5QrcodeScanner.isScanning) {
    return;
  }
  html5QrcodeScanner = new Html5QrcodeScanner(
    'reader',
    { fps: 10, qrbox: { width: 250, height: 250 } },
    /* verbose= */ false
  )
  html5QrcodeScanner.render(onScanSuccess, onScanError)
}

const onScanSuccess = async (decodedText, decodedResult) => {
  // handle the scanned code as you like, for example:
  console.log(`Code matched = ${decodedText}`, decodedResult);
  try {
    // Stop scanning after a successful scan.
    clearScanner()
    
    const res = await api.scanClubQrcode({ qrcodeToken: decodedText })
    await userStore.getBingoStatus()
    showToast(`获得${res.addedPoint}点普通积分，${res.addedSpecialPoint}点特殊积分`)
    emit('update:show', false)
  } catch (error) {
    showToast('扫码失败，请重试')
    console.error(error)
    // Optionally, resume scanning
    // html5QrcodeScanner.render(onScanSuccess, onScanError);
  }
}

const onScanError = (error) => {
  // handle scan error, usually better to ignore and keep scanning.
  // console.warn(`Code scan error = ${error}`);
}

const clearScanner = () => {
  if (html5QrcodeScanner) {
    html5QrcodeScanner.clear().catch(error => {
      console.error("Failed to clear html5QrcodeScanner.", error);
    });
    html5QrcodeScanner = null;
  }
}

onUnmounted(() => {
  clearScanner()
})
</script>

<style scoped>
.scanner-container {
  padding: 16px;
}

#reader {
  width: 100%;
}
</style>