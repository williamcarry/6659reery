<template>
  <div class="product-inquiry-edit-tab">
    <product-inquiry-edit 
      ref="editComponentRef"
      :admin-login-path="adminLoginPath" 
      :inquiry-id="inquiryId"
      :is-tab-mode="true"
      @saved="handleSaved"
      @cancelled="handleCancelled"
    />
  </div>
</template>

<script setup>
import { ref, defineProps, defineExpose } from 'vue'
import ProductInquiryEdit from './ProductInquiryEdit.vue'

const props = defineProps({
  adminLoginPath: {
    type: String,
    required: true
  },
  inquiryId: {
    type: Number,
    required: true
  },
  autoLoad: {
    type: Boolean,
    default: false
  }
})

// 子组件引用
const editComponentRef = ref(null)

// 加载询价单数据
const loadInquiry = () => {
  if (editComponentRef.value) {
    editComponentRef.value.loadInquiry()
  }
}

// 处理保存成功
const handleSaved = () => {
  // 触发关闭当前Tab并刷新列表
  window.dispatchEvent(new CustomEvent('close-current-tab'))
  window.dispatchEvent(new CustomEvent('navigate-to', {
    detail: { key: 'product-inquiry-list' }
  }))
}

// 处理取消编辑
const handleCancelled = () => {
  // 触发关闭当前Tab
  window.dispatchEvent(new CustomEvent('close-current-tab'))
}

// 暴露方法给父组件调用
defineExpose({
  loadInquiry
})
</script>

<style scoped>
.product-inquiry-edit-tab {
  width: 100%;
  height: 100%;
}
</style>
