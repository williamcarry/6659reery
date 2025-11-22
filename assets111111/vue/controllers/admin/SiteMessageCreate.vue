<template>
  <div class="site-message-create-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2 class="page-title">
        <el-icon class="title-icon"><Plus /></el-icon>
        添加公告消息
      </h2>
      <div class="header-actions">
        <el-button @click="goBack" :icon="ArrowLeft">
          返回列表
        </el-button>
      </div>
    </div>
    
    <!-- 创建表单 -->
    <el-card class="form-card">
      <el-form
        :model="form"
        :rules="rules"
        ref="formRef"
        label-position="right"
        label-width="120px"
        v-loading="loading"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="消息标题" prop="title">
              <el-input v-model="form.title" placeholder="请输入消息标题（中文）" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="英文标题" prop="titleEn">
              <el-input v-model="form.titleEn" placeholder="请输入英文标题" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="消息类型" prop="messageType">
              <el-select v-model="form.messageType" placeholder="请选择消息类型" style="width: 100%;">
                <el-option label="商城公告" value="mall_announcement" />
                <el-option label="平台消息" value="platform_message" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="优先级" prop="priority">
              <el-select v-model="form.priority" placeholder="请选择优先级" style="width: 100%;">
                <el-option label="低" value="low" />
                <el-option label="普通" value="normal" />
                <el-option label="高" value="high" />
                <el-option label="紧急" value="urgent" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="是否为草稿" prop="isDraft">
              <el-switch
                v-model="form.isDraft"
                active-text="是"
                inactive-text="否"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <!-- 新增：选择发送对象类型 -->
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="发送对象类型" prop="recipientType">
              <el-select v-model="form.recipientType" placeholder="请选择发送对象类型" clearable style="width: 100%;">
                <el-option label="全部用户" value="all" />
                <el-option label="供应商" value="supplier" />
                <el-option label="普通用户" value="customer" />
              </el-select>
              <div class="form-tip">选择"全部用户"时，消息将显示给所有供应商和普通用户</div>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="消息内容" prop="content">
              <RichTextEditor 
                v-model="form.content" 
                :admin-login-path="adminLoginPath"
                placeholder="请输入消息内容"
                height="400px"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="24">
            <div class="form-actions">
              <el-button @click="resetForm">重置</el-button>
              <el-button type="primary" @click="submitForm" :loading="loading">提交</el-button>
            </div>
          </el-col>
        </el-row>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, defineProps } from 'vue'
import RichTextEditor from './RichTextEditor.vue'
import {
  ElCard,
  ElForm,
  ElFormItem,
  ElInput,
  ElSelect,
  ElOption,
  ElSwitch,
  ElDatePicker,
  ElButton,
  ElRow,
  ElCol,
  ElIcon,
  ElMessage,
  vLoading
} from 'element-plus'
import {
  Plus,
  ArrowLeft
} from '@element-plus/icons-vue'

// 定义组件属性
const props = defineProps({
  adminLoginPath: {
    type: String,
    default: ''
  }
})

// 表单引用
const formRef = ref()

// 表单数据
const form = ref({
  title: '',
  titleEn: '',
  content: '',
  messageType: 'mall_announcement',
  priority: 'normal',
  isDraft: false,
  recipientType: ''
})

// 表单验证规则
const rules = {
  title: [
    { required: true, message: '请输入消息标题', trigger: 'blur' },
    { min: 1, max: 255, message: '长度在 1 到 255 个字符', trigger: 'blur' }
  ],
  titleEn: [
    { required: true, message: '请输入英文标题', trigger: 'blur' },
    { min: 1, max: 255, message: '长度在 1 到 255 个字符', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入消息内容', trigger: 'blur' }
  ],
  messageType: [
    { required: true, message: '请选择消息类型', trigger: 'change' }
  ],
  priority: [
    { required: true, message: '请选择优先级', trigger: 'change' }
  ],
  recipientType: [
    { required: false, message: '请选择发送对象类型', trigger: 'change' }
  ]
}

// 加载状态
const loading = ref(false)

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        const formData = {
          title: form.value.title,
          titleEn: form.value.titleEn,
          content: form.value.content,
          messageType: form.value.messageType,
          priority: form.value.priority,
          isDraft: form.value.isDraft ? '1' : '0',
          recipientType: form.value.recipientType
        }
        
        const response = await fetch(`/admin${props.adminLoginPath}/site-message/store`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
          },
          body: JSON.stringify(formData)
        })
        
        const result = await response.json()
        
        if (result.success) {
          ElMessage.success(result.message || '创建成功')
          // 重置表单
          resetForm()
          // 触发刷新列表事件
          window.dispatchEvent(new CustomEvent('refresh-site-message-list'))
          // 返回列表页面
          goBack()
        } else {
          ElMessage.error(result.error || '创建失败')
        }
      } catch (error) {
        ElMessage.error('创建失败: ' + error.message)
      } finally {
        loading.value = false
      }
    }
  })
}

// 重置表单
const resetForm = () => {
  form.value = {
    title: '',
    titleEn: '',
    content: '',
    messageType: 'mall_announcement',
    priority: 'normal',
    isDraft: false,
    recipientType: ''
  }
}

// 返回列表
const goBack = () => {
  // 触发导航事件，返回公告消息列表
  window.dispatchEvent(new CustomEvent('navigate-to-site-message-list'))
}
</script>

<style scoped>
.site-message-create-container {
  width: 100%;
  max-width: 2000px;
  box-sizing: border-box;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  width: 100%;
}

.page-title {
  font-size: 24px;
  font-weight: bold;
  margin: 0;
  display: flex;
  align-items: center;
}

.title-icon {
  margin-right: 10px;
  vertical-align: middle;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.form-card {
  width: 100%;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}
</style>