<template>
  <div class="about-me-page-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2 class="page-title">
        <el-icon class="title-icon"><Document /></el-icon>
        网站简介
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
      <!-- 简介部分 -->
      <el-card class="section-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <h3>公司简介</h3>
          </div>
        </template>
        
        <div class="section-content">
          <el-form-item label="中文标题">
            <el-input v-model="pageContent.intro.title.zh" placeholder="请输入中文标题"></el-input>
          </el-form-item>
          
          <el-form-item label="英文标题">
            <el-input v-model="pageContent.intro.title.en" placeholder="Enter English title"></el-input>
          </el-form-item>
          
          <el-form-item label="中文内容">
            <el-input
              v-model="pageContent.intro.text.zh"
              type="textarea"
              :rows="8"
              placeholder="请输入中文内容"
              class="large-textarea"
            />
          </el-form-item>
          
          <el-form-item label="英文内容">
            <el-input
              v-model="pageContent.intro.text.en"
              type="textarea"
              :rows="8"
              placeholder="Enter English content"
              class="large-textarea"
            />
          </el-form-item>
          
          <el-form-item label="简介图片">
            <div class="image-section">
              <!-- 图片预览 -->
              <div class="image-preview-container">
                <el-image
                  v-if="introImagePreview || pageContent.intro.image"
                  :src="introImagePreview || getSignedImageUrl(pageContent.intro.image)"
                  fit="cover"
                  style="width: 100%; height: 100%;"
                  :preview-src-list="[introImagePreview || getSignedImageUrl(pageContent.intro.image)]"
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
                  v-model="introImage"
                  :admin-login-path="adminLoginPath"
                  endpoint-type="about-me-page"
                  accept="image/*"
                  :max-size="5"
                  @upload-success="handleIntroImageUploadSuccess"
                />
              </div>
            </div>
          </el-form-item>
        </div>
      </el-card>
      
      <!-- 业务部分 -->
      <el-card class="section-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <h3>业务介绍</h3>
          </div>
        </template>
        
        <div class="section-content">
          <el-form-item label="中文标题">
            <el-input v-model="pageContent.business.title.zh" placeholder="请输入中文标题"></el-input>
          </el-form-item>
          
          <el-form-item label="英文标题">
            <el-input v-model="pageContent.business.title.en" placeholder="Enter English title"></el-input>
          </el-form-item>
          
          <el-form-item label="业务图片">
            <div class="image-section">
              <!-- 图片预览 -->
              <div class="image-preview-container">
                <el-image
                  v-if="businessImagePreview || pageContent.business.image"
                  :src="businessImagePreview || getSignedImageUrl(pageContent.business.image)"
                  fit="cover"
                  style="width: 100%; height: 100%;"
                  :preview-src-list="[businessImagePreview || getSignedImageUrl(pageContent.business.image)]"
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
                  v-model="businessImage"
                  :admin-login-path="adminLoginPath"
                  endpoint-type="about-me-page"
                  accept="image/*"
                  :max-size="5"
                  @upload-success="handleBusinessImageUploadSuccess"
                />
              </div>
            </div>
          </el-form-item>
        </div>
      </el-card>
      
      <!-- 服务部分 -->
      <el-card class="section-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <h3>服务项目</h3>
          </div>
        </template>
        
        <div class="section-content">
          <el-form-item label="中文标题">
            <el-input v-model="pageContent.services.title.zh" placeholder="请输入中文标题"></el-input>
          </el-form-item>
          
          <el-form-item label="英文标题">
            <el-input v-model="pageContent.services.title.en" placeholder="Enter English title"></el-input>
          </el-form-item>
          
          <!-- 服务项目列表 -->
          <div v-for="(service, index) in pageContent.services.items" :key="index" class="service-item">
            <el-divider v-if="index > 0" />
            <h4>服务项目 {{ index + 1 }}</h4>
            
            <el-form-item :label="`中文标题`">
              <el-input v-model="service.title.zh" placeholder="请输入中文标题"></el-input>
            </el-form-item>
            
            <el-form-item :label="`英文标题`">
              <el-input v-model="service.title.en" placeholder="Enter English title"></el-input>
            </el-form-item>
            
            <el-form-item label="服务图片">
              <div class="image-section">
                <!-- 图片预览 -->
                <div class="image-preview-container">
                  <el-image
                    v-if="serviceImagePreviews[index] || service.image"
                    :src="serviceImagePreviews[index] || getSignedImageUrl(service.image)"
                    fit="cover"
                    style="width: 100%; height: 100%;"
                    :preview-src-list="[serviceImagePreviews[index] || getSignedImageUrl(service.image)]"
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
                    v-model="serviceImages[index]"
                    :admin-login-path="adminLoginPath"
                    endpoint-type="about-me-page"
                    accept="image/*"
                    :max-size="5"
                    @upload-success="(data) => handleServiceImageUploadSuccess(data, index)"
                  />
                </div>
              </div>
            </el-form-item>
            
            <el-form-item :label="`中文描述`">
              <el-input
                v-model="service.description.zh"
                type="textarea"
                :rows="6"
                placeholder="请输入中文描述"
                class="large-textarea"
              />
            </el-form-item>
            
            <el-form-item :label="`英文描述`">
              <el-input
                v-model="service.description.en"
                type="textarea"
                :rows="6"
                placeholder="Enter English description"
                class="large-textarea"
              />
            </el-form-item>
            
            <el-form-item :label="`中文CTA`">
              <el-input v-model="service.cta.text.zh" placeholder="请输入中文CTA文本"></el-input>
            </el-form-item>
            
            <el-form-item :label="`英文CTA`">
              <el-input v-model="service.cta.text.en" placeholder="Enter English CTA text"></el-input>
            </el-form-item>
            
            <el-form-item label="链接">
              <el-input v-model="service.cta.link" placeholder="请输入链接地址"></el-input>
            </el-form-item>
          </div>
        </div>
      </el-card>
      
      <!-- 仓库部分 -->
      <el-card class="section-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <h3>仓库展示</h3>
          </div>
        </template>
        
        <div class="section-content">
          <el-form-item label="中文标题">
            <el-input v-model="pageContent.warehouse.title.zh" placeholder="请输入中文标题"></el-input>
          </el-form-item>
          
          <el-form-item label="英文标题">
            <el-input v-model="pageContent.warehouse.title.en" placeholder="Enter English title"></el-input>
          </el-form-item>
          
          <!-- 仓库图片列表 -->
          <div v-for="(warehouse, index) in pageContent.warehouse.images" :key="index" class="warehouse-item">
            <el-divider v-if="index > 0" />
            <h4>仓库图片 {{ index + 1 }}</h4>
            
            <el-form-item :label="`中文名称`">
              <el-input v-model="warehouse.name.zh" placeholder="请输入中文名称"></el-input>
            </el-form-item>
            
            <el-form-item :label="`英文名称`">
              <el-input v-model="warehouse.name.en" placeholder="Enter English name"></el-input>
            </el-form-item>
            
            <el-form-item label="仓库图片">
              <div class="image-section">
                <!-- 图片预览 -->
                <div class="image-preview-container">
                  <el-image
                    v-if="warehouseImagePreviews[index] || warehouse.src"
                    :src="warehouseImagePreviews[index] || getSignedImageUrl(warehouse.src)"
                    fit="cover"
                    style="width: 100%; height: 100%;"
                    :preview-src-list="[warehouseImagePreviews[index] || getSignedImageUrl(warehouse.src)]"
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
                    v-model="warehouseImages[index]"
                    :admin-login-path="adminLoginPath"
                    endpoint-type="about-me-page"
                    accept="image/*"
                    :max-size="5"
                    @upload-success="(data) => handleWarehouseImageUploadSuccess(data, index)"
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
  intro: {
    title: {
      zh: '',
      en: ''
    },
    text: {
      zh: '',
      en: ''
    },
    image: ''
  },
  business: {
    title: {
      zh: '',
      en: ''
    },
    image: ''
  },
  services: {
    title: {
      zh: '',
      en: ''
    },
    items: [
      {
        title: {
          zh: '',
          en: ''
        },
        image: '',
        description: {
          zh: '',
          en: ''
        },
        cta: {
          text: {
            zh: '',
            en: ''
          }
        }
      },
      {
        title: {
          zh: '',
          en: ''
        },
        image: '',
        description: {
          zh: '',
          en: ''
        },
        cta: {
          text: {
            zh: '',
            en: ''
          }
        }
      }
    ]
  },
  warehouse: {
    title: {
      zh: '',
      en: ''
    },
    images: [
      {
        name: {
          zh: '',
          en: ''
        },
        src: ''
      },
      {
        name: {
          zh: '',
          en: ''
        },
        src: ''
      },
      {
        name: {
          zh: '',
          en: ''
        },
        src: ''
      },
      {
        name: {
          zh: '',
          en: ''
        },
        src: ''
      },
      {
        name: {
          zh: '',
          en: ''
        },
        src: ''
      },
      {
        name: {
          zh: '',
          en: ''
        },
        src: ''
      },
      {
        name: {
          zh: '',
          en: ''
        },
        src: ''
      }
    ]
  }
})

