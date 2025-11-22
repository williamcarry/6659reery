<template>
  <div class="address-list-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span class="header-title">地址管理</span>
          <div class="header-actions">
            <el-button type="primary" @click="showAddDialog">添加地址</el-button>
          </div>
        </div>
      </template>

      <!-- 地址表格 -->
      <el-table
        :data="addresses"
        style="width: 100%; margin-top: 20px;"
        v-loading="loading"
        element-loading-text="数据加载中..."
        :fit="true"
        :border="true"
        :stripe="true"
        :header-cell-style="{ textAlign: 'center', backgroundColor: '#f5f7fa' }"
        :cell-style="{ textAlign: 'center' }"
      >
        <el-table-column prop="id" label="ID" min-width="80" />
        <el-table-column prop="typeText" label="地址类型" min-width="120">
          <template #default="scope">
            <el-tag 
              :type="getAddressTypeTagType(scope.row.type)" 
              effect="dark"
            >
              {{ scope.row.typeText }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="address" label="详细地址" min-width="300" show-overflow-tooltip />
        <el-table-column prop="shippingRegion" label="发货区域" min-width="120">
          <template #default="scope">
            <el-tag v-if="scope.row.shippingRegion" type="primary">
              {{ getRegionLabel(scope.row.shippingRegion) }}
            </el-tag>
            <span v-else style="color: #909399;">-</span>
          </template>
        </el-table-column>
        <el-table-column prop="createdAt" label="创建时间" min-width="180" />
        <el-table-column prop="updatedAt" label="更新时间" min-width="180" />
        <el-table-column label="操作" min-width="180" fixed="right">
          <template #default="scope">
            <div class="button-group">
              <template v-if="scope && scope.row">
                <el-button 
                  type="primary" 
                  size="small" 
                  @click="showEditDialog(scope.row)"
                >
                  编辑
                </el-button>
                <el-button 
                  type="danger" 
                  size="small" 
                  @click="handleDelete(scope.row)"
                >
                  删除
                </el-button>
              </template>
            </div>
          </template>
        </el-table-column>
      </el-table>

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
    </el-card>

    <!-- 添加/编辑地址对话框 -->
    <el-dialog
      :model-value="dialogVisible"
      :title="dialogTitle"
      width="500px"
      @close="handleDialogClose"
    >
      <el-form
        :model="addressForm"
        :rules="addressFormRules"
        ref="addressFormRef"
        label-width="100px"
      >
        <el-form-item label="地址类型" prop="type">
          <el-select v-model="addressForm.type" placeholder="请选择地址类型" style="width: 100%;">
            <el-option label="发货地址" value="shipping" />
            <el-option label="退货地址" value="return" />
          </el-select>
        </el-form-item>
        <el-form-item label="发货区域" prop="shippingRegion">
          <el-select v-model="addressForm.shippingRegion" placeholder="请选择发货区域" clearable style="width: 100%;">
            <el-option
              v-for="region in shippingRegionOptions"
              :key="region.value"
              :label="region.label"
              :value="region.value"
            />
          </el-select>
          <div class="form-item-tip">选择该地址对应的发货区域</div>
        </el-form-item>
        <el-form-item label="详细地址" prop="address">
          <el-input
            v-model="addressForm.address"
            type="textarea"
            :rows="4"
            placeholder="请输入详细地址"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="handleDialogClose">取消</el-button>
          <el-button type="primary" @click="handleSaveAddress" :loading="saving">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, defineProps, defineExpose } from 'vue'
import {
  ElCard,
  ElButton,
  ElTable,
  ElTableColumn,
  ElPagination,
  ElDialog,
  ElForm,
  ElFormItem,
  ElInput,
  ElSelect,
  ElOption,
  ElMessage,
  ElMessageBox,
  ElTag,
  vLoading
} from 'element-plus'

const props = defineProps({
  supplierLoginPath: {
    type: String,
    required: true
  },
  autoLoad: {
    type: Boolean,
    default: false
  }
})

const loading = ref(false)
const saving = ref(false)
const addresses = ref([])
const dialogVisible = ref(false)
const dialogTitle = ref('')
const isEdit = ref(false)
const editingAddressId = ref(null)
const shippingRegionOptions = ref([])

// 地址表单
const addressForm = reactive({
  type: 'shipping',
  address: '',
  shippingRegion: ''
})

// 表单验证规则
const addressFormRules = {
  type: [
    { required: true, message: '请选择地址类型', trigger: 'change' }
  ],
  address: [
    { required: true, message: '请输入详细地址', trigger: 'blur' }
  ]
}

// 分页数据
const pagination = reactive({
  currentPage: 1,
  totalPages: 1,
  totalItems: 0,
  itemsPerPage: 20
})

// 获取地址类型标签类型
const getAddressTypeTagType = (type) => {
  const typeMap = {
    'shipping': 'success',  // 发货地址用绿色
    'return': 'warning'     // 退货地址用橙色
  }
  return typeMap[type] || 'info'
}

