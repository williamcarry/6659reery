<template>
  <div class="file-upload">
    <el-upload
      class="file-uploader"
      :auto-upload="false"
      :show-file-list="false"
      :on-change="handleFileChange"
      :accept="accept"
    >
      <img v-if="previewImageUrl" :src="previewImageUrl" class="file-image-preview" />
      <el-icon v-else class="uploader-icon"><Plus /></el-icon>
    </el-upload>
    
    <div v-if="uploadProgress > 0 && uploadProgress < 100" class="upload-progress">
      <el-progress :percentage="uploadProgress" />
    </div>
    
    <div v-if="previewImageUrl && showRemove" class="remove-button">
      <el-button type="danger" size="small" @click="removeFile">移除</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { ElUpload, ElIcon, ElProgress, ElButton, ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

// 定义 props
const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  supplierLoginPath: {
    type: String,
    required: true
  },
  accept: {
    type: String,
    default: 'image/*'
  },
  maxSize: {
    type: Number,
    default: 5
  },
  showRemove: {
    type: Boolean,
    default: true
  },
  // 'product-main': 主图上传（验证正方形）
  // 'product': 详情图上传（无需验证正方形）
  endpointType: {
    type: String,
    default: 'product',
    validator: (value) => ['product', 'product-main'].includes(value)
  }
})

// 定义 emits
const emit = defineEmits(['update:modelValue', 'upload-success', 'upload-error', 'remove'])

// 响应式数据
const previewImageUrl = ref('')
const uploadProgress = ref(0)
const isUploading = ref(false)  // 标记是否正在上传，避免重复调用签名URL接口
const isUploadSuccess = ref(false)  // 标记是否是上传成功后设置的key

// 获取签名URL（仅用于编辑时加载已存储的图片）
const fetchSignedUrl = async (key) => {
  // 完全移除签名URL API调用
  previewImageUrl.value = ''
}

// 专门用于处理编辑时加载已存储图片的方法
const loadExistingImage = (key) => {
  // 完全移除签名URL API调用
  previewImageUrl.value = ''
}

// 监听 modelValue 变化 - 只用于编辑时从数据库加载已有图片
// 上传新图片时，直接使用后端返回的 previewUrl，不需要调用签名URL接口
watch(() => props.modelValue, (newVal) => {
  // 如果值为空（null、undefined或空字符串），强制清除预览
  if (!newVal) {
    previewImageUrl.value = ''
    return
  }
  
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
  
  // 如果是完整的URL（如previewUrl或签名URL），直接使用
  if (newVal.startsWith('http')) {
    previewImageUrl.value = newVal
    return
  }
  
  // 对于key值，不再调用签名URL接口，保持空白
  // 因为新添加的详情图会通过previewUrl传递完整URL
  previewImageUrl.value = ''
}, { immediate: true })

// 图片尺寸验证
const validateImageDimensions = (file) => {
  return new Promise((resolve, reject) => {
    const img = new Image()
    const imageUrl = URL.createObjectURL(file)
    
    img.onload = () => {
      URL.revokeObjectURL(imageUrl)
      
      // 验证最小尺寸600x600
      if (img.width < 600 || img.height < 600) {
        reject(`图片尺寸不能小于600×600，当前尺寸为${img.width}×${img.height}`)
        return
      }
      
      // 主图必须是正方形
      if (props.endpointType === 'product-main' && img.width !== img.height) {
        reject('主图必须是正方形图片，请重新选择！')
        return
      }
      
      resolve({ width: img.width, height: img.height })
    }
    
    img.onerror = () => {
      URL.revokeObjectURL(imageUrl)
      reject('图片加载失败，请重新选择')
    }
    
    img.src = imageUrl
  })
}

// 文件选择处理
const handleFileChange = async (file) => {
  const rawFile = file.raw
  
  // 验证文件大小
  const maxSizeInBytes = props.maxSize * 1024 * 1024
  if (rawFile.size > maxSizeInBytes) {
    ElMessage.error(`文件大小不能超过${props.maxSize}MB！`)
    return
  }
  
  // 验证文件类型
  if (!rawFile.type.startsWith('image/')) {
    ElMessage.error('请上传图片文件！')
    return
  }
  
  // 先显示预览
  const imageUrl = URL.createObjectURL(rawFile)
  previewImageUrl.value = imageUrl
  
  try {
    // 验证图片尺寸
    await validateImageDimensions(rawFile)
    
    // 验证通过，开始上传
    uploadFileToQiniu(rawFile)
  } catch (error) {
    // 验证失败，清除预览
    URL.revokeObjectURL(imageUrl)
    previewImageUrl.value = ''
    ElMessage.error(error)
  }
}

// 上传文件到七牛云
const uploadFileToQiniu = async (file) => {
  try {
    isUploading.value = true  // 标记开始上传
    uploadProgress.value = 30
    
    const formData = new FormData()
    formData.append('file', file)
    
    const loginPath = props.supplierLoginPath || window.supplierLoginPath || ''
    
    // 根据endpointType选择上传接口
    const uploadUrl = props.endpointType === 'product-main'
      ? `/supplier${loginPath}/product/upload-main-image`
      : `/supplier${loginPath}/upload-file`
    
    uploadProgress.value = 50
    
    const response = await fetch(uploadUrl, {
      method: 'POST',
      body: formData,
      headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    
    if (!response.ok) {
      throw new Error(`上传失败，状态码: ${response.status}`)
    }
    
    const result = await response.json()
    
    uploadProgress.value = 80
    
    if (!result.success) {
      throw new Error(result.message || result.error || '上传失败')
    }
    
    // 上传成功
    uploadProgress.value = 100
    
    // 使用previewUrl立即显示图片（不需要再调用签名URL接口）
    if (result.previewUrl) {
      previewImageUrl.value = result.previewUrl
    } else if (result.url) {
      // 兼容旧版本返回的url字段
      previewImageUrl.value = result.url
    } else {
      // 如果都没有，使用key（但这可能不会正确显示）
      previewImageUrl.value = result.key || ''
    }
    
    // 发送key给父组件（存储到数据库）
    const key = props.endpointType === 'product-main' ? (result.mainImageKey || result.key) : result.key
    isUploadSuccess.value = true; // 设置标志，表示这是上传成功后设置的key
    emit('update:modelValue', key)
    emit('upload-success', result)
    
    // 显示成功提示
    if (props.endpointType === 'product-main') {
      ElMessage.success('主图上传成功')
    } else {
      ElMessage.success('图片上传成功')
    }
    
    // 重置进度条和上传标记
    setTimeout(() => {
      uploadProgress.value = 0
      isUploading.value = false
    }, 1000)
  } catch (error) {
    console.error('[FileUpload] 上传失败:', error)
    uploadProgress.value = 0
    isUploading.value = false
    ElMessage.error(error.message || '上传失败，请稍后重试')
    emit('upload-error', error)
  }
}

// 移除文件
const removeFile = () => {
  previewImageUrl.value = ''
  uploadProgress.value = 0
  isUploadSuccess.value = true; // 设置标志，表示这是移除操作
  emit('update:modelValue', '')
  emit('remove')
}
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

.uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
  line-height: 178px;
}

.upload-progress {
  margin-top: 10px;
}

.remove-button {
  margin-top: 10px;
  text-align: center;
}
</style>