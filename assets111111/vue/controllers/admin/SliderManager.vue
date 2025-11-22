<template>
  <div class="slider-manager">
    <!-- 页面标题和添加按钮 -->
    <div class="header-section">
      <h2>首页轮播图管理</h2>
      <el-button type="primary" @click="showUploadDialog" size="large">
        <el-icon><Plus /></el-icon>
        添加轮播图
      </el-button>
    </div>

    <!-- 轮播图列表 -->
    <div class="content-section" v-loading="loading">
      <div v-if="sliders.length > 0" class="slider-list">
        <div v-for="slider in sliders" :key="slider.name" class="slider-item">
          <!-- 图片预览（左侧） -->
          <div class="image-preview">
            <el-image
              :src="getImageUrl(slider)"
              :alt="slider.name"
              fit="contain"
              class="preview-img"
              :preview-src-list="[getImageUrl(slider)]"
              :z-index="9999"
            >
              <template #placeholder>
                <div class="image-slot">
                  <el-icon><Picture /></el-icon>
                </div>
              </template>
              <template #error>
                <div class="image-slot">
                  <el-icon><PictureFilled /></el-icon>
                </div>
              </template>
            </el-image>
            <div class="image-info">
              <p class="image-name" :title="slider.name">{{ slider.name }}</p>
              <p class="image-meta">
                <span>{{ slider.extension.toUpperCase() }}</span>
                <span class="divider">|</span>
                <span>{{ formatFileSize(slider.size) }}</span>
              </p>
            </div>
          </div>

          <!-- 操作按钮区域 -->
          <div class="action-section">
            <el-upload
              :action="uploadUrl"
              :data="{ originalFileName: slider.name }"
              :headers="{ 'X-Requested-With': 'XMLHttpRequest' }"
              :before-upload="(file) => beforeUpload(file, slider)"
              :on-success="(response) => handleReplaceSuccess(response, slider)"
              :on-error="handleUploadError"
              :show-file-list="false"
              accept="image/*"
              class="upload-component"
            >
              <el-button type="primary">
                <el-icon><Upload /></el-icon>
                上传替换
              </el-button>
            </el-upload>
            
            <el-button type="danger" @click="deleteSlider(slider)">
              <el-icon><Delete /></el-icon>
              删除
            </el-button>
          </div>
        </div>
      </div>
      
      <el-empty v-else description="暂无轮播图，点击右上角添加" />
    </div>

    <!-- 添加轮播图对话框 -->
    <el-dialog
      v-model="uploadDialogVisible"
      title="添加轮播图"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-upload
        ref="uploadRef"
        :action="newUploadUrl"
        :headers="{ 'X-Requested-With': 'XMLHttpRequest' }"
        :before-upload="beforeNewUpload"
        :on-success="handleNewUploadSuccess"
        :on-error="handleUploadError"
        :auto-upload="true"
        accept="image/*"
        drag
        class="upload-dragger"
      >
        <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
        <div class="el-upload__text">
          将图片拖到此处，或<em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            支持 JPG、PNG、GIF、WEBP 格式，文件大小不超过10MB
          </div>
        </template>
      </el-upload>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  ElButton,
  ElImage,
  ElUpload,
  ElDialog,
  ElDivider,
  ElEmpty,
  ElMessage,
  ElMessageBox,
  ElIcon,
  vLoading
} from 'element-plus'
import {
  Plus,
  Upload,
  UploadFilled,
  Delete,
  Picture,
  PictureFilled
} from '@element-plus/icons-vue'

const props = defineProps({
  adminLoginPath: {
    type: String,
    required: true
  },
  autoLoad: {
    type: Boolean,
    default: true
  }
})

const sliders = ref([])
const loading = ref(false)
const uploadDialogVisible = ref(false)
const uploadRef = ref(null)
// 为每个图片维护独立的时间戳，用于破坏浏览器缓存
const imageTimestamps = ref({})

const uploadUrl = computed(() => {
  return `/admin${props.adminLoginPath}/slider/replace`
})

const newUploadUrl = computed(() => {
  return `/admin${props.adminLoginPath}/slider/upload`
})

// 获取带时间戳的图片URL，破坏浏览器缓存
const getImageUrl = (slider) => {
  if (!slider.path) return ''
  const timestamp = imageTimestamps.value[slider.name] || Date.now()
  return `${slider.path}?t=${timestamp}`
}

// 加载轮播图列表
const loadSliders = async () => {
  loading.value = true
  try {
    const response = await fetch(`/admin${props.adminLoginPath}/slider/list`, {
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    
    const data = await response.json()
    if (data.success) {
      sliders.value = data.data
      // 初始化每个图片的时间戳
      data.data.forEach(slider => {
        if (!imageTimestamps.value[slider.name]) {
          imageTimestamps.value[slider.name] = Date.now()
        }
      })
    } else {
      ElMessage.error(data.message || '加载轮播图列表失败')
    }
  } catch (error) {
    console.error('加载轮播图列表失败:', error)
    ElMessage.error('加载轮播图列表失败')
  } finally {
    loading.value = false
  }
}

// 显示上传对话框
const showUploadDialog = () => {
  uploadDialogVisible.value = true
}

// 上传前验证（替换）
const beforeUpload = (file, slider) => {
  const isImage = file.type.startsWith('image/')
  const isLt10M = file.size / 1024 / 1024 < 10

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt10M) {
    ElMessage.error('图片大小不能超过10MB!')
    return false
  }
  return true
}

// 上传前验证（新增）
const beforeNewUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt10M = file.size / 1024 / 1024 < 10

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt10M) {
    ElMessage.error('图片大小不能超过10MB!')
    return false
  }
  return true
}