// 获取区域显示名称
const getRegionLabel = (regionCode) => {
  if (!regionCode) return '-'
  const region = shippingRegionOptions.value.find(r => r.value === regionCode)
  return region ? region.label : regionCode
}

// 加载发货区域选项
const loadShippingRegions = async () => {
  try {
    const response = await fetch(`/supplier${props.supplierLoginPath}/address/shipping-regions`, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })

    const result = await response.json()

    if (result.success) {
      shippingRegionOptions.value = result.data || []
    }
  } catch (error) {
    console.error('加载发货区域选项失败:', error)
  }
}

// 加载地址数据
const loadAddressData = async (page = 1, limit = 20) => {
  loading.value = true
  try {
    const params = new URLSearchParams({
      page: page,
      limit: limit
    })

    const url = `/supplier${props.supplierLoginPath}/address/list/data?${params}`

    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })

    const result = await response.json()

    if (result.success) {
      addresses.value = result.data
      pagination.currentPage = result.pagination.currentPage
      pagination.totalPages = result.pagination.totalPages
      pagination.totalItems = result.pagination.totalItems
      pagination.itemsPerPage = result.pagination.itemsPerPage
    } else {
      ElMessage.error(result.message || '加载数据失败')
    }
  } catch (error) {
    console.error('加载数据失败:', error)
    ElMessage.error('网络错误，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 显示添加地址对话框
const showAddDialog = () => {
  dialogTitle.value = '添加地址'
  isEdit.value = false
  editingAddressId.value = null
  
  // 重置表单
  addressForm.type = 'shipping'
  addressForm.address = ''
  addressForm.shippingRegion = ''
  
  dialogVisible.value = true
}

// 显示编辑地址对话框
const showEditDialog = (row) => {
  dialogTitle.value = '编辑地址'
  isEdit.value = true
  editingAddressId.value = row.id
  
  // 填充表单数据
  addressForm.type = row.type
  addressForm.address = row.address
  addressForm.shippingRegion = row.shippingRegion || ''
  
  dialogVisible.value = true
}

// 关闭对话框
const handleDialogClose = () => {
  dialogVisible.value = false
}

// 保存地址
const handleSaveAddress = async () => {
  if (!addressForm.address.trim()) {
    ElMessage.warning('请输入详细地址')
    return
  }

  saving.value = true
  try {
    let url, method
    if (isEdit.value) {
      // 编辑地址
      url = `/supplier${props.supplierLoginPath}/address/update/${editingAddressId.value}`
      method = 'POST'
    } else {
      // 添加地址
      url = `/supplier${props.supplierLoginPath}/address/create`
      method = 'POST'
    }

    const response = await fetch(url, {
      method: method,
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: JSON.stringify({
        type: addressForm.type,
        address: addressForm.address,
        shippingRegion: addressForm.shippingRegion || null
      })
    })

    const result = await response.json()

    if (result.success) {
      ElMessage.success(result.message || (isEdit.value ? '地址更新成功' : '地址添加成功'))
      dialogVisible.value = false
      loadAddressData(pagination.currentPage, pagination.itemsPerPage)
    } else {
      ElMessage.error(result.message || (isEdit.value ? '地址更新失败' : '地址添加失败'))
    }
  } catch (error) {
    console.error('保存地址失败:', error)
    ElMessage.error('网络错误，请稍后重试')
  } finally {
    saving.value = false
  }
}

// 删除地址
const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确定要删除地址"${row.address}"吗？`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(async () => {
    try {
      const response = await fetch(`/supplier${props.supplierLoginPath}/address/delete/${row.id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        }
      })

      const result = await response.json()

      if (result.success) {
        ElMessage.success('删除成功')
        loadAddressData(pagination.currentPage, pagination.itemsPerPage)
      } else {
        ElMessage.error(result.message || '删除失败')
      }
    } catch (error) {
      console.error('删除失败:', error)
      ElMessage.error('网络错误，请稍后重试')
    }
  }).catch(() => {
    // 取消删除
  })
}

// 分页大小变化
const handleSizeChange = (val) => {
  pagination.itemsPerPage = val
  loadAddressData(pagination.currentPage, val)
}

// 当前页变化
const handleCurrentChange = (val) => {
  pagination.currentPage = val
  loadAddressData(val, pagination.itemsPerPage)
}

// 组件挂载
onMounted(() => {
  loadShippingRegions() // 加载发货区域选项
  if (props.autoLoad) {
    loadAddressData()
  }
})

// 暴露方法供父组件调用（按需加载）
defineExpose({
  loadAddressData
})
</script>

<style scoped>
.address-list-container {
  width: 100%;
  max-width: 2000px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-title {
  font-size: 18px;
  font-weight: 600;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  width: 100%;
}

:deep(.el-table) {
  font-size: 14px;
}

:deep(.el-table th) {
  background-color: #f5f7fa;
}

.button-group {
  display: flex;
  gap: 5px;
  flex-wrap: nowrap;
}

.button-group .el-button {
  margin: 0;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.form-item-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
  line-height: 1.5;
}
</style>