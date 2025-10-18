<template>
  <div class="user-info">
    <span class="name">{{ userStore.userInfo.name }}</span>
    <span class="points">
      积分：{{ userStore.bingoStatus.point }} / 
      特殊积分：{{ userStore.bingoStatus.specialPoint }}
    </span>
  </div>
</template>

<script setup>
import { useUserStore } from '@/store/user'

const userStore = useUserStore()
</script>

<style scoped>
/* UserInfo/index.vue 中的 style 部分 */
.user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

.name {
  font-weight: 600;
  color: black;
  font-size: 14px;
}

.points {
  color: rgba(0, 0, 0, 0.9);
  font-size: 12px;
  display: flex;
  gap: 8px;
}
</style>