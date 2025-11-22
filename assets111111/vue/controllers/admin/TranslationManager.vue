<template>
  <div class="translation-manager">
    <div class="header-section">
      <h2>多语言翻译管理</h2>
      <el-select
        v-model="selectedFile"
        placeholder="请选择翻译文件"
        @change="handleFileChange"
        class="file-selector"
        size="large"
      >
        <el-option
          v-for="file in translationFiles"
          :key="file.key"
          :label="file.label"
          :value="file.key"
        />
      </el-select>
    </div>

    <div v-if="selectedFile" class="content-section" v-loading="loading">
      <!-- 顶部保存按钮 -->
      <div class="action-bar top">
        <el-button type="primary" @click="saveTranslations" :loading="saving" size="large">
          保存翻译
        </el-button>
      </div>

      <!-- 翻译编辑区域 -->
      <div class="translation-section">
        <h3>翻译内容编辑</h3>
        <el-table :data="translations" border stripe class="translation-table">
          <el-table-column prop="key" label="翻译键" width="200" />
          <el-table-column label="中文翻译">
            <template #default="{ row }">
              <el-input
                v-model="row.zh"
                type="textarea"
                :rows="5"
                placeholder="请输入中文翻译"
              />
            </template>
          </el-table-column>
          <el-table-column label="英文翻译">
            <template #default="{ row }">
              <el-input
                v-model="row.en"
                type="textarea"
                :rows="5"
                placeholder="请输入英文翻译"
              />
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 翻译保存按钮 -->
      <div class="action-bar bottom">
        <el-button type="primary" @click="saveTranslations" :loading="saving" size="large">
          保存翻译
        </el-button>
      </div>

      <!-- 图片管理区域 -->
      <div class="image-section">
        <h3>图片管理</h3>
        <div v-for="image in images" :key="image.name" class="image-item">
          <div class="image-preview">
            <el-image
              :src="image.previewUrl"
              :alt="image.name"
              fit="contain"
              class="preview-img"
              :preview-src-list="[image.previewUrl]"
            />
            <div class="image-info">
              <p><strong>{{ image.name }}</strong></p>
              <p>格式: {{ image.extension.toUpperCase() }}</p>
              <p>大小: {{ formatFileSize(image.size) }}</p>
            </div>
          </div>

          <div class="image-upload">
            <el-upload
              :action="uploadUrl"
              :data="{ originalFileName: image.name }"
              :headers="{ 'X-Requested-With': 'XMLHttpRequest' }"
              :before-upload="(file) => beforeUpload(file, image)"
              :on-success="(response) => handleUploadSuccess(response, image)"
              :on-error="handleUploadError"
              :show-file-list="false"
              accept="image/*"
            >
              <el-button type="primary">
                上传替换图片
              </el-button>
            </el-upload>
            <p class="upload-hint">
              仅支持 .{{ image.extension }} 格式，最大5MB
            </p>
          </div>
        </div>

        <el-empty v-if="images.length === 0" description="该翻译文件没有关联的图片" />
      </div>
    </div>

    <el-empty v-else description="请选择一个翻译文件开始编辑" />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import {
  ElSelect,
  ElOption,
  ElTable,
  ElTableColumn,
  ElInput,
  ElButton,
  ElUpload,
  ElImage,
  ElEmpty,
  ElMessage,
  vLoading
} from 'element-plus'

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

const translationFiles = ref([])
const selectedFile = ref('')
const translations = ref([])
const images = ref([])
const saving = ref(false)
const loading = ref(false)

const uploadUrl = computed(() => {
  return `/admin${props.adminLoginPath}/translation/upload-image/${selectedFile.value}`
})

