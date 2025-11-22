<template>
  <div class="supplier-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2 class="page-title">
        <el-icon class="title-icon"><OfficeBuilding /></el-icon>
        供应商列表
      </h2>
      <div class="header-actions">
        <el-button type="primary" @click="refreshData" :icon="Refresh">
          刷新数据
        </el-button>
      </div>
    </div>
    
    <!-- 搜索和筛选 -->
    <el-card class="filter-card">
      <div class="filter-header">
        <el-icon class="filter-icon"><Search /></el-icon>
        <span class="filter-title">筛选条件</span>
      </div>
      <el-form :model="searchForm" class="search-form" label-position="left" label-width="80px">
        <el-row :gutter="20" align="middle">
          <el-col :span="5" :xs="24">
            <el-form-item label="关键词" class="right-aligned-label">
              <el-input v-model="searchForm.keyword" placeholder="用户名/邮箱/公司名/姓名" />
            </el-form-item>
          </el-col>
          <el-col :span="6" :xs="24">
            <el-form-item label="类型" class="right-aligned-label">
              <el-select v-model="searchForm.supplierType" placeholder="请选择类型" clearable>
                <el-option label="全部" value="" />
                <el-option label="公司" value="company" />
                <el-option label="个人" value="individual" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="5" :xs="24">
            <el-form-item label="审核状态" class="right-aligned-label">
              <el-select v-model="searchForm.auditStatus" placeholder="请选择状态" clearable>
                <el-option label="全部" value="" />
                <el-option label="待审核" value="pending" />
                <el-option label="已通过" value="approved" />
                <el-option label="已拒绝" value="rejected" />
                <el-option label="待重新提交" value="resubmit" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="4" :xs="24">
            <el-form-item label="账号状态" class="right-aligned-label">
              <el-select v-model="searchForm.isActive" placeholder="请选择状态" clearable>
                <el-option label="全部" value="" />
                <el-option label="激活" value="1" />
                <el-option label="禁用" value="0" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="4" :xs="24" class="action-col">
            <el-form-item label=" ">
              <div class="form-actions">
                <el-button type="primary" @click="searchSuppliers" :icon="Search">
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
    
    <!-- 供应商表格 -->
    <el-card class="table-card">
      <template #header>
        <div class="table-header">
          <div class="table-header-title">
            <el-icon class="table-icon"><List /></el-icon>
            供应商列表
          </div>
          <div class="table-header-info">
            共 {{ pagination.totalItems }} 条记录
          </div>
        </div>
      </template>
      
      <el-table 
        :data="suppliers" 
        class="supplier-table" 
        v-loading="loading"
        :fit="true"
        :border="true"
        :header-cell-style="{ textAlign: 'center' }"
        :cell-style="{ textAlign: 'center' }"
        :stripe="true"
      >
        <el-table-column label="序号" min-width="60">
          <template #default="scope">
            {{ (pagination.currentPage - 1) * pagination.itemsPerPage + scope.$index + 1 }}
          </template>
        </el-table-column>
        <!-- 客户ID -->
        <el-table-column prop="customerId" label="客户ID" min-width="120" show-overflow-tooltip />
        <!-- 合并用户名和类型，保持原有颜色 -->
        <el-table-column prop="username" label="用户名/类型" min-width="150" show-overflow-tooltip>
          <template #default="scope">
            {{ scope.row.username }}/
            <el-tag :type="scope.row.supplierType === 'company' ? 'primary' : 'success'" style="margin-left: 2px;">
              {{ scope.row.supplierType === 'company' ? '公司' : '个人' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="email" label="邮箱" min-width="180" show-overflow-tooltip />
        <el-table-column prop="displayName" label="显示名称" min-width="150" show-overflow-tooltip />
        <!-- 合并审核状态和账号状态，保持原有颜色并添加/分隔符 -->
        <el-table-column prop="status" label="审核状态/账号状态" min-width="180">
          <template #default="scope">
            <el-tag :type="getAuditStatusType(scope.row.auditStatus)">
              {{ getAuditStatusText(scope.row.auditStatus) }}
            </el-tag>
            /
            <el-tag :type="scope.row.isActive ? 'success' : 'danger'">
              {{ scope.row.isActive ? '激活' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <!-- 余额/冻结 -->
        <el-table-column prop="balance" label="余额/冻结" min-width="150">
          <template #default="scope">
            <span style="color: #67c23a;">{{ formatCurrency(scope.row.balance) || '0.00' }}</span>
            <span style="color: #909399;"> / </span>
            <span style="color: #e6a23c;">{{ formatCurrency(scope.row.balanceFrozen) || '0.00' }}</span>
          </template>
        </el-table-column>
        <!-- 会员/到期 -->
        <el-table-column prop="membership" label="会员/到期" min-width="150">
          <template #default="scope">
            <span v-if="scope.row.membershipType && scope.row.membershipType !== 'none'" style="color: #409eff;">
              {{ getMembershipTypeText(scope.row.membershipType) }}
            </span>
            <span v-else style="color: #909399;">
              无会员
            </span>
            <span style="color: #909399;"> / </span>
            <span v-if="scope.row.membershipExpiredAt" :style="{ color: isMemberActive(scope.row) ? '#67c23a' : '#f56c6c' }">
              {{ formatMembershipExpiredAt(scope.row.membershipExpiredAt) }}
            </span>
            <span v-else style="color: #909399;">
              无
            </span>
          </template>
        </el-table-column>
        <!-- 佣金 -->
        <el-table-column prop="commissionRate" label="佣金" min-width="100">
          <template #default="scope">
            <span v-if="isMemberActive(scope.row)">
              免佣金
            </span>
            <span v-else-if="scope.row.effectiveCommissionRatePercentage !== null">
              {{ scope.row.effectiveCommissionRatePercentage.toFixed(2) }}%
            </span>
            <span v-else-if="scope.row.commissionRate !== null">
              {{ (parseFloat(scope.row.commissionRate) * 100).toFixed(2) }}%
            </span>
            <span v-else>系统默认</span>
          </template>
        </el-table-column>
        <!-- 注册时间，年份显示后两位 -->
        <el-table-column prop="createdAt" label="注册时间" min-width="160">
          <template #default="scope">
            {{ formatCreatedAt(scope.row.createdAt) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="260" fixed="right">
          <template #default="scope">
            <div class="action-buttons">
              <div class="action-row">
                <el-button size="small" @click="viewSupplier(scope.row)">查看</el-button>
                <el-button size="small" @click="editSupplier(scope.row)">编辑</el-button>
              </div>
              <div class="action-row">
                <el-button size="small" type="warning" @click="showChangePasswordDialog(scope.row)">修改密码</el-button>
                <el-button size="small" type="success" @click="showAdjustBalanceDialog(scope.row)">增减余额</el-button>
              </div>
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
    
    <!-- 查看和编辑功能已移至标签页形式 -->
    
    <!-- 修改密码对话框 -->
    <el-dialog v-model="changePasswordDialogVisible" title="修改供应商密码" width="500px">
      <el-form :model="passwordForm" label-width="100px">
        <el-form-item label="用户名">
          <el-input v-model="passwordForm.username" disabled />
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword" :rules="[{ required: true, message: '请输入新密码', trigger: 'blur' }]">
          <el-input v-model="passwordForm.newPassword" type="password" show-password />
          <div class="password-hint">密码必须至少8位数</div>
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword" :rules="[
          { required: true, message: '请确认新密码', trigger: 'blur' },
          { validator: validateConfirmPassword, trigger: 'blur' }
        ]">
          <el-input v-model="passwordForm.confirmPassword" type="password" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="changePasswordDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="changePassword" :loading="passwordChanging">确定</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 增减余额对话框 -->
    <el-dialog v-model="adjustBalanceDialogVisible" title="增减余额" width="600px">
      <div class="supplier-balance-info">
        <div class="info-row">
          <span class="label">供应商：</span>
          <span class="value">{{ adjustBalanceForm.username }} ({{ adjustBalanceForm.displayName }})</span>
        </div>
        <div class="info-row">
          <span class="label">当前可用余额：</span>
          <span class="value balance">{{ currencySymbol }}{{ formatCurrency(adjustBalanceForm.currentBalance) }}</span>
        </div>
        <div class="info-row">
          <span class="label">当前冻结余额：</span>
          <span class="value frozen">{{ currencySymbol }}{{ formatCurrency(adjustBalanceForm.currentFrozen) }}</span>
        </div>
      </div>
      
      <el-divider />
      
      <el-form :model="adjustBalanceForm" label-width="120px">
        <el-form-item label="增加余额" prop="addAmount">
          <el-input 
            v-model="adjustBalanceForm.addAmount" 
            type="number" 
            placeholder="请输入增加金额" 
            step="0.01"
          >
            <template #prepend>{{ currencySymbol }}</template>
          </el-input>
          <div class="input-hint">输入正数，如：100.00</div>
        </el-form-item>
        <el-form-item label="减少余额" prop="deductAmount">
          <el-input 
            v-model="adjustBalanceForm.deductAmount" 
            type="number" 
            placeholder="请输入减少金额" 
            step="0.01"
          >
            <template #prepend>{{ currencySymbol }}</template>
          </el-input>
          <div class="input-hint">输入正数，如：50.00</div>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input 
            v-model="adjustBalanceForm.remark" 
            type="textarea" 
            :rows="3"
            placeholder="请输入备注说明（必填）"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="adjustBalanceDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmAdjustBalance" :loading="adjusting">确定</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 图片查看器 -->
    <el-image-viewer
      v-if="imageViewerVisible"
      :url-list="imageViewerUrls"
      @close="closeImageViewer"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, defineExpose, reactive } from 'vue'
import {
  ElCard,
  ElTable,
  ElTableColumn,
  ElButton,
  ElDialog,
  ElForm,
  ElFormItem,
  ElInput,
  ElSelect,
  ElOption,
  ElSwitch,
  ElTag,
  ElMessageBox,
  ElMessage,
  ElPagination,
  ElDivider,
  ElRow,
  ElCol,
  ElIcon,
  ElImageViewer,
  vLoading
} from 'element-plus'
import {
  OfficeBuilding,
  Search,
  Refresh,
  RefreshLeft,
  List
} from '@element-plus/icons-vue'
import FileUpload from './FileUpload.vue'

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
const suppliers = ref([])
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
  supplierType: '',
  auditStatus: '',
  isActive: ''
})

// 图片查看器相关
const imageViewerVisible = ref(false)
const imageViewerUrls = ref([])

// 关闭图片查看器
const closeImageViewer = () => {
  imageViewerVisible.value = false
  imageViewerUrls.value = []
}

// 获取审核状态的显示文本
const getAuditStatusText = (status) => {
  const statusMap = {
    'pending': '待审核',
    'approved': '已通过',
    'rejected': '已拒绝',
    'resubmit': '待重新提交'
  }
  return statusMap[status] || status
}

// 获取审核状态的标签类型
const getAuditStatusType = (status) => {
  const typeMap = {
    'pending': 'warning',
    'approved': 'success',
    'rejected': 'danger',
    'resubmit': 'info'
  }
  return typeMap[status] || 'info'
}

// 获取文件签名URL
const getSignedUrl = async (key) => {
  if (!key || key.startsWith('http')) {
    return key
  }
  
  try {
    const loginPath = props.adminLoginPath || window.adminLoginPath || ''
    const signedUrlEndpoint = `/admin${loginPath}/supplier/file/signed-url`
    
    const response = await fetch(signedUrlEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: JSON.stringify({ key: key })
    })
    
    const result = await response.json()
    
    if (result.success) {
      return result.url
    }
  } catch (error) {
    console.error('获取签名URL失败:', error)
  }
  
  return key
}

// 为供应商数据添加图片URL
const addImageUrlsToSupplier = async (supplier) => {
  const supplierWithUrls = { ...supplier }
  
  // 为公司信息图片获取签名URL
  if (supplierWithUrls.businessLicenseImage) {
    supplierWithUrls.businessLicenseImageUrl = await getSignedUrl(supplierWithUrls.businessLicenseImage)
  }
  if (supplierWithUrls.legalPersonIdFront) {
    supplierWithUrls.legalPersonIdFrontUrl = await getSignedUrl(supplierWithUrls.legalPersonIdFront)
  }
  if (supplierWithUrls.legalPersonIdBack) {
    supplierWithUrls.legalPersonIdBackUrl = await getSignedUrl(supplierWithUrls.legalPersonIdBack)
  }
  
  // 为个人信息图片获取签名URL
  if (supplierWithUrls.individualIdFront) {
    supplierWithUrls.individualIdFrontUrl = await getSignedUrl(supplierWithUrls.individualIdFront)
  }
  if (supplierWithUrls.individualIdBack) {
    supplierWithUrls.individualIdBackUrl = await getSignedUrl(supplierWithUrls.individualIdBack)
  }
  
  return supplierWithUrls
}

// 加载供应商数据
const loadSupplierData = async (page = 1, limit = 20) => {
  loading.value = true
  try {
    const params = new URLSearchParams({
      page: page,
      limit: limit,
      keyword: searchForm.value.keyword,
      supplierType: searchForm.value.supplierType,
      auditStatus: searchForm.value.auditStatus,
      isActive: searchForm.value.isActive
    })
    
    // 调试信息
    const url = `/admin${props.adminLoginPath}/supplier/list/tab?${params}`
    console.log('Fetching supplier data from URL:', url)
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    
    const result = await response.json()
    
    // 调试信息 - 查看返回的分页数据
    console.log('=== 供应商列表响应数据 ===')
    console.log('完整响应:', result)
    console.log('总条数 totalItems:', result.pagination?.totalItems)
    console.log('总页数 totalPages:', result.pagination?.totalPages)
    console.log('当前页 currentPage:', result.pagination?.currentPage)
    console.log('每页条数 itemsPerPage:', result.pagination?.itemsPerPage)
    console.log('实际返回数据条数:', result.data?.length)
    console.log('========================')
    
    if (result.success) {
      suppliers.value = result.data
      pagination.value = result.pagination
      
      // 读取货币符号
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
  loadSupplierData(pagination.value.currentPage, pagination.value.itemsPerPage)
}

// 搜索供应商
const searchSuppliers = () => {
  pagination.value.currentPage = 1
  loadSupplierData(1, pagination.value.itemsPerPage)
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    keyword: '',
    supplierType: '',
    auditStatus: '',
    isActive: ''
  }
  pagination.value.currentPage = 1
  loadSupplierData(1, pagination.value.itemsPerPage)
}

// 查看供应商
const viewSupplier = (supplier) => {
  // 触发导航事件，在新标签页中打开供应商详情
  window.dispatchEvent(new CustomEvent('navigate-to-supplier-view', {
    detail: { 
      supplierId: supplier.id,
      returnTo: 'supplier-list' // 指定关闭后返回供应商列表
    }
  }))
}

// 编辑供应商
const editSupplier = (supplier) => {
  // 触发导航事件，在新标签页中打开供应商编辑
  window.dispatchEvent(new CustomEvent('navigate-to-supplier-edit', {
    detail: { supplierId: supplier.id }
  }))
}

// 处理分页大小变化
const handleSizeChange = (val) => {
  pagination.value.itemsPerPage = val
  loadSupplierData(pagination.value.currentPage, val)
}

// 处理当前页变化
const handleCurrentChange = (val) => {
  pagination.value.currentPage = val
  loadSupplierData(val, pagination.value.itemsPerPage)
}

// 组件挂载时加载数据
onMounted(() => {
  // 只有当 autoLoad 为 true 时才自动加载数据
  if (props.autoLoad) {
    loadSupplierData()
  }
})

// 暴露方法给父组件调用
defineExpose({
  loadSupplierData
})

// 修改密码相关
const changePasswordDialogVisible = ref(false)
const passwordChanging = ref(false)
const passwordForm = reactive({
  id: null,
  username: '',
  newPassword: '',
  confirmPassword: ''
})

// 增减余额相关
const adjustBalanceDialogVisible = ref(false)
const adjusting = ref(false)
const adjustBalanceForm = reactive({
  supplierId: null,
  username: '',
  displayName: '',
  currentBalance: '0.00',
  currentFrozen: '0.00',
  addAmount: '',
  deductAmount: '',
  remark: ''
})
const currencySymbol = ref('$')

// 显示修改密码对话框
const showChangePasswordDialog = (supplier) => {
  passwordForm.id = supplier.id
  passwordForm.username = supplier.username
  passwordForm.newPassword = ''
  passwordForm.confirmPassword = ''
  changePasswordDialogVisible.value = true
}

// 验证确认密码
const validateConfirmPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== passwordForm.newPassword) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

// 修改密码
const changePassword = async () => {
  if (!passwordForm.newPassword || !passwordForm.confirmPassword) {
    ElMessage.error('请输入密码')
    return
  }
  
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    ElMessage.error('两次输入的密码不一致')
    return
  }
  
  passwordChanging.value = true
  try {
    const response = await fetch(`/admin${props.adminLoginPath}/supplier/${passwordForm.id}/change-password`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: JSON.stringify({
        newPassword: passwordForm.newPassword
      })
    })
    
    const result = await response.json()
    
    if (result.success) {
      ElMessage.success(result.message || '密码修改成功')
      changePasswordDialogVisible.value = false
    } else {
      ElMessage.error(result.error || '密码修改失败')
    }
  } catch (error) {
    ElMessage.error('密码修改失败: ' + error.message)
  } finally {
    passwordChanging.value = false
  }
}

