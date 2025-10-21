<template>
  <div class="user-info">
    <div class="top-row">
      <span class="id">{{ userStore.userInfo.studentId }}</span>
      <van-button size="mini" type="danger" @click="onLogout">退出</van-button>
    </div>
  </div>
</template>

<script setup>
import { useUserStore } from '@/store/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

const onLogout = () => {
  userStore.logout()
  // 重定向到首页并刷新页面，确保组件状态全部清理
  router.push('/').catch(() => {})
  window.location.reload()
}
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

.top-row {
  display: flex;
  width: 100%;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}
</style>