// 加载翻译文件列表
const loadTranslationFiles = async () => {
  try {
    const response = await fetch(`/admin${props.adminLoginPath}/translation/files`, {
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    
    const data = await response.json()
    if (data.success) {
      translationFiles.value = data.files
    }
  } catch (error) {
    console.error('加载翻译文件列表失败:', error)
    ElMessage.error('加载翻译文件列表失败')
  }
}

// 加载翻译数据
const loadTranslationData = async () => {
  if (!selectedFile.value) return

  loading.value = true
  try {
    const url = `/admin${props.adminLoginPath}/translation/data/${selectedFile.value}`
    console.log('加载翻译数据 URL:', url)
    
    const response = await fetch(url, {
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    
    const data = await response.json()
    console.log('返回的数据:', data)
    
    if (data.success) {
      translations.value = data.translations
      images.value = data.images
      console.log('翻译数据:', translations.value)
      console.log('图片数据:', images.value)
    }
  } catch (error) {
    console.error('加载翻译数据失败:', error)
    ElMessage.error('加载翻译数据失败')
  } finally {
    loading.value = false
  }
}

// 文件选择变化
const handleFileChange = () => {
  loadTranslationData()
}

// 验证JSON格式和特殊字符
const validateJsonContent = (text, fieldName) => {
  // 检查是否为空
  if (!text || text.trim() === '') {
    return { valid: false, message: `${fieldName}不能为空` }
  }

  // 检查危险字符（未转义的引号、控制字符等）
  const problematicChars = []
  
  // 检查未配对的引号
  const singleQuotes = (text.match(/(?<!\\)'/g) || []).length
  const doubleQuotes = (text.match(/(?<!\\)"/g) || []).length
  
  // 检查控制字符（除了常见的换行符、制表符）
  const controlChars = text.match(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/g)
  if (controlChars) {
    problematicChars.push('控制字符')
  }
  
  // 尝试将内容放入JSON结构中验证
  try {
    const testObj = { test: text }
    const jsonStr = JSON.stringify(testObj)
    JSON.parse(jsonStr) // 验证可以正确解析
  } catch (e) {
    return { 
      valid: false, 
      message: `${fieldName}包含无法序列化为JSON的字符，请检查特殊符号` 
    }
  }
  
  return { valid: true }
}

// 保存翻译
const saveTranslations = async () => {
  // 验证数据
  for (let i = 0; i < translations.value.length; i++) {
    const item = translations.value[i]
    const rowNum = i + 1
    
    // 检查是否为空
    if (!item.key || !item.zh || !item.en) {
      ElMessage.warning(`第${rowNum}行：请填写完整的翻译键、中文和英文内容`)
      return
    }
    
    // 验证中文翻译
    const zhValidation = validateJsonContent(item.zh, `第${rowNum}行中文翻译`)
    if (!zhValidation.valid) {
      ElMessage.error(zhValidation.message)
      return
    }
    
    // 验证英文翻译
    const enValidation = validateJsonContent(item.en, `第${rowNum}行英文翻译`)
    if (!enValidation.valid) {
      ElMessage.error(enValidation.message)
      return
    }
  }
  
  // 最终验证：尝试构建完整的JSON结构
  try {
    const testData = {
      'zh-CN': {},
      'en': {}
    }
    
    translations.value.forEach(item => {
      testData['zh-CN'][item.key] = item.zh
      testData['en'][item.key] = item.en
    })
    
    // 验证可以序列化和反序列化
    const jsonStr = JSON.stringify(testData)
    JSON.parse(jsonStr)
  } catch (error) {
    ElMessage.error('数据格式验证失败，请检查是否有特殊字符影响JSON格式')
    console.error('JSON validation error:', error)
    return
  }

  saving.value = true
  try {
    const response = await fetch(`/admin${props.adminLoginPath}/translation/save/${selectedFile.value}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: JSON.stringify({
        translations: translations.value
      })
    })

    const data = await response.json()
    if (data.success) {
      ElMessage.success('翻译保存成功')
    } else {
      ElMessage.error(data.message || '保存失败')
    }
  } catch (error) {
    console.error('保存翻译失败:', error)
    ElMessage.error('保存翻译失败')
  } finally {
    saving.value = false
  }
}

// 上传前验证
const beforeUpload = (file, image) => {
  const fileExt = file.name.split('.').pop().toLowerCase()
  const expectedExt = image.extension.toLowerCase()

  if (fileExt !== expectedExt) {
    ElMessage.error(`文件扩展名不匹配！需要 .${expectedExt} 格式，但上传的是 .${fileExt} 格式`)
    return false
  }

  const isValidType = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'].includes(file.type)
  if (!isValidType) {
    ElMessage.error('只能上传图片文件！')
    return false
  }

  const isLt5M = file.size / 1024 / 1024 < 5
  if (!isLt5M) {
    ElMessage.error('图片大小不能超过 5MB！')
    return false
  }

  return true
}

// 上传成功
const handleUploadSuccess = (response, image) => {
  if (response.success) {
    ElMessage.success('图片已保存成功')
    // 更新预览URL（带时间戳强制刷新）
    const imageIndex = images.value.findIndex(img => img.name === image.name)
    if (imageIndex !== -1) {
      images.value[imageIndex].previewUrl = response.previewUrl
      // 强制触发响应式更新
      images.value = [...images.value]
    }
  } else {
    ElMessage.error(response.message || '上传失败')
  }
}

// 上传失败
const handleUploadError = (error) => {
  console.error('上传失败:', error)
  ElMessage.error('图片上传失败')
}

// 格式化文件大小
const formatFileSize = (bytes) => {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(2) + ' MB'
}

// 初始化
onMounted(() => {
  if (props.autoLoad) {
    loadTranslationFiles()
  }
})

// 暴露方法供父组件调用
defineExpose({
  loadTranslationFiles,
  loadTranslationData
})
</script>

<style scoped>
.translation-manager {
  padding: 20px;
  background: #fff;
  min-height: 100vh;
}

.header-section {
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-section h2 {
  margin: 0;
  font-size: 24px;
  color: #333;
}

.file-selector {
  width: 300px;
}

.action-bar {
  padding: 20px 0;
  text-align: center;
  border-bottom: 2px solid #e5e7eb;
}

.action-bar.bottom {
  border-top: 2px solid #e5e7eb;
  border-bottom: none;
  margin-top: 30px;
}

.translation-section {
  margin-bottom: 40px;
}

.translation-section h3 {
  font-size: 18px;
  color: #333;
  margin-bottom: 15px;
  padding-left: 10px;
  border-left: 4px solid #409eff;
}

.translation-table {
  margin-bottom: 20px;
}

.add-translation-btn {
  text-align: center;
  padding: 20px;
}

.image-section h3 {
  font-size: 18px;
  color: #333;
  margin-bottom: 15px;
  padding-left: 10px;
  border-left: 4px solid #67c23a;
}

.image-item {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 40px;
  padding: 20px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  margin-bottom: 20px;
  background: #f9fafb;
}

.image-preview {
  display: flex;
  align-items: center;
  gap: 20px;
  flex: 1;
}

.preview-img {
  width: 200px;
  height: 150px;
  border: 1px solid #ddd;
  border-radius: 4px;
  object-fit: contain;
}

.image-info {
  flex: 1;
}

.image-info p {
  margin: 5px 0;
  color: #666;
}

.image-upload {
  text-align: center;
  flex: 0 0 auto;
}

.upload-hint {
  margin-top: 10px;
  font-size: 12px;
  color: #999;
}

.content-section {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
