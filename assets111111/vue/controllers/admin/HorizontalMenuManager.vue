<template>
  <div class="horizontal-menu-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2 class="page-title">
        <el-icon class="title-icon"><Menu /></el-icon>
        横向与楼层菜单管理
      </h2>
      <div class="header-actions" style="display: none;">
        <el-button type="primary" @click="showCreateDialog" :icon="Plus">
          新增菜单
        </el-button>
      </div>
    </div>
    
    <!-- 菜单列表 - 按固定顺序显示 -->
    <template v-for="position in orderedPositions" :key="position">
      <el-card class="menu-card" v-if="groupedMenus[position] && groupedMenus[position].length > 0">
        <template #header>
          <div class="card-header">
            <span class="position-title">{{ getPositionTitle(position) }}</span>
          </div>
        </template>
      
        <el-table 
          :data="groupedMenus[position]" 
          class="menu-table" 
          v-loading="loading"
          :fit="true"
          :border="false"
          :header-cell-style="{ textAlign: 'center' }"
          :cell-style="{ textAlign: 'center' }"
          :stripe="true"
          empty-text="暂无菜单数据"
        >
        <el-table-column prop="name" label="中文名称" min-width="150" />
        <el-table-column prop="nameEn" label="英文名称" min-width="150" />
        <el-table-column prop="position" label="位置" min-width="100" />
        <el-table-column prop="link" label="链接" min-width="200" v-if="position === 'header'">
          <template #default="scope">
            <a 
              v-if="scope.row.link" 
              :href="scope.row.link" 
              target="_blank" 
              class="link-text" 
              :title="scope.row.link"
            >
              {{ scope.row.link }}
            </a>
            <span v-else class="no-data">无链接</span>
          </template>
        </el-table-column>
        <el-table-column prop="icon" label="图标" min-width="100">
          <template #default="scope">
            <div v-if="scope.row.icon" class="icon-preview">
              <img :src="scope.row.icon" :alt="scope.row.icon" class="menu-icon" />
            </div>
            <span v-else>无图标</span>
          </template>
        </el-table-column>
        <el-table-column prop="productIds" label="关联商品" min-width="350" v-if="position === 'floor'">
          <template #default="scope">
            <div v-if="scope.row.productIds && scope.row.productIds.length > 0" class="table-products-grid">
              <div 
                v-for="(productId, index) in scope.row.productIds" 
                :key="index" 
                class="table-product-item-inline"
                :title="getTableProductTitle(productId)"
              >
                <el-image 
                  v-if="getProductMainImage(productId)" 
                  :src="getProductMainImage(productId)"
                  :preview-src-list="[getProductMainImage(productId)]"
                  class="table-product-thumb"
                  fit="cover"
                  :hide-on-click-modal="true"
                  preview-teleported
                />
                <div v-else class="table-product-thumb-placeholder">
                  <el-icon><Picture /></el-icon>
                </div>
                <div class="table-product-name">
                  {{ getTableProductTitle(productId) }}
                </div>
              </div>
            </div>
            <span v-else class="no-data">未关联商品</span>
          </template>
        </el-table-column>
        <el-table-column prop="sortOrder" label="排序" min-width="80" />
        <el-table-column prop="createdAt" label="创建时间" min-width="160" />
        <el-table-column prop="updatedAt" label="更新时间" min-width="160" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <el-button size="small" @click="showEditDialog(scope.row)">编辑</el-button>
            <el-button 
              size="small" 
              type="danger" 
              @click="deleteMenu(scope.row)"
              :disabled="scope.row.id <= 16"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
        </el-table>
      </el-card>
    </template>
    
    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
      @close="resetForm"
    >
      <el-form :model="currentMenu" :rules="rules" ref="menuForm" label-width="100px">
        <el-form-item label="中文名称" prop="name">
          <el-input v-model="currentMenu.name" placeholder="请输入中文名称" />
        </el-form-item>
        <el-form-item label="英文名称" prop="nameEn">
          <el-input v-model="currentMenu.nameEn" placeholder="请输入英文名称" />
        </el-form-item>
        <el-form-item label="位置" prop="position">
          <el-select v-model="currentMenu.position" placeholder="请选择位置" style="width: 100%;" @change="handlePositionChange">
            <el-option label="顶部菜单" value="header" />
            <el-option label="楼层菜单" value="floor" />
          </el-select>
        </el-form-item>
        <el-form-item label="链接" prop="link" v-if="currentMenu.position === 'header'">
          <el-input v-model="currentMenu.link" placeholder="请输入链接地址" :disabled="isEditMode" />
        </el-form-item>
        <el-form-item label="图标" prop="icon">
          <el-select 
            v-model="currentMenu.icon" 
            placeholder="请选择图标" 
            style="width: 100%;"
            popper-class="icon-select-popper"
          >
            <el-option label="无图标" :value="null" />
            <el-option
              v-for="icon in availableIcons"
              :key="icon.path"
              :label="icon.name"
              :value="icon.path"
            >
              <div class="icon-option">
                <img :src="icon.path" :alt="icon.name" class="option-icon" />
                <span>{{ icon.name }}</span>
              </div>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="排序" prop="sortOrder">
          <el-input-number v-model="currentMenu.sortOrder" :min="0" :max="9999" placeholder="请输入排序值" style="width: 100%;" />
        </el-form-item>
        <el-form-item label="商品ID" prop="productIds" v-if="currentMenu.position === 'floor'">
          <div class="product-selector-wrapper">
            <el-input
              v-model="productSearchInput"
              placeholder="请输入商品ID（输入后自动搜索）"
              class="product-search-input"
              @input="handleProductIdInput"
              clearable
            />
            <el-select
              v-if="searchedProducts.length > 0"
              v-model="selectedProductId"
              placeholder="请选择商品"
              class="product-select"
              @change="addProduct"
              clearable
            >
              <el-option
                v-for="product in searchedProducts"
                :key="product.id"
                :label="product.label"
                :value="product.id"
                class="product-option"
              >
                <div class="product-option-content">
                  <img 
                    v-if="product.thumbnailImage" 
                    :src="product.thumbnailImage" 
                    class="product-thumbnail"
                    @error="handleImageError"
                  />
                  <div v-else class="product-thumbnail-placeholder">
                    <el-icon><Picture /></el-icon>
                  </div>
                  <div class="product-info">
                    <div class="product-title" :title="product.title">{{ product.title }}</div>
                    <div class="product-meta">
                      <span class="product-id">ID: {{ product.id }}</span>
                      <span v-if="product.sku" class="product-sku">SKU: {{ product.sku }}</span>
                    </div>
                  </div>
                </div>
              </el-option>
            </el-select>
            <div v-if="currentMenu.productIds && currentMenu.productIds.length > 0" class="selected-products">
              <div class="selected-products-title">已选择的商品：</div>
              <div class="selected-products-grid">
                <div 
                  v-for="(productId, index) in currentMenu.productIds" 
                  :key="index"
                  class="selected-product-item-compact"
                >
                  <el-image 
                    v-if="productInfoMap[productId]?.mainImage" 
                    :src="productInfoMap[productId].mainImage"
                    :preview-src-list="[productInfoMap[productId].mainImage]"
                    class="compact-product-thumbnail"
                    fit="cover"
                    :hide-on-click-modal="true"
                    preview-teleported
                  />
                  <div v-else class="compact-product-thumbnail-placeholder">
                    <el-icon><Picture /></el-icon>
                  </div>
                  <div class="compact-product-info">
                    <div class="compact-product-title" :title="getProductFullTitle(productId)">
                      {{ getProductFullTitle(productId) }}
                    </div>
                    <div class="compact-product-id">ID: {{ productId }}</div>
                  </div>
                  <el-button 
                    type="danger" 
                    size="small" 
                    :icon="Close"
                    circle 
                    @click="removeProduct(index)"
                    class="compact-remove-btn"
                  />
                </div>
              </div>
            </div>
            <div class="form-item-tip">提示：楼层菜单最多可以选择10个商品，输入商品ID后自动搜索，从下拉列表中选择</div>
            <div v-if="currentMenu.productIds && currentMenu.productIds.length >= 10" class="form-item-warning">
              已达到最大数量限制（10个）
            </div>
          </div>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveMenu">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, defineExpose, defineProps } from 'vue'
