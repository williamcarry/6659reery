<template>
  <div class="site-message-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2 class="page-title">
        <el-icon class="title-icon"><Message /></el-icon>
        公告消息
      </h2>
      <div class="header-actions">
        <el-button type="danger" @click="batchDelete" :icon="Delete" :disabled="selectedMessages.length === 0">
          批量删除 ({{ selectedMessages.length }})
        </el-button>
        <el-button type="primary" @click="showCreateDialog" :icon="Plus">
          添加公告消息
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
          <el-col :span="4" :xs="24">
            <el-form-item label="关键词">
              <el-input v-model="searchForm.keyword" placeholder="请输入标题或内容" />
            </el-form-item>
          </el-col>
          <el-col :span="4" :xs="24">
            <el-form-item label="消息类型">
              <el-select v-model="searchForm.messageType" placeholder="请选择消息类型" clearable style="width: 100%;">
                <el-option label="全部" value="" />
                <el-option label="商城公告" value="mall_announcement" />
                <el-option label="平台消息" value="platform_message" />
                <el-option label="私信消息" value="private_message" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="4" :xs="24">
            <el-form-item label="优先级">
              <el-select v-model="searchForm.priority" placeholder="请选择优先级" clearable style="width: 100%;">
                <el-option label="全部" value="" />
                <el-option label="低" value="low" />
                <el-option label="普通" value="normal" />
                <el-option label="高" value="high" />
                <el-option label="紧急" value="urgent" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="4" :xs="24">
            <el-form-item label="草稿状态">
              <el-select v-model="searchForm.isDraft" placeholder="请选择草稿状态" clearable style="width: 100%;">
                <el-option label="全部" value="" />
                <el-option label="草稿" value="1" />
                <el-option label="已发送" value="0" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8" :xs="24" class="action-col">
            <el-form-item label=" ">
              <div class="form-actions">
                <el-button type="primary" @click="searchMessages" :icon="Search">
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
    
    <!-- 公告消息表格 -->
    <el-card class="table-card">
      <template #header>
        <div class="table-header">
          <div class="table-header-title">
            <el-icon class="table-icon"><List /></el-icon>
            公告消息列表
          </div>
          <div class="table-header-info">
            共 {{ pagination.totalItems }} 条记录
          </div>
        </div>
      </template>
      
      <el-table 
        :data="messages" 
        class="site-message-table" 
        v-loading="loading"
        :fit="true"
        :border="false"
        :header-cell-style="{ textAlign: 'center' }"
        :cell-style="{ textAlign: 'center' }"
        :stripe="true"
        empty-text="暂无公告消息记录"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" fixed />
        <el-table-column label="序号" width="60" fixed>
          <template #default="scope">
            {{ (pagination.currentPage - 1) * pagination.itemsPerPage + scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip>
          <template #default="scope">
            <el-button type="text" @click="viewMessage(scope.row)" style="color: #409eff;">
              {{ scope.row.title }}
            </el-button>
          </template>
        </el-table-column>
        <el-table-column prop="messageType" label="消息类型" min-width="100">
          <template #default="scope">
            <el-tag v-if="scope.row.messageType === 'mall_announcement'" type="danger">商城公告</el-tag>
            <el-tag v-else-if="scope.row.messageType === 'platform_message'" type="warning">平台消息</el-tag>
            <el-tag v-else-if="scope.row.messageType === 'private_message'" type="info">私信消息</el-tag>
            <el-tag v-else>{{ scope.row.messageType }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="priority" label="优先级" min-width="100">
          <template #default="scope">
            <el-tag v-if="scope.row.priority === 'urgent'" type="danger">紧急</el-tag>
            <el-tag v-else-if="scope.row.priority === 'high'" type="warning">高</el-tag>
            <el-tag v-else-if="scope.row.priority === 'normal'" type="success">普通</el-tag>
            <el-tag v-else-if="scope.row.priority === 'low'" type="info">低</el-tag>
            <el-tag v-else>{{ scope.row.priority }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="recipientType" label="接收对象" min-width="120">
          <template #default="scope">
            <el-tag v-if="scope.row.recipientType === 'all'" type="success">全部用户</el-tag>
            <el-tag v-else-if="scope.row.recipientType === 'supplier'" type="warning">供应商</el-tag>
            <el-tag v-else-if="scope.row.recipientType === 'customer'" type="primary">普通用户</el-tag>
            <el-tag v-else type="info">未指定</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="isDraft" label="状态" min-width="100">
          <template #default="scope">
            <el-tag :type="scope.row.isDraft ? 'info' : 'success'">
              {{ scope.row.isDraft ? '草稿' : '已发送' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="sendTime" label="发送时间" min-width="160" sortable>
          <template #default="scope">
            <div class="time-cell">
              <div class="date">{{ formatDate(scope.row.sendTime) }}</div>
              <div class="time">{{ formatTime(scope.row.sendTime) }}</div>
            </div>
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
        <el-table-column label="操作" min-width="250" fixed="right">
          <template #default="scope">
            <el-button size="small" @click="viewMessage(scope.row)">查看</el-button>
            <el-button size="small" @click="editMessage(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteMessage(scope.row)">删除</el-button>
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

    <!-- 查看详情对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="currentMessage.title"
      width="800px"
      :close-on-click-modal="false"
    >
      <div class="message-detail">
        <div class="detail-row">
          <span class="label">英文标题：</span>
          <span class="value">{{ currentMessage.titleEn || '-' }}</span>
        </div>
        <div class="detail-row">
          <span class="label">消息类型：</span>
          <el-tag v-if="currentMessage.messageType === 'mall_announcement'" type="danger">商城公告</el-tag>
          <el-tag v-else-if="currentMessage.messageType === 'platform_message'" type="warning">平台消息</el-tag>
          <el-tag v-else-if="currentMessage.messageType === 'private_message'" type="info">私信消息</el-tag>
          <el-tag v-else>{{ currentMessage.messageType }}</el-tag>
        </div>
        <div class="detail-row">
          <span class="label">优先级：</span>
          <el-tag v-if="currentMessage.priority === 'urgent'" type="danger">紧急</el-tag>
          <el-tag v-else-if="currentMessage.priority === 'high'" type="warning">高</el-tag>
          <el-tag v-else-if="currentMessage.priority === 'normal'" type="success">普通</el-tag>
          <el-tag v-else-if="currentMessage.priority === 'low'" type="info">低</el-tag>
          <el-tag v-else>{{ currentMessage.priority }}</el-tag>
        </div>
        <div class="detail-row">
          <span class="label">状态：</span>
          <el-tag :type="currentMessage.isDraft ? 'info' : 'success'">
            {{ currentMessage.isDraft ? '草稿' : '已发送' }}
          </el-tag>
        </div>
        <div class="detail-row">
          <span class="label">接收对象：</span>
          <el-tag v-if="currentMessage.recipientType === 'all'" type="success">全部用户</el-tag>
          <el-tag v-else-if="currentMessage.recipientType === 'supplier'" type="warning">供应商</el-tag>
          <el-tag v-else-if="currentMessage.recipientType === 'customer'" type="primary">普通用户</el-tag>
          <el-tag v-else type="info">未指定</el-tag>
        </div>
        <div class="detail-row" v-if="currentMessage.sendTime">
          <span class="label">发送时间：</span>
          <span class="value">{{ currentMessage.sendTime }}</span>
        </div>
        <div class="detail-row">
          <span class="label">创建时间：</span>
          <span class="value">{{ currentMessage.createdAt }}</span>
        </div>
        <div class="detail-content">
          <div class="content-label">消息内容：</div>
          <div class="content-box" v-html="currentMessage.content"></div>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">关闭</el-button>
          <el-button type="primary" @click="editCurrentMessage">编辑</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, defineProps, defineExpose } from 'vue'
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
  vLoading
} from 'element-plus'
import {
  Message,
  Search,
  Refresh,
  RefreshLeft,
  List,
  Plus,
  Delete
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
const messages = ref([])
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
  messageType: '',
  priority: '',
  isDraft: ''
})

// 对话框显示控制
const dialogVisible = ref(false)
const currentMessage = ref({})

// 批量选择
const selectedMessages = ref([])

// 加载站内信数据
const loadMessageData = async (page = 1, limit = 20) => {
  loading.value = true
  try {
    const params = new URLSearchParams({
      page: page,
      limit: limit,
      keyword: searchForm.value.keyword,
      messageType: searchForm.value.messageType,
      priority: searchForm.value.priority,
      isDraft: searchForm.value.isDraft
    })
    
    const url = `/admin${props.adminLoginPath}/site-message/list/tab?${params}`
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    
    const result = await response.json()
    
    if (result.success) {
      messages.value = result.data
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
  loadMessageData(pagination.value.currentPage, pagination.value.itemsPerPage)
}

// 搜索站内信
const searchMessages = () => {
  pagination.value.currentPage = 1
  loadMessageData(1, pagination.value.itemsPerPage)
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    keyword: '',
    messageType: '',
    priority: '',
    isDraft: ''
  }
  pagination.value.currentPage = 1
  loadMessageData(1, pagination.value.itemsPerPage)
}

// 处理分页大小变化
const handleSizeChange = (val) => {
  pagination.value.itemsPerPage = val
  loadMessageData(pagination.value.currentPage, val)
}

// 处理当前页变化
const handleCurrentChange = (val) => {
  pagination.value.currentPage = val
  loadMessageData(val, pagination.value.itemsPerPage)
}

// 查看消息详情
const viewMessage = (message) => {
  currentMessage.value = { ...message }
  dialogVisible.value = true
}

// 编辑当前消息
const editCurrentMessage = () => {
  dialogVisible.value = false
  editMessage(currentMessage.value)
}

// 编辑站内信
const editMessage = (message) => {
  // 触发导航事件，在新标签页中打开站内信编辑
  window.dispatchEvent(new CustomEvent('navigate-to-site-message-edit', {
    detail: { messageId: message.id }
  }))
}

// 删除站内信
const deleteMessage = (message) => {
  ElMessageBox.confirm(
    `确定要删除站内信 "${message.title}" 吗？此操作不可恢复。`,
    '确认删除',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(async () => {
    try {
      const response = await fetch(`/admin${props.adminLoginPath}/site-message/${message.id}/delete`, {
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
        loadMessageData(pagination.value.currentPage, pagination.value.itemsPerPage)
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

// 处理选择变化
const handleSelectionChange = (selection) => {
  selectedMessages.value = selection
}

// 批量删除
const batchDelete = () => {
  if (selectedMessages.value.length === 0) {
    ElMessage.warning('请先选择要删除的公告')
    return
  }
  
  ElMessageBox.confirm(
    `确定要删除选中的 ${selectedMessages.value.length} 条公告吗？此操作不可恢复。`,
    '确认批量删除',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(async () => {
    try {
      const ids = selectedMessages.value.map(msg => msg.id)
      
      const response = await fetch(`/admin${props.adminLoginPath}/site-message/batch-delete`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({ ids })
      })
      
      const result = await response.json()
      
      if (result.success) {
        ElMessage.success(result.message || `成功删除 ${result.deletedCount} 条公告`)
        // 清空选择
        selectedMessages.value = []
        // 重新加载数据
        loadMessageData(pagination.value.currentPage, pagination.value.itemsPerPage)
      } else {
        ElMessage.error(result.error || '批量删除失败')
      }
    } catch (error) {
      ElMessage.error('批量删除失败: ' + error.message)
    }
  }).catch(() => {
    // 用户取消删除
  })
}

// 显示创建对话框
const showCreateDialog = () => {
  // 触发导航事件，在新标签页中打开站内信创建
  window.dispatchEvent(new CustomEvent('navigate-to-site-message-create'))
}

// 组件挂载时加载数据
onMounted(() => {
  // 只有当 autoLoad 为 true 时才自动加载数据
  if (props.autoLoad) {
    loadMessageData()
  }
  
  // 监听刷新列表事件
  window.addEventListener('refresh-site-message-list', refreshData)
})

// 组件卸载时移除事件监听
onUnmounted(() => {
  window.removeEventListener('refresh-site-message-list', refreshData)
})

// 暴露方法给父组件调用
defineExpose({
  loadMessageData
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
.site-message-container {
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

.site-message-table {
  width: 100% !important;
  font-size: 14px;
}

.site-message-table :deep(.el-table__header th) {
  background-color: #f5f7fa;
  color: #606266;
  font-weight: bold;
}

/* 解决鼠标悬停时序号列变色延迟的问题 */
.site-message-table :deep(.el-table__body td) {
  transition: background-color 0.3s;
}

.site-message-table :deep(.el-table__row:hover) {
  background-color: #f5f7fa;
}

.site-message-table :deep(.el-table__row:hover td) {
  background-color: #f5f7fa !important;
}

/* 确保固定列也有一致的悬停效果 */
.site-message-table :deep(.el-table__fixed .el-table__row:hover td) {
  background-color: #f5f7fa !important;
}

/* 确保序号列在悬停时立即响应 */
.site-message-table :deep(.el-table__row:hover .el-table-fixed-column--left) {
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

/* 消息详情对话框样式 */
.message-detail {
  padding: 10px 0;
}

.detail-row {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.detail-row .label {
  font-weight: bold;
  color: #606266;
  width: 100px;
  flex-shrink: 0;
}

.detail-row .value {
  color: #303133;
  flex: 1;
}

.detail-content {
  margin-top: 20px;
}

.content-label {
  font-weight: bold;
  color: #606266;
  margin-bottom: 10px;
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.content-box {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 15px;
  background-color: #fff;
  min-height: 200px;
  max-height: 400px;
  overflow-y: auto;
  line-height: 1.6;
}

.content-box :deep(img) {
  max-width: 100%;
  height: auto;
}

.content-box :deep(p) {
  margin: 0 0 10px 0;
}

.content-box :deep(h1),
.content-box :deep(h2),
.content-box :deep(h3),
.content-box :deep(h4),
.content-box :deep(h5),
.content-box :deep(h6) {
  margin: 15px 0 10px 0;
}

.content-box :deep(ul),
.content-box :deep(ol) {
  margin: 10px 0;
  padding-left: 30px;
}

.content-box :deep(blockquote) {
  border-left: 4px solid #dcdfe6;
  padding-left: 15px;
  margin: 10px 0;
  color: #606266;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>