<template>
  <div class="member-edit-tab" v-loading="loading">
    <el-card class="member-edit-card">
      <!-- 头部操作栏 -->
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon"><Edit /></el-icon>
            <span class="header-title">编辑会员</span>
          </div>
          <div class="header-right">
            <el-button @click="handleBack" :icon="Back">返回列表</el-button>
            <el-button type="primary" @click="handleSave" :loading="saving" :icon="Check">保存</el-button>
          </div>
        </div>
      </template>

      <!-- 内容区域 -->
      <el-form 
        v-if="memberData" 
        :model="memberData" 
        :rules="rules"
        ref="formRef"
        label-width="120px"
        class="member-edit-form"
      >
        <!-- 账号信息 -->
        <div class="info-section">
          <div class="section-title">
            <el-icon><InfoFilled /></el-icon>
            <span>账号信息</span>
          </div>
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="会员ID">
                <el-input v-model="memberData.id" disabled />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="用户名">
                <el-input v-model="memberData.username" disabled />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="会员类型">
                <el-tag :type="memberData.customerType === 'company' ? 'warning' : 'primary'">
                  {{ memberData.customerTypeName }}
                </el-tag>
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="邮箱" prop="email">
                <el-input v-model="memberData.email" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="手机号">
                <el-input v-model="memberData.mobile" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="账号状态">
                <el-select v-model="memberData.isActive">
                  <el-option label="激活" :value="true" />
                  <el-option label="禁用" :value="false" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="实名状态">
                <el-select v-model="memberData.isVerified" @change="handleVerifiedChange">
                  <el-option label="已实名" :value="true" />
                  <el-option label="未实名" :value="false" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="审核状态">
                <el-select v-model="memberData.auditStatus" :disabled="memberData.isVerified" @change="handleAuditStatusChange">
                  <el-option label="待重新提交" value="resubmit" />
                  <el-option label="待审核" value="pending" />
                  <el-option label="已通过" value="approved" />
                  <el-option label="已拒绝" value="rejected" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="注册时间">
                <el-input v-model="memberData.createdAt" disabled />
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="最后登录">
                <el-input v-model="memberData.lastLoginAt" disabled />
              </el-form-item>
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
              <el-form-item label="真实姓名">
                <el-input v-model="memberData.realName" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="昵称">
                <el-input v-model="memberData.nickname" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="性别">
                <el-select v-model="memberData.gender">
                  <el-option label="未知" :value="0" />
                  <el-option label="男" :value="1" />
                  <el-option label="女" :value="2" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="身份证号">
                <el-input v-model="memberData.individualIdCard" />
              </el-form-item>
            </el-col>
          </el-row>
          
          <!-- 个人证件图片 -->
          <el-row :gutter="20" class="image-row">
            <el-col :span="12">
              <div class="image-upload-container">
                <div class="image-label">身份证正面</div>
                <div class="upload-container">
                  <el-upload
                    :action="`/admin${adminLoginPath}/member/upload-file`"
                    :headers="{ 'X-Requested-With': 'XMLHttpRequest' }"
                    :show-file-list="false"
                    :on-success="(response) => handleUploadSuccess(response, 'individualIdFront')"
                    :on-error="handleUploadError"
                    :before-upload="beforeUpload"
                  >
                    <div v-if="imageUrls.individualIdFront" class="image-preview" @click.stop="showImageViewer([imageUrls.individualIdFront])">
                      <img :src="imageUrls.individualIdFront" alt="身份证正面" class="preview-image" />
                      <div class="image-overlay">
                        <el-icon><ZoomIn /></el-icon>
                      </div>
                    </div>
                    <div v-else class="upload-placeholder">
                      <el-icon><Plus /></el-icon>
                      <div>点击上传</div>
                    </div>
                  </el-upload>
                </div>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="image-upload-container">
                <div class="image-label">身份证反面</div>
                <div class="upload-container">
                  <el-upload
                    :action="`/admin${adminLoginPath}/member/upload-file`"
                    :headers="{ 'X-Requested-With': 'XMLHttpRequest' }"
                    :show-file-list="false"
                    :on-success="(response) => handleUploadSuccess(response, 'individualIdBack')"
                    :on-error="handleUploadError"
                    :before-upload="beforeUpload"
                  >
                    <div v-if="imageUrls.individualIdBack" class="image-preview" @click.stop="showImageViewer([imageUrls.individualIdBack])">
                      <img :src="imageUrls.individualIdBack" alt="身份证反面" class="preview-image" />
                      <div class="image-overlay">
                        <el-icon><ZoomIn /></el-icon>
                      </div>
                    </div>
                    <div v-else class="upload-placeholder">
                      <el-icon><Plus /></el-icon>
                      <div>点击上传</div>
                    </div>
                  </el-upload>
                </div>
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
              <el-form-item label="公司名称">
                <el-input v-model="memberData.companyName" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="公司类型">
                <el-select v-model="memberData.companyType" placeholder="请选择公司类型">
                  <el-option label="工厂" value="factory" />
                  <el-option label="贸易商" value="trader" />
                  <el-option label="工贸一体" value="factory_trader" />
                  <el-option label="品牌商" value="brand" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="营业执照号">
                <el-input v-model="memberData.businessLicenseNumber" />
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="法人姓名">
                <el-input v-model="memberData.legalPersonName" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="法人身份证号">
                <el-input v-model="memberData.legalPersonIdCard" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="注册资本">
                <el-input v-model="memberData.registeredCapital" placeholder="单位：万元">
                  <template #append>万元</template>
                </el-input>
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="成立日期">
                <el-date-picker
                  v-model="memberData.establishmentDate"
                  type="date"
                  placeholder="选择日期"
                  value-format="YYYY-MM-DD"
                  style="width: 100%"
                />
              </el-form-item>
            </el-col>
            <el-col :span="16">
              <el-form-item label="经营范围">
                <el-input v-model="memberData.businessScope" type="textarea" :rows="2" />
              </el-form-item>
            </el-col>
          </el-row>
          
          <!-- 企业证件图片 -->
          <el-row :gutter="20" class="image-row">
            <el-col :span="8">
              <div class="image-upload-container">
                <div class="image-label">营业执照</div>
                <div class="upload-container">
                  <el-upload
                    :action="`/admin${adminLoginPath}/member/upload-file`"
                    :headers="{ 'X-Requested-With': 'XMLHttpRequest' }"
                    :show-file-list="false"
                    :on-success="(response) => handleUploadSuccess(response, 'businessLicenseImage')"
                    :on-error="handleUploadError"
                    :before-upload="beforeUpload"
                  >
                    <div v-if="imageUrls.businessLicenseImage" class="image-preview" @click.stop="showImageViewer([imageUrls.businessLicenseImage])">
                      <img :src="imageUrls.businessLicenseImage" alt="营业执照" class="preview-image" />
                      <div class="image-overlay">
                        <el-icon><ZoomIn /></el-icon>
                      </div>
                    </div>
                    <div v-else class="upload-placeholder">
                      <el-icon><Plus /></el-icon>
                      <div>点击上传</div>
                    </div>
                  </el-upload>
                </div>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="image-upload-container">
                <div class="image-label">法人身份证正面</div>
                <div class="upload-container">
                  <el-upload
                    :action="`/admin${adminLoginPath}/member/upload-file`"
                    :headers="{ 'X-Requested-With': 'XMLHttpRequest' }"
                    :show-file-list="false"
                    :on-success="(response) => handleUploadSuccess(response, 'legalPersonIdFront')"
                    :on-error="handleUploadError"
                    :before-upload="beforeUpload"
                  >
                    <div v-if="imageUrls.legalPersonIdFront" class="image-preview" @click.stop="showImageViewer([imageUrls.legalPersonIdFront])">
                      <img :src="imageUrls.legalPersonIdFront" alt="法人身份证正面" class="preview-image" />
                      <div class="image-overlay">
                        <el-icon><ZoomIn /></el-icon>
                      </div>
                    </div>
                    <div v-else class="upload-placeholder">
                      <el-icon><Plus /></el-icon>
                      <div>点击上传</div>
                    </div>
                  </el-upload>
                </div>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="image-upload-container">
                <div class="image-label">法人身份证反面</div>
                <div class="upload-container">
                  <el-upload
                    :action="`/admin${adminLoginPath}/member/upload-file`"
                    :headers="{ 'X-Requested-With': 'XMLHttpRequest' }"
                    :show-file-list="false"
                    :on-success="(response) => handleUploadSuccess(response, 'legalPersonIdBack')"
                    :on-error="handleUploadError"
                    :before-upload="beforeUpload"
                  >
                    <div v-if="imageUrls.legalPersonIdBack" class="image-preview" @click.stop="showImageViewer([imageUrls.legalPersonIdBack])">
                      <img :src="imageUrls.legalPersonIdBack" alt="法人身份证反面" class="preview-image" />
                      <div class="image-overlay">
                        <el-icon><ZoomIn /></el-icon>
                      </div>
                    </div>
                    <div v-else class="upload-placeholder">
                      <el-icon><Plus /></el-icon>
                      <div>点击上传</div>
                    </div>
                  </el-upload>
                </div>
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
              <el-form-item label="VIP等级">
                <el-select v-model="memberData.vipLevel">
                  <el-option label="普通用户" :value="0" />
                  <el-option label="VIP1" :value="1" />
                  <el-option label="VIP2" :value="2" />
                  <el-option label="VIP3" :value="3" />
                  <el-option label="VIP4" :value="4" />
                  <el-option label="VIP5" :value="5" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="账户余额">
                <el-input v-model="memberData.balance" disabled>
                  <template #prepend>{{ currencySymbol }}</template>
                </el-input>
              </el-form-item>
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
              <el-form-item label="开户银行">
                <el-input v-model="memberData.bankName" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="银行账号">
                <el-input v-model="memberData.bankAccount" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="支付宝账号">
                <el-input v-model="memberData.alipayAccount" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="微信账号">
                <el-input v-model="memberData.wechatAccount" />
              </el-form-item>
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
              <el-form-item label="详细地址">
                <el-input v-model="memberData.address" type="textarea" :rows="2" />
              </el-form-item>
            </el-col>
          </el-row>
        </div>
      </el-form>
      
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
  ElForm,
  ElFormItem,
  ElInput,
  ElSelect,
  ElOption,
  ElRow,
  ElCol,
  ElTag,
  ElIcon,
  ElMessage,
  ElEmpty,
  ElUpload,
  ElImageViewer,
  ElDatePicker,
  vLoading
} from 'element-plus'
import {
  User,
  Back,
  Edit,
  Check,
  InfoFilled,
  OfficeBuilding,
  Vip,
  Wallet,
  Location,
  ZoomIn,
  Plus
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
const saving = ref(false)
const memberData = ref(null)
const formRef = ref()
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

// 表单验证规则
const rules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ]
}

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

