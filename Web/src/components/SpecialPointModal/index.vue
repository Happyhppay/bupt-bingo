<template>
  <van-dialog
    :show="show"
    title="选择格子"
    :show-cancel-button="false"
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
        >
          <div class="cell-content"></div>
        </div>
      </div>
    </div>
    <div class="dialog-actions">
      <van-button type="default" @click="closeDialog" class="close-btn">
        取消选择
      </van-button>
    </div>
  </van-dialog>
</template>

<script setup>
import {useUserStore} from '@/store/user'
import {showToast} from 'vant'

const props = defineProps({
  show: Boolean
})

const emit = defineEmits(['update:show', 'confirm'])
const userStore = useUserStore()

// 关闭弹窗
const closeDialog = () => {
  emit('update:show', false)
}

const onCellSelect = (location) => {
  if (userStore.bingoStatus.bingoGrid[location[0]][location[1]] === 1) {
    showToast('该格子已被点亮')
    return
  }
  emit('confirm', location)
  closeDialog()
}
</script>

<style scoped>
.grid-selector {
  padding: 16px;
}

.grid-row {
  display: flex;
  margin-bottom: 8px;
}

.grid-row:last-child {
  margin-bottom: 0;
}

.grid-cell {
  flex: 1;
  position: relative;
  margin: 0 4px;
  cursor: pointer;
}

/* 使用 padding 技巧创建正方形 */
.cell-content {
  width: 100%;
  padding-bottom: 100%; /* 关键：padding-bottom 100% 基于宽度计算 */
  background: #b5b3b3;
  border-radius: 6px;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.grid-cell:hover .cell-content {
  transform: scale(1.05);
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.grid-cell.active .cell-content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  pointer-events: none;
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
}

.dialog-actions {
  padding: 0 16px 16px;
  display: flex;
  justify-content: center;
}

.close-btn {
  min-width: 120px;
  border-radius: 20px;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .grid-selector {
    padding: 12px;
  }

  .grid-row {
    margin-bottom: 6px;
  }

  .grid-cell {
    margin: 0 3px;
  }

  .cell-content {
    border-radius: 4px;
  }
}
</style>