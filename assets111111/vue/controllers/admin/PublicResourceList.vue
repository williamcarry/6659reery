<template>
  <div class="public-resource-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2 class="page-title">
        <el-icon class="title-icon"><Picture /></el-icon>
        前端公共资源
      </h2>
      <div class="header-actions">
        <el-button type="primary" @click="showAddDialog" :icon="Plus">
          添加资源
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
            <el-form-item label="资源类型">
              <el-select v-model="searchForm.type" placeholder="请选择类型" clearable style="width: 100%;">
                <el-option label="全部" value="" />
                <el-option label="图片资源" value="image" />
                <el-option label="文字内容" value="text" />
                <el-option label="链接资源" value="link" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="6" :xs="24">
            <el-form-item label="标题">
              <el-input v-model="searchForm.title" placeholder="请输入标题" clearable />
            </el-form-item>
          </el-col>
          <el-col :span="6" :xs="24" class="action-col">
            <el-form-item label=" ">
              <div class="form-actions">
                <el-button type="primary" @click="searchResources" :icon="Search">
                  搜索记录
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
    
    <!-- 资源表格 -->
    <el-card class="table-card">
      <template #header>
        <div class="table-header">
          <div class="table-header-title">
            <el-icon class="table-icon"><List /></el-icon>
            资源列表
          </div>
          <div class="table-header-info">
            共 {{ pagination.totalItems }} 条记录
          </div>
        </div>
      </template>
      
      <el-table 
        :data="resources" 
        class="resource-table" 
        v-loading="loading"
        :fit="true"
        :border="false"
        :header-cell-style="{ textAlign: 'center' }"
        :cell-style="{ textAlign: 'center' }"
      >
        <el-table-column label="序号" min-width="60">
          <template #default="scope">
            {{ (pagination.currentPage - 1) * pagination.itemsPerPage + scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column prop="title" label="标题（中文）" min-width="150" show-overflow-tooltip />
        <el-table-column prop="titleEn" label="标题（英文）" min-width="150" show-overflow-tooltip />
        <el-table-column prop="type" label="资源类型" min-width="100">
          <template #default="scope">
            <el-tag :type="getTypeTagType(scope.row.type)">
              {{ getTypeText(scope.row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="position" label="位置" min-width="80">
          <template #default="scope">
            <el-tag :type="getPositionTagType(scope.row.position)">
              {{ getPositionText(scope.row.position) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="positiontype" label="位置类型" min-width="120" show-overflow-tooltip>
          <template #default="scope">
            <span class="position-type-text">{{ getPositionTypeText(scope.row.positiontype) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="图片预览" min-width="100">
          <template #default="scope">
            <div v-if="scope.row.type === 'image' && scope.row.image">
              <el-image
                :src="scope.row.image"
                fit="cover"
                style="width: 50px; height: 50px; cursor: pointer;"
                :preview-src-list="[scope.row.image]"
                preview-teleported
              />
            </div>
            <div v-else>
              <span>-</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip>
          <template #default="scope">
            <span class="description-text">{{ scope.row.description || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="helpFaqId" label="关联问题" min-width="120" show-overflow-tooltip>
          <template #default="scope">
            <span v-if="scope.row.helpFaqId" class="question-title-text">
              {{ getQuestionTitle(scope.row.helpFaqId) }}
            </span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="updatedAt" label="更新时间" min-width="160" />
        <el-table-column label="操作" min-width="100" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" @click="showEditDialog(scope.row)" :icon="Edit">
              编辑
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页控件 -->
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
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
    
    <!-- 添加/编辑对话框 -->
    <el-dialog 
      v-model="dialogVisible" 
      :title="dialogTitle" 
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form :model="currentResource" label-width="120px" :rules="formRules" ref="resourceForm">
        <el-form-item label="标题（中文）" prop="title">
          <el-input v-model="currentResource.title" placeholder="请输入中文标题" />
        </el-form-item>
        <el-form-item label="标题（英文）" prop="titleEn">
          <el-input v-model="currentResource.titleEn" placeholder="请输入英文标题" />
        </el-form-item>
        <el-form-item label="资源类型" prop="type">
          <el-select v-model="currentResource.type" placeholder="请选择资源类型" style="width: 100%;" :disabled="isEditMode">
            <el-option label="图片资源" value="image" />
            <el-option label="文字内容" value="text" />
            <el-option label="链接资源" value="link" />
          </el-select>
        </el-form-item>
        <el-form-item label="位置" prop="position">
          <el-select v-model="currentResource.position" placeholder="请选择位置" style="width: 100%;" :disabled="isEditMode">
            <el-option label="页头" value="header" />
            <el-option label="页脚" value="footer" />
            <el-option label="供应商介绍" value="supplierIntro" />
            <el-option label="网站底部信息" value="copyright" />
            <el-option label="网站备案号" value="webicp" />
            <el-option label="隐私协议" value="privacyPolicy" />
            <el-option label="服务条款" value="termsOfService" />
          </el-select>
        </el-form-item>
        <el-form-item label="位置类型" prop="positiontype">
          <el-select v-model="currentResource.positiontype" placeholder="请选择位置类型" style="width: 100%;" :disabled="isEditMode">
            <el-option label="页头公众号二维码" value="headerq" />
            <el-option label="页脚官方微信二维码" value="footerqr" />
            <el-option label="页脚跳转到帮助中心的标题和链接" value="footerhelp" />
            <el-option label="供应商简介页面公众号二维码" value="supplierIntroqr" />
            <el-option label="供应商简介页面微信号二维码" value="supplierIntroaccqr" />
            <el-option label="供应商简介页面联系人" value="supplierIntroContract" />
            <el-option label="供应商简介页面联系电话" value="supplierIntroPhone" />
            <el-option label="供应商简介页面联系邮箱" value="supplierIntroEmail" />
            <el-option label="供应商简介页面工作时间" value="supplierIntroWorkTime" />
            <el-option label="网站底部信息" value="copyright" />
            <el-option label="网站备案号" value="webicp" />
            <el-option label="隐私协议与服务条款" value="legalDocuments" />
          </el-select>
        </el-form-item>
        <el-form-item label="图片" v-if="currentResource.type === 'image'" prop="image">
          <file-upload 
            v-model="currentResource.image"
            :admin-login-path="adminLoginPath"
            endpoint-type="public-resource"
            accept="image/*"
            :max-size="5"
          />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input 
            v-model="currentResource.description" 
            type="textarea" 
            :rows="3"
            placeholder="请输入资源描述"
          />
        </el-form-item>
        <el-form-item label="关联问题" prop="helpFaqId">
          <div style="width: 100%; display: flex; gap: 10px;">
            <el-select
              v-model="currentResource.helpFaqId"
              filterable
              remote
              reserve-keyword
              placeholder="请搜索常见问题"
              :remote-method="searchQuestions"
              :loading="searchingQuestions"
              clearable
              style="flex: 1;"
            >
              <el-option
                v-for="item in questionOptions"
                :key="item.id"
                :label="item.label"
                :value="item.id"
              />
            </el-select>
          </div>
          <div style="margin-top: 5px; color: #909399; font-size: 12px;">
            请输入关键词搜索常见问题，支持中文分词智能搜索
          </div>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveResource" :loading="saving">
            {{ saving ? '保存中...' : '确定' }}
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, defineProps, defineExpose } from 'vue'
import {
  ElCard,
  ElTable,
  ElTableColumn,
  ElButton,
  ElPagination,
  ElMessage,
  ElMessageBox,
  ElForm,
  ElFormItem,
  ElInput,
  ElInputNumber,
  ElSelect,
  ElOption,
  ElDialog,
  ElTag,
  ElImage,
  ElIcon,
  ElRow,
  ElCol,
  vLoading
} from 'element-plus'
import {
  Search,
  RefreshLeft,
  Refresh,
  List,
  Picture,
  Plus,
  Edit,
  Delete
} from '@element-plus/icons-vue'
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

// 数据
const resources = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('添加资源')
const isEditMode = ref(false)
const saving = ref(false)
const resourceForm = ref(null)
const questionOptions = ref([])  // 常见问题选项
const searchingQuestions = ref(false)  // 搜索中状态

// 缓存问题标题，避免重复请求
const questionTitleCache = ref(new Map())

// 搜索表单
const searchForm = ref({
  type: '',
  title: ''
})

// 分页数据
const pagination = ref({
  currentPage: 1,
  totalPages: 1,
  totalItems: 0,
  itemsPerPage: 20
})

// 当前编辑的资源
const currentResource = ref({
  id: null,
  title: '',
  titleEn: '',
  type: 'image',
  position: 'header',
  positiontype: null,
  image: '',
  description: '',
  helpFaqId: null
})

// 表单验证规则
const formRules = {
  title: [
    { required: true, message: '请输入中文标题', trigger: 'blur' }
  ],
  titleEn: [
    { required: true, message: '请输入英文标题', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择资源类型', trigger: 'change' }
  ],
  position: [
    { required: true, message: '请选择位置', trigger: 'change' }
  ]
}

// 获取类型标签类型
const getTypeTagType = (type) => {
  const typeMap = {
    'image': 'success',
    'text': 'info',
    'link': 'warning'
  }
  return typeMap[type] || 'info'
}

// 获取类型文本
const getTypeText = (type) => {
  const typeMap = {
    'image': '图片资源',
    'text': '文字内容',
    'link': '链接资源'
  }
  return typeMap[type] || type
}

// 获取位置标签类型
const getPositionTagType = (position) => {
  const positionMap = {
    'header': 'success',
    'footer': 'warning',
    'supplierIntro': 'primary',
    'copyright': 'info',
    'webicp': 'info',
    'privacyPolicy': 'danger',
    'termsOfService': 'danger'
  }
  return positionMap[position] || 'info'
}

// 获取位置文本
const getPositionText = (position) => {
  const positionMap = {
    'header': '页头',
    'footer': '页脚',
    'supplierIntro': '供应商介绍',
    'copyright': '网站底部信息',
    'webicp': '网站备案号',
    'privacyPolicy': '隐私协议',
    'termsOfService': '服务条款'
  }
  return positionMap[position] || position
}

// 获取位置类型标签类型
const getPositionTypeTagType = (positiontype) => {
  const positionTypeMap = {
    'headerq': 'success',
    'footerqr': 'warning',
    'footerhelp': 'info',
    'copyright': 'info',
    'webicp': 'info',
    'legalDocuments': 'danger'
  }
  return positionTypeMap[positiontype] || 'info'
}

// 获取位置类型文本
const getPositionTypeText = (positiontype) => {
  const positionTypeMap = {
    'headerq': '页头公众号二维码',
    'footerqr': '页脚官方微信二维码',
    'footerhelp': '页脚跳转到帮助中心的标题和链接',
    'supplierIntroqr': '供应商简介页面公众号二维码',
    'supplierIntroaccqr': '供应商简介页面微信号二维码',
    'supplierIntroContract': '供应商简介页面联系人',
    'supplierIntroPhone': '供应商简介页面联系电话',
    'supplierIntroEmail': '供应商简介页面联系邮箱',
    'supplierIntroWorkTime': '供应商简介页面工作时间',
    'copyright': '网站底部信息',
    'webicp': '网站备案号',
    'legalDocuments': '隐私协议与服务条款'
  }
  return positionTypeMap[positiontype] || positiontype || '-'
}

// 加载资源数据
const loadResourceData = async (page = 1, limit = 20) => {
  loading.value = true
  try {
    const params = new URLSearchParams({
      page: page,
      limit: limit,
      type: searchForm.value.type,
      title: searchForm.value.title
    })
    
    const url = `/admin${props.adminLoginPath}/public-resource/list?${params}`
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    
    const result = await response.json()
    
    if (result.success) {
      resources.value = result.data
      pagination.value = result.pagination
      
      // 预加载所有关联问题的标题
      preloadQuestionTitles(result.data)
    } else {
      ElMessage.error(result.message || '加载数据失败')
    }
  } catch (error) {
    ElMessage.error('加载数据失败: ' + error.message)
  } finally {
    loading.value = false
  }
}

// 预加载关联问题的标题
const preloadQuestionTitles = async (resources) => {
  // 收集所有需要加载的问题ID
  const questionIds = resources
    .filter(resource => resource.helpFaqId)
    .map(resource => resource.helpFaqId)
    .filter((id, index, arr) => arr.indexOf(id) === index) // 去重
  
  // 批量加载问题标题
  const promises = questionIds.map(id => loadQuestionTitle(id))
  await Promise.all(promises)
}

// 刷新数据
const refreshData = () => {
  loadResourceData(pagination.value.currentPage, pagination.value.itemsPerPage)
}

// 搜索资源
const searchResources = () => {
  pagination.value.currentPage = 1
  loadResourceData(1, pagination.value.itemsPerPage)
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    type: '',
    title: ''
  }
  pagination.value.currentPage = 1
  loadResourceData(1, pagination.value.itemsPerPage)
}

// 处理分页大小变化
const handleSizeChange = (val) => {
  pagination.value.itemsPerPage = val
  loadResourceData(pagination.value.currentPage, val)
}

// 处理当前页变化
const handleCurrentChange = (val) => {
  pagination.value.currentPage = val
  loadResourceData(val, pagination.value.itemsPerPage)
}

// 显示添加对话框
const showAddDialog = () => {
  dialogTitle.value = '添加资源'
  isEditMode.value = false
  currentResource.value = {
    id: null,
    title: '',
    titleEn: '',
    type: 'image',
    position: 'header',
    positiontype: null,
    image: '',
    description: '',
    helpFaqId: null
  }
  questionOptions.value = []  // 清空问题选项
  dialogVisible.value = true
}

// 显示编辑对话框
const showEditDialog = async (resource) => {
  dialogTitle.value = '编辑资源'
  isEditMode.value = true
  
  // 如果是图片类型，需要获取签名URL
  let imageValue = resource.imageKey || resource.image || ''
  if (resource.type === 'image' && resource.imageKey && !resource.imageKey.startsWith('http')) {
    try {
      const response = await fetch(`/admin${props.adminLoginPath}/public-resource/image/signed-url`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ key: resource.imageKey })
      })
      const result = await response.json()
      if (result.success) {
        imageValue = result.url // 使用签名URL作为预览
      }
    } catch (error) {
      console.error('获取签名URL失败:', error)
    }
  }
  
  currentResource.value = {
    id: resource.id,
    title: resource.title,
    titleEn: resource.titleEn,
    type: resource.type,
    position: resource.position,
    positiontype: resource.positiontype,
    image: imageValue,
    description: resource.description,
    helpFaqId: resource.helpFaqId
  }
  
  // 如果有关联问题ID，加载对应的问题信息到选项中
  if (resource.helpFaqId) {
    await loadQuestionById(resource.helpFaqId)
  } else {
    questionOptions.value = []
  }
  
  dialogVisible.value = true
}

// 根据ID加载问题信息
const loadQuestionById = async (questionId) => {
  try {
    // 调用API获取单个问题的详细信息
    const response = await fetch(`/shop/api/help/question/${questionId}`)
    
    const result = await response.json()
    
    if (result.success && result.data) {
      // 构造与搜索结果相同格式的数据
      const questionData = {
        id: result.data.id,
        question: result.data.question,
        questionEn: result.data.questionEn,
        label: `${result.data.question} / ${result.data.questionEn}`
      }
      questionOptions.value = [questionData]
    } else {
      // 如果API没有返回结果，回退到显示ID
      questionOptions.value = [{
        id: questionId,
        label: `问题 ID: ${questionId}`,
        question: '',
        questionEn: ''
      }]
    }
  } catch (error) {
    console.error('加载问题信息失败:', error)
    // 如果API调用失败，回退到显示ID
    questionOptions.value = [{
      id: questionId,
      label: `问题 ID: ${questionId}`,
      question: '',
      questionEn: ''
    }]
  }
}

// 保存资源
const saveResource = async () => {
  // 验证表单
  if (!resourceForm.value) return
  
  try {
    await resourceForm.value.validate()
  } catch (error) {
    return
  }
  
  saving.value = true
  
  try {
    const url = isEditMode.value 
      ? `/admin${props.adminLoginPath}/public-resource/update/${currentResource.value.id}`
      : `/admin${props.adminLoginPath}/public-resource/create`
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(currentResource.value)
    })
    
    const result = await response.json()
    
    if (result.success) {
      ElMessage.success(result.message || (isEditMode.value ? '更新成功' : '添加成功'))
      dialogVisible.value = false
      loadResourceData(pagination.value.currentPage, pagination.value.itemsPerPage)
    } else {
      ElMessage.error(result.message || '操作失败')
    }
  } catch (error) {
    ElMessage.error('操作失败: ' + error.message)
  } finally {
    saving.value = false
  }
}

// 删除资源（已禁用）
const deleteResource = async (resource) => {
  // 前端公共资源不允许删除
  ElMessage.warning('前端公共资源不允许删除，如需修改请使用编辑功能')
  return
}

// 获取问题标题
const getQuestionTitle = (questionId) => {
  // 如果缓存中有标题，直接返回
  if (questionTitleCache.value.has(questionId)) {
    return questionTitleCache.value.get(questionId)
  }
  
  // 如果没有缓存，返回ID并尝试获取标题
  loadQuestionTitle(questionId)
  return questionId
}

// 加载问题标题
const loadQuestionTitle = async (questionId) => {
  // 如果已经在缓存中，直接返回
  if (questionTitleCache.value.has(questionId)) {
    return questionTitleCache.value.get(questionId)
  }
  
  try {
    // 调用API获取单个问题的详细信息
    const response = await fetch(`/shop/api/help/question/${questionId}`)
    const result = await response.json()
    
    if (result.success && result.data) {
      const title = `${result.data.question} / ${result.data.questionEn}`
      // 缓存标题
      questionTitleCache.value.set(questionId, title)
      return title
    }
  } catch (error) {
    console.error('加载问题标题失败:', error)
  }
  
  // 如果获取失败，返回ID
  return questionId
}

// 显示问题详情
const showQuestionDetail = async (questionId) => {
  try {
    const response = await fetch(`/shop/api/help/question/${questionId}`)
    const result = await response.json()
    
    if (result.success && result.data) {
      ElMessage.info(`问题标题: ${result.data.question}\n英文标题: ${result.data.questionEn}`)
    }
  } catch (error) {
    console.error('获取问题详情失败:', error)
    ElMessage.error('获取问题详情失败')
  }
}

// 搜索常见问题
const searchQuestions = async (query) => {
  if (!query || query.trim().length === 0) {
    questionOptions.value = []
    return
  }
  
  searchingQuestions.value = true
  try {
    const response = await fetch(`/admin${props.adminLoginPath}/public-resource/search-questions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ keyword: query.trim() })
    })
    
    const result = await response.json()
    
    if (result.success) {
      questionOptions.value = result.data
    } else {
      ElMessage.error(result.message || '搜索失败')
      questionOptions.value = []
    }
  } catch (error) {
    ElMessage.error('搜索失败: ' + error.message)
    questionOptions.value = []
  } finally {
    searchingQuestions.value = false
  }
}

// 组件挂载时加载数据
onMounted(() => {
  if (props.autoLoad) {
    loadResourceData()
  }
})

// 暴露方法给父组件调用
defineExpose({
  loadResourceData
})
</script>

<style scoped>
.public-resource-container {
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

.resource-table {
  width: 100% !important;
  font-size: 14px;
}

.resource-table :deep(.el-table__header th) {
  background-color: #f5f7fa;
  color: #606266;
  font-weight: bold;
}

.description-text {
  font-size: 14px;
  color: #303133;
}

.position-type-text {
  font-size: 14px;
  color: #303133;
  display: inline-block;
  width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.question-title-text {
  font-size: 14px;
  color: #303133;
  display: inline-block;
  width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>