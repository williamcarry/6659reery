<template>
  <div class="supplier-statement-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2 class="page-title">
        <el-icon class="title-icon"><TrendCharts /></el-icon>
        供应商对账单
      </h2>
      <div class="header-actions">
        <el-button type="primary" @click="refreshData" :icon="Refresh">
          刷新数据
        </el-button>
        <el-button type="default" @click="closeStatement" :icon="Close">
          关闭
        </el-button>
      </div>
    </div>

    <!-- 供应商信息卡片 -->
    <el-card class="supplier-info-card" v-loading="loading">
      <template #header>
        <div class="card-header">
          <el-icon class="card-icon"><User /></el-icon>
          <span class="card-title">供应商信息</span>
        </div>
      </template>
      <el-descriptions :column="3" border v-if="supplierInfo">
        <el-descriptions-item label="供应商名称" :span="3">
          {{ supplierInfo.displayName }}
        </el-descriptions-item>
        <el-descriptions-item label="客户ID">
          {{ supplierInfo.customerId }}
        </el-descriptions-item>
        <el-descriptions-item label="联系方式" :span="2">
          <div style="display: flex; flex-direction: column; gap: 4px;">
            <div><span style="color: #909399; font-size: 12px;">联系人：</span>{{ supplierInfo.contactPerson || '-' }}</div>
            <div><span style="color: #909399; font-size: 12px;">电话：</span>{{ supplierInfo.contactPhone || '-' }}</div>
            <div><span style="color: #909399; font-size: 12px;">邮箱：</span>{{ supplierInfo.email || '-' }}</div>
          </div>
        </el-descriptions-item>
        <el-descriptions-item label="可用余额">
          <span class="available-value">{{ currencySymbol }}{{ formatCurrency(supplierInfo.balance) }}</span>
        </el-descriptions-item>
        <el-descriptions-item label="冻结余额">
          <span class="frozen-value">{{ currencySymbol }}{{ formatCurrency(supplierInfo.balanceFrozen) }}</span>
        </el-descriptions-item>
        <el-descriptions-item label="订单待结算">
          <span class="pending-value">{{ currencySymbol }}{{ formatCurrency(supplierInfo.pendingSettlementAmount || '0.00') }}</span>
        </el-descriptions-item>
        <el-descriptions-item label="计算可用余额">
          <span :class="getCalculatedBalanceClass('available')">{{ currencySymbol }}{{ formatCurrency(calculatedBalance.available) }}</span>
        </el-descriptions-item>
        <el-descriptions-item label="计算冻结余额">
          <span :class="getCalculatedBalanceClass('frozen')">{{ currencySymbol }}{{ formatCurrency(calculatedBalance.frozen) }}</span>
        </el-descriptions-item>
        <el-descriptions-item label="计算订单待结算">
          <span :class="getCalculatedBalanceClass('pending')">{{ currencySymbol }}{{ formatCurrency(calculatedBalance.pending) }}</span>
        </el-descriptions-item>
      </el-descriptions>
    </el-card>
    
    <!-- 校验结果提示 -->
    <div v-if="verifyResults.length > 0" class="verify-message">
      <div v-for="(result, index) in verifyResults" :key="index" class="verify-line" :class="result.type">
        <template v-if="result.type === 'mismatch'">
          <span class="error-text">{{ result.message }}</span>
          <span :class="result.actualClass">{{ result.actual }}</span>
          <span :class="result.calculatedClass">{{ result.calculated }}</span>
        </template>
        <template v-else>
          {{ result.message }}
        </template>
      </div>
    </div>
    
    <!-- 余额校验按钮 -->
    <div class="verify-actions" v-if="supplierInfo">
      <el-button 
        type="primary" 
        :icon="calculating ? '' : Calculator" 
        :loading="calculating"
        @click="calculateBalance"
      >
        {{ calculating ? '计算中...' : '动态计算余额' }}
      </el-button>
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
                <el-button type="primary" @click="searchStatements" :icon="Search">
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
        v-loading="tableLoading"
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
                <span class="label">冻绗余额：</span>
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
            <el-tag class="type-tag" :type="getTypeTagType(scope.row.type)" effect="dark">
              {{ scope.row.typeLabel || getTypeText(scope.row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="referenceId" label="订单号" min-width="180" show-overflow-tooltip />
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
import { ref, onMounted, defineProps, defineExpose, computed } from 'vue'
import {
  ElCard,
  ElTable,
  ElTableColumn,
  ElButton,
  ElForm,
  ElFormItem,
  ElSelect,
  ElOption,
  ElTag,
  ElMessage,
  ElPagination,
  ElRow,
  ElCol,
  ElIcon,
  ElDescriptions,
  ElDescriptionsItem,
  vLoading
} from 'element-plus'
import {
  TrendCharts,
  Search,
  RefreshLeft,
  Refresh,
  List,
  User,
  Close,
  Calculator,
  CircleCheckFilled,
  CircleCloseFilled,
  WarningFilled
} from '@element-plus/icons-vue'

const props = defineProps({
  adminLoginPath: {
    type: String,
    default: ''
  },
  supplierId: {
    type: Number,
    default: null
  },
  autoLoad: {
    type: Boolean,
    default: true
  }
})

const supplierInfo = ref(null)
const balanceHistories = ref([])
const loading = ref(false)
const tableLoading = ref(false)
const calculating = ref(false)
const currencySymbol = ref('$') // 默认货币符号

// 计算结果
const calculatedBalance = ref({
  frozen: '0.00',           // 冻结余额
  pending: '0.00',         // 订单待结算
  available: '0.00',       // 可用余额
  calculated: false,
  frozenMatch: true,       // 冻结余额匹配状态
  pendingMatch: true,      // 订单待结算匹配状态
  availableMatch: true     // 可用余额匹配状态
})

// 校验提示信息（数组形式，一行一行显示）
const verifyResults = ref([])

const searchForm = ref({
  type: ''
})

const pagination = ref({
  currentPage: 1,
  itemsPerPage: 20,
  totalItems: 0,
  totalPages: 0
})

const typeOptions = ref([
  { label: '充值', value: 'recharge' },
  { label: '提现', value: 'withdraw' },
  { label: '订单支付', value: 'order_payment' },
  { label: '购买VIP', value: 'vip_purchase' },
  { label: '后台增加余额', value: 'admin_add' },
  { label: '后台减少余额', value: 'admin_deduct' },
  { label: '网站佣金', value: 'commission' },
  { label: '佣金退款冲回', value: 'commission_refund' },
  { label: '订单冻结', value: 'order_frozen' },
  { label: '订单确认', value: 'order_confirmed' },
  { label: '订单退款', value: 'order_refund' },
  { label: '退款', value: 'refund' },
  { label: '系统调整', value: 'system' }
])

// 计算可用余额
const getAvailableBalance = () => {
  if (!supplierInfo.value) return '0.00'
  const balance = parseFloat(supplierInfo.value.balance || 0)
  const frozen = parseFloat(supplierInfo.value.balanceFrozen || 0)
  return (balance - frozen).toFixed(2)
}

// 加载供应商信息
const loadSupplierInfo = async () => {
  if (!props.supplierId) {
    ElMessage.error('供应商ID不存在')
    return
  }

  loading.value = true
  try {
    const response = await fetch(`/admin${props.adminLoginPath}/supplier-statement/${props.supplierId}/info`, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })

    const result = await response.json()

    if (result.success) {
      supplierInfo.value = result.data
      // 更新货币符号
      if (result.currencySymbol) {
        currencySymbol.value = result.currencySymbol
      }
    } else {
      ElMessage.error(result.message || '加载供应商信息失败')
    }
  } catch (error) {
    ElMessage.error('加载供应商信息失败: ' + error.message)
  } finally {
    loading.value = false
  }
}

// 加载余额记录
const loadBalanceHistories = async (page = 1, limit = 20) => {
  if (!props.supplierId) {
    ElMessage.error('供应商ID不存在')
    return
  }

  tableLoading.value = true
  try {
    const params = new URLSearchParams({
      page: page,
      limit: limit,
      supplierId: props.supplierId,
      userType: 'supplier'
    })

    if (searchForm.value.type) {
      params.append('type', searchForm.value.type)
    }

    const response = await fetch(`/admin${props.adminLoginPath}/supplier-statement/${props.supplierId}/data?${params}`, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })

    const result = await response.json()

    if (result.success) {
      balanceHistories.value = result.data
      pagination.value = {
        ...pagination.value,
        ...result.pagination
      }
    } else {
      ElMessage.error(result.message || '加载余额记录失败')
    }
  } catch (error) {
    ElMessage.error('加载余额记录失败: ' + error.message)
  } finally {
    tableLoading.value = false
  }
}

// 初始化数据
const initData = async () => {
  // 先清空所有数据
  clearAllData()
  // 再加载新数据
  await loadSupplierInfo()
  await loadBalanceHistories()
}

// 清空所有数据
const clearAllData = () => {
  supplierInfo.value = null
  balanceHistories.value = []
  verifyResults.value = []
  calculatedBalance.value = {
    frozen: '0.00',
    pending: '0.00',
    available: '0.00',
    calculated: false,
    frozenMatch: true,
    pendingMatch: true,
    availableMatch: true
  }
  searchForm.value = {
    type: ''
  }
  pagination.value = {
    currentPage: 1,
    itemsPerPage: 20,
    totalItems: 0,
    totalPages: 0
  }
}

// 刷新数据
const refreshData = () => {
  initData()
}

// 搜索
const searchStatements = () => {
  pagination.value.currentPage = 1
  loadBalanceHistories()
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    type: ''
  }
  searchStatements()
}

