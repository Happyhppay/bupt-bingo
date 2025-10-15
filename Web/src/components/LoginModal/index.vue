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
      <van-field
        v-model="form.name"
        name="name"
        label="姓名"
        placeholder="请输入姓名"
        :rules="[{ required: true, message: '请填写姓名' }]"
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
  student_id: '',
  name: ''
})

const onSubmit = async () => {
  try {
    await userStore.login(form.value)
    showToast('登录成功')
    emit('update:show', false)
  } catch (error) {
    console.error(error)
  }
}
</script>