// 检查供应商是否为活跃会员
const isMemberActive = (supplier) => {
  // 检查是否有会员类型且不为'none'
  if (!supplier.membershipType || supplier.membershipType === 'none' || !supplier.membershipExpiredAt) {
    return false;
  }
  
  // 检查会员是否过期
  const expiredAt = new Date(supplier.membershipExpiredAt);
  const now = new Date();
  return expiredAt > now;
}

// 格式化注册时间，年份显示后两位
const formatCreatedAt = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const year = date.getFullYear().toString().slice(-2) // 取年份后两位
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  const day = date.getDate().toString().padStart(2, '0')
  const hours = date.getHours().toString().padStart(2, '0')
  const minutes = date.getMinutes().toString().padStart(2, '0')
  return `${year}-${month}-${day} ${hours}:${minutes}`
}

// 格式化货币显示
const formatCurrency = (amount) => {
  if (amount === null || amount === undefined) return null
  return parseFloat(amount).toFixed(2)
}

// 获取会员类型文本
const getMembershipTypeText = (type) => {
  const typeMap = {
    'none': '无会员',
    'monthly': '月会员',
    'quarterly': '季度会员',
    'half_yearly': '半年会员',
    'yearly': '年会员'
  }
  return typeMap[type] || '无会员'
}

