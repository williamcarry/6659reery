<template>
  <el-dialog
    v-model="dialogVisible"
    title="物流查询"
    width="800px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <div v-loading="loading" class="tracking-container">
      <!-- 快递基本信息 -->
      <div v-if="trackingData && !trackingData.error" class="tracking-header">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="快递单号">
            <span class="express-no">{{ trackingData.expressNo }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="快递公司">
            <div style="display: flex; align-items: center; gap: 8px;">
              <span>{{ trackingData.companyName }}</span>
              <el-tag size="small">{{ trackingData.companyCode }}</el-tag>
            </div>
          </el-descriptions-item>
          <el-descriptions-item label="当前状态">
            <el-tag :type="getStatusType(trackingData.status)" size="large">
              {{ trackingData.statusText }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="客服电话">
            {{ trackingData.companyPhone || '-' }}
          </el-descriptions-item>
        </el-descriptions>
      </div>

      <!-- 错误信息 -->
      <el-alert
        v-if="trackingData && trackingData.error"
        :title="trackingData.message || '查询失败'"
        type="error"
        :closable="false"
        show-icon
      />

      <!-- 无物流信息 -->
      <el-empty
        v-if="trackingData && !trackingData.error && !trackingData.hasTracking"
        description="暂无物流信息"
      />

      <!-- 物流轨迹 -->
      <div v-if="trackingData && !trackingData.error && trackingData.hasTracking" class="tracking-timeline">
        <h3 class="timeline-title">物流轨迹</h3>
        <el-timeline>
          <el-timeline-item
            v-for="(trace, index) in trackingData.traces"
            :key="index"
            :timestamp="trace.time"
            :type="index === 0 ? 'primary' : 'info'"
            :size="index === 0 ? 'large' : 'normal'"
            placement="top"
          >
            <el-card :class="{ 'latest-trace': index === 0 }">
              <div class="trace-content">
                <div class="trace-desc">{{ trace.description }}</div>
                <div v-if="trace.areaName" class="trace-area">
                  <el-icon><Location /></el-icon>
                  {{ trace.areaName }}
                </div>
              </div>
            </el-card>
          </el-timeline-item>
        </el-timeline>
      </div>
    </div>

    <template #footer>
      <el-button @click="handleClose">关闭</el-button>
      <el-button type="primary" @click="handleRefresh" :loading="loading">
        <el-icon><Refresh /></el-icon>
        刷新
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref } from 'vue'
import {
  ElDialog,
  ElDescriptions,
  ElDescriptionsItem,
  ElTag,
  ElTimeline,
  ElTimelineItem,
  ElCard,
  ElAlert,
  ElEmpty,
  ElButton,
  ElIcon,
  ElMessage,
  vLoading
} from 'element-plus'
import { Location, Refresh } from '@element-plus/icons-vue'

const props = defineProps({
  supplierLoginPath: {
    type: String,
    default: ''
  }
})

const dialogVisible = ref(false)
const loading = ref(false)
const trackingData = ref(null)
const currentExpressNo = ref('')

/**
 * 打开弹窗
 */
const open = (expressNo) => {
  if (!expressNo) {
    ElMessage.warning('快递单号不能为空')
    return
  }
  
  currentExpressNo.value = expressNo
  dialogVisible.value = true
  fetchTracking(expressNo)
}

/**
 * 查询物流信息
 */
const fetchTracking = async (expressNo) => {
  loading.value = true
  try {
    const response = await fetch(`/api/common/express/track?expressNo=${encodeURIComponent(expressNo)}`, {
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    
    const result = await response.json()
    
    if (result.success) {
      trackingData.value = result.data
    } else {
      trackingData.value = {
        error: true,
        message: result.message || '查询失败'
      }
    }
  } catch (error) {
    trackingData.value = {
      error: true,
      message: '网络请求失败: ' + error.message
    }
  } finally {
    loading.value = false
  }
}

/**
 * 刷新物流信息
 */
const handleRefresh = () => {
  if (currentExpressNo.value) {
    fetchTracking(currentExpressNo.value)
  }
}

/**
 * 关闭弹窗
 */
const handleClose = () => {
  dialogVisible.value = false
  trackingData.value = null
  currentExpressNo.value = ''
}

/**
 * 获取状态标签类型
 */
const getStatusType = (status) => {
  const statusMap = {
    'WAIT_ACCEPT': 'info',
    'ACCEPT': 'primary',
    'TRANSPORT': 'warning',
    'DELIVERING': 'warning',
    'AGENT_SIGN': 'success',
    'SIGN': 'success',
    'FAILED': 'danger',
    'UNKNOWN': 'info'
  }
  return statusMap[status] || 'info'
}

defineExpose({
  open
})
</script>

<style scoped>
.tracking-container {
  min-height: 300px;
}

.tracking-header {
  margin-bottom: 24px;
}

.express-no {
  font-size: 16px;
  font-weight: 600;
  color: #409eff;
  font-family: 'Courier New', monospace;
}

.timeline-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 16px;
  padding-left: 12px;
  border-left: 3px solid #409eff;
}

.latest-trace {
  background: #ecf5ff;
  border-color: #409eff;
}

.trace-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.trace-desc {
  font-size: 14px;
  color: #303133;
  line-height: 1.6;
}

.trace-area {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #909399;
}
</style>
