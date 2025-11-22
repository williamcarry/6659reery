<template>
  <div class="supplier-edit">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>编辑供应商</span>
          <el-icon v-if="loading" class="loading-icon is-loading">
            <Loading />
          </el-icon>
        </div>
      </template>
      
      <el-form :model="supplierForm" :rules="rules" ref="formRef" label-width="120px">
        <!-- 基本信息 -->
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="用户名" prop="username">
              <el-input v-model="supplierForm.username" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="supplierForm.email" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="新密码">
              <el-input v-model="supplierForm.password" type="password" placeholder="留空则不修改密码" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="确认新密码">
              <el-input v-model="supplierForm.confirmPassword" type="password" placeholder="留空则不修改密码" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="联系人" prop="contactPerson">
              <el-input v-model="supplierForm.contactPerson" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="contactPhone">
              <el-input v-model="supplierForm.contactPhone" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="联系地址">
          <el-input v-model="supplierForm.contactAddress" type="textarea" />
        </el-form-item>
        
        <!-- 供应商类型 -->
        <el-form-item label="供应商类型" prop="supplierType">
          <el-radio-group v-model="supplierForm.supplierType" :disabled="!!supplierForm.id">
            <el-radio label="company">公司</el-radio>
            <el-radio label="individual">个人</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <!-- 公司信息 -->
        <div v-if="supplierForm.supplierType === 'company'">
          <h3>公司信息</h3>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="公司名称" prop="companyName">
                <el-input v-model="supplierForm.companyName" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="公司类型">
                <el-select v-model="supplierForm.companyType" placeholder="请选择公司类型">
                  <el-option label="工厂" value="factory" />
                  <el-option label="贸易商" value="trader" />
                  <el-option label="工贸一体" value="factory_trader" />
                  <el-option label="品牌商" value="brand" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="营业执照号" prop="businessLicenseNumber">
                <el-input v-model="supplierForm.businessLicenseNumber" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="法人姓名" prop="legalPersonName">
                <el-input v-model="supplierForm.legalPersonName" />
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-form-item label="法人身份证号" prop="legalPersonIdCard">
            <el-input v-model="supplierForm.legalPersonIdCard" />
          </el-form-item>
          
          <!-- 证件上传 - 在一行显示 -->
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="营业执照">
                <file-upload
                  v-model="supplierForm.businessLicenseImage"
                  :admin-login-path="adminLoginPath"
                  accept="image/*"
                  :max-size="5"
                  endpoint-type="supplier"
                />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="法人身份证正面">
                <file-upload
                  v-model="supplierForm.legalPersonIdFront"
                  :admin-login-path="adminLoginPath"
                  accept="image/*"
                  :max-size="5"
                  endpoint-type="supplier"
                />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="法人身份证反面">
                <file-upload
                  v-model="supplierForm.legalPersonIdBack"
                  :admin-login-path="adminLoginPath"
                  accept="image/*"
                  :max-size="5"
                  endpoint-type="supplier"
                />
              </el-form-item>
            </el-col>
          </el-row>
        </div>
        
        <!-- 个人信息 -->
        <div v-if="supplierForm.supplierType === 'individual'">
          <h3>个人信息</h3>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="真实姓名" prop="individualName">
                <el-input v-model="supplierForm.individualName" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="身份证号" prop="individualIdCard">
                <el-input v-model="supplierForm.individualIdCard" />
              </el-form-item>
            </el-col>
          </el-row>
          
          <!-- 个人身份证正反面上传 - 在一行显示 -->
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="身份证正面">
                <file-upload
                  v-model="supplierForm.individualIdFront"
                  :admin-login-path="adminLoginPath"
                  accept="image/*"
                  :max-size="5"
                  endpoint-type="supplier"
                />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="身份证反面">
                <file-upload
                  v-model="supplierForm.individualIdBack"
                  :admin-login-path="adminLoginPath"
                  accept="image/*"
                  :max-size="5"
                  endpoint-type="supplier"
                />
              </el-form-item>
            </el-col>
          </el-row>
        </div>
        
        <!-- 业务信息 -->
        <h3>业务信息</h3>
        <el-form-item label="主营业务">
          <el-input v-model="supplierForm.mainCategory" type="textarea" />
        </el-form-item>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="跨境经验">
              <el-switch v-model="supplierForm.hasCrossBorderExperience" active-text="有" inactive-text="无" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="年销售额(万元)">
              <el-input v-model="supplierForm.annualSalesVolume" type="number" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="仓库地址">
          <el-input v-model="supplierForm.warehouseAddress" type="textarea" />
        </el-form-item>
        
        <!-- 状态信息 -->
        <h3>状态信息</h3>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="账号状态">
              <el-switch v-model="supplierForm.isActive" active-text="激活" inactive-text="禁用" />
            </el-form-item>
            <div class="status-help">
              <p style="color: #f56c6c; font-size: 12px; line-height: 1.6; margin: 5px 0;">
                <strong>重要：</strong>账号未激活时，供应商无法登录账号，也无法添加商品。
              </p>
              <p style="color: #909399; font-size: 12px; line-height: 1.6; margin: 5px 0;">
                激活：供应商可以正常登录使用后台<br/>
                禁用：供应商无法登录，已登录的会被强制退出
              </p>
            </div>
          </el-col>
          <el-col :span="12">
            <el-form-item label="邮箱验证">
              <el-switch v-model="supplierForm.isVerified" active-text="已验证" inactive-text="未验证" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="审核状态">
          <el-select v-model="supplierForm.auditStatus">
            <el-option label="待审核" value="pending">
              <span>待审核</span>
              <span style="color: #909399; font-size: 12px; margin-left: 10px;">- 供应商已提交资料，等待管理员审核</span>
            </el-option>
            <el-option label="已通过" value="approved">
              <span>已通过</span>
              <span style="color: #909399; font-size: 12px; margin-left: 10px;">- 审核通过，不能修改关键认证信息</span>
            </el-option>
            <el-option label="已拒绝" value="rejected">
              <span>已拒绝</span>
              <span style="color: #909399; font-size: 12px; margin-left: 10px;">- 审核拒绝，供应商不能修改任何资料</span>
            </el-option>
            <el-option label="待重新提交" value="resubmit">
              <span>待重新提交</span>
              <span style="color: #909399; font-size: 12px; margin-left: 10px;">- 初始状态或需要修改后重新提交</span>
            </el-option>
          </el-select>
          <div class="audit-status-help">
            <p style="color: #e6a23c; font-weight: bold; margin: 10px 0 5px 0;">审核状态说明：</p>
            <p style="color: #909399; font-size: 13px; line-height: 1.8; margin: 5px 0;">
              <strong style="color: #409eff;">待审核</strong>：供应商已提交资料，等待管理员审核。供应商不能修改关键认证信息。
            </p>
            <p style="color: #909399; font-size: 13px; line-height: 1.8; margin: 5px 0;">
              <strong style="color: #67c23a;">已通过</strong>：审核通过，供应商可以正常使用后台。供应商不能修改关键认证信息。<strong style="color: #f56c6c;">只有此状态下才能添加商品。</strong>
            </p>
            <p style="color: #909399; font-size: 13px; line-height: 1.8; margin: 5px 0;">
              <strong style="color: #f56c6c;">已拒绝</strong>：审核拒绝，供应商完全不能修改任何资料也不能提交保存，也不能添加商品。
            </p>
            <p style="color: #909399; font-size: 13px; line-height: 1.8; margin: 5px 0;">
              <strong style="color: #e6a23c;">待重新提交</strong>：初始注册状态或需要修改后重新提交。供应商可以修改所有资料，但不能添加商品。
            </p>
            <p style="color: #f56c6c; font-size: 13px; font-weight: bold; line-height: 1.8; margin: 10px 0 5px 0; padding: 8px; background-color: #fef0f0; border-left: 3px solid #f56c6c;">
              ⚠️ 注意：供应商必须同时满足<strong>账号状态为“激活”</strong>且<strong>审核状态为“已通过”</strong>才能添加商品！
            </p>
          </div>
        </el-form-item>
        
        <el-form-item label="审核备注" v-if="supplierForm.auditStatus !== 'pending'">
          <el-input v-model="supplierForm.auditRemark" type="textarea" />
        </el-form-item>
        
        <!-- 操作按钮 -->
        <el-form-item>
          <el-button type="primary" @click="submitForm" :loading="submitting">保存</el-button>
          <el-button @click="cancelEdit">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import {
  ElCard,
  ElForm,
  ElFormItem,
  ElInput,
  ElRow,
  ElCol,
  ElRadioGroup,
  ElRadio,
  ElSelect,
  ElOption,
  ElSwitch,
  ElButton,
  ElMessage,
  ElIcon
} from 'element-plus'
import { Loading } from '@element-plus/icons-vue'
import FileUpload from './FileUpload.vue'

