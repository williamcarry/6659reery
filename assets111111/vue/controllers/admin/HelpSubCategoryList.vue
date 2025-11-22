<template>
  <div class="help-subcategory-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2 class="page-title">
        <el-icon class="title-icon"><Folder /></el-icon>
        帮助二级分类
      </h2>
      <div class="header-actions">
        <el-button type="primary" @click="showCreateDialog" :icon="Plus">
          添加二级分类
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
            <el-form-item label="分类类型">
              <el-select v-model="searchForm.categoryType" placeholder="请选择类型" clearable style="width: 100%;" @change="handleCategoryTypeChange">
                <el-option label="全部" value="" />
                <el-option label="常见问题" value="faq" />
                <el-option label="操作指引" value="guide" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="6" :xs="24">
            <el-form-item label="一级分类">
              <el-select v-model="searchForm.categoryId" placeholder="请选择一级分类" clearable style="width: 100%;">
                <el-option 
                  v-for="category in availableCategories" 
                  :key="category.id" 
                  :label="category.name" 
                  :value="category.id" 
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="6" :xs="24">
            <el-form-item label="关键词">
              <el-input v-model="searchForm.keyword" placeholder="请输入分类名称" />
            </el-form-item>
          </el-col>
          <el-col :span="6" :xs="24" class="action-col">
            <el-form-item label=" ">
              <div class="form-actions">
                <el-button type="primary" @click="searchSubCategories" :icon="Search">
                  搜索分类
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
    
    <!-- 分类列表表格 -->
    <el-card class="table-card">
      <template #header>
        <div class="table-header">
          <div class="table-header-title">
            <el-icon class="table-icon"><List /></el-icon>
            二级分类列表
          </div>
          <div class="table-header-info">
            共 {{ pagination.totalItems }} 条记录
          </div>
        </div>
      </template>
      
      <el-table 
        :data="subCategories" 
        class="subcategory-table" 
        v-loading="loading"
        :fit="true"
        :border="false"
        :header-cell-style="{ textAlign: 'center' }"
        :cell-style="{ textAlign: 'center' }"
        :stripe="true"
        empty-text="暂无分类"
      >
        <el-table-column label="序号" width="60" fixed>
          <template #default="scope">
            {{ (pagination.currentPage - 1) * pagination.itemsPerPage + scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column prop="name" label="分类名称" min-width="150" show-overflow-tooltip />
        <el-table-column prop="nameEn" label="英文名称" min-width="150" show-overflow-tooltip />
        <el-table-column prop="categoryName" label="所属一级分类" min-width="150" show-overflow-tooltip />
        <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
        <el-table-column prop="sortOrder" label="排序" min-width="80" sortable />
        <el-table-column prop="questionCount" label="问题数量" min-width="100" sortable>
          <template #default="scope">
            <el-tag :type="scope.row.questionCount > 0 ? 'primary' : 'info'">
              {{ scope.row.questionCount }}
            </el-tag>
          </template>
        </el-table-column>
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
            <el-button type="danger" size="small" @click="handleDelete(scope.row)" :icon="Delete" :disabled="scope.row.questionCount > 0">
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
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form :model="currentSubCategory" label-width="120px">
        <el-form-item label="分类类型" required>
          <el-select v-model="currentSubCategory.categoryType" placeholder="请选择分类类型" style="width: 100%;" @change="handleDialogCategoryTypeChange">
            <el-option label="常见问题" value="faq" />
            <el-option label="操作指引" value="guide" />
          </el-select>
        </el-form-item>
        <el-form-item label="一级分类" required>
          <el-select v-model="currentSubCategory.categoryId" placeholder="请选择一级分类" style="width: 100%;">
            <el-option 
              v-for="category in dialogCategories" 
              :key="category.id" 
              :label="category.name" 
              :value="category.id" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="分类名称" required>
          <el-input v-model="currentSubCategory.name" placeholder="请输入分类名称（中文）" />
        </el-form-item>
        <el-form-item label="英文名称">
          <el-input v-model="currentSubCategory.nameEn" placeholder="请输入分类名称（英文）" />
          <div class="form-item-hint">如果不填写英文名，网站默认显示中文名</div>
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="currentSubCategory.sortOrder" :min="0" :max="9999" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input 
            v-model="currentSubCategory.description" 
            type="textarea" 
            :rows="3" 
            placeholder="请输入分类描述" 
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSave" :loading="saving">
            保存
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, defineExpose } from 'vue'
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
  Folder,
  Search,
  Refresh,
  RefreshLeft,
  List,
  Plus,
  Edit,
  Delete
} from '@element-plus/icons-vue'

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

const subCategories = ref([])
const loading = ref(false)
const saving = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('添加二级分类')
const pagination = ref({
  currentPage: 1,
  totalPages: 1,
  totalItems: 0,
  itemsPerPage: 20
})

const searchForm = ref({
  keyword: '',
  categoryType: '',
  categoryId: ''
})

const currentSubCategory = ref({
  id: null,
  name: '',
  nameEn: '',
  description: '',
  categoryType: 'faq',
  categoryId: null,
  sortOrder: 0
})

// 一级分类列表
const availableCategories = ref([])
const dialogCategories = ref([])

