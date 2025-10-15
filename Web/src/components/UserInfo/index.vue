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
.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.name {
  font-weight: bold;
}

.points {
  color: #666;
  font-size: 14px;
}
</style>