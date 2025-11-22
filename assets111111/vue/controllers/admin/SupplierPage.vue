<template>
  <div class="supplier-page-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2 class="page-title">
        <el-icon class="title-icon"><Document /></el-icon>
        供应商介绍
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
      <!-- 页面标题部分 -->
      <el-card class="section-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <h3>页面标题</h3>
          </div>
        </template>
        
        <div class="section-content">
          <el-form-item label="中文标题">
            <el-input v-model="pageContent.pageTitle.zh" placeholder="请输入中文标题"></el-input>
          </el-form-item>
          
          <el-form-item label="英文标题">
            <el-input v-model="pageContent.pageTitle.en" placeholder="Enter English title"></el-input>
          </el-form-item>
        </div>
      </el-card>
      
      <!-- 轮播图部分 -->
      <el-card class="section-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <h3>轮播图</h3>
          </div>
        </template>
        
        <div class="section-content">
          <div v-for="(slide, index) in getHeroCarouselSlides()" :key="index" class="slide-item">
            <el-divider v-if="index > 0" />
            <h4>轮播图 {{ index + 1 }}</h4>
            
            <el-form-item :label="`中文标题`">
              <el-input v-model="slide.title.zh" placeholder="请输入中文标题"></el-input>
            </el-form-item>
            
            <el-form-item :label="`英文标题`">
              <el-input v-model="slide.title.en" placeholder="Enter English title"></el-input>
            </el-form-item>
            
            <el-form-item :label="`中文副标题`">
              <el-input
                v-model="slide.subtitle.zh"
                type="textarea"
                :rows="4"
                placeholder="请输入中文副标题"
                class="large-textarea"
              />
            </el-form-item>
            
            <el-form-item :label="`英文副标题`">
              <el-input
                v-model="slide.subtitle.en"
                type="textarea"
                :rows="4"
                placeholder="Enter English subtitle"
                class="large-textarea"
              />
            </el-form-item>
            
            <el-form-item label="轮播图图片">
              <div class="image-section">
                <!-- 图片预览 -->
                <div class="image-preview-container">
                  <el-image
                    v-if="getSlideImagePreview(index) || getSignedImageUrl(slide.image)"
                    :src="getSlideImagePreview(index) || getSignedImageUrl(slide.image)"
                    fit="cover"
                    style="width: 100%; height: 100%;"
                    :preview-src-list="[getSlideImagePreview(index) || getSignedImageUrl(slide.image)]"
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
                    v-model="slideImages[index]"
                    :admin-login-path="adminLoginPath"
                    endpoint-type="supplier-page"
                    accept="image/*"
                    :max-size="5"
                    @upload-success="(data) => handleSlideImageUploadSuccess(data, index)"
                  />
                </div>
              </div>
            </el-form-item>
            
            <el-form-item :label="`中文图片描述`">
              <el-input v-model="slide.image.description.zh" placeholder="请输入中文图片描述"></el-input>
            </el-form-item>
            
            <el-form-item :label="`英文图片描述`">
              <el-input v-model="slide.image.description.en" placeholder="Enter English image description"></el-input>
            </el-form-item>
          </div>
        </div>
      </el-card>
      
      <!-- 优势部分 -->
      <el-card class="section-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <h3>供应商优势</h3>
          </div>
        </template>
        
        <div class="section-content">
          <el-form-item label="中文标题">
            <el-input v-model="getAdvantagesSection().title.zh" placeholder="请输入中文标题"></el-input>
          </el-form-item>
          
          <el-form-item label="英文标题">
            <el-input v-model="getAdvantagesSection().title.en" placeholder="Enter English title"></el-input>
          </el-form-item>
          
          <el-form-item label="中文副标题">
            <el-input v-model="getAdvantagesSection().subtitle.zh" placeholder="请输入中文副标题"></el-input>
          </el-form-item>
          
          <el-form-item label="英文副标题">
            <el-input v-model="getAdvantagesSection().subtitle.en" placeholder="Enter English subtitle"></el-input>
          </el-form-item>
          
          <!-- 优势项目列表 -->
          <div v-for="(item, index) in getAdvantagesItems()" :key="index" class="advantage-item">
            <el-divider v-if="index > 0" />
            <h4>优势项目 {{ index + 1 }}</h4>
            
            <el-form-item :label="`编号`">
              <el-input v-model="item.number" placeholder="请输入编号"></el-input>
            </el-form-item>
            
            <el-form-item :label="`中文标题`">
              <el-input
                v-model="item.title.zh"
                type="textarea"
                :rows="3"
                placeholder="请输入中文标题"
                class="large-textarea"
              />
            </el-form-item>
            
            <el-form-item :label="`英文标题`">
              <el-input
                v-model="item.title.en"
                type="textarea"
                :rows="3"
                placeholder="Enter English title"
                class="large-textarea"
              />
            </el-form-item>
            
            <el-form-item :label="`中文描述`">
              <el-input
                v-model="item.description.zh"
                type="textarea"
                :rows="6"
                placeholder="请输入中文描述"
                class="large-textarea"
              />
            </el-form-item>
            
            <el-form-item :label="`英文描述`">
              <el-input
                v-model="item.description.en"
                type="textarea"
                :rows="6"
                placeholder="Enter English description"
                class="large-textarea"
              />
            </el-form-item>
            
            <el-form-item label="优势图片">
              <div class="image-section">
                <!-- 图片预览 -->
                <div class="image-preview-container">
                  <el-image
                    v-if="getAdvantageImagePreviews(index) || getSignedImageUrl(item.image)"
                    :src="getAdvantageImagePreviews(index) || getSignedImageUrl(item.image)"
                    fit="cover"
                    style="width: 100%; height: 100%;"
                    :preview-src-list="[getAdvantageImagePreviews(index) || getSignedImageUrl(item.image)]"
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
                    v-model="advantageImages[index]"
                    :admin-login-path="adminLoginPath"
                    endpoint-type="supplier-page"
                    accept="image/*"
                    :max-size="5"
                    @upload-success="(data) => handleAdvantageImageUploadSuccess(data, index)"
                  />
                </div>
              </div>
            </el-form-item>
            
            <el-form-item :label="`中文图片描述`">
              <el-input v-model="item.image.description.zh" placeholder="请输入中文图片描述"></el-input>
            </el-form-item>
            
            <el-form-item :label="`英文图片描述`">
              <el-input v-model="item.image.description.en" placeholder="Enter English image description"></el-input>
            </el-form-item>
          </div>
        </div>
      </el-card>
      
      <!-- 资质要求部分 -->
      <el-card class="section-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <h3>供应商资质要求</h3>
          </div>
        </template>
        
        <div class="section-content">
          <el-form-item label="中文标题">
            <el-input v-model="getQualificationSection().title.zh" placeholder="请输入中文标题"></el-input>
          </el-form-item>
          
          <el-form-item label="英文标题">
            <el-input v-model="getQualificationSection().title.en" placeholder="Enter English title"></el-input>
          </el-form-item>
          
          <el-form-item label="中文招募对象">
            <el-input v-model="getQualificationSection().recruitmentBadge.zh" placeholder="请输入中文招募对象"></el-input>
          </el-form-item>
          
          <el-form-item label="英文招募对象">
            <el-input v-model="getQualificationSection().recruitmentBadge.en" placeholder="Enter English recruitment target"></el-input>
          </el-form-item>
          
          <!-- 资质要求列表 -->
          <div v-for="(requirement, index) in getQualificationRequirements()" :key="index" class="requirement-item">
            <el-divider v-if="index > 0" />
            <h4>资质要求 {{ index + 1 }}</h4>
            
            <el-form-item :label="`中文要求`">
              <el-input v-model="requirement.zh" placeholder="请输入中文要求"></el-input>
            </el-form-item>
            
            <el-form-item :label="`英文要求`">
              <el-input v-model="requirement.en" placeholder="Enter English requirement"></el-input>
            </el-form-item>
          </div>
          
          <!-- 资质图片 -->
          <el-form-item label="资质要求图片">
            <div class="image-section">
              <!-- 图片预览 -->
              <div class="image-preview-container">
                <el-image
                  v-if="qualificationImagePreview || getSignedImageUrl(getQualificationSection().image)"
                  :src="qualificationImagePreview || getSignedImageUrl(getQualificationSection().image)"
                  fit="cover"
                  style="width: 100%; height: 100%;"
                  :preview-src-list="[qualificationImagePreview || getSignedImageUrl(getQualificationSection().image)]"
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
                  v-model="qualificationImage"
                  :admin-login-path="adminLoginPath"
                  endpoint-type="supplier-page"
                  accept="image/*"
                  :max-size="5"
                  @upload-success="handleQualificationImageUploadSuccess"
                />
              </div>
            </div>
          </el-form-item>
          
          <el-form-item :label="`中文图片描述`">
            <el-input v-model="getQualificationSection().image.description.zh" placeholder="请输入中文图片描述"></el-input>
          </el-form-item>
          
          <el-form-item :label="`英文图片描述`">
            <el-input v-model="getQualificationSection().image.description.en" placeholder="Enter English image description"></el-input>
          </el-form-item>
        </div>
      </el-card>
      
      <!-- 招商品类部分 -->
      <el-card class="section-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <h3>招商品类</h3>
          </div>
        </template>
        
        <div class="section-content">
          <el-form-item label="中文标题">
            <el-input v-model="getCategoriesSection().title.zh" placeholder="请输入中文标题"></el-input>
          </el-form-item>
          
          <el-form-item label="英文标题">
            <el-input v-model="getCategoriesSection().title.en" placeholder="Enter English title"></el-input>
          </el-form-item>
          
          <!-- 品类项目列表 -->
          <div v-for="(item, index) in getCategoriesItems()" :key="index" class="category-item">
            <el-divider v-if="index > 0" />
            <h4>招商品类 {{ index + 1 }}</h4>
            
            <el-form-item :label="`中文名称`">
              <el-input v-model="item.name.zh" placeholder="请输入中文名称"></el-input>
            </el-form-item>
            
            <el-form-item :label="`英文名称`">
              <el-input v-model="item.name.en" placeholder="Enter English name"></el-input>
            </el-form-item>
            
            <el-form-item label="品类图片">
              <div class="image-section">
                <!-- 图片预览 -->
                <div class="image-preview-container">
                  <el-image
                    v-if="getCategoryImagePreviews(index) || getSignedImageUrl(item.image)"
                    :src="getCategoryImagePreviews(index) || getSignedImageUrl(item.image)"
                    fit="cover"
                    style="width: 100%; height: 100%;"
                    :preview-src-list="[getCategoryImagePreviews(index) || getSignedImageUrl(item.image)]"
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
                    v-model="categoryImages[index]"
                    :admin-login-path="adminLoginPath"
                    endpoint-type="supplier-page"
                    accept="image/*"
                    :max-size="5"
                    @upload-success="(data) => handleCategoryImageUploadSuccess(data, index)"
                  />
                </div>
              </div>
            </el-form-item>
            
            <el-form-item :label="`中文图片描述`">
              <el-input v-model="item.image.description.zh" placeholder="请输入中文图片描述"></el-input>
            </el-form-item>
            
            <el-form-item :label="`英文图片描述`">
              <el-input v-model="item.image.description.en" placeholder="Enter English image description"></el-input>
            </el-form-item>
          </div>
        </div>
      </el-card>
      
      <!-- CTA部分 -->
      <el-card class="section-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <h3>行动号召</h3>
          </div>
        </template>
        
        <div class="section-content">
          <el-form-item label="中文标题">
            <el-input v-model="getCtaSection().title.zh" placeholder="请输入中文标题"></el-input>
          </el-form-item>
          
          <el-form-item label="英文标题">
            <el-input v-model="getCtaSection().title.en" placeholder="Enter English title"></el-input>
          </el-form-item>
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
  ElLoading,
  ElImage,
  ElDivider
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
  pageTitle: {
    zh: '',
    en: ''
  },
  sections: [
    {
      type: 'heroCarousel',
      slides: [
        {
          title: {
            zh: '',
            en: ''
          },
          subtitle: {
            zh: '',
            en: ''
          },
          image: {
            key: '',
            description: {
              zh: '',
              en: ''
            }
          }
        }
      ]
    },
    {
      type: 'advantages',
      title: {
        zh: '',
        en: ''
      },
      subtitle: {
        zh: '',
        en: ''
      },
      items: [
        {
          number: '',
          title: {
            zh: '',
            en: ''
          },
          description: {
            zh: '',
            en: ''
          },
          image: {
            key: '',
            description: {
              zh: '',
              en: ''
            }
          }
        }
      ]
    },
    {
      type: 'qualification',
      title: {
        zh: '',
        en: ''
      },
      recruitmentBadge: {
        zh: '',
        en: ''
      },
      requirements: [
        {
          zh: '',
          en: ''
        }
      ],
      image: {
        key: '',
        description: {
          zh: '',
          en: ''
        }
      }
    },
    {
      type: 'categories',
      title: {
        zh: '',
        en: ''
      },
      items: [
        {
          name: {
            zh: '',
            en: ''
          },
          image: {
            key: '',
            description: {
              zh: '',
              en: ''
            }
          }
        }
      ]
    },
    {
      type: 'cta',
      title: {
        zh: '',
        en: ''
      }
    }
  ]
})