// 格式化会员到期时间
const formatMembershipExpiredAt = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const year = date.getFullYear().toString().slice(-2) // 取年份后两位
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  const day = date.getDate().toString().padStart(2, '0')
  return `${year}-${month}-${day}`
}

// 格式化会员信息显示为 会员类型/到期时间 格式
const formatMembershipInfo = (row) => {
  // 如果没有会员类型或为none，则显示 无/无
  if (!row.membershipType || row.membershipType === 'none') {
    return '无/无'
  }
  
  // 获取会员类型文本
  const membershipTypeText = getMembershipTypeText(row.membershipType)
  
  // 如果有到期时间，格式化显示年份后两位
  if (row.membershipExpiredAt) {
    const expiredAtText = formatMembershipExpiredAt(row.membershipExpiredAt)
    return `${membershipTypeText}/${expiredAtText}`
  }
  
  // 如果没有到期时间，显示 会员类型/无
  return `${membershipTypeText}/无`
}

// 显示增减余额对话框
const showAdjustBalanceDialog = (supplier) => {
  adjustBalanceForm.supplierId = supplier.id
  adjustBalanceForm.username = supplier.username
  adjustBalanceForm.displayName = supplier.displayName
  adjustBalanceForm.currentBalance = supplier.balance || '0.00'
  adjustBalanceForm.currentFrozen = supplier.balanceFrozen || '0.00'
  adjustBalanceForm.addAmount = ''
  adjustBalanceForm.deductAmount = ''
  adjustBalanceForm.remark = ''
  adjustBalanceDialogVisible.value = true
}

