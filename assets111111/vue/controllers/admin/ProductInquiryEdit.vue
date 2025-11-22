<template>
  <div class="product-inquiry-edit-container">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <el-icon class="is-loading"><Loading /></el-icon>
      <p>加载中...</p>
    </div>
    
    <!-- 编辑表单 -->
    <el-card v-else-if="inquiry" class="edit-card">
      <!-- 头部操作栏 -->
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon"><Edit /></el-icon>
            <span class="header-title">编辑询价单</span>
          </div>
          <div class="header-right">
            <el-button @click="goBack">返回列表</el-button>
            <el-button type="primary" @click="saveInquiry" :loading="saving">保存</el-button>
          </div>
        </div>
      </template>
      
      <div class="edit-content">
      <!-- 客户信息（只读） -->
      <el-card class="info-card">
        <template #header>
          <span class="card-title">客户信息（只读）</span>
        </template>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="客户用户名">{{ inquiry.customerUsername }}</el-descriptions-item>
          <el-descriptions-item label="客户邮箱">{{ inquiry.customerEmail }}</el-descriptions-item>
          <el-descriptions-item label="联系人">{{ inquiry.contactName }}</el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ inquiry.contactPhone }}</el-descriptions-item>
          <el-descriptions-item label="询价数量">{{ inquiry.inquiryQuantity }}</el-descriptions-item>
          <el-descriptions-item label="提交时间">{{ inquiry.createdAt }}</el-descriptions-item>
        </el-descriptions>
      </el-card>
      
      <!-- 商品信息（只读） -->
      <el-card class="info-card">
        <template #header>
          <span class="card-title">商品信息（只读）</span>
        </template>
        <el-descriptions :column="1" border>
          <el-descriptions-item label="商品图片">
            <div class="product-image-wrapper" @click="openProductDetail">
              <img 
                :src="inquiry.productMainImage" 
                style="width: 100px; height: 100px; object-fit: cover; border-radius: 4px; cursor: pointer;"
                alt="商品图片"
              />
            </div>
          </el-descriptions-item>
          <el-descriptions-item label="商品标题">
            <span class="product-title-link" @click="openProductDetail">{{ inquiry.productTitle }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="商品SKU">{{ inquiry.productSku }}</el-descriptions-item>
          <el-descriptions-item label="需求描述">{{ inquiry.requirementDescription || '无' }}</el-descriptions-item>
        </el-descriptions>
      </el-card>
      
      <!-- 附件列表（只能下载，不能删除） -->
      <el-card class="info-card" v-if="inquiry.attachments && inquiry.attachments.length > 0">
        <template #header>
          <span class="card-title">附件列表 ({{ inquiry.attachments.length }})</span>
        </template>
        <div class="attachments-grid">
          <div 
            v-for="(attachment, index) in inquiry.attachments" 
            :key="index"
            class="attachment-card"
          >
            <!-- 图片附件 -->
            <div v-if="isImage(attachment.type, attachment.name)" class="attachment-content">
              <div class="attachment-preview" @click="showImageViewer([attachment.url])">
                <img 
                  :src="attachment.url" 
                  :alt="attachment.name"
                  class="preview-thumbnail"
                />
                <div class="image-overlay">
                  <el-icon :size="30"><ZoomIn /></el-icon>
                </div>
              </div>
              <div class="attachment-info">
                <p class="attachment-name" :title="attachment.name">{{ attachment.name }}</p>
                <el-button 
                  type="primary" 
                  size="small"
                  @click="downloadAttachment(attachment)"
                >
                  下载
                </el-button>
              </div>
            </div>
            
            <!-- 非图片附件 -->
            <div v-else class="attachment-content">
              <div class="attachment-preview file-preview">
                <el-icon :size="40"><Document /></el-icon>
              </div>
              <div class="attachment-info">
                <p class="attachment-name" :title="attachment.name">{{ attachment.name }}</p>
                <el-button 
                  type="primary" 
                  size="small"
                  @click="downloadAttachment(attachment)"
                >
                  下载
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </el-card>
      
      <!-- 报价信息（可编辑） -->
      <el-card class="info-card">
        <template #header>
          <span class="card-title">报价信息（可编辑 - 所有字段必填）</span>
        </template>
        <el-form :model="form" :rules="formRules" ref="formRef" label-width="100px">
          <el-form-item label="状态" prop="status">
            <el-select v-model="form.status" placeholder="请选择状态" style="width: 200px;">
              <el-option label="待处理" value="PENDING" />
              <el-option label="已完成" value="COMPLETED" />
            </el-select>
          </el-form-item>
          <el-form-item label="报价单价" prop="quotedPrice">
            <el-input 
              v-model="form.quotedPrice" 
              placeholder="请输入报价单价" 
              style="width: 200px;" 
              type="number"
              step="0.01"
            >
              <template #append>元</template>
            </el-input>
          </el-form-item>
          <el-form-item label="报价货币" prop="quotedCurrency">
            <el-select v-model="form.quotedCurrency" placeholder="请选择货币" style="width: 200px;">
              <el-option label="人民币" value="CNY" />
              <el-option label="美元" value="USD" />
              <el-option label="欧元" value="EUR" />
            </el-select>
          </el-form-item>
          <el-form-item label="报价总额" prop="quotedTotal">
            <el-input 
              v-model="form.quotedTotal" 
              placeholder="请输入报价总额" 
              style="width: 200px;" 
              type="number"
              step="0.01"
            >
              <template #append>元</template>
            </el-input>
          </el-form-item>
          <el-form-item label="报价备注" prop="quotedRemark">
            <el-input 
              v-model="form.quotedRemark" 
              type="textarea" 
              :rows="3"
              placeholder="请输入报价备注"
              style="width: 100%;"
            />
          </el-form-item>
        </el-form>
      </el-card>
      
      <!-- 底部按钮栏 -->
      <div class="bottom-actions">
        <el-button @click="goBack" size="large">返回</el-button>
        <el-button type="primary" @click="saveInquiry" :loading="saving" size="large">保存</el-button>
      </div>
    </div>
    </el-card>
    
    <!-- 图片查看器 -->
    <el-image-viewer
      v-if="imageViewerVisible"
      :url-list="imageViewerUrls"
      @close="closeImageViewer"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import {
  ElCard,
  ElButton,
  ElForm,
  ElFormItem,
  ElInput,
  ElSelect,
  ElOption,
  ElMessage,
  ElIcon,
  ElDescriptions,
  ElDescriptionsItem,
  ElImage,
  ElImageViewer
} from 'element-plus'
import {
  Edit,
  Loading,
  Document,
  ZoomIn
} from '@element-plus/icons-vue'

// 定义组件属性
const props = defineProps({
  adminLoginPath: {
    type: String,
    default: ''
  },
  inquiryId: {
    type: Number,
    required: true
  },
  isTabMode: {
    type: Boolean,
    default: false
  }
})

// 定义事件
const emit = defineEmits(['saved', 'cancelled'])

// 定义响应式数据
const loading = ref(false)
const saving = ref(false)
const inquiry = ref(null)
const formRef = ref(null)
const form = ref({
  status: '',
  quotedPrice: '',
  quotedCurrency: 'CNY',
  quotedTotal: '',
  quotedRemark: ''
})

// 表单验证规则
const formRules = {
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ],
  quotedPrice: [
    { required: true, message: '请输入报价单价', trigger: 'blur' },
    { 
      validator: (rule, value, callback) => {
        if (!value || value <= 0) {
          callback(new Error('报价单价必须大于0'))
        } else {
          callback()
        }
      }, 
      trigger: 'blur' 
    }
  ],
  quotedCurrency: [
    { required: true, message: '请选择报价货币', trigger: 'change' }
  ],
  quotedTotal: [
    { required: true, message: '请输入报价总额', trigger: 'blur' },
    { 
      validator: (rule, value, callback) => {
        if (!value || value <= 0) {
          callback(new Error('报价总额必须大于0'))
        } else {
          callback()
        }
      }, 
      trigger: 'blur' 
    }
  ],
  quotedRemark: [
    { required: true, message: '请输入报价备注', trigger: 'blur' },
    { min: 5, message: '报价备注至少输入5个字符', trigger: 'blur' }
  ]
}