const loading = ref(false)
const saving = ref(false)

// 图片上传相关
const slideImages = ref([])
const advantageImages = ref([])
const qualificationImage = ref(null)
const categoryImages = ref([])

// 图片预览URL（用于上传后立即显示）
const slideImagePreviews = ref([])
const advantageImagePreviews = ref([])
const qualificationImagePreview = ref('')
const categoryImagePreviews = ref([])

// 获取轮播图幻灯片
const getHeroCarouselSlides = () => {
  const heroCarouselSection = pageContent.value.sections.find(section => section.type === 'heroCarousel')
  return heroCarouselSection ? heroCarouselSection.slides : []
}

// 获取优势部分
const getAdvantagesSection = () => {
  const advantagesSection = pageContent.value.sections.find(section => section.type === 'advantages')
  return advantagesSection || pageContent.value.sections[1]
}

// 获取优势项目
const getAdvantagesItems = () => {
  const advantagesSection = getAdvantagesSection()
  return advantagesSection.items || []
}

// 获取资质要求部分
const getQualificationSection = () => {
  const qualificationSection = pageContent.value.sections.find(section => section.type === 'qualification')
  return qualificationSection || pageContent.value.sections[2]
}

// 获取资质要求列表
const getQualificationRequirements = () => {
  const qualificationSection = getQualificationSection()
  return qualificationSection.requirements || []
}