// 确认增减余额
const confirmAdjustBalance = async () => {
  const addAmount = parseFloat(adjustBalanceForm.addAmount) || 0
  const deductAmount = parseFloat(adjustBalanceForm.deductAmount) || 0
  
  // 验证
  if (addAmount === 0 && deductAmount === 0) {
    ElMessage.error('请输入增加或减少的金额')
    return
  }
  
  if (addAmount < 0 || deductAmount < 0) {
    ElMessage.error('金额必须为正数')
    return
  }
  
  if (addAmount > 0 && deductAmount > 0) {
    ElMessage.error('不能同时增加和减少余额')
    return
  }
  
  if (!adjustBalanceForm.remark || adjustBalanceForm.remark.trim() === '') {
    ElMessage.error('请输入备注说明')
    return
  }
  
  adjusting.value = true
  try {
    const response = await fetch(`/admin${props.adminLoginPath}/supplier/${adjustBalanceForm.supplierId}/adjust-balance`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: JSON.stringify({
        addAmount: addAmount > 0 ? addAmount : 0,
        deductAmount: deductAmount > 0 ? deductAmount : 0,
        remark: adjustBalanceForm.remark
      })
    })
    
    const result = await response.json()
    
    if (result.success) {
      ElMessage.success(result.message || '余额调整成功')
      adjustBalanceDialogVisible.value = false
      // 刷新列表
      refreshData()
    } else {
      ElMessage.error(result.message || '余额调整失败')
    }
  } catch (error) {
    ElMessage.error('余额调整失败: ' + error.message)
  } finally {
    adjusting.value = false
  }
}

