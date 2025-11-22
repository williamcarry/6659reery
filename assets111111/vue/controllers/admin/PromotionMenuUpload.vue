<template>
  <div class="promotion-menu-upload">
    <el-upload
      class="promotion-image-uploader"
      action=""
      :auto-upload="false"
      :show-file-list="false"
      :on-change="handleImageChange"
      :before-upload="beforeImageUpload"
    >
      <img v-if="previewImageUrl" :src="previewImageUrl" class="promotion-image" />
      <el-icon v-else class="promotion-uploader-icon">
        <Plus />
      </el-icon>
    </el-upload>
    
    <div v-if="uploadProgress > 0 && uploadProgress < 100" class="upload-progress">
      <el-progress :percentage="uploadProgress" />
    </div>
    
    <div v-if="uploadError" class="upload-error">
      {{ uploadError }}
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { ElUpload, ElIcon, ElProgress, ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

// 定义 props
const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  adminLoginPath: {
    type: String,
    default: ''
  }
})

// 定义 emits
const emit = defineEmits(['update:modelValue', 'upload-success', 'upload-error'])

// 响应式数据
const previewImageUrl = ref('')
const uploadProgress = ref(0)
const uploadError = ref('')
const isUploading = ref(false)  // 标记是否正在上传，避免重复调用签名URL接口
const isUploadSuccess = ref(false)  // 标记是否是上传成功后设置的key

// 获取签名URL（用于编辑时加载已存储的图片）
const fetchSignedUrl = async (key) => {
  if (!key || key.startsWith('http')) {
    console.log('[PromotionMenuUpload] Key is already URL or empty:', key)
    previewImageUrl.value = key
    return
  }
  
  try {
    const loginPath = props.adminLoginPath || window.adminLoginPath || ''
    const signedUrlEndpoint = `/admin${loginPath}/promotion/image/signed-url`
    console.log('[PromotionMenuUpload] Fetching signed URL from:', signedUrlEndpoint)
    console.log('[PromotionMenuUpload] Request key:', key)
    
    const response = await fetch(signedUrlEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ key: key })
    })
    
    const result = await response.json()
    console.log('[PromotionMenuUpload] Signed URL result:', result)
    
    if (result.success) {
      console.log('[PromotionMenuUpload] Got signed URL:', result.url)
      previewImageUrl.value = result.url
    } else {
      console.error('[PromotionMenuUpload] Failed to get signed URL:', result.error)
      previewImageUrl.value = ''  // 失败时不显示图片
    }
  } catch (error) {
    console.error('[PromotionMenuUpload] Error fetching signed URL:', error)
    previewImageUrl.value = ''
  }
}

// 监听 modelValue 变化
watch(() => props.modelValue, (newVal) => {
  console.log('[PromotionMenuUpload] modelValue changed:', {
    newVal,
    isUploading: isUploading.value,
    isUploadSuccess: isUploadSuccess.value,
    startsWithHttp: newVal && newVal.startsWith('http'),
    hasPreview: !!previewImageUrl.value
  });
  
  // 如果已经有预览图片（上传成功后设置的），跳过
  if (previewImageUrl.value) {
    console.log('[PromotionMenuUpload] Skipping because previewImageUrl already set');
    return
  }
  
  // 如果是上传成功后设置的key，跳过（上传成功后会直接使用 previewUrl）
  if (isUploadSuccess.value) {
    console.log('[PromotionMenuUpload] Skipping because isUploadSuccess is true');
    isUploadSuccess.value = false; // 重置标志
    return
  }
  
  // 如果正在上传，跳过（上传成功后会直接使用 previewUrl）
  if (isUploading.value) {
    console.log('[PromotionMenuUpload] Skipping because isUploading is true');
    return
  }
  
  // 如果值为空，清除预览
  if (!newVal) {
    console.log('[PromotionMenuUpload] Clearing preview because newVal is empty');
    previewImageUrl.value = ''
    return
  }
  
  // 如果是完整的URL（如previewUrl或签名URL），直接使用
  if (newVal.startsWith('http')) {
    console.log('[PromotionMenuUpload] Using URL directly:', newVal);
    previewImageUrl.value = newVal
    return
  }
  
  // 对于key值，需要调用签名URL接口获取可显示的URL
  console.log('[PromotionMenuUpload] Fetching signed URL for key:', newVal);
  fetchSignedUrl(newVal)
}, { immediate: true })