// 获取招商品类部分
const getCategoriesSection = () => {
  const categoriesSection = pageContent.value.sections.find(section => section.type === 'categories')
  return categoriesSection || pageContent.value.sections[3]
}

// 获取招商品类项目
const getCategoriesItems = () => {
  const categoriesSection = getCategoriesSection()
  return categoriesSection.items || []
}

// 获取CTA部分
const getCtaSection = () => {
  const ctaSection = pageContent.value.sections.find(section => section.type === 'cta')
  return ctaSection || pageContent.value.sections[4]
}

// 获取带签名的图片URL（兼容对象和字符串格式）
const getSignedImageUrl = (imageField) => {
  if (!imageField) return ''
  
  // 如果是对象格式 { key: 'xxx', signedUrl: 'xxx', description: {...} }
  if (typeof imageField === 'object' && imageField.signedUrl) {
    return imageField.signedUrl
  }
  
  // 如果是对象但没有signedUrl，使用key动态获取
  if (typeof imageField === 'object' && imageField.key) {
    const key = imageField.key
    if (!key) return ''
    if (key.startsWith('http')) return key
    return `/admin${props.adminLoginPath}/supplier-page/image/signed-url?key=${encodeURIComponent(key)}`
  }
  
  // 如果是字符串格式（兼容旧数据）
  if (typeof imageField === 'string') {
    if (imageField.startsWith('http')) return imageField
    return `/admin${props.adminLoginPath}/supplier-page/image/signed-url?key=${encodeURIComponent(imageField)}`
  }
  
  return ''
}