// 分页处理
const handleSizeChange = (val) => {
  pagination.value.itemsPerPage = val
  loadBalanceHistories(pagination.value.currentPage, val)
}

const handleCurrentChange = (val) => {
  loadBalanceHistories(val, pagination.value.itemsPerPage)
}

// 格式化金额
const formatCurrency = (amount) => {
  if (amount === null || amount === undefined || amount === '') return '0.00'
  const num = parseFloat(amount)
  if (isNaN(num)) return '0.00'
  return Math.abs(num).toFixed(2)
}

// 格式化带符号的金额
const formatCurrencyWithSign = (amount) => {
  if (amount === null || amount === undefined || amount === '') return '0.00'
  const num = parseFloat(amount)
  if (isNaN(num)) return '0.00'
  const sign = num >= 0 ? '+' : ''
  return `${sign}${num.toFixed(2)}`
}

// 获取金额样式类
const getAmountClass = (amount) => {
  if (amount === null || amount === undefined || amount === '') return ''
  const num = parseFloat(amount || 0)
  if (isNaN(num)) return ''
  if (num > 0) return 'amount-positive'
  if (num < 0) return 'amount-negative'
  return ''
}

// 获取业务类型文本
const getTypeText = (type) => {
  const option = typeOptions.value.find(opt => opt.value === type)
  return option ? option.label : type
}

