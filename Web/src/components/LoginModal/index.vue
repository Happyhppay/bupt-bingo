<template>
  <van-dialog
    :show="show"
    title="登录"
    show-cancel-button
    @confirm="onSubmit"
    @update:show="$emit('update:show', $event)"
  >
    <van-form @submit="onSubmit">
      <van-field
        v-model="form.student_id"
        name="student_id"
        label="学号"
        placeholder="请输入学号"
        :rules="[{ required: true, message: '请填写学号' }]"
      />
    </van-form>
  </van-dialog>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/store/user'
import { showToast } from 'vant'

const props = defineProps({
  show: Boolean
})

const emit = defineEmits(['update:show'])

const userStore = useUserStore()
const form = ref({
  student_id: ''
})

const onSubmit = async () => {
  try {
    await userStore.login(form.value)
    await userStore.getBingoStatus() // 获取用户状态
    showToast('登录成功')
    emit('update:show', false)
  } catch (error) {
    console.error(error)
  }
}
</script>
<style>
/* LoginModal/index.vue 中的 style 部分 */
.van-form {
  padding: 8px 0;
}

.van-field {
  background: #f8f9fa;
  border-radius: 12px;
  margin-bottom: 16px;
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.van-field:focus-within {
  border-color: #667eea;
  background: white;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
}

.van-field__label {
  font-weight: 500;
  color: #2c3e50;
}
</style>