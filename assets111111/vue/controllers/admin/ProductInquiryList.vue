<template>
  <div class="product-inquiry-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2 class="page-title">
        <el-icon class="title-icon"><ChatDotSquare /></el-icon>
        工厂直采管理
      </h2>
      <div class="header-actions">
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
          <el-col :span="5" :xs="24">
            <el-form-item label="关键词">
              <el-input 
                v-model="searchForm.keyword" 
                placeholder="询价单号/客户名/电话/SKU" 
                clearable
              />
            </el-form-item>
          </el-col>
          <el-col :span="4" :xs="24">
            <el-form-item label="状态">
              <el-select v-model="searchForm.status" placeholder="请选择状态" clearable style="width: 100%;">
                <el-option label="全部" value="" />
                <el-option label="待处理" value="PENDING" />
                <el-option label="已完成" value="COMPLETED" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="4" :xs="24">
            <el-form-item label="开始日期">
              <el-date-picker
                v-model="searchForm.startDate"
                type="date"
                placeholder="选择日期"
                value-format="YYYY-MM-DD"
                style="width: 100%;"
              />
            </el-form-item>
          </el-col>
          <el-col :span="4" :xs="24">
            <el-form-item label="结束日期">
              <el-date-picker
                v-model="searchForm.endDate"
                type="date"
                placeholder="选择日期"
                value-format="YYYY-MM-DD"
                style="width: 100%;"
              />
            </el-form-item>
          </el-col>
          <el-col :span="7" :xs="24" class="action-col">
            <el-form-item label=" ">
              <div class="form-actions">
                <el-button type="primary" @click="searchInquiries" :icon="Search">
                  搜索记录
                </el-button>
                <el-button @click="resetSearch" :icon="RefreshLeft">
                  重置条件
                </el-button>
                <el-button 
                  type="danger" 
                  @click="handleBatchDelete" 
                  :icon="Delete"
                  :disabled="selectedRows.length === 0"
                >
                  批量删除
                </el-button>
              </div>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-card>
    
    <!-- 询价单表格 -->
    <el-card class="table-card">
      <template #header>
        <div class="table-header">
          <div class="table-header-title">
            <el-icon class="table-icon"><List /></el-icon>
            询价单列表
          </div>
          <div class="table-header-info">
            共 {{ pagination.totalItems }} 条记录
          </div>
        </div>
      </template>
      
      <el-table 
        :data="inquiries" 
        class="inquiry-table" 
        v-loading="loading"
        :fit="true"
        :border="false"
        :header-cell-style="{ textAlign: 'center' }"
        :cell-style="{ textAlign: 'center' }"
        :stripe="true"
        empty-text="暂无询价单记录"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" fixed />
        <el-table-column label="序号" width="80" fixed>
          <template #default="scope">
            {{ (pagination.currentPage - 1) * pagination.itemsPerPage + scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column prop="inquiryNo" label="询价单号" min-width="180" fixed show-overflow-tooltip>
          <template #default="scope">
            <span class="inquiry-no">{{ scope.row.inquiryNo }}</span>
          </template>
        </el-table-column>
        <el-table-column label="商品信息" min-width="300">
          <template #default="scope">
            <div class="product-info">
              <div class="product-image-wrapper" @click="openProductDetail(scope.row.productId)">
                <img 
                  :src="scope.row.productMainImage" 
                  class="product-image"
                  alt="商品图片"
                />
              </div>
              <div class="product-details">
                <div class="product-title" @click="openProductDetail(scope.row.productId)">{{ scope.row.productTitle }}</div>
                <div class="product-sku">SKU: {{ scope.row.productSku }}</div>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="customerUsername" label="客户信息" min-width="150">
          <template #default="scope">
            <div class="customer-info">
              <div class="customer-name">{{ scope.row.customerUsername }}</div>
              <div class="customer-email">{{ scope.row.customerEmail }}</div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="联系信息" min-width="150">
          <template #default="scope">
            <div class="contact-info">
              <div class="contact-name">{{ scope.row.contactName }}</div>
              <div class="contact-phone">{{ scope.row.contactPhone }}</div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="inquiryQuantity" label="询价数量" min-width="100">
          <template #default="scope">
            <span class="quantity">{{ scope.row.inquiryQuantity }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" min-width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ scope.row.statusLabel }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createdAt" label="提交时间" min-width="160" sortable>
          <template #default="scope">
            <div class="time-cell">
              <div class="date">{{ formatDate(scope.row.createdAt) }}</div>
              <div class="time">{{ formatTime(scope.row.createdAt) }}</div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="scope">
            <div class="action-buttons">
              <el-button 
                type="primary" 
                size="small" 
                @click="editInquiry(scope.row)"
                :icon="Edit"
              >
                编辑
              </el-button>
              <el-button 
                type="danger" 
                size="small" 
                @click="deleteInquiry(scope.row)"
                :icon="Delete"
              >
                删除
              </el-button>
            </div>
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
        :pager-count="5"
        layout="total, sizes, prev, pager, next, jumper"
        prev-text="上一页"
        next-text="下一页"
        background
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import {
  ElCard,
  ElTable,
  ElTableColumn,
  ElButton,
  ElForm,
  ElFormItem,
  ElInput,
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
  ElDescriptions,
  ElDescriptionsItem,
  ElImage,
  ElDatePicker,
  vLoading
} from 'element-plus'
import {
  ChatDotSquare,
  Search,
  Refresh,
  RefreshLeft,
  List,
  Edit,
  Delete,
  Document,
  ArrowLeft,
  ArrowRight
} from '@element-plus/icons-vue'

// 定义组件属性
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

// 定义响应式数据
const inquiries = ref([])
const loading = ref(false)
const pagination = ref({
  currentPage: 1,
  totalPages: 1,
  totalItems: 0,
  itemsPerPage: 20
})

// 搜索表单
const searchForm = ref({
  keyword: '',
  status: '',
  startDate: '',
  endDate: ''
})

// 选中的行
const selectedRows = ref([])

// 获取状态类型
const getStatusType = (status) => {
  const typeMap = {
    'PENDING': 'warning',
    'COMPLETED': 'success'
  }
  return typeMap[status] || 'info'
}

// 判断是否为图片（同时支持MIME类型和文件后缀名判断）
const isImage = (type, name) => {
  // 1. 先检查MIME类型
  if (type && type.startsWith('image/')) {
    return true
  }
  
  // 2. 如果MIME类型不可靠，检查文件后缀名
  if (name) {
    const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg']
    const lowerName = name.toLowerCase()
    return imageExtensions.some(ext => lowerName.endsWith(ext))
  }
  
  return false
}

// 获取所有图片URL - 删除，不再需要
const getImageUrls = () => {
  return []
}

// 加载询价单数据
const loadInquiryData = async (page = 1, limit = 20) => {
  loading.value = true
  try {
    const params = new URLSearchParams({
      page: page,
      limit: limit,
      keyword: searchForm.value.keyword,
      status: searchForm.value.status,
      startDate: searchForm.value.startDate,
      endDate: searchForm.value.endDate
    })
    
    const url = `/admin${props.adminLoginPath}/product-inquiry/list?${params}`
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    
    const result = await response.json()
    
    if (result.success) {
      inquiries.value = result.data
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

// 刷新数据
const refreshData = () => {
  loadInquiryData(pagination.value.currentPage, pagination.value.itemsPerPage)
}

// 搜索询价单
const searchInquiries = () => {
  pagination.value.currentPage = 1
  loadInquiryData(1, pagination.value.itemsPerPage)
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    keyword: '',
    status: '',
    startDate: '',
    endDate: ''
  }
  pagination.value.currentPage = 1
  loadInquiryData(1, pagination.value.itemsPerPage)
}

// 处理分页大小变化
const handleSizeChange = (val) => {
  pagination.value.itemsPerPage = val
  loadInquiryData(pagination.value.currentPage, val)
}

// 处理当前页变化
const handleCurrentChange = (val) => {
  pagination.value.currentPage = val
  loadInquiryData(val, pagination.value.itemsPerPage)
}

// 处理选择变化
const handleSelectionChange = (selection) => {
  selectedRows.value = selection
}

// 编辑询价单 - 在后台Tab中打开
const editInquiry = (row) => {
  // 触发打开询价单编辑tab的事件
  window.dispatchEvent(new CustomEvent('open-inquiry-edit-tab', {
    detail: { inquiryId: row.id }
  }))
}

// 打开商品详情
const openProductDetail = (productId) => {
  if (productId) {
    window.open(`/shop/item/${productId}`, '_blank')
  }
}

// 保存编辑 - 删除，不再需要
const saveEdit = async () => {
  // 这个方法将在编辑页面中实现
}

// 预览图片 - 删除，不再需要
const previewImage = (index) => {
  // 这个方法将在编辑页面中实现
}

// 上一张图片
const prevImage = () => {
  if (currentImageIndex.value > 0) {
    currentImageIndex.value--
    currentPreviewImage.value = imageList.value[currentImageIndex.value]
  }
}

// 下一张图片
const nextImage = () => {
  if (currentImageIndex.value < imageList.value.length - 1) {
    currentImageIndex.value++
    currentPreviewImage.value = imageList.value[currentImageIndex.value]
  }
}

// 下载附件 - 删除，不再需要
const downloadAttachment = (attachment) => {
  // 这个方法将在编辑页面中实现
}

// 删除询价单
const deleteInquiry = (row) => {
  ElMessageBox.confirm(
    `确定要删除询价单 ${row.inquiryNo} 吗？`,
    '确认删除',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      const url = `/admin${props.adminLoginPath}/product-inquiry/delete/${row.id}`
      
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      
      const result = await response.json()
      
      if (result.success) {
        ElMessage.success('删除成功')
        refreshData()
      } else {
        ElMessage.error(result.message || '删除失败')
      }
    } catch (error) {
      ElMessage.error('删除失败: ' + error.message)
    }
  }).catch(() => {
    // 用户取消删除
  })
}

// 批量删除
const handleBatchDelete = () => {
  if (selectedRows.value.length === 0) {
    ElMessage.warning('请选择要删除的记录')
    return
  }

  ElMessageBox.confirm(
    `确定要删除选中的 ${selectedRows.value.length} 条记录吗？`,
    '确认批量删除',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      const ids = selectedRows.value.map(row => row.id)
      const url = `/admin${props.adminLoginPath}/product-inquiry/batch-delete`
      
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({ ids })
      })
      
      const result = await response.json()
      
      if (result.success) {
        ElMessage.success(result.message || '批量删除成功')
        refreshData()
      } else {
        ElMessage.error(result.message || '批量删除失败')
      }
    } catch (error) {
      ElMessage.error('批量删除失败: ' + error.message)
    }
  }).catch(() => {
    // 用户取消删除
  })
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

