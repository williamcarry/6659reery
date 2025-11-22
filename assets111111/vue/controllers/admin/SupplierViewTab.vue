<template>
  <div class="supplier-view-tab" v-loading="loading">
    <el-card class="supplier-view-card">
      <!-- 头部操作栏 -->
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon"><OfficeBuilding /></el-icon>
            <span class="header-title">供应商详情</span>
          </div>
          <div class="header-right">
            <el-button @click="handleBack" :icon="Back">返回列表</el-button>
          </div>
        </div>
      </template>

      <!-- 内容区域 -->
      <div v-if="supplier.id" class="supplier-detail-content">
        <!-- 账号信息 -->
        <div class="info-section">
          <div class="section-title">
            <el-icon><InfoFilled /></el-icon>
            <span>账号信息</span>
          </div>
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="info-item">
                <span class="label">供应商ID:</span>
                <span class="value">{{ supplier.id }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">用户名:</span>
                <span class="value">{{ supplier.username }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">供应商类型:</span>
                <el-tag :type="supplier.supplierType === 'company' ? 'warning' : 'primary'">
                  {{ supplier.supplierType === 'company' ? '公司' : '个人' }}
                </el-tag>
              </div>
            </el-col>
          </el-row>
          
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="info-item">
                <span class="label">邮箱:</span>
                <span class="value">{{ supplier.email }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">显示名称:</span>
                <span class="value">{{ supplier.displayName || '-' }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">账号状态:</span>
                <el-tag :type="supplier.isActive ? 'success' : 'danger'">
                  {{ supplier.isActive ? '激活' : '禁用' }}
                </el-tag>
              </div>
            </el-col>
          </el-row>
          
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="info-item">
                <span class="label">邮箱验证:</span>
                <el-tag :type="supplier.isVerified ? 'success' : 'info'">
                  {{ supplier.isVerified ? '已验证' : '未验证' }}
                </el-tag>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">注册时间:</span>
                <span class="value">{{ supplier.createdAt || '-' }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">最后登录:</span>
                <span class="value">{{ supplier.lastLoginAt || '-' }}</span>
              </div>
            </el-col>
          </el-row>
        </div>

        <!-- 基本信息 -->
        <div class="info-section">
          <div class="section-title">
            <el-icon><User /></el-icon>
            <span>基本信息</span>
          </div>
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="info-item">
                <span class="label">联系人:</span>
                <span class="value">{{ supplier.contactPerson || '-' }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">联系电话:</span>
                <span class="value">{{ supplier.contactPhone || '-' }}</span>
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="24">
              <div class="info-item">
                <span class="label">联系地址:</span>
                <span class="value">{{ supplier.contactAddress || '-' }}</span>
              </div>
            </el-col>
          </el-row>
        </div>

        <!-- 公司信息 -->
        <div v-if="supplier.supplierType === 'company'" class="info-section">
          <div class="section-title">
            <el-icon><OfficeBuilding /></el-icon>
            <span>公司信息</span>
          </div>
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="info-item">
                <span class="label">公司名称:</span>
                <span class="value">{{ supplier.companyName || '-' }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">公司类型:</span>
                <span class="value">{{ getCompanyTypeLabel(supplier.companyType) }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">营业执照号:</span>
                <span class="value">{{ supplier.businessLicenseNumber || '-' }}</span>
              </div>
            </el-col>
          </el-row>
          
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="info-item">
                <span class="label">法人姓名:</span>
                <span class="value">{{ supplier.legalPersonName || '-' }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">法人身份证:</span>
                <span class="value">{{ supplier.legalPersonIdCard || '-' }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">注册资本:</span>
                <span class="value">{{ supplier.registeredCapital ? supplier.registeredCapital + '万元' : '-' }}</span>
              </div>
            </el-col>
          </el-row>
          
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="info-item">
                <span class="label">成立日期:</span>
                <span class="value">{{ supplier.establishmentDate || '-' }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">税务登记号:</span>
                <span class="value">{{ supplier.taxNumber || '-' }}</span>
              </div>
            </el-col>
          </el-row>
          
          <el-row :gutter="20">
            <el-col :span="24">
              <div class="info-item">
                <span class="label">经营范围:</span>
                <span class="value">{{ supplier.businessScope || '-' }}</span>
              </div>
            </el-col>
          </el-row>
          
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="info-item">
                <span class="label">银行开户名:</span>
                <span class="value">{{ supplier.bankAccountName || '-' }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">银行账号:</span>
                <span class="value">{{ supplier.bankAccountNumber || '-' }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">开户银行:</span>
                <span class="value">{{ supplier.bankName || '-' }}</span>
              </div>
            </el-col>
          </el-row>
          
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="info-item">
                <span class="label">开户支行:</span>
                <span class="value">{{ supplier.bankBranch || '-' }}</span>
              </div>
            </el-col>
          </el-row>
          
          <!-- 公司证件图片 -->
          <el-row :gutter="15" class="image-row">
            <el-col :span="8">
              <div class="image-item">
                <div class="image-label">营业执照</div>
                <div v-if="supplier.businessLicenseImageUrl" class="image-preview" @click="showImageViewer([supplier.businessLicenseImageUrl])">
                  <img :src="supplier.businessLicenseImageUrl" alt="营业执照" class="preview-image" />
                  <div class="image-overlay">
                    <el-icon><ZoomIn /></el-icon>
                  </div>
                </div>
                <div v-else class="no-image">暂无图片</div>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="image-item">
                <div class="image-label">法人身份证正面</div>
                <div v-if="supplier.legalPersonIdFrontUrl" class="image-preview" @click="showImageViewer([supplier.legalPersonIdFrontUrl])">
                  <img :src="supplier.legalPersonIdFrontUrl" alt="法人身份证正面" class="preview-image" />
                  <div class="image-overlay">
                    <el-icon><ZoomIn /></el-icon>
                  </div>
                </div>
                <div v-else class="no-image">暂无图片</div>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="image-item">
                <div class="image-label">法人身份证反面</div>
                <div v-if="supplier.legalPersonIdBackUrl" class="image-preview" @click="showImageViewer([supplier.legalPersonIdBackUrl])">
                  <img :src="supplier.legalPersonIdBackUrl" alt="法人身份证反面" class="preview-image" />
                  <div class="image-overlay">
                    <el-icon><ZoomIn /></el-icon>
                  </div>
                </div>
                <div v-else class="no-image">暂无图片</div>
              </div>
            </el-col>
          </el-row>
        </div>

        <!-- 个人信息 -->
        <div v-if="supplier.supplierType === 'individual'" class="info-section">
          <div class="section-title">
            <el-icon><User /></el-icon>
            <span>个人信息</span>
          </div>
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="info-item">
                <span class="label">真实姓名:</span>
                <span class="value">{{ supplier.individualName || '-' }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">身份证号:</span>
                <span class="value">{{ supplier.individualIdCard || '-' }}</span>
              </div>
            </el-col>
          </el-row>
          
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="info-item">
                <span class="label">个人银行账号:</span>
                <span class="value">{{ supplier.individualBankAccount || '-' }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">个人开户银行:</span>
                <span class="value">{{ supplier.individualBankName || '-' }}</span>
              </div>
            </el-col>
          </el-row>
          
          <!-- 个人证件图片 -->
          <el-row :gutter="20" class="image-row">
            <el-col :span="12">
              <div class="image-item">
                <div class="image-label">身份证正面</div>
                <div v-if="supplier.individualIdFrontUrl" class="image-preview" @click="showImageViewer([supplier.individualIdFrontUrl])">
                  <img :src="supplier.individualIdFrontUrl" alt="身份证正面" class="preview-image" />
                  <div class="image-overlay">
                    <el-icon><ZoomIn /></el-icon>
                  </div>
                </div>
                <div v-else class="no-image">暂无图片</div>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="image-item">
                <div class="image-label">身份证反面</div>
                <div v-if="supplier.individualIdBackUrl" class="image-preview" @click="showImageViewer([supplier.individualIdBackUrl])">
                  <img :src="supplier.individualIdBackUrl" alt="身份证反面" class="preview-image" />
                  <div class="image-overlay">
                    <el-icon><ZoomIn /></el-icon>
                  </div>
                </div>
                <div v-else class="no-image">暂无图片</div>
              </div>
            </el-col>
          </el-row>
        </div>

        <!-- 业务信息 -->
        <div class="info-section">
          <div class="section-title">
            <el-icon><ShoppingBag /></el-icon>
            <span>业务信息</span>
          </div>
          <el-row :gutter="20">
            <el-col :span="24">
              <div class="info-item">
                <span class="label">主营业务:</span>
                <span class="value">{{ supplier.mainCategory || '-' }}</span>
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="info-item">
                <span class="label">跨境经验:</span>
                <el-tag :type="supplier.hasCrossBorderExperience ? 'success' : 'info'">
                  {{ supplier.hasCrossBorderExperience ? '有' : '无' }}
                </el-tag>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">年销售额:</span>
                <span class="value">{{ supplier.annualSalesVolume ? supplier.annualSalesVolume + '万元' : '-' }}</span>
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="24">
              <div class="info-item">
                <span class="label">仓库地址:</span>
                <span class="value">{{ supplier.warehouseAddress || '-' }}</span>
              </div>
            </el-col>
          </el-row>
        </div>

        <!-- 审核信息 -->
        <div class="info-section">
          <div class="section-title">
            <el-icon><DocumentChecked /></el-icon>
            <span>审核信息</span>
          </div>
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="info-item">
                <span class="label">审核状态:</span>
                <el-tag :type="getAuditStatusType(supplier.auditStatus)">
                  {{ getAuditStatusLabel(supplier.auditStatus) }}
                </el-tag>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">审核人:</span>
                <span class="value">{{ supplier.auditedBy || '-' }}</span>
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="24">
              <div class="info-item">
                <span class="label">审核备注:</span>
                <span class="value">{{ supplier.auditRemark || '-' }}</span>
              </div>
            </el-col>
          </el-row>
        </div>

        <!-- 财务信息 -->
        <div class="info-section">
          <div class="section-title">
            <el-icon><Wallet /></el-icon>
            <span>财务信息</span>
          </div>
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="info-item">
                <span class="label">账户余额:</span>
                <span class="value highlight">{{ currencySymbol }}{{ supplier.balance }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">冻结余额:</span>
                <span class="value">{{ currencySymbol }}{{ supplier.balanceFrozen }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">佣金比例:</span>
                <span class="value">{{ formatCommissionRate(supplier) }}</span>
              </div>
            </el-col>
          </el-row>
        </div>

        <!-- 会员信息 -->
        <div class="info-section">
          <div class="section-title">
            <el-icon><Vip /></el-icon>
            <span>会员信息</span>
          </div>
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="info-item">
                <span class="label">会员类型:</span>
                <el-tag :type="supplier.membershipType !== 'none' ? 'success' : 'info'">
                  {{ getMembershipTypeLabel(supplier.membershipType) }}
                </el-tag>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">会员到期时间:</span>
                <span class="value">{{ supplier.membershipExpiredAt || '-' }}</span>
              </div>
            </el-col>
          </el-row>
        </div>
      </div>
      
      <div v-else class="no-data">
        <el-empty description="暂无供应商数据" />
      </div>
    </el-card>

    <!-- 图片查看器 -->
    <el-image-viewer
      v-if="imageViewerVisible"
      :url-list="imageViewerUrls"
      @close="closeImageViewer"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, defineExpose } from 'vue'
import {
  ElCard,
  ElButton,
  ElRow,
  ElCol,
  ElTag,
  ElIcon,
  ElMessage,
  ElEmpty,
  ElImageViewer,
  vLoading
} from 'element-plus'
import {
  User,
  Back,
  InfoFilled,
  OfficeBuilding,
  Vip,
  Wallet,
  ShoppingBag,
  DocumentChecked,
  ZoomIn
} from '@element-plus/icons-vue'

// 定义组件属性
const props = defineProps({
  adminLoginPath: {
    type: String,
    default: ''
  },
  supplierId: {
    type: [Number, null],
    default: null
  },
  autoLoad: {
    type: Boolean,
    default: false
  },
  returnTo: {
    type: String,
    default: 'supplier-list' // 默认返回供应商列表
  }
})

// 响应式数据
const loading = ref(false)
const supplier = reactive({
  id: null,
  username: '',
  email: '',
  supplierType: 'company',
  displayName: '',
  createdAt: '',
  lastLoginAt: '',
  updatedAt: '',
  contactPerson: '',
  contactPhone: '',
  contactAddress: '',
  companyName: '',
  companyType: '',
  businessLicenseNumber: '',
  businessLicenseImageUrl: '',
  legalPersonName: '',
  legalPersonIdCard: '',
  legalPersonIdFrontUrl: '',
  legalPersonIdBackUrl: '',
  registeredCapital: '',
  establishmentDate: '',
  taxNumber: '',
  businessScope: '',
  bankAccountName: '',
  bankAccountNumber: '',
  bankName: '',
  bankBranch: '',
  individualName: '',
  individualIdCard: '',
  individualIdFrontUrl: '',
  individualIdBackUrl: '',
  individualBankAccount: '',
  individualBankName: '',
  mainCategory: '',
  hasCrossBorderExperience: false,
  annualSalesVolume: '',
  warehouseAddress: '',
  auditStatus: 'pending',
  auditRemark: '',
  auditedBy: '',
  balance: '0.00',
  balanceFrozen: '0.00',
  commissionRate: null,
  effectiveCommissionRatePercentage: null,
  membershipType: 'none',
  membershipExpiredAt: '',
  isActive: true,
  isVerified: false
})
const currencySymbol = ref('$')

// 图片查看器相关
const imageViewerVisible = ref(false)
const imageViewerUrls = ref([])

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

// 加载供应商数据
const initData = async () => {
  if (!props.supplierId) {
    ElMessage.error('未指定供应商ID')
    return
  }
  
  loading.value = true
  try {
    const response = await fetch(`/admin${props.adminLoginPath}/supplier/${props.supplierId}/detail`, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    
    const result = await response.json()
    
    if (result.success) {
      Object.assign(supplier, result.data)
      
      // 读取货币符号
      if (result.currencySymbol) {
        currencySymbol.value = result.currencySymbol
      }
      
      // 立即隐藏loading，让页面先显示出来
      loading.value = false
      
      // 异步加载图片URL，不阻塞页面显示
      loadImageUrls()
    } else {
      ElMessage.error(result.error || '加载数据失败')
      loading.value = false
    }
  } catch (error) {
    ElMessage.error('加载数据失败: ' + error.message)
    loading.value = false
  }
}

// 加载图片URL
const loadImageUrls = async () => {
  // 公司证件图片
  if (supplier.supplierType === 'company') {
    if (supplier.businessLicenseImage) {
      supplier.businessLicenseImageUrl = await getSignedUrl(supplier.businessLicenseImage)
    }
    if (supplier.legalPersonIdFront) {
      supplier.legalPersonIdFrontUrl = await getSignedUrl(supplier.legalPersonIdFront)
    }
    if (supplier.legalPersonIdBack) {
      supplier.legalPersonIdBackUrl = await getSignedUrl(supplier.legalPersonIdBack)
    }
  }
  
  // 个人证件图片
  if (supplier.supplierType === 'individual') {
    if (supplier.individualIdFront) {
      supplier.individualIdFrontUrl = await getSignedUrl(supplier.individualIdFront)
    }
    if (supplier.individualIdBack) {
      supplier.individualIdBackUrl = await getSignedUrl(supplier.individualIdBack)
    }
  }
}

// 显示图片查看器
const showImageViewer = (urls) => {
  imageViewerUrls.value = urls
  imageViewerVisible.value = true
}

// 关闭图片查看器
const closeImageViewer = () => {
  imageViewerVisible.value = false
  imageViewerUrls.value = []
}

// 返回列表
const handleBack = () => {
  // 关闭当前标签页
  window.dispatchEvent(new CustomEvent('close-current-tab'))
  // 切换到指定的返回页面
  setTimeout(() => {
    window.dispatchEvent(new CustomEvent('navigate-to', {
      detail: { key: props.returnTo }
    }))
  }, 100)
}

// 获取公司类型标签
const getCompanyTypeLabel = (type) => {
  const labels = {
    'factory': '工厂',
    'trader': '贸易商',
    'factory_trader': '工贸一体',
    'brand': '品牌商'
  }
  return labels[type] || '-'
}

// 获取审核状态标签
const getAuditStatusLabel = (status) => {
  const labels = {
    'pending': '待审核',
    'approved': '已通过',
    'rejected': '已拒绝',
    'resubmit': '待重新提交'
  }
  return labels[status] || '-'
}

// 获取审核状态类型
const getAuditStatusType = (status) => {
  const types = {
    'pending': 'warning',
    'approved': 'success',
    'rejected': 'danger',
    'resubmit': 'info'
  }
  return types[status] || 'info'
}

// 获取会员类型标签
const getMembershipTypeLabel = (type) => {
  const labels = {
    'none': '无会员',
    'monthly': '月会员',
    'quarterly': '季度会员',
    'half_yearly': '半年会员',
    'yearly': '年会员'
  }
  return labels[type] || '-'
}

// 检查供应商是否为活跃会员
const isMemberActive = (supplierData) => {
  if (!supplierData.membershipType || supplierData.membershipType === 'none' || !supplierData.membershipExpiredAt) {
    return false
  }
  
  const expiredAt = new Date(supplierData.membershipExpiredAt)
  const now = new Date()
  return expiredAt > now
}

// 格式化佣金比例显示
const formatCommissionRate = (supplierData) => {
  if (isMemberActive(supplierData)) {
    return '免佣金'
  }
  
  if (supplierData.effectiveCommissionRatePercentage !== null && supplierData.effectiveCommissionRatePercentage !== undefined) {
    return supplierData.effectiveCommissionRatePercentage.toFixed(2) + '%'
  }
  
  if (supplierData.commissionRate !== null && supplierData.commissionRate !== undefined) {
    return (parseFloat(supplierData.commissionRate) * 100).toFixed(2) + '%'
  }
  
  return '系统默认'
}

// 组件挂载时加载数据
onMounted(() => {
  if (props.autoLoad && props.supplierId) {
    initData()
  }
})

// 暴露方法给父组件调用
defineExpose({
  initData
})
</script>

<style scoped>
.supplier-view-tab {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.supplier-view-card {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-icon {
  font-size: 20px;
  color: #409eff;
}

.header-title {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
}

.header-right {
  display: flex;
  gap: 10px;
}

.supplier-detail-content {
  padding: 20px 0;
}

.info-section {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.info-section:last-child {
  margin-bottom: 0;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #409eff;
}

.section-title .el-icon {
  font-size: 18px;
  color: #409eff;
}

.info-item {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  min-height: 32px;
}

.info-item .label {
  font-weight: 500;
  color: #606266;
  margin-right: 10px;
  min-width: 100px;
  flex-shrink: 0;
}

.info-item .value {
  color: #303133;
  flex: 1;
}

.info-item .value.highlight {
  color: #f56c6c;
  font-weight: bold;
  font-size: 16px;
}

.image-row {
  margin-top: 20px;
}

.image-item {
  text-align: center;
}

.image-label {
  font-weight: 500;
  color: #606266;
  margin-bottom: 10px;
  font-size: 14px;
}

.image-preview {
  position: relative;
  width: 100%;
  height: 200px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
  cursor: pointer;
  background-color: #fff;
}

.image-preview:hover .image-overlay {
  opacity: 1;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.image-overlay .el-icon {
  font-size: 40px;
  color: #fff;
}

.no-image {
  width: 100%;
  height: 200px;
  border: 1px dashed #dcdfe6;
  border-radius: 4px;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #909399;
  background-color: #fafafa;
}

.no-data {
  padding: 40px;
  text-align: center;
}
</style>