// 图片查看器相关
const imageViewerVisible = ref(false)
const imageViewerUrls = ref([])

// 判断是否为图片
const isImage = (type, name) => {
  if (type && type.startsWith('image/')) return true
  if (name) {
    const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg']
    const lowerName = name.toLowerCase()
    return imageExtensions.some(ext => lowerName.endsWith(ext))
  }
  return false
}

// 加载询价单详情
const loadInquiry = async () => {
  loading.value = true
  try {
    const url = `/admin${props.adminLoginPath}/product-inquiry/detail/${props.inquiryId}`
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    
    const result = await response.json()
    
    if (result.success) {
      inquiry.value = result.data
      // 初始化表单数据
      form.value = {
        status: result.data.status || 'PENDING',
        quotedPrice: result.data.quotedPrice || '',
        quotedCurrency: result.data.quotedCurrency || 'CNY',
        quotedTotal: result.data.quotedTotal || '',
        quotedRemark: result.data.quotedRemark || ''
      }
    } else {
      ElMessage.error(result.message || '加载数据失败')
    }
  } catch (error) {
    ElMessage.error('加载数据失败: ' + error.message)
  } finally {
    loading.value = false
  }
}

// 保存询价单
const saveInquiry = async () => {
  // 验证表单
  if (!formRef.value) {
    ElMessage.error('表单未初始化')
    return
  }
  
  try {
    await formRef.value.validate()
  } catch (error) {
    ElMessage.error('请正确填写所有必填项')
    return
  }
  
  saving.value = true
  try {
    const url = `/admin${props.adminLoginPath}/product-inquiry/update/${props.inquiryId}`
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: JSON.stringify(form.value)
    })
    
    const result = await response.json()
    
    if (result.success) {
      ElMessage.success('保存成功')
      
      if (props.isTabMode) {
        // Tab模式：触发保存事件
        emit('saved')
      } else {
        // 独立页面模式：通知父窗口刷新数据
        if (window.opener && !window.opener.closed) {
          try {
            window.opener.postMessage({ type: 'INQUIRY_UPDATED' }, window.location.origin)
          } catch (e) {
            console.error('Failed to notify parent window:', e)
          }
        }
        // 延迟关闭当前标签页或跳转回列表
        setTimeout(() => {
          if (window.opener) {
            window.close()
          } else {
            window.location.href = `/admin${props.adminLoginPath}/product-inquiry`
          }
        }, 1000)
      }
    } else {
      ElMessage.error(result.message || '保存失败')
    }
  } catch (error) {
    ElMessage.error('保存失败: ' + error.message)
  } finally {
    saving.value = false
  }
}