import {
  ElCard,
  ElTable,
  ElTableColumn,
  ElButton,
  ElForm,
  ElFormItem,
  ElInput,
  ElInputNumber,
  ElSelect,
  ElOption,
  ElDialog,
  ElMessage,
  ElMessageBox,
  ElIcon,
  ElTag,
  ElImage,
  vLoading
} from 'element-plus'
import {
  Menu,
  Plus,
  Close,
  Picture
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
const groupedMenus = ref({})
const loading = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('新增菜单')
const isEditMode = ref(false) // 是否为编辑模式
const availableIcons = ref([])
const invalidProductIds = ref([]) // 存储无效的商品ID
const searchedProducts = ref([]) // 搜索到的商品列表
const searchLoading = ref(false) // 搜索加载状态
const productSearchInput = ref('') // 商品ID搜索输入
const selectedProductId = ref(null) // 当前选中的商品ID
const productInfoMap = ref({}) // 存储已选商品的信息
const tableProductInfoMap = ref({}) // 存储表格中显示的商品信息
const menuForm = ref(null) // 表单引用
let searchTimer = null // 搜索防抖定时器

// 定义固定的显示顺序：顶部菜单永远在上，楼层菜单永远在下
const orderedPositions = ['header', 'floor']

// 当前编辑的菜单
const currentMenu = ref({
  id: null,
  name: '',
  nameEn: '',
  position: '',
  link: '',
  icon: null,
  sortOrder: 0,
  productIds: []
})

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入中文名称', trigger: 'blur' }
  ],
  nameEn: [
    { required: true, message: '请输入英文名称', trigger: 'blur' }
  ],
  position: [
    { required: true, message: '请选择位置', trigger: 'change' }
  ],
  link: [
    { 
      required: true, 
      message: '请输入链接地址', 
      trigger: 'blur',
      validator: (rule, value, callback) => {
        if (currentMenu.value.position === 'header' && (!value || value.trim() === '')) {
          callback(new Error('请输入链接地址'))
        } else {
          callback()
        }
      }
    }
  ]
}