</script>

<style scoped>
.supplier-list {
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
  width: 100px;
  margin-right: 10px;
  margin-bottom: 0;
  text-align: right;
  flex-shrink: 0;
  display: flex;
  justify-content: flex-end;
}

.search-form :deep(.right-aligned-label .el-form-item__label) {
  text-align: right;
}

.search-form :deep(.el-form-item__content) {
  width: calc(100% - 90px);
  display: flex;
  align-items: center;
  min-width: 100px;
}

.right-aligned-label :deep(.el-form-item__label) {
  text-align: right !important;
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

.supplier-table {
  width: 100% !important;
  font-size: 14px;
}

.supplier-table :deep(.el-table__header th) {
  background-color: #f5f7fa;
  color: #606266;
  font-weight: bold;
}

.supplier-table :deep(.el-table__row:hover) {
  background-color: #f5f7fa;
}

.supplier-table :deep(.el-table__row:hover td) {
  background-color: #f5f7fa !important;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  width: 100%;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.password-hint {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}

/* 操作按钮布局 */
.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
}

.action-row {
  display: flex;
  gap: 8px;
  justify-content: center;
}

.action-row .el-button {
  flex: 1;
  min-width: 0;
}

/* 增减余额对话框样式 */
.supplier-balance-info {
  background-color: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 15px;
}

.supplier-balance-info .info-row {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  font-size: 14px;
}

.supplier-balance-info .info-row:last-child {
  margin-bottom: 0;
}

.supplier-balance-info .label {
  color: #606266;
  font-weight: 600;
  min-width: 140px;
}

.supplier-balance-info .value {
  color: #303133;
}

.supplier-balance-info .value.balance {
  color: #67c23a;
  font-weight: bold;
  font-size: 16px;
}

.supplier-balance-info .value.frozen {
  color: #e6a23c;
  font-weight: bold;
  font-size: 16px;
}

.input-hint {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}

@media (max-width: 768px) {
  .search-form {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-form :deep(.el-form-item) {
    margin-right: 0;
    width: 100%;
  }
  
  .search-form :deep(.el-form-item:last-child) {
    margin-left: 0;
    margin-top: 10px;
  }
}
</style>