// 处理轮播图图片上传成功
const handleSlideImageUploadSuccess = (data, index) => {
  const slides = getHeroCarouselSlides()
  if (slides[index]) {
    // 更新原始数据中的key
    if (originalData.value && originalData.value.sections) {
      const heroSection = originalData.value.sections.find(s => s.type === 'heroCarousel')
      if (heroSection && heroSection.slides[index]) {
        heroSection.slides[index].image.key = data.key
      }
    }
    // 更新显示数据
    slides[index].image.key = data.key
    // 使用上传接口返回的预览URL更新预览
    if (data.previewUrl) {
      slideImagePreviews.value[index] = data.previewUrl
    }
  }
  ElMessage.success(`轮播图${index+1}图片上传成功`)
}

// 处理优势图片上传成功
const handleAdvantageImageUploadSuccess = (data, index) => {
  const items = getAdvantagesItems()
  if (items[index]) {
    // 更新原始数据中的key
    if (originalData.value && originalData.value.sections) {
      const advantagesSection = originalData.value.sections.find(s => s.type === 'advantages')
      if (advantagesSection && advantagesSection.items[index]) {
        advantagesSection.items[index].image.key = data.key
      }
    }
    // 更新显示数据
    items[index].image.key = data.key
    // 使用上传接口返回的预览URL更新预览
    if (data.previewUrl) {
      advantageImagePreviews.value[index] = data.previewUrl
    }
  }
  ElMessage.success(`优势${index+1}图片上传成功`)
}

