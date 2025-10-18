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
        @click="onCellClick([i + 1, j + 1])"
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
.bingo-grid {
  width: 100%;
  aspect-ratio: 1;
  background: #fff;
  border-radius: 8px;
  padding: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.grid-row {
  display: flex;
  height: 20%;
}

.grid-cell {
  flex: 1;
  margin: 2px;
  background: #f5f5f5;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.grid-cell.active {
  background: #1989fa;
}
</style>