<template>
  <div class="help-center-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2 class="page-title">
        <el-icon class="title-icon"><QuestionFilled /></el-icon>
        常见问题管理
      </h2>
      <div class="header-actions">
        <el-button type="primary" @click="showCreateDialog" :icon="Plus">
          添加问题
        </el-button>
        <el-button type="danger" @click="handleBatchDelete" :icon="Delete" :disabled="selectedQuestions.length === 0">
          批量删除 ({{ selectedQuestions.length }})
        </el-button>
        <el-button type="primary" @click="refreshData" :icon="Refresh">
          刷新数据
        </el-button>
      </div>
    </div>
    
    <!-- 搜索和筛选区域 -->
    <el-card class="filter-card">
      <div class="filter-header">
        <el-icon class="filter-icon"><Search /></el-icon>
        <span class="filter-title">筛选条件</span>
      </div>
      <el-form :model="searchForm" class="search-form" label-position="left" label-width="80px">
        <el-row :gutter="20" align="middle">
          <el-col :span="6" :xs="24">
            <el-form-item label="一级分类">
              <el-select v-model="searchForm.categoryId" placeholder="请选择一级分类" clearable style="width: 100%;" @change="handleCategoryFilterChange">
                <el-option label="全部" value="" />
                <el-option
                  v-for="category in categories"
                  :key="category.id"
                  :label="category.name"
                  :value="category.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="6" :xs="24">
            <el-form-item label="二级分类">
              <el-select v-model="searchForm.subCategoryId" placeholder="请选择二级分类" clearable style="width: 100%;">
                <el-option label="全部" value="" />
                <el-option
                  v-for="subCategory in filterSubCategories"
                  :key="subCategory.id"
                  :label="subCategory.name"
                  :value="subCategory.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="6" :xs="24">
            <el-form-item label="关键词">
              <el-input v-model="searchForm.keyword" placeholder="请输入问题关键词" />
            </el-form-item>
          </el-col>
          <el-col :span="6" :xs="24" class="action-col">
            <el-form-item label=" ">
              <div class="form-actions">
                <el-button type="primary" @click="searchQuestions" :icon="Search">
                  搜索问题
                </el-button>
                <el-button @click="resetSearch" :icon="RefreshLeft">
                  重置条件
                </el-button>
              </div>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-card>
    
    <!-- 问题列表表格 -->
    <el-card class="table-card">
      <template #header>
        <div class="table-header">
          <div class="table-header-title">
            <el-icon class="table-icon"><List /></el-icon>
            常见问题列表
          </div>
          <div class="table-header-info">
            共 {{ pagination.totalItems }} 条记录
          </div>
        </div>
      </template>
      
      <el-table 
        :data="questions" 
        class="question-table" 
        v-loading="loading"
        :fit="true"
        :border="false"
        :header-cell-style="{ textAlign: 'center' }"
        :cell-style="{ textAlign: 'center' }"
        :stripe="true"
        empty-text="暂无问题"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column label="序号" width="60" fixed>
          <template #default="scope">
            {{ (pagination.currentPage - 1) * pagination.itemsPerPage + scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column prop="question" label="问题标题" min-width="200" show-overflow-tooltip />
        <el-table-column prop="categoryName" label="一级分类" min-width="120" />
        <el-table-column prop="subCategoryName" label="二级分类" min-width="120" />
        <el-table-column prop="viewCount" label="浏览次数" min-width="100" sortable />
        <el-table-column prop="solvedCount" label="有帮助" min-width="100" sortable>
          <template #default="scope">
            <el-tag type="success">{{ scope.row.solvedCount }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="unsolvedCount" label="无帮助" min-width="100" sortable>
          <template #default="scope">
            <el-tag type="warning">{{ scope.row.unsolvedCount }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="sortOrder" label="排序" min-width="80" sortable />
        <el-table-column prop="createdAt" label="创建时间" min-width="160" sortable>
          <template #default="scope">
            <div class="time-cell">
              <div class="date">{{ formatDate(scope.row.createdAt) }}</div>
              <div class="time">{{ formatTime(scope.row.createdAt) }}</div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" @click="showEditDialog(scope.row)" :icon="Edit">
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="handleDelete(scope.row)" :icon="Delete">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 分页 -->
    <div class="pagination-container">
      <el-pagination
        v-model:current-page="pagination.currentPage"
        v-model:page-size="pagination.itemsPerPage"
        :page-sizes="[10, 20, 50, 100]"
        :total="pagination.totalItems"
        :pager-count="11"
        layout="total, sizes, prev, pager, next, jumper"
        prev-text="上一页"
        next-text="下一页"
        background
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 创建/编辑对话框 -->
    <el-dialog 
      v-model="dialogVisible" 
      :title="dialogTitle"
      width="1400px"
      :close-on-click-modal="false"
    >
      
      <el-form :model="currentQuestion" label-width="120px">
        <el-form-item label="问题标题" required>
          <template #label>
            问题标题 <span class="required">*</span>
          </template>
          <el-input v-model="currentQuestion.question" placeholder="请输入问题标题（中文）" />
        </el-form-item>
        <el-form-item label="问题标题(英文)">
          <el-input v-model="currentQuestion.questionEn" placeholder="请输入问题标题（英文）" />
          <div class="dialog-note" style="color: #ccc;">英文标题为空时，将默认显示中文标题</div>
        </el-form-item>
        <!-- 一级分类选择 -->
        <el-form-item label="一级分类" required>
          <template #label>
            一级分类 <span class="required">*</span>
          </template>
          <el-select 
            v-model="currentQuestion.categoryId" 
            placeholder="请选择一级分类" 
            style="width: 100%;"
            @change="handleCategoryChange"
          >
            <el-option
              v-for="category in faqCategories"
              :key="category.id"
              :label="category.name"
              :value="category.id"
            />
          </el-select>
        </el-form-item>
        <!-- 二级分类选择 -->
        <el-form-item label="二级分类" v-if="currentQuestion.categoryId">
          <el-select 
            v-model="currentQuestion.subCategoryId" 
            placeholder="请选择二级分类" 
            style="width: 100%;"
          >
            <el-option
              v-for="subCategory in subCategories"
              :key="subCategory.id"
              :label="subCategory.name"
              :value="subCategory.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="currentQuestion.sortOrder" :min="0" :max="9999" />
        </el-form-item>
        <!-- 图片上传 -->
        <el-form-item label="相关图片">
          <div class="image-upload-container">
            <div 
              v-for="(image, index) in currentQuestion.images" 
              :key="index" 
              class="image-preview-item"
            >
              <img :src="getProcessedImageUrl(image)" class="image-preview" />
              <el-button 
                type="danger" 
                size="small" 
                @click="removeImage(index)"
                class="remove-image-btn"
              >
                移除
              </el-button>
            </div>
            <file-upload
              v-if="currentQuestion.images.length < 10"
              :key="`new-image-upload-${newImageUploadKey}`"
              v-model="newImageKey"
              :admin-login-path="adminLoginPath"
              accept="image/*"
              :max-size="5"
              :show-remove="false"
              endpoint-type="supplier"
              @upload-success="handleImageUploadSuccess"
              class="image-uploader"
            />
          </div>
          <div class="image-upload-note">
            最多可上传10张图片，每张图片大小不超过5MB
          </div>
        </el-form-item>

        <el-form-item label="问题答案">
          <rich-text-editor 
            v-model="currentQuestion.content"
            :admin-login-path="adminLoginPath"
            :height="'400px'"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="handleSave" :loading="saving">
            保存
          </el-button>
          <el-button @click="dialogVisible = false">取消</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, defineExpose, computed } from 'vue'
import {
  ElCard,
  ElTable,
  ElTableColumn,
  ElButton,
  ElForm,
  ElFormItem,
  ElInput,
  ElInputNumber,
  ElSelect,
  ElOption,
  ElTag,
  ElMessage,
  ElMessageBox,
  ElPagination,
  ElRow,
  ElCol,
  ElIcon,
  ElDialog,
  vLoading
} from 'element-plus'
import {
  QuestionFilled,
  Search,
  Refresh,
  RefreshLeft,
  List,
  Plus,
  Edit,
  Delete
} from '@element-plus/icons-vue'
import RichTextEditor from './RichTextEditor.vue'
import FileUpload from './FileUpload.vue'

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

const questions = ref([])
const categories = ref([])
const faqCategories = ref([]) // 专门用于FAQ的一级分类
const subCategories = ref([]) // 二级分类
const allSubCategories = ref([]) // 所有二级分类
const loading = ref(false)
const saving = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('添加问题')
const pagination = ref({
  currentPage: 1,
  totalPages: 1,
  totalItems: 0,
  itemsPerPage: 20
})

const searchForm = ref({
  keyword: '',
  categoryId: '',
  subCategoryId: ''
})

const currentQuestion = ref({
  id: null,
  question: '',
  questionEn: '',
  content: '',
  images: [], // 添加图片字段
  categoryId: null,
  subCategoryId: null,
  sortOrder: 0
})

// 用于存储图片预览URL的临时数组（key -> previewUrl映射）
const imagePreviewUrls = ref({})

// 用于上传新图片的临时变量和key
const newImageKey = ref('') // 用于新增图片的临时key
const newImageUploadKey = ref(0) // 用于强制刷新新的图片上传组件

// 选中的问题
const selectedQuestions = ref([])

// 计算属性：根据选择的一级分类过滤二级分类
const filterSubCategories = computed(() => {
  if (!searchForm.value.categoryId) {
    return []
  }
  return allSubCategories.value.filter(sub => sub.categoryId === searchForm.value.categoryId)
})

// 处理表格选择变化
const handleSelectionChange = (selection) => {
  selectedQuestions.value = selection
}

// 处理一级分类筛选变化
const handleCategoryFilterChange = (categoryId) => {
  // 清空二级分类选择
  searchForm.value.subCategoryId = ''
}

// 加载数据
const loadQuestionData = async (page = 1, limit = 20) => {
  loading.value = true
  try {
    const params = new URLSearchParams({
      page: page,
      limit: limit,
      keyword: searchForm.value.keyword,
      categoryId: searchForm.value.categoryId,
      subCategoryId: searchForm.value.subCategoryId
    })
    
    const url = `/admin${props.adminLoginPath}/help-center/faq/list?${params}`
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    
    const result = await response.json()
    
    if (result.success) {
      questions.value = result.data
      categories.value = result.categories
      pagination.value = result.pagination
      // 收集所有二级分类数据
      const subCategorySet = new Set()
      allSubCategories.value = []
      result.data.forEach(question => {
        if (question.subCategoryId && question.subCategoryName) {
          const subCategoryKey = `${question.subCategoryId}-${question.categoryId}`
          if (!subCategorySet.has(subCategoryKey)) {
            subCategorySet.add(subCategoryKey)
            allSubCategories.value.push({
              id: question.subCategoryId,
              name: question.subCategoryName,
              categoryId: question.categoryId
            })
          }
        }
      })
    } else {
      ElMessage.error(result.message || '加载数据失败')
    }
  } catch (error) {
    ElMessage.error('加载数据失败: ' + error.message)
  } finally {
    loading.value = false
  }
}

// 刷新数据
const refreshData = () => {
  loadQuestionData(pagination.value.currentPage, pagination.value.itemsPerPage)
}

// 搜索问题
const searchQuestions = () => {
  pagination.value.currentPage = 1
  loadQuestionData(1, pagination.value.itemsPerPage)
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    keyword: '',
    categoryId: '',
    subCategoryId: ''
  }
  pagination.value.currentPage = 1
  loadQuestionData(1, pagination.value.itemsPerPage)
}

// 显示创建对话框
const showCreateDialog = () => {
  dialogTitle.value = '添加问题'
  // 只显示category_type为'faq'的分类
  const filteredFaqCategories = categories.value.filter(category => category.categoryType === 'faq')
  currentQuestion.value = {
    id: null,
    question: '',
    questionEn: '',
    content: '',
    images: [],
    categoryId: filteredFaqCategories.length > 0 ? filteredFaqCategories[0].id : null,
    subCategoryId: null,
    sortOrder: 0
  }
  // 重置图片预览URL映射
  imagePreviewUrls.value = {}
  // 重置图片上传键
  newImageKey.value = ''
  newImageUploadKey.value = 0
  // 保存FAQ分类到专门的变量中
  faqCategories.value = filteredFaqCategories
  // 加载选中分类的二级分类
  if (currentQuestion.value.categoryId) {
    loadSubCategories(currentQuestion.value.categoryId)
  }
  dialogVisible.value = true
}

// 显示编辑对话框
const showEditDialog = (question) => {
  dialogTitle.value = '编辑问题'
  // 只显示category_type为'faq'的分类
  const filteredFaqCategories = categories.value.filter(category => category.categoryType === 'faq')
  currentQuestion.value = {
    id: question.id,
    question: question.question,
    questionEn: question.questionEn,
    content: question.content,
    images: [...(question.originalImages || question.images || [])], // 优先使用原始的key数组
    categoryId: question.categoryId,
    subCategoryId: question.subCategoryId,
    sortOrder: question.sortOrder
  }
  
  // 初始化图片预览URL映射（从后端获取带签名的URL）
  imagePreviewUrls.value = {}
  if (question.images && question.originalImages) {
    // 建立原始key到处理后URL的映射
    for (let i = 0; i < question.originalImages.length; i++) {
      const key = question.originalImages[i]
      const url = question.images[i]
      if (key && url) {
        imagePreviewUrls.value[key] = url
      }
    }
  }
  
  // 重置图片上传键
  newImageKey.value = ''
  newImageUploadKey.value = 0
  // 保存FAQ分类到专门的变量中
  faqCategories.value = filteredFaqCategories
  // 加载选中分类的二级分类
  if (question.categoryId) {
    loadSubCategories(question.categoryId)
  }
  dialogVisible.value = true
}

// 处理一级分类变化
const handleCategoryChange = async (categoryId) => {
  // 清空之前选择的二级分类
  currentQuestion.value.subCategoryId = null
  // 加载新的二级分类
  await loadSubCategories(categoryId)
}

// 加载二级分类
const loadSubCategories = async (categoryId) => {
  if (!categoryId) {
    subCategories.value = []
    return
  }
  
  try {
    const response = await fetch(`/admin${props.adminLoginPath}/help-center/sub-categories/${categoryId}`, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    
    const result = await response.json()
    
    if (result.success) {
      subCategories.value = result.data
    } else {
      subCategories.value = []
      ElMessage.error(result.message || '加载二级分类失败')
    }
  } catch (error) {
    subCategories.value = []
    ElMessage.error('加载二级分类失败: ' + error.message)
  }
}

// 处理图片上传成功
const handleImageUploadSuccess = (result) => {
  if (result.key && result.previewUrl) {
    // 添加到图片数组（只保存七牛云返回的key）
    currentQuestion.value.images.push(result.key)
    // 保存key到previewUrl的映射，用于预览
    imagePreviewUrls.value[result.key] = result.previewUrl
    // 清空临时变量
    newImageKey.value = ''
    // 强制刷新上传组件
    newImageUploadKey.value++
    ElMessage.success('图片上传成功')
  } else {
    ElMessage.error('图片上传失败：未返回文件key或预览URL')
  }
}

// 移除图片
const removeImage = (index) => {
  currentQuestion.value.images.splice(index, 1)
}

// 保存问题
const handleSave = async () => {
  if (!currentQuestion.value.question) {
    ElMessage.warning('请输入问题标题')
    return
  }
  if (!currentQuestion.value.categoryId) {
    ElMessage.warning('请选择一级分类')
    return
  }

  // 直接保存，因为images数组中已经是原始的key
  saving.value = true
  try {
    const url = currentQuestion.value.id
      ? `/admin${props.adminLoginPath}/help-center/question/update`
      : `/admin${props.adminLoginPath}/help-center/question/create`
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: JSON.stringify(currentQuestion.value)
    })
    
    const result = await response.json()
    
    if (result.success) {
      ElMessage.success(result.message || '保存成功')
      dialogVisible.value = false
      refreshData()
    } else {
      ElMessage.error(result.message || '保存失败')
    }
  } catch (error) {
    ElMessage.error('保存失败: ' + error.message)
  } finally {
    saving.value = false
  }
}

// 删除问题
const handleDelete = async (question) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除问题"${question.question}"吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    const response = await fetch(`/admin${props.adminLoginPath}/help-center/question/delete`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: JSON.stringify({ id: question.id })
    })
    
    const result = await response.json()
    
    if (result.success) {
      ElMessage.success('删除成功')
      refreshData()
    } else {
      ElMessage.error(result.message || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败: ' + error.message)
    }
  }
}

