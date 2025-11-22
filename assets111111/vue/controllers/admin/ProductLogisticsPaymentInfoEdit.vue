<template>
  <div class="product-logistics-payment-info-edit">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2 class="page-title">
        <el-icon class="title-icon"><Document /></el-icon>
        商品详情物流支付说明
      </h2>
    </div>
    
    <!-- 编辑表单 -->
    <el-card class="edit-card">
      <el-form :model="form" label-position="top" class="edit-form">
        <!-- 中文内容 -->
        <el-form-item label="中文内容">
          <rich-text-editor
            v-model="form.content"
            :admin-login-path="adminLoginPath"
            placeholder="请输入中文物流与支付说明..."
            height="400px"
          />
        </el-form-item>
        
        <!-- 英文内容 -->
        <el-form-item label="英文内容">
          <rich-text-editor
            v-model="form.contentEn"
            :admin-login-path="adminLoginPath"
            placeholder="Please enter English logistics and payment information..."
            height="400px"
          />
        </el-form-item>
        
        <!-- 操作按钮 -->
        <el-form-item>
          <div class="form-actions">
            <el-button 
              type="primary" 
              @click="saveData" 
              :loading="saving"
            >
              <el-icon><Check /></el-icon>
              保存内容
            </el-button>
            <el-button @click="resetForm">
              <el-icon><RefreshLeft /></el-icon>
              重置表单
            </el-button>
          </div>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 保存提示 -->
    <el-alert
      v-if="saveSuccess"
      title="保存成功"
      type="success"
      show-icon
      closable
      class="save-success-alert"
    />
  </div>
</template>

<script>
import {
  ElCard,
  ElForm,
  ElFormItem,
  ElButton,
  ElAlert,
  ElIcon,
  ElMessage
} from 'element-plus'
import {
  Document,
  Check,
  RefreshLeft
} from '@element-plus/icons-vue'
import RichTextEditor from './RichTextEditor.vue'

export default {
  name: 'ProductLogisticsPaymentInfoEdit',
  components: {
    RichTextEditor,
    ElCard,
    ElForm,
    ElFormItem,
    ElButton,
    ElAlert,
    ElIcon,
    Document,
    Check,
    RefreshLeft
  },
  props: {
    adminLoginPath: {
      type: String,
      required: true
    },
    autoLoad: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      form: {
        id: null,
        content: '',
        contentEn: ''
      },
      loading: false,
      saving: false,
      saveSuccess: false
    }
  },
  methods: {
    // 加载数据
    async loadData() {
      this.loading = true
      try {
        const response = await fetch(`/admin${this.adminLoginPath}/product-logistics-payment-info/data`)
        const result = await response.json()
        
        if (result.success) {
          this.form = {
            id: result.data.id,
            content: result.data.content || '',
            contentEn: result.data.contentEn || ''
          }
        } else {
          ElMessage.error('加载数据失败: ' + (result.message || '未知错误'))
        }
      } catch (error) {
        console.error('加载数据出错:', error)
        ElMessage.error('加载数据时发生网络错误')
      } finally {
        this.loading = false
      }
    },
    
    // 保存数据
    async saveData() {
      this.saving = true
      this.saveSuccess = false
      
      try {
        const response = await fetch(`/admin${this.adminLoginPath}/product-logistics-payment-info/save`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
          },
          body: JSON.stringify({
            content: this.form.content,
            contentEn: this.form.contentEn
          })
        })
        
        const result = await response.json()
        
        if (result.success) {
          this.form.id = result.data.id
          this.saveSuccess = true
          ElMessage.success('保存成功')
          
          // 3秒后隐藏成功提示
          setTimeout(() => {
            this.saveSuccess = false
          }, 3000)
        } else {
          ElMessage.error('保存失败: ' + (result.message || '未知错误'))
        }
      } catch (error) {
        console.error('保存数据出错:', error)
        ElMessage.error('保存数据时发生网络错误')
      } finally {
        this.saving = false
      }
    },
    
    // 重置表单
    resetForm() {
      this.form = {
        id: null,
        content: '',
        contentEn: ''
      }
      this.saveSuccess = false
      ElMessage.info('表单已重置')
    }
  },
  mounted() {
    // 组件挂载时
    if (this.autoLoad) {
      this.loadData()
    }
  }
}
</script>

<style scoped>
.product-logistics-payment-info-edit {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #ebeef5;
}

.page-title {
  margin: 0;
  font-size: 24px;
  color: #303133;
  display: flex;
  align-items: center;
  gap: 10px;
}

.title-icon {
  font-size: 28px;
  color: #409eff;
}

.edit-card {
  margin-bottom: 20px;
}

.edit-form {
  padding: 20px 0;
}

.form-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-start;
}

.save-success-alert {
  margin-top: 20px;
  border-radius: 8px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #606266;
}
</style>