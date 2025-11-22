<template>
  <div class="file-upload">
    <el-upload
      class="file-uploader"
      action=""
      :auto-upload="false"
      :show-file-list="false"
      :on-change="handleFileChange"
      :before-upload="beforeFileUpload"
      :accept="accept"
    >
      <img v-if="previewImageUrl && isImage" :src="previewImageUrl" class="file-image-preview" />
      <div v-else-if="previewImageUrl && !isImage" class="file-preview">
        <el-icon class="file-icon"><Document /></el-icon>
        <span class="file-name">{{ fileName }}</span>
      </div>
      <el-icon v-else class="uploader-icon">
        <Plus />
      </el-icon>
    </el-upload>
    
    <div v-if="uploadProgress > 0 && uploadProgress < 100" class="upload-progress">
      <el-progress :percentage="uploadProgress" />
    </div>
    
    <div v-if="uploadError" class="upload-error">
      {{ uploadError }}
    </div>
    
    <div v-if="previewImageUrl && showRemove" class="remove-button">
      <el-button type="danger" size="small" @click="removeFile">移除</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed, defineProps, defineEmits } from 'vue'
import { ElUpload, ElIcon, ElProgress, ElButton, ElMessage } from 'element-plus'
import { Plus, Document } from '@element-plus/icons-vue'

// 定义 props
const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  adminLoginPath: {
    type: String,
    default: ''
  },
  accept: {
    type: String,
    default: 'image/*'  // 默认只接受图片
  },
  maxSize: {
    type: Number,
    default: 5  // 默认5MB
  },
  showRemove: {
    type: Boolean,
    default: true
  },
  endpointType: {
    type: String,
    default: 'supplier'  // 默认使用供应商接口，可选 'supplier'、'member'、'site-config'、'product'、'product-main'
  }
})

// 定义 emits
const emit = defineEmits(['update:modelValue', 'upload-success', 'upload-error', 'remove'])

// 响应式数据
const fileKey = ref(props.modelValue)  // 存储七牛云的key
const previewImageUrl = ref('')  // 用于显示的预览URL
const uploadProgress = ref(0)
const uploadError = ref('')
const fileName = ref('')
const isUploading = ref(false)  // 标记是否正在上传，避免重复调用签名URL接口
const isUploadSuccess = ref(false)  // 标记是否是上传成功后设置的key

// 计算属性
const isImage = computed(() => {
  // 如果有预览URL，基于预览URL判断是否为图片
  if (previewImageUrl.value) {
    // 检查预览URL是否为图片URL
    const url = previewImageUrl.value.toLowerCase();
    const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'];
    // 检查URL路径部分是否以图片扩展名结尾（忽略查询参数）
    const urlPath = url.split('?')[0]; // 移除查询参数
    return imageExtensions.some(ext => urlPath.endsWith(ext));
  }
  
  // 如果没有预览URL，基于fileKey判断
  if (!fileKey.value) return false
  const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']
  return imageExtensions.some(ext => fileKey.value.toLowerCase().endsWith(ext))
})

// 获取签名URL（用于显示已存储的文件）
const fetchSignedUrl = async (key) => {
  // 完全移除签名URL API调用，直接使用previewUrl
  console.log('[FileUpload] fetchSignedUrl disabled for key:', key);
  previewImageUrl.value = ''
}

// 监听 modelValue 变化
watch(() => props.modelValue, (newVal) => {
  // modelValue changed
  
  // 如果已经有预览图片（上传成功后设置的），跳过
  if (previewImageUrl.value) {
    return
  }
  
  // 如果是上传成功后设置的key，跳过（上传成功后会直接使用 previewUrl）
  if (isUploadSuccess.value) {
    isUploadSuccess.value = false; // 重置标志
    return
  }
  
  // 如果正在上传，跳过（上传成功后会直接使用 previewUrl）
  if (isUploading.value) {
    return
  }
  
  // 如果值为空，清除预览
  if (!newVal) {
    previewImageUrl.value = ''
    return
  }
  
  // 如果是完整的URL（如previewUrl或签名URL），直接使用
  if (newVal.startsWith('http')) {
    previewImageUrl.value = newVal
    return
  }
  
  // 对于key值，不再调用签名URL接口，保持空白
  // 因为新添加的详情图会通过previewUrl传递完整URL
  previewImageUrl.value = ''
}, { immediate: true })

