<template>
  <div class="contact-us-page-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2 class="page-title">
        <el-icon class="title-icon"><Document /></el-icon>
        联系我们
      </h2>
      <div class="header-actions">
        <el-button type="primary" @click="savePage" :loading="saving" size="large">
          {{ saving ? '保存中...' : '保存页面' }}
        </el-button>
        <el-button @click="loadPageData" size="large">刷新数据</el-button>
      </div>
    </div>
    
    <!-- 页面内容编辑区域 -->
    <div class="content-section" v-loading="loading">
      <!-- 横幅图片 -->
      <el-card class="section-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <h3>横幅图片</h3>
          </div>
        </template>
        
        <div class="section-content">
          <el-form-item label="横幅图片">
            <div class="image-section">
              <!-- 图片预览 -->
              <div class="image-preview-container">
                <el-image
                  v-if="bannerImagePreview || pageContent.contact_us.banner.image"
                  :src="bannerImagePreview || getSignedImageUrl(pageContent.contact_us.banner.image)"
                  fit="cover"
                  style="width: 100%; height: 100%;"
                  :preview-src-list="[bannerImagePreview || getSignedImageUrl(pageContent.contact_us.banner.image)]"
                  preview-teleported
                  class="preview-image"
                />
                <div v-else class="preview-placeholder">
                  暂无图片
                </div>
              </div>
              
              <!-- 上传组件 -->
              <div class="upload-container">
                <file-upload 
                  v-model="bannerImage"
                  :admin-login-path="adminLoginPath"
                  endpoint-type="contact-us-page"
                  accept="image/*"
                  :max-size="5"
                  @upload-success="handleBannerImageUploadSuccess"
                />
              </div>
            </div>
          </el-form-item>
        </div>
      </el-card>
      
      <!-- 内容部分 -->
      <el-card v-for="(section, sectionIndex) in pageContent.contact_us.sections" :key="sectionIndex" class="section-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <h3>{{ section.title }}</h3>
          </div>
        </template>
        
        <div class="section-content">
          <el-form-item label="中文标题">
            <el-input v-model="section.title" placeholder="请输入中文标题"></el-input>
          </el-form-item>
          
          <el-form-item label="英文标题">
            <el-input v-model="section.title_en" placeholder="Enter English title"></el-input>
          </el-form-item>
          
          <!-- 项目列表 -->
          <div v-for="(item, itemIndex) in section.items" :key="itemIndex" class="item">
            <el-divider v-if="itemIndex > 0" />
            <h4>项目 {{ itemIndex + 1 }}</h4>
            
            <el-form-item v-if="item.text !== undefined" label="中文文本">
              <el-input v-model="item.text" placeholder="请输入中文文本" type="textarea" :rows="2"></el-input>
            </el-form-item>
            
            <el-form-item v-if="item.text_en !== undefined" label="英文文本">
              <el-input v-model="item.text_en" placeholder="Enter English text" type="textarea" :rows="2"></el-input>
            </el-form-item>
            
            <el-form-item v-if="item.image !== undefined" label="图片">
              <div class="image-section">
                <!-- 图片预览 -->
                <div class="image-preview-container">
                  <el-image
                    v-if="sectionImagePreviews[sectionIndex] && sectionImagePreviews[sectionIndex][itemIndex] || item.image"
                    :src="(sectionImagePreviews[sectionIndex] && sectionImagePreviews[sectionIndex][itemIndex]) || getSignedImageUrl(item.image)"
                    fit="cover"
                    style="width: 100%; height: 100%;"
                    :preview-src-list="[(sectionImagePreviews[sectionIndex] && sectionImagePreviews[sectionIndex][itemIndex]) || getSignedImageUrl(item.image)]"
                    preview-teleported
                    class="preview-image"
                  />
                  <div v-else class="preview-placeholder">
                    暂无图片
                  </div>
                </div>
                
                <!-- 上传组件 -->
                <div class="upload-container">
                  <file-upload 
                    :model-value="getImageModelValue(sectionImages, sectionIndex, itemIndex)"
                    @update:model-value="(value) => setImageModelValue(sectionImages, sectionIndex, itemIndex, value)"
                    :admin-login-path="adminLoginPath"
                    endpoint-type="contact-us-page"
                    accept="image/*"
                    :max-size="5"
                    @upload-success="(data) => handleSectionImageUploadSuccess(data, sectionIndex, itemIndex)"
                  />
                </div>
              </div>
            </el-form-item>
          </div>
        </div>
      </el-card>
      
      <!-- 底部操作按钮 -->
      <div class="footer-actions">
        <el-button type="primary" @click="savePage" :loading="saving" size="large">
          {{ saving ? '保存中...' : '保存页面' }}
        </el-button>
        <el-button @click="loadPageData" size="large">刷新数据</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, defineProps, defineExpose } from 'vue'
