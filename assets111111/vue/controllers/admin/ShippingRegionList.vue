<template>
  <div class="shipping-region-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2 class="page-title">
        <el-icon class="title-icon"><Location /></el-icon>
        发货区域
      </h2>
      <div class="header-actions">
        <el-button type="primary" @click="showCreateDialog" :icon="Plus">
          添加发货区域
        </el-button>
        <el-button type="primary" @click="refreshData" :icon="Refresh">
          刷新数据
        </el-button>
      </div>
    </div>
    
    <!-- 重要说明 -->
    <el-alert 
      type="info" 
      :closable="false" 
      show-icon
      style="margin-bottom: 20px;"
    >
      <template #title>
        <div class="alert-content">
          <strong>功能说明：</strong>
          <ul class="info-list">
            <li>🔒 <strong>币种和货币符号不可修改</strong>，由后端从系统配置（site_config.site_currency）自动读取</li>
            <li>添加或编辑发货区域时，只需填写区域代码和名称，币种信息会自动填充</li>
            <li>禁用区域不会影响已有商品的显示和销售，仅影响新商品的区域选择</li>
            <li>已配置该区域的商品将继续保留原有配置，不受禁用影响</li>
          </ul>
        </div>
      </template>
    </el-alert>
    
    <!-- 搜索和筛选区域 -->
    <el-card class="filter-card">
      <div class="filter-header">
        <el-icon class="filter-icon"><Search /></el-icon>
        <span class="filter-title">筛选条件</span>
      </div>
      <el-form :model="searchForm" class="search-form" label-position="left" label-width="80px">
        <el-row :gutter="20" align="middle">
          <el-col :span="8" :xs="24">
            <el-form-item label="关键词">
              <el-input v-model="searchForm.keyword" placeholder="请输入区域名称" />
            </el-form-item>
          </el-col>
          <el-col :span="8" :xs="24">
            <el-form-item label="状态">
              <el-select v-model="searchForm.isActive" placeholder="请选择状态" clearable style="width: 100%;">
                <el-option label="全部" value="" />
                <el-option label="启用" value="1" />
                <el-option label="禁用" value="0" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8" :xs="24" class="action-col">
            <el-form-item label=" ">
              <div class="form-actions">
                <el-button type="primary" @click="searchShippingRegions" :icon="Search">
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
    
    <!-- 发货区域表格 -->
    <el-card class="table-card">
      <template #header>
        <div class="table-header">
          <div class="table-header-title">
            <el-icon class="table-icon"><List /></el-icon>
            发货区域列表
          </div>
          <div class="table-header-info">
            共 {{ pagination.totalItems }} 条记录
          </div>
        </div>
      </template>
      
      <el-table 
        :data="shippingRegions" 
        class="shipping-region-table" 
        v-loading="loading"
        :fit="true"
        :border="false"
        :header-cell-style="{ textAlign: 'center' }"
        :cell-style="{ textAlign: 'center' }"
        :stripe="true"
        empty-text="暂无发货区域记录"
      >
        <el-table-column label="序号" width="60" fixed>
          <template #default="scope">
            {{ (pagination.currentPage - 1) * pagination.itemsPerPage + scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column prop="code" label="区域代码" min-width="100" />
        <el-table-column prop="label" label="中文名称" min-width="120" show-overflow-tooltip />
        <el-table-column prop="labelEn" label="英文名称" min-width="120" show-overflow-tooltip />
        <el-table-column prop="currencyCode" label="币种代码" min-width="100" />
        <el-table-column prop="currencySymbol" label="币种符号" min-width="100" />
        <el-table-column prop="isActive" label="状态" min-width="100">
          <template #default="scope">
            <el-tag :type="scope.row.isActive ? 'success' : 'danger'">
              {{ scope.row.isActive ? '启用' : '禁用' }}
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
        <el-table-column prop="updatedAt" label="更新时间" min-width="160" sortable>
          <template #default="scope">
            <div class="time-cell">
              <div class="date">{{ formatDate(scope.row.updatedAt) }}</div>
              <div class="time">{{ formatTime(scope.row.updatedAt) }}</div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="200" fixed="right">
          <template #default="scope">
            <el-button size="small" @click="editShippingRegion(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteShippingRegion(scope.row)">删除</el-button>
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
    
    <!-- 添加/编辑发货区域弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <el-form
        :model="dialogForm"
        :rules="dialogRules"
        ref="dialogFormRef"
        label-position="right"
        label-width="100px"
        v-loading="dialogLoading"
      >
        <el-form-item label="区域代码" prop="code">
          <el-input v-model="dialogForm.code" placeholder="请输入区域代码（如：US、CN、DE）" :disabled="isEditMode" />
          <div class="form-item-tip" v-if="isEditMode">区域代码不可编辑</div>
        </el-form-item>
        <el-form-item label="中文名称" prop="label">
          <el-input v-model="dialogForm.label" placeholder="请输入中文名称（如：美国、中国）" />
        </el-form-item>
        <el-form-item label="英文名称" prop="labelEn">
          <el-input v-model="dialogForm.labelEn" placeholder="请输入英文名称（如：United States、China）" />
        </el-form-item>
        <el-form-item label="币种代码" prop="currencyCode">
          <el-input v-model="dialogForm.currencyCode" placeholder="由系统配置自动填充，不可修改" disabled />
          <div class="form-item-tip">⚠️ 币种代码由后端从 site_config.site_currency 自动读取，不可修改</div>
        </el-form-item>
        <el-form-item label="货币符号" prop="currencySymbol">
          <el-input v-model="dialogForm.currencySymbol" placeholder="由系统配置自动填充，不可修改" disabled />
          <div class="form-item-tip">⚠️ 货币符号由后端从 site_config.site_currency 自动读取，不可修改</div>
        </el-form-item>
        <el-form-item label="状态" prop="isActive">
          <el-switch
            v-model="dialogForm.isActive"
            active-text="启用"
            inactive-text="禁用"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm" :loading="dialogLoading">确定</el-button>
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
  ElSelect,
  ElOption,
  ElTag,
  ElMessage,
  ElPagination,
  ElRow,
  ElCol,
  ElIcon,
  ElMessageBox,
  ElDialog,
  ElSwitch,
  ElAlert,
  vLoading
} from 'element-plus'
import {
  Location,
  Search,
  Refresh,
  RefreshLeft,
  List,
  Plus
} from '@element-plus/icons-vue'

// 定义组件属性
const props = defineProps({
  adminLoginPath: {
    type: String,
    default: ''
  },
  // 添加一个属性来控制是否自动加载数据
  autoLoad: {
    type: Boolean,
    default: false
  }
})

// 弹窗相关数据
const dialogVisible = ref(false)
const dialogLoading = ref(false)
const dialogTitle = ref('添加发货区域')
const isEditMode = ref(false)
const currentEditId = ref(null)

const dialogForm = ref({
  code: '',
  label: '',
  labelEn: '',
  currencyCode: '',
  currencySymbol: '',
  isActive: true
})

// 弹窗表单验证规则
const dialogRules = {
  code: [
    { required: true, message: '请输入区域代码', trigger: 'blur' },
    { min: 1, max: 10, message: '长度在 1 到 10 个字符', trigger: 'blur' }
  ],
  label: [
    { required: true, message: '请输入中文名称', trigger: 'blur' },
    { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
  ],
  labelEn: [
    { required: true, message: '请输入英文名称', trigger: 'blur' },
    { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
  ],
  // 币种和货币符号由后端自动从 site_config 读取，前端不需要验证
  isActive: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ]
}

// 显示创建弹窗
const showCreateDialog = () => {
  // 重置表单数据
  dialogForm.value = {
    code: '',
    label: '',
    labelEn: '',
    currencyCode: '',
    currencySymbol: '',
    isActive: true
  }
  isEditMode.value = false
  dialogTitle.value = '添加发货区域'
  currentEditId.value = null
  
  // 清除表单验证状态
  if (dialogFormRef.value) {
    dialogFormRef.value.clearValidate()
  }
  
  dialogVisible.value = true
}

// 显示编辑弹窗
const showEditDialog = (region) => {
  // 填充表单数据
  dialogForm.value = {
    code: region.code,
    label: region.label,
    labelEn: region.labelEn,
    currencyCode: region.currencyCode,
    currencySymbol: region.currencySymbol,
    isActive: region.isActive
  }
  isEditMode.value = true
  dialogTitle.value = '编辑发货区域'
  currentEditId.value = region.id
  
  // 清除表单验证状态
  if (dialogFormRef.value) {
    dialogFormRef.value.clearValidate()
  }
  
  dialogVisible.value = true
}

// 提交表单
const submitForm = async () => {
  // 先验证表单
  if (!dialogFormRef.value) {
    ElMessage.error('表单初始化失败')
    return
  }
  
  try {
    // 等待表单验证
    await dialogFormRef.value.validate()
  } catch (error) {
    ElMessage.error('请填写所有必填项')
    return
  }
  
  dialogLoading.value = true
  try {
    let response
    let result
    
    if (isEditMode.value) {
      // 编辑模式
      response = await fetch(`/admin${props.adminLoginPath}/shipping-region/${currentEditId.value}/update`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify(dialogForm.value)
      })
    } else {
      // 创建模式
      response = await fetch(`/admin${props.adminLoginPath}/shipping-region/create`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify(dialogForm.value)
      })
    }
    
    result = await response.json()
    
    if (result.success) {
      ElMessage.success(result.message || (isEditMode.value ? '更新成功' : '创建成功'))
      dialogVisible.value = false
      // 重新加载数据
      loadShippingRegionData(pagination.value.currentPage, pagination.value.itemsPerPage)
    } else {
      ElMessage.error(result.error || (isEditMode.value ? '更新失败' : '创建失败'))
    }
  } catch (error) {
    ElMessage.error((isEditMode.value ? '更新失败' : '创建失败') + ': ' + error.message)
  } finally {
    dialogLoading.value = false
  }
}

