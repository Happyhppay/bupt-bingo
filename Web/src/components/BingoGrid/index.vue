<template>
  <div class="bingo-grid">
    <div 
      v-for="(row, i) in userStore.bingoStatus.bingoGrid" 
      :key="i" 
      class="grid-row"
    >
      <div 
        v-for="(cell, j) in row" 
        :key="j"
        :class="['grid-cell', { active: cell === 1 }]"
        @click="onCellClick([i, j])"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { useUserStore } from '@/store/user'

const userStore = useUserStore()

const onCellClick = (location) => {
  emit('cell-click', location)
}

defineEmits(['cell-click'])
</script>

<style scoped>
/* BingoGrid/index.vue 中的 style 部分 */
.bingo-grid {
  width: 100%;
  aspect-ratio: 1;
  background: linear-gradient(145deg, #ffffff, #f0f0f0);
  border-radius: 20px;
  padding: 8px; /* 减少内边距 */
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.2);
  /* 添加以下属性确保内容不溢出 */
  overflow: hidden;
  box-sizing: border-box;
}

.grid-row {
  display: flex;
  height: calc(20% - 2px); /* 使用calc考虑间隙 */
  gap: 2px; /* 减少间隙 */
  margin-bottom: 2px;
  /* 确保行不溢出 */
  box-sizing: border-box;
}

.grid-row:last-child {
  margin-bottom: 0;
}

.grid-cell {
  flex: 1;
  background: linear-gradient(145deg, #b5b3b3, #9f9f9f);
  border-radius: 8px; /* 稍微减小圆角 */
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  border: 1px solid transparent; /* 减小边框 */
  position: relative;
  overflow: hidden;
  /* 确保单元格不溢出 */
  box-sizing: border-box;
  min-height: 0; /* 重要：允许flex项目缩小 */
}
.grid-cell::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
  opacity: 0;
  transition: opacity 0.3s ease;
}

.grid-cell:hover::before {
  opacity: 1;
}

.grid-cell:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  border-color: #667eea;
}

.grid-cell.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow:
    0 4px 16px rgba(102, 126, 234, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow:
      0 4px 16px rgba(102, 126, 234, 0.4),
      inset 0 1px 0 rgba(255, 255, 255, 0.3);
  }
  50% {
    box-shadow:
      0 6px 20px rgba(102, 126, 234, 0.6),
      inset 0 1px 0 rgba(255, 255, 255, 0.3);
  }
  100% {
    box-shadow:
      0 4px 16px rgba(102, 126, 234, 0.4),
      inset 0 1px 0 rgba(255, 255, 255, 0.3);
  }
}
</style>