// 获取业务类型标签类型
const getTypeTagType = (type) => {
  const typeMap = {
    'recharge': 'success',
    'withdraw': 'warning',
    'order_payment': 'primary',
    'vip_purchase': 'primary',
    'admin_add': 'success',
    'admin_deduct': 'danger',
    'commission': 'warning',
    'commission_refund': 'success',
    'order_frozen': 'warning',
    'order_confirmed': 'success',
    'order_refund': 'danger',
    'refund': 'danger',
    'system': 'info'
  }
  return typeMap[type] || 'info'
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

// 格式化时间
const formatTime = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')
  return `${hours}:${minutes}:${seconds}`
}

// 关闭对账单（触发导航回供应商列表）
const closeStatement = () => {
  window.dispatchEvent(new CustomEvent('close-current-tab'))
}

// 动态计算余额
const calculateBalance = async () => {
  if (!props.supplierId) {
    ElMessage.error('供应商ID不存在')
    return
  }

  calculating.value = true
  verifyResults.value = []
  
  try {
    const response = await fetch(`/admin${props.adminLoginPath}/supplier-statement/${props.supplierId}/calculate-balance`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      }
    })

    const result = await response.json()

    if (result.success) {
      const data = result.data
      
      // 更新计算结果（只保留三个字段）
      calculatedBalance.value = {
        frozen: data.calculatedFrozen,
        pending: data.calculatedPending || '0.00',
        available: data.calculatedAvailable,
        calculated: true,
        frozenMatch: data.frozenMatch,
        pendingMatch: data.pendingMatch !== undefined ? data.pendingMatch : true,
        availableMatch: data.availableMatch
      }

      // 生成提示信息（一行一行）
      if (!data.frozenMatch || !data.pendingMatch || !data.availableMatch) {
        verifyResults.value.push({ type: 'error', message: '余额校验不匹配！' })
        verifyResults.value.push({ type: 'divider', message: '' })
        
        if (!data.frozenMatch) {
          const diff = (parseFloat(data.actualFrozen) - parseFloat(data.calculatedFrozen)).toFixed(2)
          verifyResults.value.push({ 
            type: 'mismatch', 
            message: `冻结余额差异: ¥${diff}`,
            actual: `实际值: ¥${data.actualFrozen}`,
            calculated: `计算值: ¥${data.calculatedFrozen}`,
            actualClass: 'frozen-color',
            calculatedClass: 'frozen-color'
          })
        }
        
        if (!data.pendingMatch) {
          const diff = (parseFloat(data.actualPending || 0) - parseFloat(data.calculatedPending || 0)).toFixed(2)
          verifyResults.value.push({ 
            type: 'mismatch', 
            message: `订单待结算差异: ¥${diff}`,
            actual: `实际值: ¥${data.actualPending || '0.00'}`,
            calculated: `计算值: ¥${data.calculatedPending || '0.00'}`,
            actualClass: 'pending-color',
            calculatedClass: 'pending-color'
          })
        }
        
        if (!data.availableMatch) {
          const diff = (parseFloat(data.actualAvailable) - parseFloat(data.calculatedAvailable)).toFixed(2)
          verifyResults.value.push({ 
            type: 'mismatch', 
            message: `可用余额差异: ¥${diff}`,
            actual: `实际值: ¥${data.actualAvailable}`,
            calculated: `计算值: ¥${data.calculatedAvailable}`,
            actualClass: 'available-color',
            calculatedClass: 'available-color'
          })
        }
      } else {
        verifyResults.value.push({ type: 'success', message: '✓ 余额校验通过，数据一致！' })
        verifyResults.value.push({ type: 'info', message: `共计算 ${data.totalRecords} 条余额记录` })
      }
    } else {
      verifyResults.value = [{ type: 'error', message: result.message || '计算余额失败' }]
    }

  } catch (error) {
    console.error('计算余额失败:', error)
    verifyResults.value = [{ type: 'error', message: `计算余额失败: ${error.message}` }]
  } finally {
    calculating.value = false
  }
}

