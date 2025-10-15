<template>
  <van-dialog
    :show="show"
    title="选择格子"
    show-cancel-button
    :show-confirm-button="false"
    @update:show="$emit('update:show', $event)"
  >
    <div class="grid-selector">
      <div 
        v-for="(row, i) in userStore.bingoStatus.bingoGrid" 
        :key="i" 
        class="grid-row"
      >
        <div 
          v-for="(cell, j) in row" 
          :key="j"
          :class="['grid-cell', { active: cell === 1 }]"
          @click="onCellSelect([i, j])"
        ></div>
      </div>
    </div>
  </van-dialog>
</template>

<script setup>
import { useUserStore } from '@/store/user'
import { showToast } from 'vant'

const props = defineProps({
  show: Boolean
})

const emit = defineEmits(['update:show', 'confirm'])
const userStore = useUserStore()

const onCellSelect = (location) => {
  if (userStore.bingoStatus.bingoGrid[location[0]][location[1]] === 1) {
    showToast('该格子已被点亮')
    return
  }
  emit('confirm', location)
}
</script>

<style scoped>
.grid-selector {
  padding: 16px;
}

.grid-row {
  display: flex;
  height: 48px;
  margin: 4px 0;
}

.grid-cell {
  flex: 1;
  margin: 0 4px;
  background: #f5f5f5;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.grid-cell.active {
  background: #1989fa;
  pointer-events: none;
}
</style>