import {
  ElCard,
  ElForm,
  ElFormItem,
  ElInput,
  ElButton,
  ElMessage,
  ElIcon,
  ElImage,
  ElDivider,
  vLoading
} from 'element-plus'
import { Document } from '@element-plus/icons-vue'
import FileUpload from './FileUpload.vue'

// Props
const props = defineProps({
  adminLoginPath: {
    type: String,
    default: ''
  },
  autoLoad: {
    type: Boolean,
    default: false
  }
})

// 原始数据状态（从后端读取的完整数据，包含所有key，用于保存时传回后端）
const originalData = ref(null)

// 显示数据状态（用于页面显示和编辑）
const pageContent = ref({
  contact_us: {
    banner: {
      image: ''
    },
    sections: [
      {
        title: '',
        title_en: '',
        items: [
          {
            text: '',
            text_en: ''
          },
          {
            text: '',
            text_en: ''
          },
          {
            text: '',
            text_en: ''
          },
          {
            text: '',
            text_en: ''
          }
        ]
      },
      {
        title: '',
        title_en: '',
        items: [
          {
            text: '',
            text_en: ''
          },
          {
            image: ''
          },
          {
            text: '',
            text_en: ''
          },
          {
            text: '',
            text_en: ''
          }
        ]
      },
      {
        title: '',
        title_en: '',
        items: [
          {
            text: '',
            text_en: ''
          },
          {
            text: '',
            text_en: ''
          },
          {
            image: ''
          }
        ]
      },
      {
        title: '',
        title_en: '',
        items: [
          {
            text: '',
            text_en: ''
          },
          {
            text: '',
            text_en: ''
          },
          {
            image: ''
          }
        ]
      },
      {
        title: '',
        title_en: '',
        items: [
          {
            text: '',
            text_en: ''
          },
          {
            text: '',
            text_en: ''
          }
        ]
      }
    ]
  }
})

const loading = ref(false)
const saving = ref(false)

// 图片上传变量（用于FileUpload组件的v-model）
const bannerImage = ref('')
const sectionImages = ref([])

// 图片预览URL（用于上传后立即显示）
const bannerImagePreview = ref('')
const sectionImagePreviews = ref([])

// 获取带签名的图片URL（兼容对象和字符串格式）
const getSignedImageUrl = (imageField) => {
  if (!imageField) return ''
  
  // 如果是对象格式 { key: 'xxx', signedUrl: 'xxx' }
  if (typeof imageField === 'object' && imageField.signedUrl) {
    return imageField.signedUrl
  }
  
  // 如果是对象但没有signedUrl，使用key动态获取
  if (typeof imageField === 'object' && imageField.key) {
    const key = imageField.key
    if (!key) return ''
    if (key.startsWith('http')) return key
    return `/admin${props.adminLoginPath}/contact-us-page/image/signed-url?key=${encodeURIComponent(key)}`
  }
  
  // 如果是字符串格式（兼容旧数据）
  if (typeof imageField === 'string') {
    if (imageField.startsWith('http')) return imageField
    return `/admin${props.adminLoginPath}/contact-us-page/image/signed-url?key=${encodeURIComponent(imageField)}`
  }
  
  return ''
}

