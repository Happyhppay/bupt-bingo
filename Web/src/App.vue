<template>
  <div class="app">
    <router-view></router-view>
  </div>
</template>

<script setup>
// App level logic here
</script>

<style>
/* App.vue 中的 style 部分 */
.app {
  width: 100%;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Helvetica Neue', Arial, 'PingFang SC', 'Microsoft YaHei', sans-serif;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  color: #2c3e50;
  line-height: 1.6;
}

/* 统一的卡片阴影效果 */
.card-shadow {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border-radius: 16px;
}

/* 按钮样式增强 */
.van-button {
  border-radius: 12px !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
  font-weight: 500;
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.van-button--primary {
  background: linear-gradient(135deg, #8fa1f4 0%, #cfa6fb 100%) !important;
  border: none !important;
}

.van-button--primary:active {
  transform: translateY(2px);
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
}

.van-button--disabled {
  opacity: 0.6;
  transform: none !important;
}

/* 导航栏样式美化 */
.van-nav-bar {
  background: linear-gradient(90deg, #2d4de1 0%, #cfa6fb 100%) !important;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.van-nav-bar__title {
  color: white !important;
  font-weight: 600;
  font-size: 18px;
}

/* 对话框样式美化 */
.van-dialog {
  border-radius: 20px !important;
  overflow: hidden;
}

.van-dialog__header {
  padding: 20px;
  font-weight: 600;
  font-size: 18px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.van-dialog__content {
  padding: 24px;
}
</style>