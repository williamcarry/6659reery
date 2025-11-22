<template>
  <div class="member-create">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2 class="page-title">
        <el-icon class="title-icon"><User /></el-icon>
        添加会员
      </h2>
    </div>
    
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <div class="card-header-title">
            <el-icon class="card-icon"><Plus /></el-icon>
            会员信息
          </div>
        </div>
      </template>
      
      <el-form :model="memberForm" :rules="rules" ref="formRef" label-width="120px">
        <!-- 基本信息 -->
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="用户名" prop="username">
              <el-input v-model="memberForm.username" />
              <div class="form-item-help">用户名必须是英文字母、数字和下划线的组合，且不能以数字或下划线开头</div>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="memberForm.email" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="密码" prop="password">
              <el-input v-model="memberForm.password" type="password" />
              <div class="form-item-help">密码长度至少8个字符</div>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="确认密码" prop="confirmPassword">
              <el-input v-model="memberForm.confirmPassword" type="password" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <!-- 会员类型选择 -->
        <el-form-item label="会员类型" prop="customerType">
          <el-radio-group v-model="memberForm.customerType">
            <el-radio label="individual">个人</el-radio>
            <el-radio label="company">企业</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <!-- 个人会员信息 -->
        <div v-if="memberForm.customerType === 'individual'">
          <h3>个人信息</h3>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="姓名" prop="realName">
                <el-input v-model="memberForm.realName" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="身份证号" prop="individualIdCard">
                <el-input v-model="memberForm.individualIdCard" />
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="手机号" prop="mobile">
                <el-input v-model="memberForm.mobile" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="昵称">
                <el-input v-model="memberForm.nickname" />
              </el-form-item>
            </el-col>
          </el-row>
          
          <!-- 个人证件上传 -->
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="身份证正面">
                <file-upload
                  v-model="memberForm.individualIdFront"
                  :admin-login-path="adminLoginPath"
                  accept="image/*"
                  :max-size="5"
                  endpoint-type="member"
                />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="身份证反面">
                <file-upload
                  v-model="memberForm.individualIdBack"
                  :admin-login-path="adminLoginPath"
                  accept="image/*"
                  :max-size="5"
                  endpoint-type="member"
                />
              </el-form-item>
            </el-col>
          </el-row>
        </div>
        
        <!-- 企业会员信息 -->
        <div v-if="memberForm.customerType === 'company'">
          <h3>企业信息</h3>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="公司名称" prop="companyName">
                <el-input v-model="memberForm.companyName" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="公司类型">
                <el-select v-model="memberForm.companyType" placeholder="请选择公司类型">
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
                <el-input v-model="memberForm.businessLicenseNumber" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="法人姓名" prop="legalPersonName">
                <el-input v-model="memberForm.legalPersonName" />
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="法人身份证" prop="legalPersonIdCard">
                <el-input v-model="memberForm.legalPersonIdCard" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="手机号" prop="mobile">
                <el-input v-model="memberForm.mobile" />
              </el-form-item>
            </el-col>
          </el-row>
          
          <!-- 企业证件上传 - 并列一排 -->
          <el-row :gutter="10">
            <el-col :span="8">
              <el-form-item label="营业执照">
                <file-upload
                  v-model="memberForm.businessLicenseImage"
                  :admin-login-path="adminLoginPath"
                  accept="image/*"
                  :max-size="5"
                  endpoint-type="member"
                />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="法人身份证正面">
                <file-upload
                  v-model="memberForm.legalPersonIdFront"
                  :admin-login-path="adminLoginPath"
                  accept="image/*"
                  :max-size="5"
                  endpoint-type="member"
                />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="法人身份证反面">
                <file-upload
                  v-model="memberForm.legalPersonIdBack"
                  :admin-login-path="adminLoginPath"
                  accept="image/*"
                  :max-size="5"
                  endpoint-type="member"
                />
              </el-form-item>
            </el-col>
          </el-row>
        </div>
        
        <!-- 操作按钮 -->
        <el-form-item class="bottom-btns">
          <el-button type="primary" @click="submitForm" :loading="submitting">创建会员</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import {
  ElCard,
  ElForm,
  ElFormItem,
  ElInput,
  ElRow,
  ElCol,
  ElSelect,
  ElOption,
  ElRadioGroup,
  ElRadio,
  ElButton,
  ElMessage,
  ElIcon
} from 'element-plus'
import { User, Plus } from '@element-plus/icons-vue'
import FileUpload from './FileUpload.vue'