// 处理横幅图片上传成功
const handleBannerImageUploadSuccess = (data) => {
  // 更新原始数据中的key
  if (originalData.value) {
    originalData.value.contact_us.banner.image = data.key
  }
  // 更新显示数据中的key
  pageContent.value.contact_us.banner.image = data.key
  // 使用上传接口返回的预览URL更新预览
  if (data.previewUrl) {
    bannerImagePreview.value = data.previewUrl
  }
  ElMessage.success('横幅图片上传成功')
}

// 处理部分图片上传成功
const handleSectionImageUploadSuccess = (data, sectionIndex, itemIndex) => {
  // 确保数组已初始化
  if (!originalData.value.contact_us.sections[sectionIndex]) {
    originalData.value.contact_us.sections[sectionIndex] = { items: [] };
  }
  if (!originalData.value.contact_us.sections[sectionIndex].items[itemIndex]) {
    originalData.value.contact_us.sections[sectionIndex].items[itemIndex] = {};
  }
  
  // 更新原始数据中的key
  originalData.value.contact_us.sections[sectionIndex].items[itemIndex].image = data.key
  
  // 更新显示数据中的key
  pageContent.value.contact_us.sections[sectionIndex].items[itemIndex].image = data.key
  
  // 使用上传接口返回的预览URL更新预览
  if (data.previewUrl) {
    if (!sectionImagePreviews.value[sectionIndex]) {
      sectionImagePreviews.value[sectionIndex] = [];
    }
    sectionImagePreviews.value[sectionIndex][itemIndex] = data.previewUrl;
  }
  ElMessage.success(`部分${sectionIndex+1}项目${itemIndex+1}图片上传成功`);
}

// 加载页面数据
const loadPageData = async () => {
  console.log('ContactUsPage: loadPageData called');
  loading.value = true
  try {
    const response = await fetch(`/admin${props.adminLoginPath}/contact-us-page/data`, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json',
      }
    })
    
    console.log('ContactUsPage: API response status', response.status);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const result = await response.json()
    console.log('ContactUsPage: API response data', result);
    
    if (result.success && result.data && result.data.pageInfo) {
      try {
        const content = JSON.parse(result.data.pageInfo.content)
        
        // 提取原始key（用于保存）
        const extractedKeys = extractImageKeys(content)
        originalData.value = extractedKeys
        
        // 设置显示数据（使用signedUrl显示）
        pageContent.value = content
        
        // 初始化图片上传变量（用于FileUpload组件的v-model）
        bannerImage.value = ''
        sectionImages.value = []
        
        // 初始化预览数组
        sectionImagePreviews.value = []
        
        // 清空预览URL
        bannerImagePreview.value = ''
        
        // 初始化每个部分的图片数组
        pageContent.value.contact_us.sections.forEach((section, sectionIndex) => {
          if (!sectionImages.value[sectionIndex]) {
            sectionImages.value[sectionIndex] = []
          }
          if (!sectionImagePreviews.value[sectionIndex]) {
            sectionImagePreviews.value[sectionIndex] = []
          }
          section.items.forEach((item, itemIndex) => {
            if (item.image !== undefined) {
              if (!sectionImages.value[sectionIndex][itemIndex]) {
                sectionImages.value[sectionIndex][itemIndex] = ''
              }
              if (!sectionImagePreviews.value[sectionIndex][itemIndex]) {
                sectionImagePreviews.value[sectionIndex][itemIndex] = ''
              }
            }
          })
        })
        
        console.log('ContactUsPage: Data loaded successfully');
        console.log('ContactUsPage: 原始keys', originalData.value);
      } catch (e) {
        console.error('解析页面内容失败:', e)
        ElMessage.error('解析页面内容失败')
      }
    }
  } catch (error) {
    console.error('加载页面数据失败:', error)
    ElMessage.error('加载页面数据失败: ' + error.message)
  } finally {
    loading.value = false
  }
}

// 从内容数据中提取原始key（递归处理）
const extractImageKeys = (data) => {
  const result = JSON.parse(JSON.stringify(data)) // 深度复制
  
  // 提取banner.image的key
  if (result.contact_us && result.contact_us.banner && result.contact_us.banner.image) {
    result.contact_us.banner.image = getImageKey(result.contact_us.banner.image)
  }
  
  // 提取sections[*].items[*].image的key
  if (result.contact_us && Array.isArray(result.contact_us.sections)) {
    result.contact_us.sections.forEach(section => {
      if (Array.isArray(section.items)) {
        section.items.forEach(item => {
          if (item.image !== undefined) {
            item.image = getImageKey(item.image)
          }
        })
      }
    })
  }
  
  return result
}

