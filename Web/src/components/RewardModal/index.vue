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
      <div class="dialog-actions">
        <van-button type="primary" @click="closeDialog" class="close-btn">
          关闭
        </van-button>
      </div>
    </div>
  </van-dialog>
</template>

<script setup>
import QrcodeVue from 'qrcode.vue'

const props = defineProps({
  show: Boolean,
  rewardToken: String
})

const emit = defineEmits(['update:show'])

// 关闭弹窗
const closeDialog = () => {
  emit('update:show', false)
}
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
  text-align: center;
}

.dialog-actions {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  width: 100%;
}

.close-btn {
  min-width: 120px;
  border-radius: 20px;
}
</style>