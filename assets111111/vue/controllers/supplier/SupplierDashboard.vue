<template>
  <div class="supplier-dashboard">
    <!-- 清理缓存按钮 -->
    <div class="dashboard-header">
      <el-button 
        type="primary" 
        :icon="Refresh" 
        :loading="clearing" 
        @click="clearCacheAndReload"
        class="clear-cache-btn"
      >
        {{ clearing ? '清理中...' : '清理统计缓存并重新载入' }}
      </el-button>
    </div>
    
    <div v-loading="loading" element-loading-background="rgba(255, 255, 255, 0.5)">
      <!-- 核心指标卡片 -->
      <el-row :gutter="20" style="margin-bottom: 20px">
        <el-col :span="6">
          <el-card shadow="hover" class="stats-card">
            <el-statistic title="今日订单数" :value="stats.todayOrderCount" />
            <div class="stats-footer">
              <span v-if="stats.orderGrowth !== undefined" 
                    :class="stats.orderGrowth >= 0 ? 'growth-up' : 'growth-down'">
                {{ stats.orderGrowth >= 0 ? '↑' : '↓' }} {{ Math.abs(stats.orderGrowth) }}%
              </span>
              <span class="footer-text">较昨日</span>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6">
          <el-card shadow="hover" class="stats-card primary">
            <el-statistic title="今日销售额" :value="stats.todaySales" :precision="2" />
            <div class="stats-footer">
              <span v-if="stats.salesGrowth !== undefined"
                    :class="stats.salesGrowth >= 0 ? 'growth-up' : 'growth-down'">
                {{ stats.salesGrowth >= 0 ? '↑' : '↓' }} {{ Math.abs(stats.salesGrowth) }}%
              </span>
              <span class="footer-text">较昨日</span>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6">
          <el-card shadow="hover" class="stats-card warning">
            <el-statistic title="待发货订单" :value="stats.pendingShipmentCount" />
            <div class="stats-footer">
              <span v-if="stats.shipmentGrowth !== undefined"
                    :class="stats.shipmentGrowth >= 0 ? 'growth-up' : 'growth-down'">
                {{ stats.shipmentGrowth >= 0 ? '↑' : '↓' }} {{ Math.abs(stats.shipmentGrowth) }}%
              </span>
              <span class="footer-text">较昨日</span>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6">
          <el-card shadow="hover" class="stats-card success">
            <el-statistic title="待结算金额" :value="stats.pendingSettlementAmount" :precision="2" />
            <div class="stats-footer">
              <span class="footer-text">账户余额: {{ stats.accountBalance?.toFixed(2) || '0.00' }}</span>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 错误提示 -->
      <el-alert
        v-if="error"
        :title="error"
        type="error"
        :closable="false"
        show-icon
        style="margin-bottom: 20px"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { 
  ElCard, 
  ElRow, 
  ElCol, 
  ElStatistic, 
  ElAlert,
  ElButton,
  ElMessage,
  ElMessageBox,
  ElLoading
} from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import { vLoading } from 'element-plus/es/components/loading/src/directive'

const props = defineProps({
  supplierLoginPath: {
    type: String,
    default: ''
  },
  autoLoad: {
    type: Boolean,
    default: true
  }
})

const loading = ref(false)
const clearing = ref(false)
const error = ref(null)
const stats = ref({
  todayOrderCount: 0,
  todaySales: 0,
  pendingShipmentCount: 0,
  pendingSettlementAmount: 0,
  accountBalance: 0,
  orderGrowth: 0,
  salesGrowth: 0,
  shipmentGrowth: 0
})

const loadDashboardData = async () => {
  loading.value = true
  error.value = null
  
  try {
    const loginPath = props.supplierLoginPath || window.supplierLoginPath || ''
    const response = await fetch(`/api/supplier/stats/dashboard`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const result = await response.json()
    
    if (result.success !== false) {
      stats.value = {
        todayOrderCount: result.todayOrderCount || 0,
        todaySales: result.todaySales || 0,
        pendingShipmentCount: result.pendingShipmentCount || 0,
        pendingSettlementAmount: result.pendingSettlementAmount || 0,
        accountBalance: result.accountBalance || 0,
        orderGrowth: result.orderGrowth,
        salesGrowth: result.salesGrowth,
        shipmentGrowth: result.shipmentGrowth
      }
    } else {
      error.value = result.message || '加载数据失败'
    }
  } catch (err) {
    error.value = '网络错误: ' + err.message
    console.error('加载供应商首页数据失败:', err)
  } finally {
    loading.value = false
  }
}

const clearCacheAndReload = async () => {
  // 弹出确认对话框
  const confirmed = await ElMessageBox.confirm(
    '系统缓存会自动定时刷新，通常无需手动清理。确定要立即清理缓存并重新加载数据吗？',
    '确认操作',
    {
      confirmButtonText: '确定清理',
      cancelButtonText: '取消',
      type: 'warning',
      center: true
    }
  ).catch(() => false)
  
  if (!confirmed) {
    return // 用户取消操作
  }
  
  clearing.value = true
  
  try {
    // 1. 清除缓存
    const clearResponse = await fetch('/api/supplier/stats/cache/clear', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    
    const clearResult = await clearResponse.json()
    
    if (!clearResult.success) {
      throw new Error(clearResult.message || '清除缓存失败')
    }
    
    ElMessage.success({
      message: '缓存清除成功，正在重新加载数据...',
      duration: 2000
    })
    
    // 2. 重新加载数据
    await loadDashboardData()
    
    ElMessage.success({
      message: '数据加载成功！',
      duration: 2000
    })
  } catch (err) {
    ElMessage.error({
      message: '操作失败: ' + err.message,
      duration: 3000
    })
    console.error('清除缓存失败:', err)
  } finally {
    clearing.value = false
  }
}

onMounted(() => {
  if (props.autoLoad) {
    loadDashboardData()
  }
})

defineExpose({
  loadData: loadDashboardData,
  loadDashboardData
})
</script>

<style scoped>
.supplier-dashboard {
  padding: 0;
  position: relative;
}

.dashboard-header {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}

.clear-cache-btn {
  animation: pulse 2s infinite;
}

.clear-cache-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.4);
}

@keyframes pulse {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(64, 158, 255, 0.4);
  }
  50% {
    box-shadow: 0 0 0 8px rgba(64, 158, 255, 0);
  }
}

.stats-card {
  transition: all 0.3s ease;
}

.stats-card:hover {
  transform: translateY(-5px);
}

.stats-card.primary :deep(.el-statistic__number) {
  color: #409EFF;
}

.stats-card.success :deep(.el-statistic__number) {
  color: #67C23A;
}

.stats-card.warning :deep(.el-statistic__head) {
  color: #E6A23C;
}

.stats-card.info :deep(.el-statistic__head) {
  color: #409EFF;
}

.stats-footer {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #EBEEF5;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
}

.growth-up {
  color: #67C23A;
  font-weight: bold;
}

.growth-down {
  color: #F56C6C;
  font-weight: bold;
}

.footer-text {
  color: #909399;
}
</style>