// 获取计算余额的样式类
const getCalculatedBalanceClass = (type) => {
  if (!calculatedBalance.value.calculated) return 'calculated-value'
  
  if (type === 'frozen') {
    return calculatedBalance.value.frozenMatch ? 'calculated-value match' : 'calculated-value mismatch'
  } else if (type === 'pending') {
    return calculatedBalance.value.pendingMatch ? 'calculated-value match' : 'calculated-value mismatch'
  } else if (type === 'available') {
    return calculatedBalance.value.availableMatch ? 'calculated-value match' : 'calculated-value mismatch'
  }
  
  return 'calculated-value'
}

// 暴露方法供父组件调用
defineExpose({
  initData
})

onMounted(() => {
  if (props.autoLoad) {
    initData()
  }
})
</script>

<style scoped>
.supplier-statement-container {
  width: 100%;
  max-width: 1600px;
  box-sizing: border-box;
  margin: 0 auto;
  padding: 20px;
}

/* 页面头部 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #e4e7ed;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

.title-icon {
  font-size: 28px;
  color: #409eff;
}

.header-actions {
  display: flex;
  gap: 10px;
}

/* 供应商信息卡片 */
.supplier-info-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-icon {
  font-size: 18px;
  color: #409eff;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
}

.balance-value {
  font-size: 18px;
  font-weight: bold;
  color: #67c23a;
}

