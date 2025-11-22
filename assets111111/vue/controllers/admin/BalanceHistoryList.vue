<template>
  <div class="balance-history-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2 class="page-title">
        <el-icon class="title-icon"><TrendCharts /></el-icon>
        余额变化记录
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
            <el-form-item label="业务类型">
              <el-select v-model="searchForm.type" placeholder="请选择类型" clearable style="width: 100%;">
                <el-option label="全部" value="" />
                <el-option
                  v-for="option in typeOptions"
                  :key="option.value"
                  :label="option.label"
                  :value="option.value"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="6" :xs="24" class="action-col">
            <el-form-item label=" ">
              <div class="form-actions">
                <el-button type="primary" @click="searchBalanceHistories" :icon="Search">
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
    
    <!-- 余额变化记录表格 -->
    <el-card class="table-card">
      <template #header>
        <div class="table-header">
          <div class="table-header-title">
            <el-icon class="table-icon"><List /></el-icon>
            余额明细列表
          </div>
          <div class="table-header-info">
            共 {{ pagination.totalItems }} 条记录
          </div>
        </div>
      </template>
      
      <el-table 
        :data="balanceHistories" 
        class="balance-history-table" 
        v-loading="loading"
        :fit="true"
        :border="false"
        :header-cell-style="{ textAlign: 'center' }"
        :cell-style="{ textAlign: 'center' }"
        :stripe="true"
        empty-text="暂无余额变化记录"
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
        <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip>
          <template #default="scope">
            <span class="description-text">{{ scope.row.description || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="balanceBefore" label="变化前金额" min-width="150">
          <template #default="scope">
            <div class="balance-cell multi-line">
              <div class="line-item">
                <span class="label">可用余额：</span>
                <span class="balance-value">{{ currencySymbol }}{{ formatCurrency(scope.row.balanceBefore) }}</span>
              </div>
              <div class="line-item">
                <span class="label">冻结余额：</span>
                <span class="frozen-balance-value">{{ currencySymbol }}{{ formatCurrency(scope.row.frozenBalanceBefore) }}</span>
              </div>
              <div class="line-item">
                <span class="label">订单待结算：</span>
                <span class="pending-balance-value">{{ currencySymbol }}{{ formatCurrency(scope.row.pendingSettlementBefore) }}</span>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="amount" label="变化金额" min-width="150" sortable>
          <template #default="scope">
            <div class="amount-cell multi-line">
              <div class="line-item">
                <span class="label">可用余额：</span>
                <span 
                  class="amount-value" 
                  :class="getAmountClass(scope.row.amount)"
                >
                  {{ formatCurrencyWithSign(scope.row.amount) }}
                </span>
              </div>
              <div class="line-item">
                <span class="label">冻结余额：</span>
                <span 
                  class="frozen-value" 
                  :class="getAmountClass(scope.row.frozenAmount)"
                >
                  {{ formatCurrencyWithSign(scope.row.frozenAmount) }}
                </span>
              </div>
              <div class="line-item">
                <span class="label">订单待结算：</span>
                <span 
                  class="pending-value" 
                  :class="getAmountClass(scope.row.pendingSettlementAmount)"
                >
                  {{ formatCurrencyWithSign(scope.row.pendingSettlementAmount) }}
                </span>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="balanceAfter" label="变化后金额" min-width="150" sortable>
          <template #default="scope">
            <div class="balance-cell multi-line">
              <div class="line-item">
                <span class="label">可用余额：</span>
                <span class="balance-value">{{ currencySymbol }}{{ formatCurrency(scope.row.balanceAfter) }}</span>
              </div>
              <div class="line-item">
                <span class="label">冻结余额：</span>
                <span class="frozen-balance-value">{{ currencySymbol }}{{ formatCurrency(scope.row.frozenBalanceAfter) }}</span>
              </div>
              <div class="line-item">
                <span class="label">订单待结算：</span>
                <span class="pending-balance-value">{{ currencySymbol }}{{ formatCurrency(scope.row.pendingSettlementAfter) }}</span>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="type" label="业务类型" min-width="120">
          <template #default="scope">
            <el-tag class="type-tag" :type="getTypeTagType(scope.row.type)" :class="getTypeCustomClass(scope.row.type)" effect="plain">
              {{ scope.row.typeLabel || getTypeText(scope.row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="referenceId" label="订单号" min-width="180" show-overflow-tooltip>
          <template #default="scope">
            <span 
              v-if="isOrderRelatedType(scope.row.type) && scope.row.referenceId" 
              class="order-link" 
              @click="viewOrderDetail(scope.row.referenceId)"
            >
              {{ scope.row.referenceId }}
            </span>
            <span v-else>{{ scope.row.referenceId || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="createdAt" label="时间" min-width="160" sortable>
          <template #default="scope">
            <div class="time-cell">
              <div class="date">{{ formatDate(scope.row.createdAt) }}</div>
              <div class="time">{{ formatTime(scope.row.createdAt) }}</div>
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
  TrendCharts,
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
const balanceHistories = ref([])
const loading = ref(false)
const currencySymbol = ref('$') // 默认货币符号
const pagination = ref({
  currentPage: 1,
  totalPages: 1,
  totalItems: 0,
  itemsPerPage: 20
})

// 业务类型选项
const typeOptions = ref([])

// 搜索表单
const searchForm = ref({
  userType: '',
  username: '',
  type: ''
})

// 获取业务类型显示文本（作为后备方案）
const getTypeText = (type) => {
  // 默认类型映射
  const typeMap = {
    'recharge': '充值',
    'withdraw': '提现',
    'order_payment': '订单支付',
    'order': '订单',
    'commission': '佣金',
    'refund': '退款',
    'system': '系统调整',
    'vip_purchase': '购买VIP',
    'admin_add': '后台增加余额',
    'admin_deduct': '后台减少余额'
  }
  return typeMap[type] || type
}

// 获取业务类型标签类型
const getTypeTagType = (type) => {
  const typeMap = {
    'recharge': 'success',
    'withdraw': 'warning',
    'order_payment': 'primary',
    'order': 'primary',
    'commission': 'info',
    'refund': 'danger',
    'system': '',
    'vip_purchase': 'success',
    'admin_add': 'success',
    'admin_deduct': 'danger',
    'order_refund': 'success'
  }
  return typeMap[type] || 'info'
}

// 获取业务类型自定义样式类（用于成功状态的彩色显示）
const getTypeCustomClass = (type) => {
  const customClasses = {
    'recharge': 'type-recharge',           // 充值成功 - 绿色
    'withdraw': 'type-withdraw',           // 提现 - 橙色
    'order_payment': 'type-order-payment', // 订单支付 - 蓝色
    'order_refund': 'type-order-refund',   // 订单退款成功 - 紫色
    'admin_add': 'type-admin-add',         // 后台增加余额 - 绿色
    'admin_deduct': 'type-admin-deduct',   // 后台减少余额 - 红色
    'commission': 'type-commission',       // 佣金 - 青色
    'vip_purchase': 'type-vip-purchase',   // VIP购买 - 黄色
    'system': 'type-system'                // 系统调整 - 靛蓝色
  }
  return customClasses[type] || ''
}

// 获取金额样式类
const getAmountClass = (amount) => {
  if (amount === null || amount === undefined || amount === '') return 'zero'
  const value = parseFloat(amount)
  if (isNaN(value)) return 'zero'
  if (value > 0) return 'positive'
  if (value < 0) return 'negative'
  return 'zero'
}

// 判断是否为订单相关类型
const isOrderRelatedType = (type) => {
  return ['order_frozen', 'order_confirmed', 'order_refund', 'order_payment'].includes(type)
}

// 查看订单详情
const viewOrderDetail = (orderNo) => {
  if (!orderNo) return
  // 触发导航到订单详情页的事件，传递订单号
  window.dispatchEvent(new CustomEvent('navigate-to-order-detail', {
    detail: { orderNo: orderNo }
  }))
}

// 加载余额变化记录数据
const loadBalanceHistoryData = async (page = 1, limit = 20) => {
  loading.value = true
  try {
    const params = new URLSearchParams({
      page: page,
      limit: limit,
      userType: searchForm.value.userType,
      username: searchForm.value.username,
      type: searchForm.value.type
    })
    
    const url = `/admin${props.adminLoginPath}/balance-history/list?${params}`
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    
    const result = await response.json()
    
    if (result.success) {
      balanceHistories.value = result.data
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
  loadBalanceHistoryData(pagination.value.currentPage, pagination.value.itemsPerPage)
}

// 搜索余额变化记录
const searchBalanceHistories = () => {
  pagination.value.currentPage = 1
  loadBalanceHistoryData(1, pagination.value.itemsPerPage)
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    userType: '',
    username: '',
    type: ''
  }
  pagination.value.currentPage = 1
  loadBalanceHistoryData(1, pagination.value.itemsPerPage)
}

// 处理分页大小变化
const handleSizeChange = (val) => {
  pagination.value.itemsPerPage = val
  loadBalanceHistoryData(pagination.value.currentPage, val)
}

// 处理当前页变化
const handleCurrentChange = (val) => {
  pagination.value.currentPage = val
  loadBalanceHistoryData(val, pagination.value.itemsPerPage)
}

// 组件挂载时加载数据
onMounted(() => {
  // 始终加载业务类型映射（筛选条件需要）
  loadTypeMapping()
  
  // 只有当 autoLoad 为 true 时才自动加载数据
  if (props.autoLoad) {
    loadBalanceHistoryData()
  }
})

// 暴露方法给父组件调用
defineExpose({
  loadBalanceHistoryData
})

// 获取业务类型映射
const loadTypeMapping = async () => {
  try {
    const url = `/admin${props.adminLoginPath}/balance-history/type-mapping`
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    
    const result = await response.json()
    
    if (result.success) {
      typeOptions.value = result.data
    }
  } catch (error) {
    console.error('加载业务类型映射失败:', error)
  }
}

// 格式化货币显示
const formatCurrency = (amount) => {
  if (amount === null || amount === undefined || amount === '') return '0.00'
  const value = parseFloat(amount)
  if (isNaN(value)) return '0.00'
  return value.toFixed(2)
}

// 格式化带符号的货币显示
const formatCurrencyWithSign = (amount) => {
  if (amount === null || amount === undefined || amount === '') return '0.00'
  const value = parseFloat(amount)
  if (isNaN(value)) return '0.00'
  if (value > 0) {
    return '+' + value.toFixed(2)
  }
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
.balance-history-container {
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

.balance-history-table {
  width: 100% !important;
  font-size: 14px;
}

.balance-history-table :deep(.el-table__header th) {
  background-color: #f5f7fa;
  color: #606266;
  font-weight: bold;
}

/* 解决鼠标悬停时序号列变色延迟的问题 */
.balance-history-table :deep(.el-table__body td) {
  transition: background-color 0.3s;
}

.balance-history-table :deep(.el-table__row:hover) {
  background-color: #f5f7fa;
}

.balance-history-table :deep(.el-table__row:hover td) {
  background-color: #f5f7fa !important;
}

/* 确保固定列也有一致的悬停效果 */
.balance-history-table :deep(.el-table__fixed .el-table__row:hover td) {
  background-color: #f5f7fa !important;
}

/* 确保序号列在悬停时立即响应 */
.balance-history-table :deep(.el-table__row:hover .el-table-fixed-column--left) {
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

.type-tag {
  font-size: 12px;
}

/* 业务类型彩色标记样式 */
.type-recharge {
  background-color: #d1fae5 !important;
  color: #065f46 !important;
  border-color: #34d399 !important;
}

.type-withdraw {
  background-color: #fed7aa !important;
  color: #9a3412 !important;
  border-color: #fb923c !important;
}

.type-order-payment {
  background-color: #dbeafe !important;
  color: #1e40af !important;
  border-color: #60a5fa !important;
}

.type-order-refund {
  background-color: #e9d5ff !important;
  color: #6b21a8 !important;
  border-color: #a855f7 !important;
}

.type-admin-add {
  background-color: #d1fae5 !important;
  color: #065f46 !important;
  border-color: #34d399 !important;
}

.type-admin-deduct {
  background-color: #fee2e2 !important;
  color: #991b1b !important;
  border-color: #f87171 !important;
}

.type-commission {
  background-color: #cffafe !important;
  color: #164e63 !important;
  border-color: #22d3ee !important;
}

.type-vip-purchase {
  background-color: #fef3c7 !important;
  color: #92400e !important;
  border-color: #fbbf24 !important;
}

.type-system {
  background-color: #e0e7ff !important;
  color: #3730a3 !important;
  border-color: #818cf8 !important;
}

.description-text {
  font-size: 14px;
  color: #303133;
}

.amount-cell {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.amount-cell.multi-line {
  padding: 8px 0;
}

.amount-value {
  font-size: 14px;
  font-weight: 600;
}

.amount-value.positive {
  color: #67c23a;
}

.amount-value.negative {
  color: #f56c6c;
}

.amount-value.zero {
  color: #909399;
}

.balance-cell {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.balance-cell.multi-line {
  padding: 8px 0;
}

.balance-cell .line-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
}

.balance-cell .label {
  color: #909399;
  font-size: 12px;
}

.balance-value {
  font-size: 14px;
  color: #67c23a;
  font-weight: 600;
}

.frozen-balance-value {
  font-size: 14px;
  color: #e6a23c;
  font-weight: 600;
}

.frozen-cell {
  display: flex;
  justify-content: center;
}

.frozen-value {
  font-size: 14px;
}

.frozen-value.positive {
  color: #67c23a;
}

.frozen-value.negative {
  color: #f56c6c;
}

.frozen-value.zero {
  color: #909399;
}

.pending-value {
  font-size: 14px;
}

.pending-value.positive {
  color: #67c23a;
}

.pending-value.negative {
  color: #f56c6c;
}

.pending-value.zero {
  color: #909399;
}

.pending-balance-value {
  font-size: 14px;
  color: #409eff;
  font-weight: 600;
}

.order-link {
  color: #409eff;
  cursor: pointer;
  text-decoration: underline;
  font-weight: 500;
}

.order-link:hover {
  color: #66b1ff;
  text-decoration: underline;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  width: 100%;
}
</style>