// 获取位置标题
const getPositionTitle = (position) => {
  const titles = {
    'header': '顶部菜单',
    'floor': '楼层菜单'
  }
  return titles[position] || position
}

// 处理位置变化
const handlePositionChange = (value) => {
  // 如果切换到楼层菜单，清空链接
  if (value === 'floor') {
    currentMenu.value.link = ''
  }
  // 清空搜索状态
  productSearchInput.value = ''
  selectedProductId.value = null
  searchedProducts.value = []
}

// 处理商品ID输入（防抖自动搜索）
const handleProductIdInput = (value) => {
  // 清除之前的定时器
  if (searchTimer) {
    clearTimeout(searchTimer)
  }
  
  // 如果输入为空，清空搜索结果
  if (!value || value.trim() === '') {
    searchedProducts.value = []
    return
  }
  
  // 设置防抖定时器（500毫秒）
  searchTimer = setTimeout(() => {
    searchProductById()
  }, 500)
}

// 根据商品ID搜索商品
// 根据商品ID搜索商品
const searchProductById = async () => {
  const productId = productSearchInput.value.trim()
  
  if (!productId) {
    searchedProducts.value = []
    return
  }
  
  // 检查是否为数字
  if (!/^\d+$/.test(productId)) {
    searchedProducts.value = []
    return
  }
  
  searchLoading.value = true
  try {
    const response = await fetch(`/admin${props.adminLoginPath}/product/detail/${productId}`, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    
    const result = await response.json()
    
    if (result.success && result.data) {
      const product = result.data
      
      // 检查商品状态是否为approved
      if (product.status !== 'approved') {
        ElMessage.warning('该商品未审核通过，无法添加')
        searchedProducts.value = []
        return
      }
      
      // 检查商品是否已经被添加
      if (currentMenu.value.productIds && currentMenu.value.productIds.includes(product.id)) {
        ElMessage.warning('该商品已经被添加')
        searchedProducts.value = []
        return
      }
      
      // 设置搜索结果
      searchedProducts.value = [{
        id: product.id,
        title: product.title,
        sku: product.sku,
        thumbnailImage: product.thumbnailImage || product.mainImage || '',
        mainImage: product.mainImage || product.thumbnailImage || '',
        label: `[ID:${product.id}] ${product.title} (SKU: ${product.sku || '-'})`
      }]
      
      // 存储商品信息供后续显示
      productInfoMap.value[product.id] = {
        id: product.id,
        title: product.title,
        sku: product.sku,
        thumbnailImage: product.thumbnailImage || product.mainImage || '',
        mainImage: product.mainImage || product.thumbnailImage || ''
      }
    } else {
      searchedProducts.value = []
    }
  } catch (error) {
    console.error('搜索商品失败:', error)
    searchedProducts.value = []
  } finally {
    searchLoading.value = false
  }
}

// 添加商品
const addProduct = () => {
  if (!selectedProductId.value) {
    return
  }
  
  // 检查是否超过最大数量
  if (currentMenu.value.productIds && currentMenu.value.productIds.length >= 10) {
    ElMessage.warning('最多只能添加10个商品')
    return
  }
  
  // 添加到已选列表
  if (!currentMenu.value.productIds) {
    currentMenu.value.productIds = []
  }
  
  currentMenu.value.productIds.push(selectedProductId.value)
  
  // 清空搜索状态
  productSearchInput.value = ''
  selectedProductId.value = null
  searchedProducts.value = []
  
  ElMessage.success('添加成功')
}

// 移除商品
const removeProduct = (index) => {
  currentMenu.value.productIds.splice(index, 1)
}

// 获取商品显示标签
const getProductLabel = (productId) => {
  const product = productInfoMap.value[productId]
  if (product) {
    return `[ID:${product.id}] ${product.title} (SKU: ${product.sku || '-'})`
  }
  return `ID: ${productId}`
}

// 获取商品完整标题
const getProductFullTitle = (productId) => {
  const product = productInfoMap.value[productId]
  if (product) {
    return product.title
  }
  return `商品 ${productId}`
}

// 处理图片加载错误
const handleImageError = (event) => {
  event.target.style.display = 'none'
}

// 加载已选商品的信息
const loadSelectedProductsInfo = async (productIds) => {
  if (!productIds || productIds.length === 0) {
    return
  }
  
  for (const productId of productIds) {
    if (!productInfoMap.value[productId]) {
      try {
        const response = await fetch(`/admin${props.adminLoginPath}/product/detail/${productId}`, {
          method: 'GET',
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          }
        })
        
        const result = await response.json()
        
        if (result.success && result.data) {
          const product = result.data
          productInfoMap.value[product.id] = {
            id: product.id,
            title: product.title,
            sku: product.sku,
            thumbnailImage: product.thumbnailImage || product.mainImage || '',
            mainImage: product.mainImage || product.thumbnailImage || ''
          }
        }
      } catch (error) {
        console.error(`加载商品${productId}信息失败:`, error)
      }
    }
  }
}

