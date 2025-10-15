<template>
  <van-dialog
    :show="show"
    title="领奖二维码"
    :show-confirm-button="false"
    @update:show="$emit('update:show', $event)"
  >
    <div class="qrcode-container">
      <qrcode-vue :value="rewardToken" :size="200" level="H" />
      <p class="tip">请向管理员出示此二维码领取奖励</p>
    </div>
  </van-dialog>
</template>

<script setup>
import QrcodeVue from 'qrcode.vue'

defineProps({
  show: Boolean,
  rewardToken: String
})

defineEmits(['update:show'])
</script>

<style scoped>
.qrcode-container {
  padding: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.tip {
  margin-top: 16px;
  color: #666;
  font-size: 14px;
}
</style>