const loading = ref(false)
const saving = ref(false)

// 图片上传变量（用于FileUpload组件的v-model）
const introImage = ref('')
const businessImage = ref('')
const serviceImages = ref([])
const warehouseImages = ref([])

// 图片预览URL（用于上传后立即显示）
const introImagePreview = ref('')
const businessImagePreview = ref('')
const serviceImagePreviews = ref([])
const warehouseImagePreviews = ref([])

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
    return `/admin${props.adminLoginPath}/about-me-page/image/signed-url?key=${encodeURIComponent(key)}`
  }
  
  // 如果是字符串格式（兼容旧数据）
  if (typeof imageField === 'string') {
    if (imageField.startsWith('http')) return imageField
    return `/admin${props.adminLoginPath}/about-me-page/image/signed-url?key=${encodeURIComponent(imageField)}`
  }
  
  return ''
}

// 处理intro图片上传成功
const handleIntroImageUploadSuccess = (data) => {
  // 更新原始数据中的key
  if (originalData.value) {
    originalData.value.intro.image = data.key
  }
  // 更新显示数据中的key
  pageContent.value.intro.image = data.key
  // 使用上传接口返回的预览URL更新预览
  if (data.previewUrl) {
    introImagePreview.value = data.previewUrl
  }
  ElMessage.success('简介图片上传成功')
}

