<template>
  <div class="member-view-tab" v-loading="loading">
    <el-card class="member-view-card">
      <!-- 头部操作栏 -->
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon"><User /></el-icon>
            <span class="header-title">会员详情</span>
          </div>
          <div class="header-right">
            <el-button @click="handleBack" :icon="Back">返回列表</el-button>
          </div>
        </div>
      </template>

      <!-- 内容区域 -->
      <div v-if="memberData" class="member-detail-content">
        <!-- 账号信息 -->
        <div class="info-section">
          <div class="section-title">
            <el-icon><InfoFilled /></el-icon>
            <span>账号信息</span>
          </div>
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="info-item">
                <span class="label">会员ID:</span>
                <span class="value">{{ memberData.id }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">用户名:</span>
                <span class="value">{{ memberData.username }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">会员类型:</span>
                <el-tag :type="memberData.customerType === 'company' ? 'warning' : 'primary'">
                  {{ memberData.customerTypeName }}
                </el-tag>
              </div>
            </el-col>
          </el-row>
          
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="info-item">
                <span class="label">邮箱:</span>
                <span class="value">{{ memberData.email }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">手机号:</span>
                <span class="value">{{ memberData.mobile || '-' }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">账号状态:</span>
                <el-tag :type="memberData.isActive ? 'success' : 'danger'">
                  {{ memberData.isActive ? '激活' : '禁用' }}
                </el-tag>
              </div>
            </el-col>
          </el-row>
          
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="info-item">
                <span class="label">实名状态:</span>
                <el-tag :type="memberData.isVerified ? 'success' : 'info'">
                  {{ memberData.isVerified ? '已实名' : '未实名' }}
                </el-tag>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">注册时间:</span>
                <span class="value">{{ memberData.createdAt || '-' }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">最后登录:</span>
                <span class="value">{{ memberData.lastLoginAt || '-' }}</span>
              </div>
            </el-col>
          </el-row>
        </div>

        <!-- 个人会员信息 -->
        <div v-if="memberData.customerType === 'individual'" class="info-section">
          <div class="section-title">
            <el-icon><User /></el-icon>
            <span>个人信息</span>
          </div>
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="info-item">
                <span class="label">真实姓名:</span>
                <span class="value">{{ memberData.realName || '-' }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">昵称:</span>
                <span class="value">{{ memberData.nickname || '-' }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">性别:</span>
                <span class="value">
                  {{ memberData.gender === 1 ? '男' : memberData.gender === 2 ? '女' : '未知' }}
                </span>
              </div>
            </el-col>
          </el-row>
          
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="info-item">
                <span class="label">身份证号:</span>
                <span class="value">{{ memberData.individualIdCard || '-' }}</span>
              </div>
            </el-col>
          </el-row>
          
          <!-- 个人证件图片 -->
          <el-row :gutter="20" class="image-row">
            <el-col :span="12">
              <div class="image-item">
                <div class="image-label">身份证正面</div>
                <div v-if="imageUrls.individualIdFront" class="image-preview" @click="showImageViewer([imageUrls.individualIdFront])">
                  <img :src="imageUrls.individualIdFront" alt="身份证正面" class="preview-image" />
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
                <div v-if="imageUrls.individualIdBack" class="image-preview" @click="showImageViewer([imageUrls.individualIdBack])">
                  <img :src="imageUrls.individualIdBack" alt="身份证反面" class="preview-image" />
                  <div class="image-overlay">
                    <el-icon><ZoomIn /></el-icon>
                  </div>
                </div>
                <div v-else class="no-image">暂无图片</div>
              </div>
            </el-col>
          </el-row>
        </div>

        <!-- 企业会员信息 -->
        <div v-if="memberData.customerType === 'company'" class="info-section">
          <div class="section-title">
            <el-icon><OfficeBuilding /></el-icon>
            <span>企业信息</span>
          </div>
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="info-item">
                <span class="label">公司名称:</span>
                <span class="value">{{ memberData.companyName || '-' }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">公司类型:</span>
                <span class="value">
                  <template v-if="memberData.companyType === 'factory'">工厂</template>
                  <template v-else-if="memberData.companyType === 'trader'">贸易商</template>
                  <template v-else-if="memberData.companyType === 'factory_trader'">工贸一体</template>
                  <template v-else-if="memberData.companyType === 'brand'">品牌商</template>
                  <template v-else>-</template>
                </span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">营业执照号:</span>
                <span class="value">{{ memberData.businessLicenseNumber || '-' }}</span>
              </div>
            </el-col>
          </el-row>
          
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="info-item">
                <span class="label">法人姓名:</span>
                <span class="value">{{ memberData.legalPersonName || '-' }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">法人身份证号:</span>
                <span class="value">{{ memberData.legalPersonIdCard || '-' }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">注册资本:</span>
                <span class="value">{{ memberData.registeredCapital ? memberData.registeredCapital + ' 万元' : '-' }}</span>
              </div>
            </el-col>
          </el-row>
          
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="info-item">
                <span class="label">成立日期:</span>
                <span class="value">{{ memberData.establishmentDate || '-' }}</span>
              </div>
            </el-col>
            <el-col :span="16">
              <div class="info-item">
                <span class="label">经营范围:</span>
                <span class="value">{{ memberData.businessScope || '-' }}</span>
              </div>
            </el-col>
          </el-row>
          
          <!-- 企业证件图片 -->
          <el-row :gutter="15" class="image-row">
            <el-col :span="8">
              <div class="image-item">
                <div class="image-label">营业执照</div>
                <div v-if="imageUrls.businessLicenseImage" class="image-preview" @click="showImageViewer([imageUrls.businessLicenseImage])">
                  <img :src="imageUrls.businessLicenseImage" alt="营业执照" class="preview-image" />
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
                <div v-if="imageUrls.legalPersonIdFront" class="image-preview" @click="showImageViewer([imageUrls.legalPersonIdFront])">
                  <img :src="imageUrls.legalPersonIdFront" alt="法人身份证正面" class="preview-image" />
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
                <div v-if="imageUrls.legalPersonIdBack" class="image-preview" @click="showImageViewer([imageUrls.legalPersonIdBack])">
                  <img :src="imageUrls.legalPersonIdBack" alt="法人身份证反面" class="preview-image" />
                  <div class="image-overlay">
                    <el-icon><ZoomIn /></el-icon>
                  </div>
                </div>
                <div v-else class="no-image">暂无图片</div>
              </div>
            </el-col>
          </el-row>
        </div>

        <!-- VIP信息 -->
        <div class="info-section">
          <div class="section-title">
            <el-icon><Vip /></el-icon>
            <span>VIP信息</span>
          </div>
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="info-item">
                <span class="label">VIP等级:</span>
                <el-tag :type="memberData.vipLevel === 0 ? 'info' : 'success'">
                  {{ memberData.vipLevelName }}
                </el-tag>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">账户余额:</span>
                <span class="value highlight">{{ currencySymbol }}{{ memberData.balance }}</span>
              </div>
            </el-col>
          </el-row>
        </div>

        <!-- 银行账号信息 -->
        <div class="info-section">
          <div class="section-title">
            <el-icon><Wallet /></el-icon>
            <span>银行账号信息</span>
          </div>
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="info-item">
                <span class="label">开户银行:</span>
                <span class="value">{{ memberData.bankName || '-' }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">银行账号:</span>
                <span class="value">{{ memberData.bankAccount || '-' }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="info-item">
                <span class="label">支付宝账号:</span>
                <span class="value">{{ memberData.alipayAccount || '-' }}</span>
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="info-item">
                <span class="label">微信账号:</span>
                <span class="value">{{ memberData.wechatAccount || '-' }}</span>
              </div>
            </el-col>
          </el-row>
        </div>

        <!-- 地址信息 -->
        <div class="info-section">
          <div class="section-title">
            <el-icon><Location /></el-icon>
            <span>地址信息</span>
          </div>
          <el-row :gutter="20">
            <el-col :span="24">
              <div class="info-item">
                <span class="label">详细地址:</span>
                <span class="value">{{ memberData.address || '-' }}</span>
              </div>
            </el-col>
          </el-row>
        </div>
      </div>
      
      <div v-else class="no-data">
        <el-empty description="暂无会员数据" />
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
import { ref, onMounted, defineExpose } from 'vue'
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
  Location,
  ZoomIn
} from '@element-plus/icons-vue'

// 定义组件属性
const props = defineProps({
  adminLoginPath: {
    type: String,
    default: ''
  },
  memberId: {
    type: Number,
    default: null
  },
  autoLoad: {
    type: Boolean,
    default: false
  }
})

// 响应式数据
const loading = ref(false)
const memberData = ref(null)
const currencySymbol = ref('$')
const imageUrls = ref({
  individualIdFront: '',
  individualIdBack: '',
  businessLicenseImage: '',
  legalPersonIdFront: '',
  legalPersonIdBack: ''
})

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
    const signedUrlEndpoint = `/admin${loginPath}/member/file/signed-url`
    
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

// 加载会员数据
const initData = async () => {
  if (!props.memberId) {
    ElMessage.error('未指定会员ID')
    return
  }
  
  loading.value = true
  try {
    const response = await fetch(`/admin${props.adminLoginPath}/member/${props.memberId}/view/tab`, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    
    const result = await response.json()
    
    if (result.success) {
      memberData.value = result.data
      
      // 更新货币符号
      if (result.currencySymbol) {
        currencySymbol.value = result.currencySymbol
      }
      
      // 加载图片URL
      await loadImageUrls()
    } else {
      ElMessage.error(result.error || '加载数据失败')
    }
  } catch (error) {
    ElMessage.error('加载数据失败: ' + error.message)
  } finally {
    loading.value = false
  }
}

// 加载图片URL
const loadImageUrls = async () => {
  if (!memberData.value) return
  
  // 个人会员图片
  if (memberData.value.customerType === 'individual') {
    if (memberData.value.individualIdFront) {
      imageUrls.value.individualIdFront = await getSignedUrl(memberData.value.individualIdFront)
    }
    if (memberData.value.individualIdBack) {
      imageUrls.value.individualIdBack = await getSignedUrl(memberData.value.individualIdBack)
    }
  }
  
  // 企业会员图片
  if (memberData.value.customerType === 'company') {
    if (memberData.value.businessLicenseImage) {
      imageUrls.value.businessLicenseImage = await getSignedUrl(memberData.value.businessLicenseImage)
    }
    if (memberData.value.legalPersonIdFront) {
      imageUrls.value.legalPersonIdFront = await getSignedUrl(memberData.value.legalPersonIdFront)
    }
    if (memberData.value.legalPersonIdBack) {
      imageUrls.value.legalPersonIdBack = await getSignedUrl(memberData.value.legalPersonIdBack)
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
  // 触发关闭当前标签页事件
  window.dispatchEvent(new CustomEvent('close-current-tab'))
}

// 组件挂载时加载数据
onMounted(() => {
  if (props.autoLoad && props.memberId) {
    initData()
  }
})

// 暴露方法给父组件调用
defineExpose({
  initData
})
</script>

<style scoped>
.member-view-tab {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.member-view-card {
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

.member-detail-content {
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
