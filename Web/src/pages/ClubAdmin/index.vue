<template>
  <div class="club-admin">
    <van-nav-bar
      title="社团后台"
      left-arrow
      @click-left="onBack"
    />

    <div class="content">
      <van-button type="primary" block @click="refreshQrcode">
        刷新二维码
      </van-button>

      <div class="qrcode-container" v-if="qrcodeToken">
        <qrcode-vue :value="qrcodeToken" :size="200" level="H" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import QrcodeVue from 'qrcode.vue'
import { api } from '@/api'

const router = useRouter()
const qrcodeToken = ref('')

const onBack = () => {
  router.push('/')
}

const refreshQrcode = async () => {
  try {
    const res = await api.getClubQrcode()
    qrcodeToken.value = res.qrcodeToken
  } catch (error) {
    showToast('获取二维码失败')
    console.error(error)
  }
}
</script>

<style scoped>
.club-admin {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.content {
  flex: 1;
  padding: 16px;
}

.qrcode-container {
  margin-top: 32px;
  display: flex;
  justify-content: center;
}
</style>