// 批量删除问题
const handleBatchDelete = async () => {
  if (selectedQuestions.value.length === 0) {
    ElMessage.warning('请先选择要删除的问题')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedQuestions.value.length} 个问题吗？`,
      '确认批量删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    const ids = selectedQuestions.value.map(question => question.id)
    
    const response = await fetch(`/admin${props.adminLoginPath}/help-center/question/batch-delete`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: JSON.stringify({ ids: ids })
    })
    
    const result = await response.json()
    
    if (result.success) {
      ElMessage.success(result.message || '批量删除成功')
      selectedQuestions.value = []
      refreshData()
    } else {
      ElMessage.error(result.message || '批量删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('批量删除失败: ' + error.message)
    }
  }
}

// 处理分页大小变化
const handleSizeChange = (val) => {
  pagination.value.itemsPerPage = val
  loadQuestionData(pagination.value.currentPage, val)
}

// 处理当前页变化
const handleCurrentChange = (val) => {
  pagination.value.currentPage = val
  loadQuestionData(val, pagination.value.itemsPerPage)
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

// 格式化时间
const formatTime = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// 获取处理后的图片URL（如果是key则返回处理后的URL，如果是URL则直接返回）
const getProcessedImageUrl = (image) => {
  // 如果已经是完整URL，则直接返回
  if (image.startsWith('http')) {
    return image;
  }
  // 如果有对应的预览URL，返回预览URL
  if (imagePreviewUrls.value[image]) {
    return imagePreviewUrls.value[image];
  }
  // 否则构造七牛云URL（这里简化处理，实际应该从后端获取处理后的URL）
  return `http://t51c3boh7.bkt.gdipper.com/${image}`;
};