// 获取图片的key（从对象或字符串中提取）
const getImageKey = (imageField) => {
  if (!imageField) return ''
  
  // 如果是对象格式 { key: 'xxx', signedUrl: 'xxx' }
  if (typeof imageField === 'object' && imageField.key) {
    return imageField.key
  }
  
  // 如果是字符串，直接返回
  if (typeof imageField === 'string') {
    return imageField
  }
  
  return ''
}

// 获取嵌套数组中的图片模型值
const getImageModelValue = (array, sectionIndex, itemIndex) => {
  if (array.value && array.value[sectionIndex] && array.value[sectionIndex][itemIndex]) {
    return array.value[sectionIndex][itemIndex]
  }
  return ''
}

// 设置嵌套数组中的图片模型值
const setImageModelValue = (array, sectionIndex, itemIndex, value) => {
  if (!array.value) {
    array.value = []
  }
  if (!array.value[sectionIndex]) {
    array.value[sectionIndex] = []
  }
  array.value[sectionIndex][itemIndex] = value
}

// 保存页面
const savePage = async () => {
  saving.value = true
  
  try {
    // 确保originalData已初始化
    if (!originalData.value) {
      ElMessage.error('数据未加载，请先刷新数据')
      return
    }
    
    // 构建要保存的数据：合并用户编辑的内容和原始数据中的key
    const dataToSave = {
      contact_us: {
        banner: {
          image: originalData.value.contact_us.banner.image || ''  // 使用原始数据中的key
        },
        sections: pageContent.value.contact_us.sections.map((section, sectionIndex) => ({
          title: section.title,
          title_en: section.title_en,
          items: section.items.map((item, itemIndex) => {
            if (item.text !== undefined) {
              return {
                text: item.text,
                text_en: item.text_en
              };
            } else if (item.image !== undefined) {
              // 确保原始数据中存在该图像字段
              let imageKey = '';
              if (originalData.value.contact_us.sections[sectionIndex] && 
                  originalData.value.contact_us.sections[sectionIndex].items[itemIndex]) {
                imageKey = originalData.value.contact_us.sections[sectionIndex].items[itemIndex].image || '';
              }
              return {
                image: imageKey  // 使用原始数据中的key
              };
            }
            return item;
          })
        }))
      }
    }
    
    const response = await fetch(`/admin${props.adminLoginPath}/contact-us-page/save`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        content: JSON.stringify(dataToSave)
      })
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const result = await response.json()
    
    if (result.success) {
      ElMessage.success(result.message || '页面保存成功')
      // 重新加载数据，同步原始数据
      await loadPageData()
    } else {
      ElMessage.error(result.message || '保存失败')
    }
  } catch (error) {
    ElMessage.error('保存失败: ' + error.message)
  } finally {
    saving.value = false
  }
}

// 组件挂载时加载数据
onMounted(() => {
  if (props.autoLoad) {
    loadPageData()
  }
})

// 添加新部分
const addSection = () => {
  pageContent.value.contact_us.sections.push({
    title: '',
    title_en: '',
    items: [
      {
        text: '',
        text_en: ''
      }
    ]
  });
  
  // 初始化新部分的图片数组
  const sectionIndex = pageContent.value.contact_us.sections.length - 1;
  if (!sectionImages.value[sectionIndex]) {
    sectionImages.value[sectionIndex] = [];
  }
  if (!sectionImagePreviews.value[sectionIndex]) {
    sectionImagePreviews.value[sectionIndex] = [];
  }
};

// 删除部分
const removeSection = (sectionIndex) => {
  pageContent.value.contact_us.sections.splice(sectionIndex, 1);
  if (sectionImages.value[sectionIndex]) {
    sectionImages.value.splice(sectionIndex, 1);
  }
  if (sectionImagePreviews.value[sectionIndex]) {
    sectionImagePreviews.value.splice(sectionIndex, 1);
  }
};

