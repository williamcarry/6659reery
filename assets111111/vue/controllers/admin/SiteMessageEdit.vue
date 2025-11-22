<template>
  <div class="site-message-edit-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2 class="page-title">
        <el-icon class="title-icon"><Edit /></el-icon>
        编辑公告消息
      </h2>
      <div class="header-actions">
        <el-button @click="goBack" :icon="ArrowLeft">
          返回列表
        </el-button>
      </div>
    </div>
    
    <!-- 编辑表单 -->
    <el-card class="form-card" v-loading="loading">
      <el-form
        :model="form"
        :rules="rules"
        ref="formRef"
        label-position="right"
        label-width="120px"
        v-if="!loading"
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
              <el-button type="primary" @click="submitForm">提交</el-button>
            </div>
          </el-col>
        </el-row>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, defineProps } from 'vue'
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
  Edit,
  ArrowLeft
} from '@element-plus/icons-vue'

// 定义组件属性
const props = defineProps({
  adminLoginPath: {
    type: String,
    default: ''
  },
  message: {
    type: Object,
    default: () => ({})
  },
  // 添加 messageId 属性来接收消息ID
  messageId: {
    type: [String, Number],
    default: null
  },
  // 添加一个属性来控制是否自动加载数据
  autoLoad: {
    type: Boolean,
    default: false
  }
})

// 表单引用
const formRef = ref()

// 表单数据
const form = ref({
  id: null,
  title: '',
  titleEn: '',
  content: '',
  messageType: 'mall_announcement',
  priority: 'normal',
  isDraft: false,
  sendTime: null,
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

// 初始化表单数据
const initFormData = () => {
  if (props.message && props.message.id) {
    form.value = {
      id: props.message.id,
      title: props.message.title || '',
      titleEn: props.message.titleEn || '',
      content: props.message.content || '',
      messageType: props.message.messageType || 'mall_announcement',
      priority: props.message.priority || 'normal',
      isDraft: props.message.isDraft || false,
      sendTime: props.message.sendTime || null,
      recipientType: props.message.recipientType || ''
    }
  }
}

// 加载消息数据
const loadMessageData = async () => {
  console.log('loadMessageData called');
  console.log('props.message:', props.message);
  console.log('props.messageId:', props.messageId);
  
  if (props.message && props.message.id) {
    // 如果已经通过props传递了数据，直接使用
    console.log('使用props数据');
    initFormData()
  } else if (props.messageId) {
    // 如果通过messageId属性传递了ID，使用该ID加载数据
    console.log('使用props.messageId加载数据:', props.messageId);
    loading.value = true
    try {
      const url = `/admin${props.adminLoginPath}/site-message/${props.messageId}/edit/tab`
      console.log('正在请求:', url);
      
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      
      console.log('响应状态:', response.status);
      
      if (response.ok) {
        const result = await response.json()
        console.log('响应数据:', result);
        
        if (result.success && result.data) {
          form.value = {
            id: result.data.id,
            title: result.data.title || '',
            titleEn: result.data.titleEn || '',
            content: result.data.content || '',
            messageType: result.data.messageType || 'mall_announcement',
            priority: result.data.priority || 'normal',
            isDraft: result.data.isDraft || false,
            sendTime: result.data.sendTime || null,
            recipientType: result.data.recipientType || ''
          }
          console.log('表单数据已设置:', form.value);
        } else {
          ElMessage.error('获取数据失败: ' + (result.error || '未知错误'))
        }
      } else {
        ElMessage.error('请求失败: ' + response.statusText)
      }
    } catch (error) {
      console.error('加载数据错误:', error);
      ElMessage.error('加载数据失败: ' + error.message)
    } finally {
      loading.value = false
    }
  } else {
    // 否则从URL参数中获取ID并加载数据
    const urlParams = new URLSearchParams(window.location.search)
    const messageId = urlParams.get('id')
    
    console.log('URL参数 id:', messageId);
    
    if (messageId) {
      loading.value = true
      try {
        const url = `/admin${props.adminLoginPath}/site-message/${messageId}/edit/tab`
        console.log('正在请求:', url);
        
        const response = await fetch(url, {
          method: 'GET',
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          }
        })
        
        console.log('响应状态:', response.status);
        
        if (response.ok) {
          const result = await response.json()
          console.log('响应数据:', result);
          
          if (result.success && result.data) {
            form.value = {
              id: result.data.id,
              title: result.data.title || '',
              titleEn: result.data.titleEn || '',
              content: result.data.content || '',
              messageType: result.data.messageType || 'mall_announcement',
              priority: result.data.priority || 'normal',
              isDraft: result.data.isDraft || false,
              sendTime: result.data.sendTime || null,
              recipientType: result.data.recipientType || ''
            }
            console.log('表单数据已设置:', form.value);
          } else {
            ElMessage.error('获取数据失败: ' + (result.error || '未知错误'))
          }
        } else {
          ElMessage.error('请求失败: ' + response.statusText)
        }
      } catch (error) {
        console.error('加载数据错误:', error);
        ElMessage.error('加载数据失败: ' + error.message)
      } finally {
        loading.value = false
      }
    } else {
      console.log('没有消息ID，等待手动加载');
    }
  }
}

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid && form.value.id) {
      loading.value = true
      try {
        const formData = {
          title: form.value.title,
          titleEn: form.value.titleEn,
          content: form.value.content,
          messageType: form.value.messageType,
          priority: form.value.priority,
          isDraft: form.value.isDraft ? '1' : '0',
          sendTime: form.value.sendTime,
          recipientType: form.value.recipientType
        }
        
        const response = await fetch(`/admin${props.adminLoginPath}/site-message/${form.value.id}/update`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
          },
          body: JSON.stringify(formData)
        })
        
        const result = await response.json()
        
        if (result.success) {
          ElMessage.success(result.message || '更新成功')
          // 返回列表页面
          goBack()
        } else {
          ElMessage.error(result.error || '更新失败')
        }
      } catch (error) {
        ElMessage.error('更新失败: ' + error.message)
      } finally {
        loading.value = false
      }
    }
  })
}

// 重置表单
const resetForm = () => {
  initFormData()
}

// 返回列表
const goBack = () => {
  // 触发导航事件，返回公告消息列表
  window.dispatchEvent(new CustomEvent('navigate-to-site-message-list'))
}

// 组件挂载时加载数据
onMounted(() => {
  // 只有当 autoLoad 为 true 时才自动加载数据
  if (props.autoLoad) {
    loadMessageData()
  }
})

// 暴露方法给父组件调用
defineExpose({
  loadMessageData
})
</script>

<style scoped>
.site-message-edit-container {
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