// 返回列表
const goBack = () => {
  if (props.isTabMode) {
    // Tab模式：触发取消事件
    emit('cancelled')
  } else {
    // 独立页面模式：尝试关闭窗口，如果无法关闭则跳转回列表页
    if (window.opener) {
      window.close()
    } else {
      window.location.href = `/admin${props.adminLoginPath}/product-inquiry`
    }
  }
}

// 打开商品详情
const openProductDetail = () => {
  if (inquiry.value && inquiry.value.productId) {
    window.open(`/shop/item/${inquiry.value.productId}`, '_blank')
  }
}

// 显示图片查看器
const showImageViewer = (urls) => {
  imageViewerUrls.value = urls
  imageViewerVisible.value = true
}

// 关闭图片查看器
const closeImageViewer = () => {
  imageViewerVisible.value = false
  imageViewerUrls.value = []
}

// 下载附件
const downloadAttachment = (attachment) => {
  try {
    const a = document.createElement('a')
    a.href = attachment.url
    a.download = attachment.name
    a.target = '_blank'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
  } catch (error) {
    console.error('Download failed:', error)
    ElMessage.error('下载失败')
  }
}

// 监听窗口关闭前事件
const handleBeforeUnload = (e) => {
  // 这里可以添加未保存警告
}

// 组件挂载
onMounted(() => {
  // 如果不是Tab模式（独立页面模式），则自动加载数据
  if (!props.isTabMode) {
    loadInquiry()
  }
  window.addEventListener('beforeunload', handleBeforeUnload)
})

// 组件卸载
onBeforeUnmount(() => {
  window.removeEventListener('beforeunload', handleBeforeUnload)
})

// 暴露方法给父组件
defineExpose({
  loadInquiry
})
</script>

<style scoped>
.product-inquiry-edit-container {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100px 0;
  font-size: 16px;
  color: #909399;
  background-color: #fff;
  border-radius: 8px;
  min-height: 400px;
}

.loading-container .el-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.edit-card {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-icon {
  font-size: 20px;
  color: #409eff;
}

.header-title {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
}

.header-right {
  display: flex;
  gap: 10px;
}

.edit-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px 0;
}

.info-card {
  width: 100%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.card-title {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
}

.product-title-link {
  color: #409eff;
  cursor: pointer;
  text-decoration: underline;
}

.product-title-link:hover {
  color: #66b1ff;
}

.product-image-wrapper {
  display: inline-block;
  cursor: pointer;
  transition: transform 0.3s;
}

.product-image-wrapper:hover {
  transform: scale(1.05);
}

/* 附件列表样式 */
.attachments-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.attachment-card {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 12px;
  transition: all 0.3s;
  background-color: #fff;
}

.attachment-card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-color: #409eff;
}

.attachment-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.attachment-preview {
  width: 100%;
  height: 120px;
  overflow: hidden;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f7fa;
  cursor: pointer;
  transition: transform 0.3s;
  position: relative;
}

.attachment-preview:hover {
  transform: scale(1.05);
}

.attachment-preview:hover .image-overlay {
  opacity: 1;
}

.preview-thumbnail {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
  color: #fff;
}

.file-preview {
  background-color: #f5f7fa;
  color: #909399;
}

.attachment-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.attachment-name {
  font-size: 13px;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin: 0;
}

/* 底部按钮栏样式 */
.bottom-actions {
  position: sticky;
  bottom: 0;
  right: 0;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 12px;
  padding: 20px;
  background-color: #fff;
  border-top: 1px solid #e5e7eb;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1);
  margin-top: 30px;
  border-radius: 0 0 8px 8px;
}

.bottom-actions .el-button {
  min-width: 100px;
}
</style>