// 加载菜单数据
const loadMenuData = async () => {
  loading.value = true
  try {
    const url = `/admin${props.adminLoginPath}/horizontal-menu/list`
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    
    const result = await response.json()
    
    if (result.success) {
      groupedMenus.value = result.data
      // 立即隐藏loading，让表格先显示出来
      loading.value = false
      // 在后台异步加载商品图片信息，不阻塞页面显示
      loadAllProductsInfo()
    } else {
      ElMessage.error(result.message || '加载数据失败')
      loading.value = false
    }
  } catch (error) {
    ElMessage.error('加载数据失败: ' + error.message)
    loading.value = false
  }
}

// 加载所有商品信息用于表格显示
const loadAllProductsInfo = async () => {
  const allProductIds = new Set()
  
  // 收集所有楼层菜单的商品ID
  if (groupedMenus.value.floor) {
    groupedMenus.value.floor.forEach(menu => {
      if (menu.productIds && Array.isArray(menu.productIds)) {
        menu.productIds.forEach(id => allProductIds.add(id))
      }
    })
  }
  
  // 批量加载商品信息
  for (const productId of allProductIds) {
    if (!tableProductInfoMap.value[productId]) {
      try {
        const response = await fetch(`/admin${props.adminLoginPath}/product/detail/${productId}`, {
          method: 'GET',
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          }
        })
        
        const result = await response.json()
        
        if (result.success && result.data) {
          const product = result.data
          tableProductInfoMap.value[productId] = {
            id: product.id,
            title: product.title,
            thumbnailImage: product.thumbnailImage || product.mainImage || '',
            mainImage: product.mainImage || product.thumbnailImage || ''
          }
        }
      } catch (error) {
        console.error(`加载商品${productId}信息失败:`, error)
      }
    }
  }
}