// 替换成功
const handleReplaceSuccess = (response, slider) => {
  if (response.success) {
    ElMessage.success('替换成功')
    // 只更新被替换图片的时间戳
    imageTimestamps.value[slider.name] = Date.now()
    // 更新该图片的信息（如果后端返回了新的文件信息）
    if (response.data) {
      const index = sliders.value.findIndex(s => s.name === slider.name)
      if (index !== -1) {
        sliders.value[index] = { ...sliders.value[index], ...response.data }
      }
    }
  } else {
    ElMessage.error(response.message || '替换失败')
  }
}

// 新增成功
const handleNewUploadSuccess = (response) => {
  if (response.success) {
    ElMessage.success('上传成功')
    uploadDialogVisible.value = false
    // 重新加载列表以显示新图片
    loadSliders()
  } else {
    ElMessage.error(response.message || '上传失败')
  }
}

// 上传失败
const handleUploadError = (error) => {
  console.error('上传失败:', error)
  ElMessage.error('上传失败，请重试')
}

// 删除轮播图
const deleteSlider = async (slider) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除轮播图 "${slider.name}" 吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    const response = await fetch(`/admin${props.adminLoginPath}/slider/delete`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: JSON.stringify({
        fileName: slider.name
      })
    })

    const data = await response.json()
    if (data.success) {
      ElMessage.success('删除成功')
      loadSliders()
    } else {
      ElMessage.error(data.message || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 格式化文件大小
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return (bytes / Math.pow(k, i)).toFixed(2) + ' ' + sizes[i]
}

onMounted(() => {
  // 实现按需加载
  if (props.autoLoad) {
    loadSliders()
  }
})

// 暴露方法供父组件调用
defineExpose({
  loadSliders
})
</script>

<style scoped>
.slider-manager {
  padding: 20px;
  background: #f5f7fa;
  min-height: calc(100vh - 60px);
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 16px 24px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
}

.header-section h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

.content-section {
  background: #fff;
  border-radius: 8px;
  padding: 24px;
  min-height: 400px;
}

.slider-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.slider-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 24px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  background: #fafafa;
  transition: box-shadow 0.3s;
}

.slider-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.image-preview {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.image-preview .preview-img {
  width: 100%;
  max-width: 500px;
  height: 250px;
  border-radius: 6px;
  border: 1px solid #dcdfe6;
  background: #fff;
  cursor: pointer;
}

.image-preview .image-slot {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background: #f5f7fa;
  color: #909399;
  font-size: 30px;
}

.image-preview .image-info {
  text-align: center;
  width: 100%;
  max-width: 500px;
}

.image-preview .image-info .image-name {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  margin: 0 0 4px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.image-preview .image-info .image-meta {
  font-size: 12px;
  color: #909399;
  margin: 0;
}

.image-preview .image-info .image-meta .divider {
  margin: 0 8px;
}

.action-section {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
}

.action-section .upload-component {
  flex-shrink: 0;
}

.upload-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.upload-section .upload-component {
  width: 100%;
}

.upload-section .upload-hint {
  font-size: 12px;
  color: #909399;
  margin: 0;
  text-align: center;
}

.button-group {
  display: flex;
  gap: 12px;
}

.upload-dragger {
  width: 100%;
}

.upload-dragger :deep(.el-upload) {
  width: 100%;
}

.upload-dragger :deep(.el-upload-dragger) {
  padding: 40px;
}

.upload-dragger .el-icon--upload {
  font-size: 67px;
  color: #c0c4cc;
  margin-bottom: 16px;
}

.upload-dragger .el-upload__text {
  color: #606266;
  font-size: 14px;
}

.upload-dragger .el-upload__text em {
  color: #409eff;
  font-style: normal;
}

.upload-dragger :deep(.el-upload__tip) {
  font-size: 12px;
  color: #909399;
  margin-top: 8px;
}

.replace-dialog-content .current-image {
  text-align: center;
  margin-bottom: 20px;
}

.replace-dialog-content .current-image .label {
  font-size: 14px;
  font-weight: 500;
  color: #606266;
  margin-bottom: 12px;
}

.replace-dialog-content .current-image .current-preview {
  width: 100%;
  max-height: 200px;
  border-radius: 6px;
  border: 1px solid #dcdfe6;
}

.replace-dialog-content .current-image .current-name {
  font-size: 13px;
  color: #909399;
  margin-top: 8px;
  word-break: break-all;
}
</style>