// 图片选择处理
const handleImageChange = (file) => {
  // 验证文件类型
  const isValidType = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'].includes(file.raw.type)
  if (!isValidType) {
    ElMessage.error('只支持 JPG、PNG、GIF、WEBP 格式的图片!')
    return false
  }
  
  // 验证文件大小 (5MB)
  const isLt5M = file.raw.size / 1024 / 1024 < 5
  if (!isLt5M) {
    ElMessage.error('图片大小不能超过 5MB!')
    return false
  }
  
  // 先显示预览
  const imageUrl = URL.createObjectURL(file.raw)
  previewImageUrl.value = imageUrl
  
  // 上传图片
  uploadImageToQiniu(file.raw)
  
  return true
}

// 上传前验证
const beforeImageUpload = (rawFile) => {
  // 这个函数会在 handleImageChange 之前执行，但我们已经在 handleImageChange 中处理了验证
  return false // 阻止自动上传，我们手动处理
}

// 上传图片到七牛云
const uploadImageToQiniu = async (file) => {
  try {
    isUploading.value = true  // 标记开始上传
    uploadProgress.value = 10
    uploadError.value = ''
    
    // 创建 FormData
    const formData = new FormData()
    formData.append('image', file)
    
    // 使用从prop传入的adminLoginPath
    const loginPath = props.adminLoginPath || window.adminLoginPath || ''
    const uploadUrl = `/admin${loginPath}/promotion/menu/upload-image`
    console.log('[PromotionMenuUpload] Uploading to:', uploadUrl)
    
    // 上传到服务器
    uploadProgress.value = 30
    const response = await fetch(uploadUrl, {
      method: 'POST',
      body: formData
    })
    
    if (!response.ok) {
      throw new Error(`上传失败，状态码: ${response.status}`)
    }
    
    uploadProgress.value = 70
    const result = await response.json()
    console.log('[PromotionMenuUpload] Upload result:', result)
    
    if (result.success) {
      // 上传成功
      uploadProgress.value = 100
      
      // 使用previewUrl立即显示图片（不需要再调用签名URL接口）
      console.log('[PromotionMenuUpload] Upload success, using previewUrl:', result.previewUrl);
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
      isUploadSuccess.value = true; // 设置标志，表示这是上传成功后设置的key
      emit('update:modelValue', result.url)  // 发送key给父组件
      emit('upload-success', result)
      ElMessage.success('图片上传成功!')
    } else {
      throw new Error(result.error || '上传失败')
    }
    
    // 重置进度条和上传标记
    setTimeout(() => {
      uploadProgress.value = 0
      isUploading.value = false
    }, 1000)
  } catch (error) {
    console.error('[PromotionMenuUpload] Upload error:', error)
    uploadProgress.value = 0
    isUploading.value = false
    uploadError.value = error.message || '上传失败，请稍后重试'
    emit('upload-error', error)
    ElMessage.error(uploadError.value)
  }
}

// 暴露方法给父组件
defineExpose({
  clearImage() {
    previewImageUrl.value = ''
    uploadProgress.value = 0
    uploadError.value = ''
    isUploadSuccess.value = true; // 设置标志，表示这是移除操作
    emit('update:modelValue', '')
  }
})
</script>

<style scoped>
.promotion-image-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: border-color 0.3s;
  width: 178px;
  height: 178px;
}

.promotion-image-uploader:hover {
  border-color: #409eff;
}

.promotion-image {
  width: 178px;
  height: 178px;
  display: block;
}

.promotion-uploader-icon {
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

.upload-error {
  color: #f56c6c;
  font-size: 12px;
  margin-top: 5px;
}
</style>