// 获取表格中商品的缩略图
const getProductThumbnail = (productId) => {
  return tableProductInfoMap.value[productId]?.thumbnailImage || ''
}

// 获取表格中商品的主图
const getProductMainImage = (productId) => {
  return tableProductInfoMap.value[productId]?.mainImage || ''
}

// 获取表格中商品的标题
const getTableProductTitle = (productId) => {
  const product = tableProductInfoMap.value[productId]
  if (product) {
    return product.title
  }
  return `ID: ${productId}`
}

// 加载图标数据
const loadIcons = async () => {
  try {
    const url = `/admin${props.adminLoginPath}/horizontal-menu/icons`
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    
    const result = await response.json()
    
    if (result.success) {
      availableIcons.value = result.data
    } else {
      ElMessage.error(result.message || '加载图标失败')
    }
  } catch (error) {
    ElMessage.error('加载图标失败: ' + error.message)
  }
}

// 显示新增对话框
const showCreateDialog = () => {
  dialogTitle.value = '新增菜单'
  isEditMode.value = false // 新增模式
  currentMenu.value = {
    id: null,
    name: '',
    nameEn: '',
    position: '',
    link: '',
    icon: null,
    sortOrder: 0,
    productIds: []
  }
  dialogVisible.value = true
  // 确保图标数据已加载
  if (availableIcons.value.length === 0) {
    loadIcons()
  }
  // 清空搜索状态
  productSearchInput.value = ''
  selectedProductId.value = null
  searchedProducts.value = []
}

// 显示编辑对话框
const showEditDialog = async (menu) => {
  dialogTitle.value = '编辑菜单'
  isEditMode.value = true // 编辑模式
  currentMenu.value = { 
    ...menu,
    productIds: menu.productIds || []
  }
  dialogVisible.value = true
  // 确保图标数据已加载
  if (availableIcons.value.length === 0) {
    loadIcons()
  }
  // 清空搜索状态
  productSearchInput.value = ''
  selectedProductId.value = null
  searchedProducts.value = []
  
  // 加载已选商品的信息
  if (currentMenu.value.productIds && currentMenu.value.productIds.length > 0) {
    await loadSelectedProductsInfo(currentMenu.value.productIds)
  }
}

// 保存菜单
const saveMenu = async () => {
  // 验证表单
  if (!menuForm.value) {
    return
  }
  
  try {
    await menuForm.value.validate()
  } catch (error) {
    ElMessage.warning('请完善必填信息')
    return
  }
  
  try {
    let url, method
    if (currentMenu.value.id) {
      // 编辑
      url = `/admin${props.adminLoginPath}/horizontal-menu/${currentMenu.value.id}/update`
      method = 'POST'
    } else {
      // 新增
      url = `/admin${props.adminLoginPath}/horizontal-menu/create`
      method = 'POST'
    }
    
    const response = await fetch(url, {
      method: method,
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: JSON.stringify(currentMenu.value)
    })
    
    const result = await response.json()
    
    if (result.success) {
      ElMessage.success(result.message || '保存成功')
      dialogVisible.value = false
      loadMenuData() // 重新加载数据
    } else {
      ElMessage.error(result.message || '保存失败')
    }
  } catch (error) {
    ElMessage.error('保存失败: ' + error.message)
  }
}

