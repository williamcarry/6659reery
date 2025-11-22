<template>
  <div class="recharge-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2 class="page-title">
        <el-icon class="title-icon"><Money /></el-icon>
        充值记录
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
          <el-col :span="6" :xs="24">
            <el-form-item label="用户类型">
              <el-select v-model="searchForm.userType" placeholder="请选择类型" clearable style="width: 100%;">
                <el-option label="全部" value="" />
                <el-option label="供应商" value="supplier" />
                <el-option label="普通用户" value="customer" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="6" :xs="24">
            <el-form-item label="用户名">
              <el-input v-model="searchForm.username" placeholder="请输入用户名" />
            </el-form-item>
          </el-col>
          <el-col :span="6" :xs="24">
            <el-form-item label="订单状态">
              <el-select v-model="searchForm.status" placeholder="请选择状态" clearable style="width: 100%;">
                <el-option label="全部" value="" />
                <el-option label="待支付" value="pending" />
                <el-option label="支付处理中" value="processing" />
                <el-option label="支付完成" value="completed" />
                <el-option label="支付失败" value="failed" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="6" :xs="24" class="action-col">
            <el-form-item label=" ">
              <div class="form-actions">
                <el-button type="primary" @click="searchRecharges" :icon="Search">
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
    
    <!-- 充值记录表格 -->
    <el-card class="table-card">
      <template #header>
        <div class="table-header">
          <div class="table-header-title">
            <el-icon class="table-icon"><List /></el-icon>
            充值明细列表
          </div>
          <div class="table-header-info">
            共 {{ pagination.totalItems }} 条记录
          </div>
        </div>
      </template>
      
      <el-table 
        :data="recharges" 
        class="recharge-table" 
        v-loading="loading"
        :fit="true"
        :border="false"
        :header-cell-style="{ textAlign: 'center' }"
        :cell-style="{ textAlign: 'center' }"
        :stripe="true"
        empty-text="暂无充值记录"
      >
        <el-table-column label="ID" width="80" fixed>
          <template #default="scope">
            {{ scope.row.id }}
          </template>
        </el-table-column>
        <el-table-column prop="userType" label="用户类型" min-width="100">
          <template #default="scope">
            <el-tag :type="scope.row.userType === 'supplier' ? 'primary' : 'success'">
              {{ scope.row.userType === 'supplier' ? '供应商' : '普通用户' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="username" label="用户名" min-width="120" show-overflow-tooltip />
        <el-table-column prop="orderNo" label="订单号" min-width="160" show-overflow-tooltip>
          <template #default="scope">
            <span class="order-no">{{ scope.row.orderNo || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="amount" label="充值金额" min-width="120" sortable>
          <template #default="scope">
            <span class="amount-text">{{ currencySymbol }}{{ formatCurrency(scope.row.amount) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="paymentMethod" label="支付方式" min-width="120">
          <template #default="scope">
            <span class="payment-method">{{ scope.row.paymentMethodText || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="订单状态" min-width="120">
          <template #default="scope">
            <el-tag class="status-tag" :type="scope.row.statusTagType" effect="dark">
              {{ scope.row.statusText }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="paymentTransactionId" label="支付流水号" min-width="180" show-overflow-tooltip>
          <template #default="scope">
            <span class="transaction-id">{{ scope.row.paymentTransactionId || '-' }}</span>
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
        <el-table-column prop="paidAt" label="支付时间" min-width="160" sortable>
          <template #default="scope">
            <div class="time-cell" v-if="scope.row.paidAt">
              <div class="date">{{ formatDate(scope.row.paidAt) }}</div>
              <div class="time">{{ formatTime(scope.row.paidAt) }}</div>
            </div>
            <span v-else class="no-data">-</span>
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
  vLoading
} from 'element-plus'
import {
  Money,
  Search,
  Refresh,
  RefreshLeft,
  List
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

// 定义响应式数据
const recharges = ref([])
const loading = ref(false)
const currencySymbol = ref('$') // 默认货币符号
const pagination = ref({
  currentPage: 1,
  totalPages: 1,
  totalItems: 0,
  itemsPerPage: 20
})

// 搜索表单
const searchForm = ref({
  userType: '',
  username: '',
  status: ''
})

// 加载充值记录数据
const loadRechargeData = async (page = 1, limit = 20) => {
  loading.value = true
  try {
    const params = new URLSearchParams({
      page: page,
      limit: limit,
      userType: searchForm.value.userType,
      username: searchForm.value.username,
      status: searchForm.value.status
    })
    
    const url = `/admin${props.adminLoginPath}/recharge/list?${params}`
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    
    const result = await response.json()
    
    if (result.success) {
      recharges.value = result.data
      pagination.value = result.pagination
      // 更新货币符号
      if (result.currencySymbol) {
        currencySymbol.value = result.currencySymbol
      }
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
  loadRechargeData(pagination.value.currentPage, pagination.value.itemsPerPage)
}

// 搜索充值记录
const searchRecharges = () => {
  pagination.value.currentPage = 1
  loadRechargeData(1, pagination.value.itemsPerPage)
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    userType: '',
    username: '',
    status: ''
  }
  pagination.value.currentPage = 1
  loadRechargeData(1, pagination.value.itemsPerPage)
}

// 处理分页大小变化
const handleSizeChange = (val) => {
  pagination.value.itemsPerPage = val
  loadRechargeData(pagination.value.currentPage, val)
}

// 处理当前页变化
const handleCurrentChange = (val) => {
  pagination.value.currentPage = val
  loadRechargeData(val, pagination.value.itemsPerPage)
}

// 组件挂载时加载数据
onMounted(() => {
  // 只有当 autoLoad 为 true 时才自动加载数据
  if (props.autoLoad) {
    loadRechargeData()
  }
})

// 暴露方法给父组件调用
defineExpose({
  loadRechargeData
})

// 格式化货币显示
const formatCurrency = (amount) => {
  if (amount === null || amount === undefined || amount === '') return '0.00'
  const value = parseFloat(amount)
  if (isNaN(value)) return '0.00'
  return value.toFixed(2)
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
</script>

<style scoped>
.recharge-container {
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

.recharge-table {
  width: 100% !important;
  font-size: 14px;
}

.recharge-table :deep(.el-table__header th) {
  background-color: #f5f7fa;
  color: #606266;
  font-weight: bold;
}

/* 解决鼠标悬停时序号列变色延迟的问题 */
.recharge-table :deep(.el-table__body td) {
  transition: background-color 0.3s;
}

.recharge-table :deep(.el-table__row:hover) {
  background-color: #f5f7fa;
}

.recharge-table :deep(.el-table__row:hover td) {
  background-color: #f5f7fa !important;
}

/* 确保固定列也有一致的悬停效果 */
.recharge-table :deep(.el-table__fixed .el-table__row:hover td) {
  background-color: #f5f7fa !important;
}

/* 确保序号列在悬停时立即响应 */
.recharge-table :deep(.el-table__row:hover .el-table-fixed-column--left) {
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

.status-tag {
  font-size: 12px;
}

.order-no {
  font-size: 14px;
  color: #303133;
  font-weight: 500;
}

.amount-text {
  font-size: 14px;
  color: #67c23a;
  font-weight: 600;
}

.payment-method {
  font-size: 14px;
  color: #606266;
}

.transaction-id {
  font-size: 13px;
  color: #909399;
}

.no-data {
  color: #909399;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  width: 100%;
}
</style>