// 定义组件属性
const props = defineProps({
  adminLoginPath: {
    type: String,
    default: ''
  }
})

// 定义事件
const emit = defineEmits(['member-created'])

// 表单引用
const formRef = ref()

// 提交状态
const submitting = ref(false)

// 会员表单数据
const memberForm = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  customerType: 'individual', // 默认为个人
  // 个人信息
  nickname: '',
  realName: '',
  mobile: '',
  gender: 0,
  individualIdCard: '',
  individualIdFront: '',
  individualIdBack: '',
  // 企业信息
  companyName: '',
  companyType: '',
  businessLicenseNumber: '',
  businessLicenseImage: '',
  legalPersonName: '',
  legalPersonIdCard: '',
  legalPersonIdFront: '',
  legalPersonIdBack: '',
  parentId: 0
})

// 表单验证规则
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度应在3-20个字符之间', trigger: 'blur' },
    { 
      pattern: /^[a-zA-Z][a-zA-Z0-9_]*$/, 
      message: '用户名必须是英文字母、数字和下划线的组合，且不能以数字或下划线开头', 
      trigger: 'blur' 
    }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 8, message: '密码长度至少8个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { 
      validator: (rule, value, callback) => {
        if (value !== memberForm.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  customerType: [
    { required: true, message: '请选择会员类型', trigger: 'change' }
  ],
  mobile: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { 
      pattern: /^1[3-9]\d{9}$/, 
      message: '请输入正确的手机号格式', 
      trigger: 'blur' 
    }
  ],
  // 个人会员必填项
  realName: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  individualIdCard: [
    { required: true, message: '请输入身份证号', trigger: 'blur' }
  ],
  // 企业会员必填项
  companyName: [
    { required: true, message: '请输入公司名称', trigger: 'blur' }
  ],
  businessLicenseNumber: [
    { required: true, message: '请输入营业执照号', trigger: 'blur' }
  ],
  legalPersonName: [
    { required: true, message: '请输入法人姓名', trigger: 'blur' }
  ],
  legalPersonIdCard: [
    { required: true, message: '请输入法人身份证号', trigger: 'blur' }
  ]
}

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        const response = await fetch(`/admin${props.adminLoginPath}/member/create`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
          },
          body: JSON.stringify(memberForm)
        })
        
        const result = await response.json()
        
        if (result.success) {
          ElMessage.success(result.message)
          resetForm()
          emit('member-created', result.member)
        } else {
          ElMessage.error(result.error || '创建失败')
        }
      } catch (error) {
        ElMessage.error('创建失败: ' + error.message)
      } finally {
        submitting.value = false
      }
    } else {
      ElMessage.error('请填写正确的表单信息')
    }
  })
}

// 重置表单
const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  
  // 重置表单数据
  Object.keys(memberForm).forEach(key => {
    if (typeof memberForm[key] === 'string') {
      memberForm[key] = ''
    } else if (typeof memberForm[key] === 'number') {
      memberForm[key] = key === 'gender' ? 0 : 0
    }
  })
}
</script>

<style scoped>
.member-create {
  width: 100%;
  max-width: 1200px;
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

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header-title {
  font-size: 18px;
  font-weight: bold;
  display: flex;
  align-items: center;
}

.card-icon {
  margin-right: 10px;
  vertical-align: middle;
}

.form-item-help {
  font-size: 12px;
  color: #909399;
  line-height: 1.5;
  margin-top: 5px;
}

.upload-row {
  margin-bottom: 20px;
}

.upload-section {
  text-align: center;
}

.upload-label {
  margin-bottom: 10px;
  font-weight: 500;
  color: #606266;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 20px;
}
.bottom-btns {
  margin-left: 0!important;
  display: flex;
  justify-content: center;
}
</style>