// 处理资质图片上传成功
const handleQualificationImageUploadSuccess = (data) => {
  const qualificationSection = getQualificationSection()
  // 更新原始数据中的key
  if (originalData.value && originalData.value.sections) {
    const qualSection = originalData.value.sections.find(s => s.type === 'qualification')
    if (qualSection) {
      qualSection.image.key = data.key
    }
  }
  // 更新显示数据
  qualificationSection.image.key = data.key
  // 使用上传接口返回的预览URL更新预览
  if (data.previewUrl) {
    qualificationImagePreview.value = data.previewUrl
  }
  ElMessage.success('资质图片上传成功')
}

// 处理品类图片上传成功
const handleCategoryImageUploadSuccess = (data, index) => {
  const items = getCategoriesItems()
  if (items[index]) {
    // 更新原始数据中的key
    if (originalData.value && originalData.value.sections) {
      const categoriesSection = originalData.value.sections.find(s => s.type === 'categories')
      if (categoriesSection && categoriesSection.items[index]) {
        categoriesSection.items[index].image.key = data.key
      }
    }
    // 更新显示数据
    items[index].image.key = data.key
    // 使用上传接口返回的预览URL更新预览
    if (data.previewUrl) {
      categoryImagePreviews.value[index] = data.previewUrl
    }
  }
  ElMessage.success(`品类${index+1}图片上传成功`)
}

// 获取轮播图图片预览
const getSlideImagePreview = (index) => {
  return slideImagePreviews.value[index] || ''
}

// 获取优势图片预览
const getAdvantageImagePreviews = (index) => {
  return advantageImagePreviews.value[index] || ''
}

// 获取品类图片预览
const getCategoryImagePreviews = (index) => {
  return categoryImagePreviews.value[index] || ''
}