// 处理业务图片上传成功
const handleBusinessImageUploadSuccess = (data) => {
  // 更新原始数据中的key
  if (originalData.value) {
    originalData.value.business.image = data.key
  }
  // 更新显示数据中的key
  pageContent.value.business.image = data.key
  // 使用上传接口返回的预览URL更新预览
  if (data.previewUrl) {
    businessImagePreview.value = data.previewUrl
  }
  ElMessage.success('业务图片上传成功')
}

// 处理服务图片上传成功
const handleServiceImageUploadSuccess = (data, index) => {
  // 更新原始数据中的key
  if (originalData.value && originalData.value.services.items[index]) {
    originalData.value.services.items[index].image = data.key
  }
  // 更新显示数据中的key
  pageContent.value.services.items[index].image = data.key
  // 使用上传接口返回的预览URL更新预览
  if (data.previewUrl) {
    serviceImagePreviews.value[index] = data.previewUrl
  }
  ElMessage.success(`服务${index+1}图片上传成功`)
}

// 处理仓库图片上传成功
const handleWarehouseImageUploadSuccess = (data, index) => {
  // 更新原始数据中的key
  if (originalData.value && originalData.value.warehouse.images[index]) {
    originalData.value.warehouse.images[index].src = data.key
  }
  // 更新显示数据中的key
  pageContent.value.warehouse.images[index].src = data.key
  // 使用上传接口返回的预览URL更新预览
  if (data.previewUrl) {
    warehouseImagePreviews.value[index] = data.previewUrl
  }
  ElMessage.success(`仓库${index+1}图片上传成功`)
}

// 加载页面数据
const loadPageData = async () => {
  loading.value = true
  try {
    const response = await fetch(`/admin${props.adminLoginPath}/about-me-page/data`, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json',
      }
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const result = await response.json()
    
    if (result.success && result.data && result.data.pageInfo) {
      try {
        const content = JSON.parse(result.data.pageInfo.content)
        
        // 提取原始key（用于保存）
        const extractedKeys = extractImageKeys(content)
        originalData.value = extractedKeys
        
        // 设置显示数据（使用signedUrl显示）
        pageContent.value = content
        
        // 初始化图片上传变量（用于FileUpload组件的v-model）
        introImage.value = ''
        businessImage.value = ''
        serviceImages.value = Array(pageContent.value.services.items.length).fill('')
        warehouseImages.value = Array(pageContent.value.warehouse.images.length).fill('')
        
        // 初始化预览数组
        serviceImagePreviews.value = Array(pageContent.value.services.items.length).fill('')
        warehouseImagePreviews.value = Array(pageContent.value.warehouse.images.length).fill('')
        
        // 清空预览URL
        introImagePreview.value = ''
        businessImagePreview.value = ''
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
  
  // 提取intro.image的key
  if (result.intro && result.intro.image) {
    result.intro.image = getImageKey(result.intro.image)
  }
  
  // 提取business.image的key
  if (result.business && result.business.image) {
    result.business.image = getImageKey(result.business.image)
  }
  
  // 提取services.items[*].image的key
  if (result.services && Array.isArray(result.services.items)) {
    result.services.items.forEach(item => {
      if (item.image) {
        item.image = getImageKey(item.image)
      }
    })
  }
  
  // 提取warehouse.images[*].src的key
  if (result.warehouse && Array.isArray(result.warehouse.images)) {
    result.warehouse.images.forEach(img => {
      if (img.src) {
        img.src = getImageKey(img.src)
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
      intro: {
        title: pageContent.value.intro.title,
        text: pageContent.value.intro.text,
        image: originalData.value.intro.image || ''  // 使用原始数据中的key
      },
      business: {
        title: pageContent.value.business.title,
        image: originalData.value.business.image || ''  // 使用原始数据中的key
      },
      services: {
        title: pageContent.value.services.title,
        items: pageContent.value.services.items.map((item, index) => ({
          title: item.title,
          image: originalData.value.services.items[index]?.image || '',  // 使用原始数据中的key
          description: item.description,
          cta: item.cta
        }))
      },
      warehouse: {
        title: pageContent.value.warehouse.title,
        images: pageContent.value.warehouse.images.map((img, index) => ({
          name: img.name,
          src: originalData.value.warehouse.images[index]?.src || ''  // 使用原始数据中的key
        }))
      }
    }
    
    const response = await fetch(`/admin${props.adminLoginPath}/about-me-page/save`, {
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

// 暴露方法给父组件调用
defineExpose({
  loadPageData
})
</script>

<style scoped>
.about-me-page-container {
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

.service-item h4, .warehouse-item h4 {
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

@media (max-width: 768px) {
  .about-me-page-container {
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