// 删除菜单
const deleteMenu = (menu) => {
  ElMessageBox.confirm(
    `确定要删除菜单 "${menu.name}" 吗？`,
    '确认删除',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(async () => {
    try {
      const url = `/admin${props.adminLoginPath}/horizontal-menu/${menu.id}/delete`
      
      const response = await fetch(url, {
        method: 'DELETE',
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      
      const result = await response.json()
      
      if (result.success) {
        ElMessage.success(result.message || '删除成功')
        loadMenuData() // 重新加载数据
      } else {
        ElMessage.error(result.message || '删除失败')
      }
    } catch (error) {
      ElMessage.error('删除失败: ' + error.message)
    }
  }).catch(() => {
    // 用户取消删除
  })
}

// 重置表单
const resetForm = () => {
  currentMenu.value = {
    id: null,
    name: '',
    nameEn: '',
    position: '',
    link: '',
    icon: null,
    sortOrder: 0,
    productIds: []
  }
  invalidProductIds.value = [] // 清空无效商品ID列表
  productSearchInput.value = '' // 清空搜索输入
  selectedProductId.value = null // 清空选中的商品
  searchedProducts.value = [] // 清空搜索结果
}

// 组件挂载时加载数据
onMounted(() => {
  // 只有当 autoLoad 为 true 时才自动加载数据
  if (props.autoLoad) {
    loadMenuData()
    loadIcons()
  }
})

// 暴露方法给父组件调用
defineExpose({
  loadMenuData,
  loadIcons
})
</script>

<style scoped>
.horizontal-menu-container {
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

.menu-card {
  margin-bottom: 20px;
  width: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.position-title {
  font-size: 18px;
  font-weight: bold;
}

.menu-table {
  width: 100% !important;
  font-size: 14px;
}

.menu-table :deep(.el-table__header th) {
  background-color: #f5f7fa;
  color: #606266;
  font-weight: bold;
}

/* 解决鼠标悬停时序号列变色延迟的问题 */
.menu-table :deep(.el-table__body td) {
  transition: background-color 0.3s;
}

.menu-table :deep(.el-table__row:hover) {
  background-color: #f5f7fa;
}

.menu-table :deep(.el-table__row:hover td) {
  background-color: #f5f7fa !important;
}

/* 确保固定列也有一致的悬停效果 */
.menu-table :deep(.el-table__fixed .el-table__row:hover td) {
  background-color: #f5f7fa !important;
}

/* 确保序号列在悬停时立即响应 */
.menu-table :deep(.el-table__row:hover .el-table-fixed-column--left) {
  background-color: #f5f7fa !important;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.icon-preview {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.menu-icon {
  max-width: 30px;
  max-height: 30px;
  object-fit: contain;
}

.icon-option {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 30px;
}

.option-icon {
  width: 20px;
  height: 20px;
  object-fit: contain;
}

/* 确保下拉选项中的图标正确显示 */
:deep(.icon-select-popper) .el-select-dropdown__item {
  height: auto;
  padding: 5px 10px;
}

:deep(.el-select-dropdown__item.hover) {
  background-color: #f5f7fa;
}

.form-item-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
  line-height: 1.5;
}

.form-item-error {
  font-size: 12px;
  color: #f56c6c;
  margin-top: 5px;
  line-height: 1.5;
  font-weight: bold;
}

.form-item-warning {
  font-size: 12px;
  color: #e6a23c;
  margin-top: 5px;
  line-height: 1.5;
  font-weight: bold;
}

/* 商品选择器样式 */
.product-selector-wrapper {
  width: 100%;
}

.product-search-input {
  width: 100%;
  margin-bottom: 10px;
}

.product-select {
  width: 100%;
  margin-bottom: 10px;
}

/* 下拉选项样式 */
.product-option {
  height: auto !important;
  padding: 0 !important;
}

.product-option-content {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  width: 100%;
}

.product-thumbnail {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 4px;
  margin-right: 12px;
  flex-shrink: 0;
}

.product-thumbnail-placeholder {
  width: 50px;
  height: 50px;
  background-color: #f5f7fa;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  flex-shrink: 0;
  color: #909399;
  font-size: 24px;
}

.product-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.product-title {
  font-size: 14px;
  color: #303133;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-meta {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: #909399;
}

.product-id {
  color: #409eff;
}

.product-sku {
  color: #67c23a;
}

/* 已选商品列表样式 - 紧凑网格布局 */
.selected-products {
  margin-left: -100px;
  width: 470px;
  margin-top: 10px;
  padding: 12px;
  background-color: #f5f7fa;
  border-radius: 6px;
  box-sizing: border-box; /* 确保内边距不会超出 */
}

.selected-products-title {
  font-size: 13px;
  font-weight: 500;
  color: #606266;
  margin-bottom: 10px;
}

.selected-products-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

.selected-product-item-compact {
  display: flex;
  align-items: center;
  padding: 6px 8px;
  background-color: #ffffff;
  border-radius: 4px;
  border: 1px solid #e4e7ed;
  transition: all 0.3s;
  min-height: 50px;
  max-width: 220px;
}

.selected-product-item-compact:hover {
  border-color: #409eff;
  box-shadow: 0 2px 4px rgba(64, 158, 255, 0.1);
}

.compact-product-thumbnail {
  width: 40px;
  height: 40px;
  border-radius: 3px;
  margin-right: 8px;
  flex-shrink: 0;
  cursor: pointer;
}

.compact-product-thumbnail :deep(.el-image__inner) {
  width: 40px;
  height: 40px;
  object-fit: cover;
  border-radius: 3px;
}

.compact-product-thumbnail-placeholder {
  width: 40px;
  height: 40px;
  background-color: #f5f7fa;
  border-radius: 3px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 8px;
  flex-shrink: 0;
  color: #909399;
  font-size: 20px;
}

.compact-product-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.compact-product-title {
  font-size: 13px;
  color: #303133;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  line-height: 1.4;
}

.compact-product-id {
  font-size: 11px;
  color: #909399;
}

.compact-remove-btn {
  flex-shrink: 0;
  margin-left: 6px;
  width: 24px;
  height: 24px;
}

.compact-remove-btn :deep(.el-icon) {
  font-size: 12px;
}

.product-ids-display {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  align-items: center;
}

.product-id-tag {
  margin: 2px;
}

.no-data {
  color: #909399;
  font-size: 14px;
}

/* 表格中的商品显示 - 网格布局 */
.table-products-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 6px;
  padding: 4px;
}

.table-product-item-inline {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 6px;
  background-color: #f5f7fa;
  border-radius: 3px;
  transition: background-color 0.3s;
  min-height: 36px;
}

.table-product-item-inline:hover {
  background-color: #e4e7ed;
}

.table-product-thumb {
  width: 30px;
  height: 30px;
  border-radius: 3px;
  flex-shrink: 0;
  cursor: pointer;
}

.table-product-thumb :deep(.el-image__inner) {
  width: 30px;
  height: 30px;
  object-fit: cover;
  border-radius: 3px;
}

.table-product-thumb-placeholder {
  width: 30px;
  height: 30px;
  background-color: #ffffff;
  border-radius: 3px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: #909399;
  font-size: 16px;
}

.table-product-name {
  flex: 1;
  font-size: 12px;
  color: #606266;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  line-height: 1.3;
}

/* 链接文本样式 */
.link-text {
  color: #409eff;
  text-decoration: underline;
  cursor: pointer;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: block;
}
</style>