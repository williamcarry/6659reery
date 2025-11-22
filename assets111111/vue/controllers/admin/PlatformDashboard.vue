<template>
  <div class="platform-dashboard">
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
        <el-col :span="5">
          <el-card shadow="hover" class="stats-card primary">
            <el-statistic title="今日GMV" :value="stats.todayGMV" :precision="2" :prefix="stats.currencySymbol" />
          </el-card>
        </el-col>
        
        <el-col :span="5">
          <el-card shadow="hover" class="stats-card">
            <el-statistic title="今日订单数" :value="stats.todayOrderCount" />
          </el-card>
        </el-col>
        
        <el-col :span="5">
          <el-card shadow="hover" class="stats-card success">
            <el-statistic title="新增客户" :value="stats.todayNewCustomers" />
          </el-card>
        </el-col>
        
        <el-col :span="5">
          <el-card shadow="hover" class="stats-card warning">
            <el-statistic title="新增供应商" :value="stats.todayNewSuppliers" />
          </el-card>
        </el-col>
        
        <el-col :span="4">
          <el-card shadow="hover" class="stats-card danger">
            <el-statistic title="平台佣金" :value="stats.todayCommission" :precision="2" :prefix="stats.currencySymbol" />
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
  adminLoginPath: {
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
  todayGMV: 0,
  todayOrderCount: 0,
  todayNewCustomers: 0,
  todayNewSuppliers: 0,
  todayCommission: 0,
  currencySymbol: '$'
})

const loadPlatformData = async () => {
  loading.value = true
  error.value = null
  
  try {
    const loginPath = props.adminLoginPath || window.adminLoginPath || ''
    const response = await fetch(`/api/admin/stats/platform/overview`, {
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
        todayGMV: result.todayGMV || 0,
        todayOrderCount: result.todayOrderCount || 0,
        todayNewCustomers: result.todayNewCustomers || 0,
        todayNewSuppliers: result.todayNewSuppliers || 0,
        todayCommission: result.todayCommission || 0,
        currencySymbol: result.currencySymbol || '$'
      }
    } else {
      error.value = result.message || '加载数据失败'
    }
  } catch (err) {
    error.value = '网络错误: ' + err.message
    console.error('加载平台概览数据失败:', err)
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
    const clearResponse = await fetch('/api/admin/stats/cache/clear', {
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
    await loadPlatformData()
    
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
    loadPlatformData()
  }
})

defineExpose({
  loadData: loadPlatformData,
  loadPlatformData
})
</script>

<style scoped>
.platform-dashboard {
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
  text-align: center;
}

.stats-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.stats-card.primary :deep(.el-statistic__number) {
  color: #409EFF;
}

.stats-card.success :deep(.el-statistic__number) {
  color: #67C23A;
}

.stats-card.warning :deep(.el-statistic__number) {
  color: #E6A23C;
}

.stats-card.danger :deep(.el-statistic__number) {
  color: #F56C6C;
}
</style>