.frozen-value {
  font-size: 18px;
  font-weight: bold;
  color: #e6a23c;
}

.available-value {
  font-size: 18px;
  font-weight: bold;
  color: #409eff;
}

/* 计算余额样式 */
.calculated-value {
  font-size: 18px;
  font-weight: bold;
  color: #909399;
}

.calculated-value.match {
  color: #67c23a;
}

.calculated-value.mismatch {
  color: #f56c6c;
}

/* 校验按钮区域 */
.verify-actions {
  margin-bottom: 20px;
  text-align: center;
}

/* 校验结果提示 */
.verify-message {
  margin-bottom: 20px;
  padding: 15px 20px;
  border-radius: 4px;
  background-color: #ffffff;
  border: 1px solid #e4e7ed;
}

.verify-line {
  padding: 6px 0;
  font-size: 14px;
  line-height: 1.6;
  display: flex;
  align-items: center;
  gap: 15px;
}

.verify-line.success {
  color: #67c23a;
  font-weight: bold;
}

.verify-line.error {
  color: #f56c6c;
  font-weight: bold;
}

.verify-line.mismatch {
  color: #606266;
}

.verify-line.divider {
  height: 0;
  padding: 0;
  margin: 0;
}

.verify-line.info {
  color: #909399;
}

.verify-line .error-text {
  color: #f56c6c;
  font-weight: bold;
  min-width: 150px;
}

.verify-line .balance-color {
  color: #67c23a;
  font-weight: bold;
}

.verify-line .frozen-color {
  color: #e6a23c;
  font-weight: bold;
}

.verify-line .available-color {
  color: #409eff;
  font-weight: bold;
}

/* 筛选卡片 */
.filter-card {
  margin-bottom: 20px;
}

.filter-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e4e7ed;
}

.filter-icon {
  font-size: 18px;
  color: #409eff;
}

.filter-title {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
}

.search-form {
  margin: 0;
}

.form-actions {
  display: flex;
  gap: 10px;
}

/* 表格卡片 */
.table-card {
  margin-bottom: 20px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.table-header-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
}

.table-icon {
  font-size: 18px;
  color: #409eff;
}

.table-header-info {
  font-size: 14px;
  color: #909399;
}

/* 表格样式 */
.balance-history-table {
  width: 100%;
}

.description-text {
  color: #606266;
}

.amount-cell,
.balance-cell,
.frozen-cell {
  display: flex;
  justify-content: center;
  align-items: center;
}

.amount-cell.multi-line,
.balance-cell.multi-line {
  flex-direction: column;
  gap: 4px;
  padding: 8px 0;
}

.line-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
}

.line-item .label {
  color: #909399;
  font-size: 12px;
}

.amount-value {
  font-weight: 600;
  font-size: 14px;
}

.amount-positive {
  color: #67c23a;
}

.amount-negative {
  color: #f56c6c;
}

.balance-value {
  color: #67c23a;
  font-weight: 600;
  font-size: 14px;
}

.frozen-balance-value {
  color: #e6a23c;
  font-weight: 600;
  font-size: 14px;
}

.frozen-value {
  font-weight: 600;
  font-size: 14px;
}

.pending-value {
  font-weight: 600;
  font-size: 14px;
}

.pending-balance-value {
  color: #409eff;
  font-weight: 600;
  font-size: 14px;
}

.type-tag {
  font-size: 12px;
}

.time-cell {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.date {
  font-weight: 600;
  color: #303133;
}

.time {
  font-size: 12px;
  color: #909399;
}

/* 分页 */
.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

/* 响应式 */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }

  .header-actions {
    width: 100%;
  }

  .header-actions button {
    flex: 1;
  }

  .action-col {
    margin-top: 10px;
  }

  .form-actions {
    flex-direction: column;
    width: 100%;
  }

  .form-actions button {
    width: 100%;
  }
}
</style>