// 文件选择处理
const handleFileChange = (file) => {
  // 验证文件类型
  const fileType = file.raw.type
  const fileOriginalName = file.raw.name
  const fileExtension = '.' + fileOriginalName.split('.').pop().toLowerCase()
  
  // 检查文件类型是否符合accept属性要求
  const acceptTypes = props.accept.split(',').map(type => type.trim())
  let isValidType = false
  
  for (const acceptType of acceptTypes) {
    if (acceptType === '*/*' || acceptType === '') {
      isValidType = true
      break
    }
    
    if (acceptType.endsWith('/*')) {
      // 例如 image/* 匹配 image/png, image/jpeg 等
      const mainType = acceptType.slice(0, -2)
      if (fileType.startsWith(mainType)) {
        isValidType = true
        break
      }
    } else if (acceptType.startsWith('.')) {
      // 例如 .jpg, .png 匹配文件扩展名
      if (fileExtension === acceptType.toLowerCase()) {
        isValidType = true
        break
      }
    } else {
      // 例如 image/png 匹配完整MIME类型
      if (fileType === acceptType) {
        isValidType = true
        break
      }
    }
  }
  
  if (!isValidType) {
    ElMessage.error(`文件类型不支持，请上传符合要求的文件!`)
    return false
  }
  
  // 验证文件大小
  const maxSizeInBytes = props.maxSize * 1024 * 1024
  const isLtMaxSize = file.raw.size < maxSizeInBytes
  if (!isLtMaxSize) {
    ElMessage.error(`文件大小不能超过 ${props.maxSize}MB!`)
    return false
  }
  
  // 保存文件名
  fileName.value = fileOriginalName
  
  // 预览文件并验证图片尺寸
  if (fileType.startsWith('image/')) {
    const imageUrl = URL.createObjectURL(file.raw)
    previewImageUrl.value = imageUrl
    
    // 对于商品相关的图片，验证最小尺寸为600x600
    if (props.endpointType === 'product' || props.endpointType === 'product-main') {
      const img = new Image()
      img.onload = () => {
        if (img.width < 600 || img.height < 600) {
          ElMessage.error(`图片尺寸不能小于600x600，当前尺寸为${img.width}x${img.height}`)
          previewImageUrl.value = ''
          URL.revokeObjectURL(imageUrl)
          return
        }
        
        // 对于商品主图，额外验证是否为正方形
        if (props.endpointType === 'product-main') {
          if (img.width !== img.height) {
            ElMessage.error('主图必须是正方形图片，请重新选择!')
            previewImageUrl.value = ''
            URL.revokeObjectURL(imageUrl)
            return
          }
        }
        
        // 尺寸验证通过，继续上传
        uploadFileToQiniu(file.raw)
      }
      img.onerror = () => {
        ElMessage.error('图片加载失败，请重新选择')
        previewImageUrl.value = ''
        URL.revokeObjectURL(imageUrl)
      }
      img.src = imageUrl
      return true // 异步验证，先返回true
    } else {
      // 非商品图片，直接上传
      uploadFileToQiniu(file.raw)
    }
  } else {
    previewImageUrl.value = ''  // 非图片文件不预览
    uploadFileToQiniu(file.raw)
  }
  
  return true
}

// 上传前验证
const beforeFileUpload = (rawFile) => {
  // 这个函数会在 handleFileChange 之前执行，但我们已经在 handleFileChange 中处理了验证
  return false // 阻止自动上传，我们手动处理
}