// 文件上传前验证
const beforeUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt5M = file.size / 1024 / 1024 < 5

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt5M) {
    ElMessage.error('图片大小不能超过 5MB!')
    return false
  }
  return true
}

// 处理文件上传成功
const handleUploadSuccess = async (response, field) => {
  if (response.success) {
    // 更新数据字段
    memberData.value[field] = response.key
    // 更新预览URL
    imageUrls.value[field] = response.previewUrl
    ElMessage.success('图片上传成功')
  } else {
    ElMessage.error(response.error || '图片上传失败')
  }
}

// 处理文件上传失败
const handleUploadError = (error) => {
  ElMessage.error('图片上传失败: ' + error.message)
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

// 处理实名状态变化
const handleVerifiedChange = (value) => {
  // 如果选择了已实名，审核状态自动设置为已通过
  if (value === true) {
    memberData.value.auditStatus = 'approved'
  } else {
    // 如果选择了未实名，但审核状态是已通过，则改为待审核
    if (memberData.value.auditStatus === 'approved') {
      memberData.value.auditStatus = 'pending'
    }
  }
}

// 处理审核状态变化
const handleAuditStatusChange = (value) => {
  // 如果选择了已通过，实名状态自动设置为已实名
  if (value === 'approved') {
    memberData.value.isVerified = true
  }
}

// 保存会员信息
const handleSave = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
  } catch (error) {
    ElMessage.error('请填写正确的表单信息')
    return
  }
  
  saving.value = true
  try {
    const response = await fetch(`/admin${props.adminLoginPath}/member/${props.memberId}/update`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: JSON.stringify(memberData.value)
    })
    
    const result = await response.json()
    
    if (result.success) {
      ElMessage.success(result.message || '保存成功')
      // 触发事件通知父组件
      window.dispatchEvent(new CustomEvent('member-save-success'))
    } else {
      ElMessage.error(result.error || '保存失败')
    }
  } catch (error) {
    ElMessage.error('保存失败: ' + error.message)
  } finally {
    saving.value = false
  }
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
.member-edit-tab {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.member-edit-card {
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

.member-edit-form {
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

.image-row {
  margin-top: 20px;
}

/* 图片上传区域容器 - 文字在上，图片在下，垂直居中 */
.image-upload-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.image-label {
  text-align: center;
  margin-bottom: 10px;
  font-size: 14px;
  font-weight: 500;
  color: #606266;
}

.upload-container {
  width: 100%;
  display: flex;
  justify-content: center;
}

.image-preview {
  position: relative;
  width: 178px;
  height: 178px;
  border: 1px solid #dcdfe6;
  border-radius: 6px;
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

.upload-placeholder {
  width: 178px;
  height: 178px;
  border: 1px dashed #dcdfe6;
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: #909399;
  background-color: #fafafa;
  cursor: pointer;
  transition: border-color 0.3s;
}

.upload-placeholder:hover {
  border-color: #CB261C;
  color: #409eff;
}

.upload-placeholder .el-icon {
  font-size: 40px;
  margin-bottom: 10px;
}

.no-data {
  padding: 40px;
  text-align: center;
}
</style>