// 加载页面数据
const loadPageData = async () => {
  console.log('SupplierPage: loadPageData called');
  loading.value = true
  try {
    const response = await fetch(`/admin${props.adminLoginPath}/supplier-page/data`, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json',
      }
    })
    
    console.log('SupplierPage: API response status', response.status);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const result = await response.json()
    console.log('SupplierPage: API response data', result);
    
    if (result.success && result.data && result.data.pageInfo) {
      try {
        const content = JSON.parse(result.data.pageInfo.content)
        
        // 提取原始key（用于保存）
        const extractedKeys = extractImageKeys(content)
        originalData.value = extractedKeys
        
        // 设置显示数据（使用signedUrl显示）
        pageContent.value = content
        
        // 初始化图片数组
        const slides = getHeroCarouselSlides()
        const advantages = getAdvantagesItems()
        const categories = getCategoriesItems()
        
        slideImages.value = Array(slides.length).fill('')
        advantageImages.value = Array(advantages.length).fill('')
        categoryImages.value = Array(categories.length).fill('')
        qualificationImage.value = ''
        
        // 初始化预览数组
        slideImagePreviews.value = Array(slides.length).fill('')
        advantageImagePreviews.value = Array(advantages.length).fill('')
        categoryImagePreviews.value = Array(categories.length).fill('')
        qualificationImagePreview.value = ''
        
        console.log('SupplierPage: Data loaded successfully');
        console.log('SupplierPage: 原始keys', originalData.value);
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
      pageTitle: pageContent.value.pageTitle,
      sections: pageContent.value.sections.map((section, sectionIndex) => {
        const originalSection = originalData.value.sections[sectionIndex] || section
        
        // 基础section数据
        const savedSection = {
          type: section.type,
          title: section.title,
          subtitle: section.subtitle
        }
        
        // 处理轮播图
        if (section.type === 'heroCarousel' && section.slides) {
          savedSection.slides = section.slides.map((slide, slideIndex) => ({
            title: slide.title,
            subtitle: slide.subtitle,
            image: originalSection.slides?.[slideIndex]?.image || { key: '', description: { zh: '', en: '' } }
          }))
        }
        
        // 处理优势项
        if (section.type === 'advantages' && section.items) {
          savedSection.items = section.items.map((item, itemIndex) => ({
            number: item.number,
            title: item.title,
            description: item.description,
            image: originalSection.items?.[itemIndex]?.image || { key: '', description: { zh: '', en: '' } }
          }))
        }
        
        // 处理资质图片
        if (section.type === 'qualification') {
          savedSection.recruitmentBadge = section.recruitmentBadge
          savedSection.requirements = section.requirements
          savedSection.image = originalSection.image || { key: '', description: { zh: '', en: '' } }
        }
        
        // 处理品类图片
        if (section.type === 'categories' && section.items) {
          savedSection.items = section.items.map((item, itemIndex) => ({
            name: item.name,
            image: originalSection.items?.[itemIndex]?.image || { key: '', description: { zh: '', en: '' } }
          }))
        }
        
        return savedSection
      })
    }
    
    console.log('SupplierPage: 保存的数据', dataToSave);
    
    const response = await fetch(`/admin${props.adminLoginPath}/supplier-page/save`, {
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

// 从内容数据中提取原始key（递归处理）
const extractImageKeys = (data) => {
  const result = JSON.parse(JSON.stringify(data)) // 深度复制
  
  // 处理sections中的图片
  if (result.sections && Array.isArray(result.sections)) {
    result.sections.forEach(section => {
      // 处理轮播图
      if (section.type === 'heroCarousel' && section.slides && Array.isArray(section.slides)) {
        section.slides.forEach(slide => {
          if (slide.image) {
            slide.image = getImageKeyFromField(slide.image)
          }
        })
      }
      
      // 处理优势项
      if (section.type === 'advantages' && section.items && Array.isArray(section.items)) {
        section.items.forEach(item => {
          if (item.image) {
            item.image = getImageKeyFromField(item.image)
          }
        })
      }
      
      // 处理资质图片
      if (section.type === 'qualification' && section.image) {
        section.image = getImageKeyFromField(section.image)
      }
      
      // 处理品类图片
      if (section.type === 'categories' && section.items && Array.isArray(section.items)) {
        section.items.forEach(item => {
          if (item.image) {
            item.image = getImageKeyFromField(item.image)
          }
        })
      }
    })
  }
  
  return result
}

// 从图片字段中提取key（保留description）
const getImageKeyFromField = (imageField) => {
  if (!imageField) {
    return { key: '', description: { zh: '', en: '' } }
  }
  
  // 如果是对象格式 { key: 'xxx', signedUrl: 'xxx', description: {...} }
  if (typeof imageField === 'object') {
    return {
      key: imageField.key || '',
      description: imageField.description || { zh: '', en: '' }
    }
  }
  
  // 如果是字符串（旧数据格式）
  if (typeof imageField === 'string') {
    return {
      key: imageField,
      description: { zh: '', en: '' }
    }
  }
  
  return { key: '', description: { zh: '', en: '' } }
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
.supplier-page-container {
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

.slide-item h4, .advantage-item h4, .requirement-item h4, .category-item h4 {
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
  .supplier-page-container {
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