// 加载数据
const loadSubCategoryData = async (page = 1, limit = 20) => {
  loading.value = true
  try {
    const params = new URLSearchParams({
      page: page,
      limit: limit,
      keyword: searchForm.value.keyword,
      categoryType: searchForm.value.categoryType,
      categoryId: searchForm.value.categoryId
    })
    
    const url = `/admin${props.adminLoginPath}/help-center/sub-category/list?${params}`
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    
    const result = await response.json()
    
    if (result.success) {
      subCategories.value = result.data
      pagination.value = result.pagination
    } else {
      ElMessage.error(result.message || '加载数据失败')
    }
  } catch (error) {
    ElMessage.error('加载数据失败: ' + error.message)
  } finally {
    loading.value = false
  }
}

// 加载一级分类数据
const loadCategories = async (categoryType = '') => {
  try {
    const params = new URLSearchParams()
    if (categoryType) {
      params.append('categoryType', categoryType)
    }
    
    const url = `/admin${props.adminLoginPath}/help-center/category/list?${params}`
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    
    const result = await response.json()
    
    if (result.success) {
      return result.data
    } else {
      ElMessage.error(result.message || '加载一级分类失败')
      return []
    }
  } catch (error) {
    ElMessage.error('加载一级分类失败: ' + error.message)
    return []
  }
}

// 刷新数据
const refreshData = () => {
  loadSubCategoryData(pagination.value.currentPage, pagination.value.itemsPerPage)
}

// 搜索分类
const searchSubCategories = () => {
  pagination.value.currentPage = 1
  loadSubCategoryData(1, pagination.value.itemsPerPage)
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    keyword: '',
    categoryType: '',
    categoryId: ''
  }
  pagination.value.currentPage = 1
  loadSubCategoryData(1, pagination.value.itemsPerPage)
}

// 分类类型变化时更新一级分类列表
const handleCategoryTypeChange = async (categoryType) => {
  if (categoryType) {
    availableCategories.value = await loadCategories(categoryType)
  } else {
    availableCategories.value = []
  }
  searchForm.value.categoryId = ''
}

// 对话框中分类类型变化时更新一级分类列表
const handleDialogCategoryTypeChange = async (categoryType) => {
  if (categoryType) {
    dialogCategories.value = await loadCategories(categoryType)
  } else {
    dialogCategories.value = []
  }
  currentSubCategory.value.categoryId = null
}

// 显示创建对话框
const showCreateDialog = async () => {
  dialogTitle.value = '添加二级分类'
  currentSubCategory.value = {
    id: null,
    name: '',
    nameEn: '',
    description: '',
    categoryType: 'faq',
    categoryId: null,
    sortOrder: 0
  }
  
  // 加载默认的faq类型一级分类
  dialogCategories.value = await loadCategories('faq')
  dialogVisible.value = true
}

// 显示编辑对话框
const showEditDialog = async (subCategory) => {
  dialogTitle.value = '编辑二级分类'
  currentSubCategory.value = {
    id: subCategory.id,
    name: subCategory.name,
    nameEn: subCategory.nameEn,
    description: subCategory.description,
    categoryType: subCategory.categoryType,
    categoryId: subCategory.categoryId,
    sortOrder: subCategory.sortOrder
  }
  
  // 加载对应类型的一级分类
  dialogCategories.value = await loadCategories(subCategory.categoryType)
  dialogVisible.value = true
}

// 保存分类
const handleSave = async () => {
  if (!currentSubCategory.value.name) {
    ElMessage.warning('请输入分类名称')
    return
  }
  if (!currentSubCategory.value.categoryType) {
    ElMessage.warning('请选择分类类型')
    return
  }
  if (!currentSubCategory.value.categoryId) {
    ElMessage.warning('请选择一级分类')
    return
  }

  saving.value = true
  try {
    const url = currentSubCategory.value.id
      ? `/admin${props.adminLoginPath}/help-center/sub-category/update`
      : `/admin${props.adminLoginPath}/help-center/sub-category/create`
    
    const requestData = {
      ...currentSubCategory.value,
      categoryId: currentSubCategory.value.categoryId // 确保categoryId被正确传递
    }
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: JSON.stringify(requestData)
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

// 删除分类
const handleDelete = async (subCategory) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除二级分类"${subCategory.name}"吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    const response = await fetch(`/admin${props.adminLoginPath}/help-center/sub-category/delete`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: JSON.stringify({ id: subCategory.id })
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

// 处理分页大小变化
const handleSizeChange = (val) => {
  pagination.value.itemsPerPage = val
  loadSubCategoryData(pagination.value.currentPage, val)
}

// 处理当前页变化
const handleCurrentChange = (val) => {
  pagination.value.currentPage = val
  loadSubCategoryData(val, pagination.value.itemsPerPage)
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

// 组件挂载时加载数据
onMounted(() => {
  if (props.autoLoad) {
    loadSubCategoryData()
  }
})

// 暴露方法给父组件调用
defineExpose({
  loadSubCategoryData
})
</script>

<style scoped>
.help-subcategory-container {
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

.subcategory-table {
  width: 100% !important;
  font-size: 14px;
}

.subcategory-table :deep(.el-table__header th) {
  background-color: #f5f7fa;
  color: #606266;
  font-weight: bold;
}

.subcategory-table :deep(.el-table__body td) {
  transition: background-color 0.3s;
}

.subcategory-table :deep(.el-table__row:hover) {
  background-color: #f5f7fa;
}

.subcategory-table :deep(.el-table__row:hover td) {
  background-color: #f5f7fa !important;
}

.subcategory-table :deep(.el-table__fixed .el-table__row:hover td) {
  background-color: #f5f7fa !important;
}

.subcategory-table :deep(.el-table__row:hover .el-table-fixed-column--left) {
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

.form-item-hint {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  width: 100%;
}
</style>