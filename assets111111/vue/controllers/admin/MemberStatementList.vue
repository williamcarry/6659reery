<template>
  <div class="member-statement-list-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2 class="page-title">
        <el-icon class="title-icon"><TrendCharts /></el-icon>
        会员对账单
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
          <el-col :span="8" :xs="24">
            <el-form-item label="关键词">
              <el-input v-model="searchForm.keyword" placeholder="客户ID/用户名/手机号/邮箱" clearable />
            </el-form-item>
          </el-col>
          <el-col :span="6" :xs="24" class="action-col">
            <el-form-item label=" ">
              <div class="form-actions">
                <el-button type="primary" @click="searchMembers" :icon="Search">
                  搜索
                </el-button>
                <el-button @click="resetSearch" :icon="RefreshLeft">
                  重置
                </el-button>
              </div>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-card>
    
    <!-- 会员对账单表格 -->
    <el-card class="table-card">
      <template #header>
        <div class="table-header">
          <div class="table-header-title">
            <el-icon class="table-icon"><List /></el-icon>
            会员对账单列表
          </div>
          <div class="table-header-info">
            共 {{ pagination.totalItems }} 条记录
          </div>
        </div>
      </template>
      
      <el-table 
        :data="members" 
        class="member-statement-table" 
        v-loading="loading"
        :fit="true"
        :border="false"
        :header-cell-style="{ textAlign: 'center' }"
        :cell-style="{ textAlign: 'center' }"
        :stripe="true"
        empty-text="暂无会员记录"
      >
        <el-table-column label="序号" width="60" fixed>
          <template #default="scope">
            {{ (pagination.currentPage - 1) * pagination.itemsPerPage + scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column prop="customerId" label="客户ID" min-width="120" show-overflow-tooltip />
        <el-table-column prop="username" label="用户名/类型" min-width="150">
          <template #default="scope">
            {{ scope.row.username }}
            <el-tag :type="scope.row.customerType === 'company' ? 'primary' : 'success'" size="small" style="margin-left: 5px;">
              {{ scope.row.customerType === 'company' ? '企业' : '个人' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="联系方式" min-width="200">
          <template #default="scope">
            <div style="display: flex; flex-direction: column; gap: 4px; align-items: flex-start; padding: 8px 0;">
              <div style="width: 100%;"><span style="color: #909399; font-size: 12px;">昵称：</span>{{ scope.row.nickname || '-' }}</div>
              <div style="width: 100%;"><span style="color: #909399; font-size: 12px;">姓名：</span>{{ scope.row.realName || '-' }}</div>
              <div style="width: 100%;"><span style="color: #909399; font-size: 12px;">手机：</span>{{ scope.row.mobile || '-' }}</div>
              <div style="width: 100%;"><span style="color: #909399; font-size: 12px;">邮箱：</span>{{ scope.row.email || '-' }}</div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="余额" min-width="120" sortable>
          <template #default="scope">
            <span style="color: #67c23a; font-weight: 600;">{{ currencySymbol }}{{ formatCurrency(scope.row.balance) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="冻结" min-width="120" sortable>
          <template #default="scope">
            <span style="color: #e6a23c; font-weight: 600;">{{ currencySymbol }}{{ formatCurrency(scope.row.frozenBalance) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="VIP等级" min-width="100">
          <template #default="scope">
            <el-tag :type="getVipTagType(scope.row.vipLevel)">
              {{ scope.row.vipLevelName || 'VIP0' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="注册时间" min-width="160" sortable>
          <template #default="scope">
            <div class="time-cell">
              <div class="date">{{ formatDate(scope.row.createdAt) }}</div>
              <div class="time">{{ formatTime(scope.row.createdAt) }}</div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="180" fixed="right">
          <template #default="scope">
            <el-button size="small" @click="viewMember(scope.row)">查看</el-button>
            <el-button size="small" type="primary" @click="viewStatement(scope.row)">对账单</el-button>
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

const members = ref([])
const loading = ref(false)
const currencySymbol = ref('$') // 默认货币符号
const pagination = ref({
  currentPage: 1,
  totalPages: 1,
  totalItems: 0,
  itemsPerPage: 20
})

const searchForm = ref({
  keyword: ''
})

// 加载会员数据
const loadMemberData = async (page = 1, limit = 20) => {
  loading.value = true
  try {
    const params = new URLSearchParams({
      page: page,
      limit: limit,
      keyword: searchForm.value.keyword
    })
    
    const url = `/admin${props.adminLoginPath}/member-statement/list/data?${params}`
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    
    const result = await response.json()
    
    if (result.success) {
      members.value = result.data
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
  loadMemberData(pagination.value.currentPage, pagination.value.itemsPerPage)
}

// 搜索会员
const searchMembers = () => {
  pagination.value.currentPage = 1
  loadMemberData(1, pagination.value.itemsPerPage)
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    keyword: ''
  }
  pagination.value.currentPage = 1
  loadMemberData(1, pagination.value.itemsPerPage)
}

// 查看会员详情
const viewMember = (member) => {
  // 触发导航事件，打开会员查看标签页
  window.dispatchEvent(new CustomEvent('navigate-to-member-view', {
    detail: { 
      memberId: member.id,
      returnTo: 'member-statement-list' // 指定关闭后返回会员对账单列表
    }
  }))
}

// 查看对账单
const viewStatement = (member) => {
  // 触发导航事件，打开会员对账单标签页
  window.dispatchEvent(new CustomEvent('navigate-to-member-statement', {
    detail: { memberId: member.id }
  }))
}

// 处理分页大小变化
const handleSizeChange = (val) => {
  pagination.value.itemsPerPage = val
  loadMemberData(pagination.value.currentPage, val)
}

// 处理当前页变化
const handleCurrentChange = (val) => {
  pagination.value.currentPage = val
  loadMemberData(val, pagination.value.itemsPerPage)
}

// 获取VIP标签类型
const getVipTagType = (vipLevel) => {
  if (vipLevel >= 5) return 'danger'
  if (vipLevel >= 3) return 'warning'
  if (vipLevel >= 1) return 'success'
  return 'info'
}

// 格式化货币
const formatCurrency = (amount) => {
  if (amount === null || amount === undefined) return '0.00'
  return parseFloat(amount).toFixed(2)
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  const year = date.getFullYear().toString().slice(-2)
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

// 格式化时间
const formatTime = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  return `${hours}:${minutes}`
}

onMounted(() => {
  // 只有当 autoLoad 为 true 时才自动加载数据
  if (props.autoLoad) {
    loadMemberData()
  }
})

// 暴露方法给父组件调用
defineExpose({
  loadMemberData
})
</script>

<style scoped>
.member-statement-list-container {
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

.member-statement-table {
  width: 100% !important;
  font-size: 14px;
}

.member-statement-table :deep(.el-table__header th) {
  background-color: #f5f7fa;
  color: #606266;
  font-weight: bold;
}

.member-statement-table :deep(.el-table__body td) {
  transition: background-color 0.3s;
}

.member-statement-table :deep(.el-table__row:hover) {
  background-color: #f5f7fa;
}

.member-statement-table :deep(.el-table__row:hover td) {
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
</style>