// 组件挂载时加载数据
onMounted(() => {
  if (props.autoLoad) {
    loadQuestionData()
  }
})

// 暴露方法给父组件调用
defineExpose({
  loadQuestionData
})
</script>

<style scoped>
.help-center-container {
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

.filter-card {
  margin-bottom: 20px;
  width: 100%;
}

.filter-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.filter-icon {
  margin-right: 10px;
  vertical-align: middle;
}

.filter-title {
  font-size: 18px;
  font-weight: bold;
  display: flex;
  align-items: center;
}

.search-form {
  width: 100%;
}

.search-form :deep(.el-form-item) {
  margin-bottom: 0;
  display: flex;
  align-items: center;
}

.search-form :deep(.el-form-item__label) {
  width: 80px;
  margin-right: 10px;
  margin-bottom: 0;
  text-align: right;
  flex-shrink: 0;
}

.search-form :deep(.el-form-item__content) {
  width: calc(100% - 90px);
  display: flex;
  align-items: center;
}

.action-col {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.form-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.table-card {
  width: 100%;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.table-header-title {
  font-size: 18px;
  font-weight: bold;
  display: flex;
  align-items: center;
}

.table-icon {
  margin-right: 10px;
  vertical-align: middle;
}

.table-header-info {
  font-size: 14px;
  color: #909399;
}

.question-table {
  width: 100% !important;
  font-size: 14px;
}

.question-table :deep(.el-table__header th) {
  background-color: #f5f7fa;
  color: #606266;
  font-weight: bold;
}

.question-table :deep(.el-table__body td) {
  transition: background-color 0.3s;
}

.question-table :deep(.el-table__row:hover) {
  background-color: #f5f7fa;
}

.question-table :deep(.el-table__row:hover td) {
  background-color: #f5f7fa !important;
}

.question-table :deep(.el-table__fixed .el-table__row:hover td) {
  background-color: #f5f7fa !important;
}

.question-table :deep(.el-table__row:hover .el-table-fixed-column--left) {
  background-color: #f5f7fa !important;
}

.time-cell {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.date {
  font-size: 14px;
  color: #303133;
}

.time {
  font-size: 12px;
  color: #909399;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  width: 100%;
}

/* 图片上传相关样式 */
.image-upload-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: flex-start;
}

.image-preview-item {
  position: relative;
  width: 120px;
  height: 120px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
}

.image-preview {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-image-btn {
  position: absolute;
  top: 4px;
  right: 4px;
  padding: 2px 6px;
  font-size: 12px;
}

.image-uploader {
  width: 120px;
  height: 120px;
  border: 1px dashed #d9d9d9;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #fafafa;
  cursor: pointer;
  transition: border-color 0.3s;
}

.image-uploader:hover {
  border-color: #409eff;
}

.image-uploader :deep(.file-uploader) {
  width: 120px;
  height: 120px;
  border: none;
  border-radius: 4px;
}

.image-uploader :deep(.uploader-icon) {
  width: 120px;
  height: 120px;
  line-height: 120px;
}

.image-uploader :deep(.file-image-preview) {
  width: 120px;
  height: 120px;
}

.image-upload-note {
  font-size: 12px;
  color: #909399;
  margin-top: 8px;
  display: block;
  width: 100%;
  text-align: left;
}

/* 必填项标记样式 */
.required {
  color: #f56c6c;
}
</style>