// 定义组件属性
const props = defineProps({
  adminLoginPath: {
    type: String,
    default: ''
  },
  supplier: {
    type: Object,
    default: () => ({})
  }
})

// 定义事件
const emit = defineEmits(['supplier-updated', 'cancel'])

// 表单引用
const formRef = ref()

// 加载状态
const loading = ref(false)

// 提交状态
const submitting = ref(false)

// 供应商表单数据
const supplierForm = reactive({
  id: null,
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  contactPerson: '',
  contactPhone: '',
  contactAddress: '',
  supplierType: 'company',
  companyName: '',
  companyType: '',
  businessLicenseNumber: '',
  businessLicenseImage: '',
  legalPersonName: '',
  legalPersonIdCard: '',
  legalPersonIdFront: '',
  legalPersonIdBack: '',
  individualName: '',
  individualIdCard: '',
  individualIdFront: '',
  individualIdBack: '',
  mainCategory: '',
  hasCrossBorderExperience: false,
  annualSalesVolume: '',
  warehouseAddress: '',
  isActive: true,
  isVerified: false,
  auditStatus: 'pending',
  auditRemark: ''
})

// 表单验证规则
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度应在3-20个字符之间', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { 
      validator: (rule, value, callback) => {
        if (value && value.length < 6) {
          callback(new Error('密码长度至少6个字符'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  confirmPassword: [
    { 
      validator: (rule, value, callback) => {
        if (value && value !== supplierForm.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  contactPerson: [
    { required: true, message: '请输入联系人', trigger: 'blur' }
  ],
  contactPhone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' }
  ],
  companyName: [
    { 
      required: true, 
      message: '请输入公司名称', 
      trigger: 'blur',
      validator: (rule, value, callback) => {
        if (supplierForm.supplierType === 'company' && !value) {
          callback(new Error('请输入公司名称'))
        } else {
          callback()
        }
      }
    }
  ],
  businessLicenseNumber: [
    { 
      required: true, 
      message: '请输入营业执照号', 
      trigger: 'blur',
      validator: (rule, value, callback) => {
        if (supplierForm.supplierType === 'company' && !value) {
          callback(new Error('请输入营业执照号'))
        } else {
          callback()
        }
      }
    }
  ],
  legalPersonName: [
    { 
      required: true, 
      message: '请输入法人姓名', 
      trigger: 'blur',
      validator: (rule, value, callback) => {
        if (supplierForm.supplierType === 'company' && !value) {
          callback(new Error('请输入法人姓名'))
        } else {
          callback()
        }
      }
    }
  ],
  legalPersonIdCard: [
    { 
      required: true, 
      message: '请输入法人身份证号', 
      trigger: 'blur',
      validator: (rule, value, callback) => {
        if (supplierForm.supplierType === 'company' && !value) {
          callback(new Error('请输入法人身份证号'))
        } else {
          callback()
        }
      }
    }
  ],
  individualName: [
    { 
      required: true, 
      message: '请输入真实姓名', 
      trigger: 'blur',
      validator: (rule, value, callback) => {
        if (supplierForm.supplierType === 'individual' && !value) {
          callback(new Error('请输入真实姓名'))
        } else {
          callback()
        }
      }
    }
  ],
  individualIdCard: [
    { 
      required: true, 
      message: '请输入身份证号', 
      trigger: 'blur',
      validator: (rule, value, callback) => {
        if (supplierForm.supplierType === 'individual' && !value) {
          callback(new Error('请输入身份证号'))
        } else {
          callback()
        }
      }
    }
  ]
}

// 组件挂载时初始化表单数据
onMounted(() => {
  if (props.supplier && props.supplier.id) {
    // 初始化表单数据
    Object.keys(supplierForm).forEach(key => {
      if (props.supplier.hasOwnProperty(key)) {
        supplierForm[key] = props.supplier[key]
      }
    })
  }
})

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        const response = await fetch(`/admin${props.adminLoginPath}/supplier/${supplierForm.id}/update`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
          },
          body: JSON.stringify(supplierForm)
        })
        
        const result = await response.json()
        
        if (result.success) {
          ElMessage.success(result.message)
          emit('supplier-updated', result.supplier)
        } else {
          ElMessage.error(result.error || '更新失败')
        }
      } catch (error) {
        ElMessage.error('更新失败: ' + error.message)
      } finally {
        submitting.value = false
      }
    } else {
      ElMessage.error('请填写正确的表单信息')
    }
  })
}

// 取消编辑
const cancelEdit = () => {
  emit('cancel')
}
</script>

<style scoped>
.supplier-edit {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.loading-icon {
  margin-left: 10px;
  font-size: 18px;
  color: #409eff;
}

.loading-icon.is-loading {
  animation: rotating 2s linear infinite;
}

@keyframes rotating {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

h3 {
  margin: 20px 0 10px 0;
  padding-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
  color: #606266;
}

.audit-status-help {
  margin-top: 10px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 6px;
  border-left: 4px solid #409eff;
}

.audit-status-help p {
  margin: 5px 0;
}

:deep(.el-select-dropdown__item) {
  height: auto;
  line-height: 1.5;
  padding: 10px 20px;
  white-space: normal;
}
</style>