// 上传文件到七牛云
const uploadFileToQiniu = async (file) => {
  try {
    isUploading.value = true  // 标记开始上传
    uploadProgress.value = 10
    uploadError.value = ''
    
    // 创建 FormData
    const formData = new FormData()
    formData.append('file', file)
    
    // 管理员后台 - 根据endpointType选择接口
    const loginPath = props.adminLoginPath || window.adminLoginPath || ''
    let uploadUrl = ''
    if (props.endpointType === 'member') {
      uploadUrl = `/admin${loginPath}/member/upload-file`
    } else if (props.endpointType === 'site-config') {
      uploadUrl = `/admin${loginPath}/site-config/upload-file`
    } else if (props.endpointType === 'public-resource') {
      uploadUrl = `/admin${loginPath}/public-resource/upload-image`
    } else {
      uploadUrl = `/admin${loginPath}/supplier/upload-file`
    }
    
    console.log('[FileUpload] Uploading to:', uploadUrl)
    console.log('[FileUpload] File info:', { name: file.name, type: file.type, size: file.size })
    
    // 上传到服务器
    uploadProgress.value = 30
    const response = await fetch(uploadUrl, {
      method: 'POST',
      body: formData,
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    
    console.log('[FileUpload] Response status:', response.status)
    console.log('[FileUpload] Response headers:', response.headers.get('content-type'))
    
    // 检查响应类型
    const contentType = response.headers.get('content-type')
    if (!contentType || !contentType.includes('application/json')) {
      // 响应不是JSON，可能是HTML错误页面
      const text = await response.text()
      console.error('[FileUpload] Non-JSON response:', text.substring(0, 500))
      
      // 检查是否是登录页面（包含登录表单）
      if (text.includes('login-form') || text.includes('登录')) {
        throw new Error('请先登录管理后台再进行文件上传操作')
      }
      
      throw new Error('服务器返回了非JSON响应，可能是权限错误或路径错误。状态码: ' + response.status)
    }
    
    uploadProgress.value = 70
    const result = await response.json()
    console.log('[FileUpload] Upload result:', result)
    
    // 处理特定的错误状态码
    if (response.status === 401) {
      throw new Error('请先登录管理后台再进行文件上传操作')
    }
    
    if (response.status === 403) {
      throw new Error('没有权限进行文件上传操作')
    }
    
    if (!result.success) {
      throw new Error(result.error || '上传失败')
    }
    
    // 上传成功
    if (result.success) {
      // 使用previewUrl立即显示图片（不需要再调用签名URL接口）
      console.log('[FileUpload] Upload success, using previewUrl:', result.previewUrl);
      if (result.previewUrl) {
        previewImageUrl.value = result.previewUrl
      } else if (result.url) {
        // 兼容旧版本返回的url字段
        previewImageUrl.value = result.url
      } else {
        // 如果都没有，使用key（但这可能不会正确显示）
        previewImageUrl.value = result.key || ''
      }
      
      uploadProgress.value = 100
      fileKey.value = result.key  // 这是key，不是完整URL
      console.log('[FileUpload] Stored key:', result.key)
      isUploadSuccess.value = true; // 设置标志，表示这是上传成功后设置的key
      emit('update:modelValue', result.key)  // 发送key给父组件
      emit('upload-success', result)
      // 移除通用的成功提示，由父组件根据具体场景显示更合适的提示
      // ElMessage.success('文件上传成功!')
    } else {
      throw new Error(result.error || '上传失败')
    }
  } catch (error) {
    console.error('[FileUpload] Upload error:', error)
    uploadProgress.value = 0
    uploadError.value = error.message || '上传失败，请稍后重试'
    
    // 特别处理商品主图非正方形的情况
    if (props.endpointType === 'product-main' && error.message && error.message.includes('正方形')) {
      ElMessage.error('主图必须是正方形图片，请重新选择!')
    } else {
      ElMessage.error(uploadError.value)
    }
    
    emit('upload-error', error)
  } finally {
    // 重置进度条和上传标记
    setTimeout(() => {
      uploadProgress.value = 0
      isUploading.value = false
    }, 1000)
  }
}

// 移除文件
const removeFile = () => {
  fileKey.value = ''
  previewImageUrl.value = ''
  fileName.value = ''
  uploadProgress.value = 0
  uploadError.value = ''
  isUploadSuccess.value = true; // 设置标志，表示这是移除操作
  emit('update:modelValue', '')
  emit('remove')
}

// 暴露方法给父组件
defineExpose({
  clearFile() {
    removeFile()
  }
})
</script>

<style scoped>
.file-upload {
  display: inline-block;
}

.file-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: border-color 0.3s;
  width: 178px;
  height: 178px;
}

.file-uploader:hover {
  border-color: #409eff;
}

.file-image-preview {
  width: 178px;
  height: 178px;
  display: block;
  object-fit: cover;
}

.file-preview {
  width: 178px;
  height: 178px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #f5f7fa;
}

.file-icon {
  font-size: 48px;
  color: #909399;
  margin-bottom: 10px;
}

.file-name {
  font-size: 12px;
  color: #606266;
  text-align: center;
  padding: 0 10px;
  word-break: break-all;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.uploader-icon {
  font-size: 28px;
  color: #8c9399;
  width: 178px;
  height: 178px;
  text-align: center;
  line-height: 178px;
}

.upload-progress {
  margin-top: 10px;
}

.upload-error {
  color: #f56c6c;
  font-size: 12px;
  margin-top: 5px;
}

.remove-button {
  margin-top: 10px;
  text-align: center;
}
</style>