// 定义响应式数据
const shippingRegions = ref([])
const loading = ref(false)
const pagination = ref({
  currentPage: 1,
  totalPages: 1,
  totalItems: 0,
  itemsPerPage: 20
})

// 弹窗引用
const dialogFormRef = ref()

// 搜索表单
const searchForm = ref({
  keyword: '',
  isActive: ''
})

// 加载发货区域数据
const loadShippingRegionData = async (page = 1, limit = 20) => {
  loading.value = true
  try {
    const params = new URLSearchParams({
      page: page,
      limit: limit,
      keyword: searchForm.value.keyword,
      isActive: searchForm.value.isActive
    })
    
    const url = `/admin${props.adminLoginPath}/shipping-region/list/tab?${params}`
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    
    const result = await response.json()
    
    if (result.success) {
      shippingRegions.value = result.data
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
  loadShippingRegionData(pagination.value.currentPage, pagination.value.itemsPerPage)
}

// 搜索发货区域
const searchShippingRegions = () => {
  pagination.value.currentPage = 1
  loadShippingRegionData(1, pagination.value.itemsPerPage)
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    keyword: '',
    isActive: ''
  }
  pagination.value.currentPage = 1
  loadShippingRegionData(1, pagination.value.itemsPerPage)
}

// 处理分页大小变化
const handleSizeChange = (val) => {
  pagination.value.itemsPerPage = val
  loadShippingRegionData(pagination.value.currentPage, val)
}

// 处理当前页变化
const handleCurrentChange = (val) => {
  pagination.value.currentPage = val
  loadShippingRegionData(val, pagination.value.itemsPerPage)
}

// 编辑发货区域
const editShippingRegion = (region) => {
  showEditDialog(region)
}

// 删除发货区域
const deleteShippingRegion = (region) => {
  ElMessageBox.confirm(
    `确定要删除发货区域 "${region.label}" 吗？此操作不可恢复。`,
    '确认删除',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(async () => {
    try {
      const response = await fetch(`/admin${props.adminLoginPath}/shipping-region/${region.id}/delete`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      
      const result = await response.json()
      
      if (result.success) {
        ElMessage.success(result.message || '删除成功')
        // 重新加载数据
        loadShippingRegionData(pagination.value.currentPage, pagination.value.itemsPerPage)
      } else {
        ElMessage.error(result.error || '删除失败')
      }
    } catch (error) {
      ElMessage.error('删除失败: ' + error.message)
    }
  }).catch(() => {
    // 用户取消删除
  })
}

// 组件挂载时加载数据
onMounted(() => {
  // 只有当 autoLoad 为 true 时才自动加载数据
  if (props.autoLoad) {
    loadShippingRegionData()
  }
})

// 暴露方法给父组件调用
defineExpose({
  loadShippingRegionData
})

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
</script>

<style scoped>
.shipping-region-container {
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

.shipping-region-table {
  width: 100% !important;
  font-size: 14px;
}

.shipping-region-table :deep(.el-table__header th) {
  background-color: #f5f7fa;
  color: #606266;
  font-weight: bold;
}

/* 解决鼠标悬停时序号列变色延迟的问题 */
.shipping-region-table :deep(.el-table__body td) {
  transition: background-color 0.3s;
}

.shipping-region-table :deep(.el-table__row:hover) {
  background-color: #f5f7fa;
}

.shipping-region-table :deep(.el-table__row:hover td) {
  background-color: #f5f7fa !important;
}

/* 确保固定列也有一致的悬停效果 */
.shipping-region-table :deep(.el-table__fixed .el-table__row:hover td) {
  background-color: #f5f7fa !important;
}

/* 确保序号列在悬停时立即响应 */
.shipping-region-table :deep(.el-table__row:hover .el-table-fixed-column--left) {
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

/* 表单项提示样式 */
.form-item-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
  line-height: 1.5;
}

/* 禁用状态的输入框样式 */
:deep(.el-input.is-disabled .el-input__inner) {
  background-color: #f5f7fa;
  color: #909399;
  cursor: not-allowed;
}

/* 功能说明样式 */
.alert-content {
  line-height: 1.8;
}

.info-list {
  margin: 8px 0 0 0;
  padding-left: 20px;
  list-style-type: disc;
}

.info-list li {
  margin: 5px 0;
  color: #606266;
  font-size: 14px;
  line-height: 1.6;
}
</style>