// 组件挂载时加载数据（按需加载）
onMounted(() => {
  if (props.autoLoad) {
    loadInquiryData()
  }
})

// 暴露方法给父组件调用
defineExpose({
  loadInquiryData
})
</script>

<style scoped>
.product-inquiry-container {
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

.inquiry-table {
  width: 100% !important;
  font-size: 14px;
}

.inquiry-table :deep(.el-table__header th) {
  background-color: #f5f7fa;
  color: #606266;
  font-weight: bold;
}

.inquiry-table :deep(.el-table__body td) {
  transition: background-color 0.3s;
}

.inquiry-table :deep(.el-table__row:hover) {
  background-color: #f5f7fa;
}

.inquiry-table :deep(.el-table__row:hover td) {
  background-color: #f5f7fa !important;
}

.inquiry-table :deep(.el-table__fixed .el-table__row:hover td) {
  background-color: #f5f7fa !important;
}

.inquiry-table :deep(.el-table__row:hover .el-table-fixed-column--left) {
  background-color: #f5f7fa !important;
}

.inquiry-no {
  font-family: monospace;
  font-weight: 600;
  color: #409eff;
}

.product-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.product-image-wrapper {
  width: 60px;
  height: 60px;
  flex-shrink: 0;
  border-radius: 4px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s;
}

.product-image-wrapper:hover {
  transform: scale(1.1);
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-details {
  flex: 1;
  text-align: left;
}

.product-title {
  font-size: 14px;
  color: #303133;
  margin-bottom: 4px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  cursor: pointer;
  transition: color 0.3s;
}

.product-title:hover {
  color: #409eff;
}

.product-sku {
  font-size: 12px;
  color: #909399;
}

.customer-info,
.contact-info {
  text-align: center;
}

.customer-name,
.contact-name {
  font-size: 14px;
  color: #303133;
  margin-bottom: 4px;
}

.customer-email,
.contact-phone {
  font-size: 12px;
  color: #909399;
}

.quantity {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
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

.action-buttons {
  display: flex;
  gap: 8px;
  justify-content: center;
  flex-wrap: wrap;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  width: 100%;
}

.detail-container {
  padding: 20px 0;
}

.mb-20 {
  margin-bottom: 20px;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 12px;
}

/* 附件列表样式 */
.attachments-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  margin-top: 12px;
}

.attachment-card {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 12px;
  transition: all 0.3s;
  background-color: #fff;
}

.attachment-card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-color: #409eff;
}

.attachment-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.attachment-preview {
  width: 100%;
  height: 120px;
  overflow: hidden;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f7fa;
  cursor: pointer;
  transition: transform 0.3s;
}

.attachment-preview:hover {
  transform: scale(1.05);
}

.preview-thumbnail {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.file-preview {
  background-color: #f5f7fa;
  color: #909399;
}

.attachment-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.attachment-name {
  font-size: 13px;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin: 0;
}

/* 图片预览样式 */
.image-preview-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.image-nav {
  display: flex;
  align-items: center;
  gap: 20px;
  font-size: 14px;
  color: #606266;
}

.mt-20 {
  margin-top: 20px;
}

.attachment-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-top: 12px;
}

.attachment-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.attachment-preview {
  width: 100px;
  height: 100px;
  border-radius: 4px;
}

.file-icon {
  width: 100px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f7fa;
  border-radius: 4px;
  color: #909399;
}

.attachment-name {
  font-size: 12px;
  color: #606266;
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