// 添加文本项目
const addItem = (sectionIndex) => {
  pageContent.value.contact_us.sections[sectionIndex].items.push({
    text: '',
    text_en: ''
  });
};

// 添加图片项目
const addImageItem = (sectionIndex) => {
  pageContent.value.contact_us.sections[sectionIndex].items.push({
    image: ''
  });
  
  // 初始化新项目的图片数组
  const itemIndex = pageContent.value.contact_us.sections[sectionIndex].items.length - 1;
  if (!sectionImages.value[sectionIndex]) {
    sectionImages.value[sectionIndex] = [];
  }
  if (!sectionImagePreviews.value[sectionIndex]) {
    sectionImagePreviews.value[sectionIndex] = [];
  }
  sectionImages.value[sectionIndex][itemIndex] = '';
  sectionImagePreviews.value[sectionIndex][itemIndex] = '';
};

// 删除项目
const removeItem = (sectionIndex, itemIndex) => {
  pageContent.value.contact_us.sections[sectionIndex].items.splice(itemIndex, 1);
  if (sectionImages.value[sectionIndex] && sectionImages.value[sectionIndex][itemIndex]) {
    sectionImages.value[sectionIndex].splice(itemIndex, 1);
  }
  if (sectionImagePreviews.value[sectionIndex] && sectionImagePreviews.value[sectionIndex][itemIndex]) {
    sectionImagePreviews.value[sectionIndex].splice(itemIndex, 1);
  }
};

// 暴露方法给父组件调用
defineExpose({
  loadPageData
})

</script>

<style scoped>
.contact-us-page-container {
  width: 100%;
  max-width: 1200px;
  box-sizing: border-box;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  width: 100%;
  padding-bottom: 15px;
  border-bottom: 1px solid #ebeef5;
}

.page-title {
  font-size: 28px;
  font-weight: bold;
  margin: 0;
  display: flex;
  align-items: center;
  color: #303133;
}

.title-icon {
  margin-right: 10px;
  vertical-align: middle;
  font-size: 32px;
  color: #409eff;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.content-section {
  width: 100%;
}

.section-card {
  margin-bottom: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.section-card :deep(.el-card__header) {
  background-color: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
  padding: 15px 20px;
}

.card-header h3 {
  font-size: 20px;
  font-weight: 600;
  margin: 0;
  color: #303133;
}

.section-content {
  padding: 20px;
}

.social-item h4, .warehouse-item h4 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #303133;
  font-size: 18px;
  font-weight: 500;
}

.image-section {
  display: flex;
  align-items: flex-start;
  gap: 30px;
  width: 100%;
  justify-content: center;
  padding: 15px 0;
}

.image-preview-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-width: 250px;
  min-height: 150px;
  padding: 15px;
  position: relative;
  background-color: #f9f9f9;
}

.preview-image {
  max-width: 100%;
  max-height: 200px;
  cursor: pointer;
  object-fit: cover;
}

.preview-image:hover {
  opacity: 0.8;
}

.preview-placeholder {
  color: #909399;
  font-size: 14px;
}

.upload-container {
  flex: 1;
  min-width: 250px;
}

:deep(.el-form-item) {
  margin-bottom: 20px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #606266;
}

.large-textarea {
  width: 100%;
}

:deep(.large-textarea .el-textarea__inner) {
  min-height: 150px !important;
}

.footer-actions {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 30px;
  padding: 20px 0;
  border-top: 1px solid #ebeef5;
}

.add-section-button, .add-item-button {
  margin-top: 20px;
  text-align: center;
}

.add-item-button {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.item h4 {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

@media (max-width: 768px) {
  .contact-us-page-container {
    padding: 10px;
  }
  
  .page-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .header-actions {
    width: 100%;
    justify-content: flex-end;
  }
  
  .image-section {
    flex-direction: column;
    gap: 15px;
  }
  
  .image-preview-container, .upload-container {
    min-width: 100%;
  }
  
  .footer-actions {
    flex-direction: column;
    align-items: center;
  }
}
</style>