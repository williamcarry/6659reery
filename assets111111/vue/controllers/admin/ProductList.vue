<template>
  <div class="product-list" v-loading="loading" element-loading-text="数据加载中..." element-loading-background="rgba(255, 255, 255, 0.9)">
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="statistics-row" v-if="statistics">
      <el-col :span="4">
        <el-card class="stat-card">
          <div class="stat-number">{{ statistics.total }}</div>
          <div class="stat-label">全部商品</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card class="stat-card">
          <div class="stat-number pending">{{ statistics.pending }}</div>
          <div class="stat-label">待审核</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card class="stat-card">
          <div class="stat-number approved">{{ statistics.approved }}</div>
          <div class="stat-label">已通过</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card class="stat-card">
          <div class="stat-number rejected">{{ statistics.rejected }}</div>
          <div class="stat-label">已拒绝</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card class="stat-card">
          <div class="stat-number draft">{{ statistics.draft }}</div>
          <div class="stat-label">草稿</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card class="stat-card">
          <div class="stat-number offline">{{ statistics.offline }}</div>
          <div class="stat-label">已下架</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 搜索和筛选 -->
    <el-card class="search-card">
      <el-form :model="searchParams" inline>
        <el-form-item label="关键词">
          <el-input
            v-model="searchParams.keyword"
            placeholder="ID/SKU/SPU/商品名称/标签"
            clearable
            style="width: 250px"
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        
        <el-form-item label="状态">
          <el-select v-model="searchParams.status" placeholder="全部" clearable style="width: 120px">
            <el-option label="全部" value="" />
            <el-option label="草稿" value="draft" />
            <el-option label="待审核" value="pending" />
            <el-option label="已通过" value="approved" />
            <el-option label="已拒绝" value="rejected" />
            <el-option label="已下架" value="offline" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="供应商用户名">
          <el-input
            v-model="searchParams.supplierUsername"
            placeholder="请输入供应商用户名"
            clearable
            style="width: 200px"
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><User /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleSearch" :loading="searching">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 操作栏 -->
    <el-card class="operation-card">
      <el-button type="success" :disabled="selectedIds.length === 0" @click="handleBatchAudit('approved')">
        批量通过
      </el-button>
      <el-button type="danger" :disabled="selectedIds.length === 0" @click="handleBatchAudit('rejected')">
        批量拒绝
      </el-button>
      <el-button type="primary" :disabled="selectedIds.length === 0" @click="showBatchTagDialog('add')">
        <el-icon><Plus /></el-icon>
        批量添加标签
      </el-button>
      <el-button type="warning" :disabled="selectedIds.length === 0" @click="showBatchTagDialog('remove')">
        <el-icon><Delete /></el-icon>
        批量删除标签
      </el-button>
      <el-button @click="handleRefresh">
        <el-icon><Refresh /></el-icon>
        刷新
      </el-button>
    </el-card>

    <!-- 商品列表表格 -->
    <el-card class="table-card">
      <el-table
        :data="products"
        @selection-change="handleSelectionChange"
        style="width: 100%; margin-top: 20px;"
        :fit="true"
        :border="true"
        :stripe="true"
        :header-cell-style="{ textAlign: 'center', backgroundColor: '#f5f7fa' }"
        :cell-style="{ textAlign: 'center' }"
      >
        <el-table-column type="selection" width="55" />
        
        <el-table-column label="序号" width="70">
          <template #default="scope">
            {{ (pagination.currentPage - 1) * pagination.itemsPerPage + scope.$index + 1 }}
          </template>
        </el-table-column>
        
        <el-table-column label="商品ID" width="100" prop="id" />
        
        <el-table-column label="供应商" width="150">
          <template #default="scope">
            <span 
              v-if="scope.row.supplier" 
              class="supplier-info"
              :title="`${scope.row.supplier.username}/${scope.row.supplier.companyName || '-'}`"
            >
              {{ formatSupplierInfo(scope.row.supplier) }}
            </span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        
        <el-table-column label="商品图片" width="100">
          <template #default="scope">
            <el-image
              v-if="scope.row.mainImageUrl"
              :src="scope.row.mainImageUrl"
              fit="cover"
              style="width: 60px; height: 60px; border-radius: 4px"
              :preview-src-list="[scope.row.mainImageUrl]"
              preview-teleported
            />
            <span v-else>无图片</span>
          </template>
        </el-table-column>
        
        <el-table-column label="SKU/SPU" min-width="200">
          <template #default="scope">
            <div>
              <div>SKU: {{ scope.row.sku || '-' }}</div>
              <div>SPU: {{ scope.row.spu || '-' }}</div>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="title" label="商品名称" min-width="200" show-overflow-tooltip />
        
        <el-table-column label="标签" min-width="150">
          <template #default="scope">
            <div v-if="scope.row.tags && scope.row.tags.length > 0" class="tags-container">
              <el-tag
                v-for="(tag, index) in scope.row.tags"
                :key="index"
                size="small"
                style="margin-right: 5px; margin-bottom: 3px;"
              >
                {{ tag }}
              </el-tag>
            </div>
            <span v-else class="no-tags">-</span>
          </template>
        </el-table-column>
        
        <el-table-column label="发货区域" min-width="150">
          <template #default="scope">
            <template v-if="scope && scope.row && scope.row.shippingRegions && scope.row.shippingRegions.length > 0">
              <el-tag
                v-for="(region, index) in scope.row.shippingRegions"
                :key="index"
                type="success"
                size="small"
                style="margin-right: 5px; margin-bottom: 3px;"
              >
                {{ region }}
              </el-tag>
            </template>
            <template v-else>
              <span>-</span>
            </template>
          </template>
        </el-table-column>
        
        <el-table-column label="是否限量" width="100" align="center">
          <template #default="scope">
            <el-tag v-if="scope.row.isLimited" type="danger" size="small">限量</el-tag>
            <el-tag v-else type="info" size="small">不限量</el-tag>
          </template>
        </el-table-column>
        
        <el-table-column label="分类" width="120">
          <template #default="scope">
            {{ scope.row.category || '-' }}
          </template>
        </el-table-column>
        
        <el-table-column label="多区域价格" min-width="150">
          <template #default="scope">
            <el-popover
              v-if="scope && scope.row && scope.row.shippingRegions && scope.row.shippingRegions.length > 0"
              placement="left"
              :width="300"
              trigger="hover"
            >
              <template #reference>
                <el-button type="primary" size="small" text>
                  {{ scope.row.shippingRegions.length }}个区域 👁️
                </el-button>
              </template>
              <div class="region-price-popover">
                <div 
                  v-for="region in scope.row.shippingRegions" 
                  :key="region"
                  class="region-price-item"
                >
                  <div class="region-name">
                    <el-tag type="success" size="small">{{ getRegionLabel(region) }}</el-tag>
                  </div>
                  <div class="region-info">
                    <div>💰 原价：{{ getRegionCurrencySymbol(region) }}{{ formatPrice(scope.row.regionConfigs?.[region]?.price?.originalPrice) }}</div>
                    <div>💵 售价：{{ getRegionCurrencySymbol(region) }}{{ formatPrice(scope.row.regionConfigs?.[region]?.price?.sellingPrice) }}</div>
                    <div v-if="scope.row.regionConfigs?.[region]?.price?.discountRate" class="discount-info">
                      🏷️ 商品折扣：{{ (parseFloat(scope.row.regionConfigs[region].price.discountRate) * 100).toFixed(0) }}%
                    </div>
                    <div class="member-discount-section">
                      <div>👥 会员折扣：</div>
                      <div class="member-discount-detail">{{ formatMemberDiscount(scope.row.regionConfigs?.[region]?.price?.memberDiscount) }}</div>
                    </div>
                    <div class="member-prices-section">
                      <div>💳 会员价：</div>
                      <div class="member-prices-detail">{{ formatMemberPrices(scope.row.regionConfigs?.[region]?.price, region) }}</div>
                    </div>
                    <div>🎁 满减：{{ formatDiscountRule(scope.row.regionConfigs?.[region]?.discountRule, region) }}</div>
                    <div>🚚 运费：{{ getRegionCurrencySymbol(region) }}{{ formatPrice(scope.row.regionConfigs?.[region]?.shipping?.shippingPrice) }}</div>
                  </div>
                </div>
                <div class="popover-tip">
                  <el-icon><InfoFilled /></el-icon>
                  点击"查看"了解详细价格配置
                </div>
              </div>
            </el-popover>
            <span v-else>-</span>
          </template>
        </el-table-column>
        
        <el-table-column label="满减活动" min-width="120">
          <template #default="scope">
            <div v-if="scope.row.enableDiscount === true || scope.row.enableDiscount === 1" class="discount-info">
              <el-tag type="success" size="small">已启用</el-tag>
              <div class="discount-details">
                满{{ scope.row.minAmount }}减{{ scope.row.discountAmount }}
              </div>
            </div>
            <el-tag v-else type="info" size="small">未启用</el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="brand" label="品牌" width="100" />
        
        <el-table-column label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusTagType(scope.row.status)">
              {{ scope.row.statusText }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="salesCount" label="销量" width="80" align="center" />
        
        <el-table-column prop="createdAt" label="创建时间" width="160" />
        
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="scope">
            <div class="button-group">
              <el-button
                v-if="scope.row.status === 'pending'"
                type="success"
                size="small"
                @click="handleAudit(scope.row, 'approved')"
              >
                通过
              </el-button>
              <el-button
                v-if="scope.row.status === 'pending'"
                type="warning"
                size="small"
                @click="handleAudit(scope.row, 'rejected')"
              >
                拒绝
              </el-button>
              <el-button
                size="small"
                @click="handleView(scope.row)"
              >
                查看
              </el-button>
              <el-button
                type="danger"
                size="small"
                @click="handleDelete(scope.row)"
              >
                删除
              </el-button>
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

    <!-- 批量修改标签对话框 -->
    <el-dialog v-model="batchTagDialogVisible" :title="batchTagAction === 'add' ? '批量添加标签' : '批量删除标签'" width="600px">
      <el-form :model="batchTagForm" label-width="100px">
        <el-form-item :label="batchTagAction === 'add' ? '添加标签' : '删除标签'">
          <el-select
            v-model="batchTagForm.tags"
            multiple
            filterable
            allow-create
            default-first-option
            :reserve-keyword="false"
            placeholder="请选择或输入标签"
            style="width: 100%"
          >
            <el-option
              v-for="tag in defaultTags"
              :key="tag"
              :label="tag"
              :value="tag"
            />
          </el-select>
          <div class="form-tip">
            默认标签：{{ defaultTags.length > 0 ? defaultTags.join('、') : '暂无' }}<br/>
            可从默认标签中选择，也可手动输入自定义标签，按回车键添加
          </div>
        </el-form-item>
        <el-form-item label="选中商品">
          <el-tag type="info">{{ selectedIds.length }} 个商品</el-tag>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="batchTagDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmBatchTag" :loading="batchTagProcessing">
          {{ batchTagAction === 'add' ? '添加' : '删除' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- 审核对话框 -->
    <el-dialog v-model="auditDialogVisible" title="审核商品" width="500px">
      <el-form :model="auditForm" label-width="100px">
        <el-form-item label="审核结果">
          <el-radio-group v-model="auditForm.status">
            <el-radio label="approved">通过</el-radio>
            <el-radio label="rejected">拒绝</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="审核备注">
          <el-input
            v-model="auditForm.remark"
            type="textarea"
            :rows="4"
            placeholder="请输入审核备注（选填）"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="auditDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmAudit" :loading="auditing">确定</el-button>
      </template>
    </el-dialog>

    <!-- 查看商品详情对话框 -->
    <el-dialog v-model="viewDialogVisible" title="商品详情" width="800px">
      <el-descriptions v-if="currentProduct" :column="2" border>
        <el-descriptions-item label="SKU">{{ currentProduct.sku }}</el-descriptions-item>
        <el-descriptions-item label="SPU">{{ currentProduct.spu }}</el-descriptions-item>
        <el-descriptions-item label="商品名称">{{ currentProduct.title }}</el-descriptions-item>
        <el-descriptions-item label="英文名称">{{ currentProduct.titleEn || '-' }}</el-descriptions-item>
        <el-descriptions-item label="供应商">
          {{ currentProduct.supplier?.companyName || currentProduct.supplier?.username || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="品牌">{{ currentProduct.brand || '-' }}</el-descriptions-item>
        <el-descriptions-item label="分类">{{ currentProduct.category || '-' }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusTagType(currentProduct.status)">
            {{ currentProduct.statusText }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="浏览量">{{ currentProduct.viewCount }}</el-descriptions-item>
        <el-descriptions-item label="销量">{{ currentProduct.salesCount }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ currentProduct.createdAt }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ currentProduct.updatedAt }}</el-descriptions-item>
        <el-descriptions-item label="审核备注">{{ currentProduct.auditRemark || '-' }}</el-descriptions-item>
        <el-descriptions-item label="审核人">{{ currentProduct.auditedBy || '-' }}</el-descriptions-item>
        <el-descriptions-item label="审核时间">{{ currentProduct.auditedAt || '-' }}</el-descriptions-item>
        <el-descriptions-item label="首次上架时间">{{ currentProduct.publishDate || '-' }}</el-descriptions-item>
        <el-descriptions-item label="商品图片" :span="2">
          <el-image
            v-if="currentProduct.mainImages && currentProduct.mainImages.length > 0"
            :src="currentProduct.mainImages[0].url"
            fit="contain"
            style="max-width: 200px; max-height: 200px"
            :preview-src-list="currentProduct.mainImages.map(img => img.url)"
            preview-teleported
          />
          <el-image
            v-else-if="currentProduct.mainImage"
            :src="currentProduct.mainImage"
            fit="contain"
            style="max-width: 200px; max-height: 200px"
            :preview-src-list="[currentProduct.mainImage]"
            preview-teleported
          />
          <span v-else>无图片</span>
        </el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <el-button @click="viewDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, defineProps, defineExpose } from 'vue'
import {
  ElCard,
  ElRow,
  ElCol,
  ElForm,
  ElFormItem,
  ElInput,
  ElSelect,
  ElOption,
  ElButton,
  ElTable,
  ElTableColumn,
  ElPagination,
  ElImage,
  ElTag,
  ElDialog,
  ElRadioGroup,
  ElRadio,
  ElDescriptions,
  ElDescriptionsItem,
  ElMessage,
  ElMessageBox,
  ElIcon,
  ElPopover,
  vLoading
} from 'element-plus'
import { Search, Refresh, User, Plus, Delete, InfoFilled } from '@element-plus/icons-vue'

const props = defineProps({
  adminLoginPath: {
    type: String,
    required: true
  },
  autoLoad: {
    type: Boolean,
    default: false
  }
})

const loading = ref(false)
const searching = ref(false)
const products = ref([])
const statistics = ref(null)
const suppliers = ref([])
const selectedIds = ref([])
const auditDialogVisible = ref(false)
const viewDialogVisible = ref(false)
const auditing = ref(false)
const currentProduct = ref(null)
const siteCurrency = ref('USD') // 网站币种代码，默认USD
const siteCurrencySymbol = ref('$') // 网站货币符号，默认为$

// 批量标签相关
const batchTagDialogVisible = ref(false)
const batchTagAction = ref('add') // 'add' 或 'remove'
const batchTagProcessing = ref(false)
const defaultTags = ref([]) // 默认标签列表
const batchTagForm = reactive({
  tags: []
})

// 搜索参数
const searchParams = reactive({
  keyword: '',
  status: '',
  supplierUsername: '', // 供应商用户名搜索字段
  sortField: 'createdAt',
  sortOrder: 'DESC'
})

// 分页数据
const pagination = reactive({
  currentPage: 1,
  totalPages: 1,
  totalItems: 0,
  itemsPerPage: 20
})

// 审核表单
const auditForm = reactive({
  productId: null,
  status: 'approved',
  remark: ''
})

// 搜索
const handleSearch = () => {
  pagination.currentPage = 1
  loadProductData()
}

// 重置
const handleReset = () => {
  searchParams.keyword = ''
  searchParams.status = ''
  searchParams.supplierUsername = ''
  searchParams.sortField = 'createdAt'
  searchParams.sortOrder = 'DESC'
  pagination.currentPage = 1
  loadProductData()
}

// 加载商品数据
const loadProductData = async (page = 1, limit = 20) => {
  // 确保区域选项已加载（按需加载时也会请求）
  if (regionOptions.length === 0) {
    await loadRegionOptions()
  }
  
  // 如果是搜索操作，显示搜索按钮的loading状态
  if (page === 1 && searchParams.keyword || searchParams.status || searchParams.supplierUsername) {
    searching.value = true
  }
  
  loading.value = true
  try {
    // 构建查询参数
    const params = new URLSearchParams({
      page: page,
      limit: limit,
      keyword: searchParams.keyword,
      status: searchParams.status,
      sortField: searchParams.sortField,
      sortOrder: searchParams.sortOrder
    })

    // 如果供应商用户名不为空，则添加到参数中
    if (searchParams.supplierUsername !== '') {
      params.append('supplierUsername', searchParams.supplierUsername)
    }

    const url = `/admin${props.adminLoginPath}/product/list/data?${params}`

    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })

    const result = await response.json()

    if (result.success) {
      products.value = result.data
      pagination.currentPage = result.pagination.currentPage
      pagination.totalPages = result.pagination.totalPages
      pagination.totalItems = result.pagination.totalItems
      pagination.itemsPerPage = result.pagination.itemsPerPage
      
      // 更新网站币种和货币符号
      if (result.siteCurrency) {
        siteCurrency.value = result.siteCurrency
      }
      if (result.currencySymbol) {
        siteCurrencySymbol.value = result.currencySymbol
      }
      
      // 立即隐藏loading，让表格先显示出来
      loading.value = false
      searching.value = false
    } else {
      ElMessage.error(result.message || '加载数据失败')
      loading.value = false
      searching.value = false
    }
  } catch (error) {
    console.error('加载数据失败:', error)
    ElMessage.error('网络错误，请稍后重试')
    loading.value = false
    searching.value = false
  }
}

// 加载统计数据
const loadStatistics = async () => {
  try {
    const response = await fetch(`/admin${props.adminLoginPath}/product/statistics`, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })

    const result = await response.json()

    if (result.success) {
      statistics.value = result.data
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

// 加载供应商列表
const loadSuppliers = async () => {
  try {
    const response = await fetch(`/admin${props.adminLoginPath}/product/suppliers`, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })

    const result = await response.json()

    if (result.success) {
      suppliers.value = result.data
    }
  } catch (error) {
    console.error('加载供应商列表失败:', error)
  }
}

// 刷新
const handleRefresh = () => {
  loadProductData(pagination.currentPage, pagination.itemsPerPage)
  loadStatistics()
}

// 分页大小改变
const handleSizeChange = (val) => {
  pagination.itemsPerPage = val
  loadProductData(pagination.currentPage, val)
}

// 当前页改变
const handleCurrentChange = (val) => {
  pagination.currentPage = val
  loadProductData(val, pagination.itemsPerPage)
}

// 选择改变
const handleSelectionChange = (selection) => {
  selectedIds.value = selection.map(item => item.id)
}

// 审核商品
const handleAudit = (product, status) => {
  auditForm.productId = product.id
  auditForm.status = status
  auditForm.remark = ''
  auditDialogVisible.value = true
}

// 确认审核
const confirmAudit = async () => {
  auditing.value = true
  try {
    const response = await fetch(`/admin${props.adminLoginPath}/product/audit/${auditForm.productId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: JSON.stringify({
        status: auditForm.status,
        remark: auditForm.remark
      })
    })

    const result = await response.json()

    if (result.success) {
      ElMessage.success(result.message)
      auditDialogVisible.value = false
      loadProductData(pagination.currentPage, pagination.itemsPerPage)
      loadStatistics()
    } else {
      ElMessage.error(result.message || '审核失败')
    }
  } catch (error) {
    console.error('审核失败:', error)
    ElMessage.error('网络错误，请稍后重试')
  } finally {
    auditing.value = false
  }
}

// 批量审核
const handleBatchAudit = async (status) => {
  if (selectedIds.value.length === 0) {
    ElMessage.warning('请选择要审核的商品')
    return
  }

  const statusText = status === 'approved' ? '通过' : '拒绝'
  
  try {
    await ElMessageBox.confirm(
      `确定要批量${statusText}选中的 ${selectedIds.value.length} 个商品吗？`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    const response = await fetch(`/admin${props.adminLoginPath}/product/batch-audit`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: JSON.stringify({
        ids: selectedIds.value,
        status: status
      })
    })

    const result = await response.json()

    if (result.success) {
      ElMessage.success(result.message)
      selectedIds.value = []
      loadProductData(pagination.currentPage, pagination.itemsPerPage)
      loadStatistics()
    } else {
      ElMessage.error(result.message || '批量审核失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('批量审核失败:', error)
      ElMessage.error('网络错误，请稍后重试')
    }
  }
}

// 查看商品
const handleView = (product) => {
  // 触发导航事件，在新标签页中打开商品详情
  window.dispatchEvent(new CustomEvent('navigate-to-product-view', {
    detail: { productId: product.id }
  }))
}

// 删除商品
const handleDelete = async (product) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除商品 "${product.title}" 吗？此操作不可恢复！`,
      '警告',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'error'
      }
    )

    const response = await fetch(`/admin${props.adminLoginPath}/product/delete/${product.id}`, {
      method: 'POST',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })

    const result = await response.json()

    if (result.success) {
      ElMessage.success(result.message)
      loadProductData(pagination.currentPage, pagination.itemsPerPage)
      loadStatistics()
    } else {
      ElMessage.error(result.message || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('网络错误，请稍后重试')
    }
  }
}

// 获取状态标签类型
const getStatusTagType = (status) => {
  const typeMap = {
    'draft': 'info',
    'pending': 'warning',
    'approved': 'success',
    'rejected': 'danger',
    'offline': ''
  }
  return typeMap[status] || 'info'
}

// 从枚举类获取区域信息
let regionOptions = []

const loadRegionOptions = async () => {
  try {
    const response = await fetch(`/admin${props.adminLoginPath}/product/shipping-regions`, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    const result = await response.json()
    if (result.success) {
      regionOptions = result.data
    }
  } catch (error) {
    console.error('获取区域选项失败:', error)
  }
}

// 获取区域对应的币种符号
const getRegionCurrencySymbol = (region) => {
  if (regionOptions.length > 0) {
    const option = regionOptions.find(r => r.value === region)
    return option?.currencySymbol || siteCurrencySymbol.value
  }
  // 如果没有区域配置，使用网站默认货币符号
  return siteCurrencySymbol.value
}

// 获取区域显示标签
const getRegionLabel = (region) => {
  const flagMap = {
    'CN': '🇨🇳',
    'US': '🇺🇸',
    'UK': '🇬🇧',
    'PR': '🇵🇷'
  }
  
  if (regionOptions.length > 0) {
    const option = regionOptions.find(r => r.value === region)
    return option ? `${flagMap[region] || ''} ${option.label}` : region
  }
  // 后备方案
  const labelMap = {
    'CN': '🇨🇳 中国大陆',
    'US': '🇺🇸 美国',
    'UK': '🇬🇧 英国',
    'PR': '🇵🇷 欧洲'
  }
  return labelMap[region] || region
}

// 格式化满减规则显示
const formatDiscountRule = (discountRule, region) => {
  if (!discountRule || !discountRule.minAmount || !discountRule.discountAmount) {
    return '未配置'
  }
  const symbol = getRegionCurrencySymbol(region)
  const minAmount = parseFloat(discountRule.minAmount).toFixed(2)
  const discountAmount = parseFloat(discountRule.discountAmount).toFixed(2)
  return `满${symbol}${minAmount}减${symbol}${discountAmount}`
}

// 格式化价格显示（两位小数）
const formatPrice = (price) => {
  if (price === null || price === undefined || price === '' || price === '--') {
    return '--'
  }
  const numPrice = parseFloat(price)
  if (isNaN(numPrice)) {
    return '--'
  }
  return numPrice.toFixed(2)
}

// 格式化会员折扣后价格显示
const formatMemberPrices = (priceConfig, region) => {
  if (!priceConfig || !priceConfig.sellingPrice) {
    return '未配置'
  }
  
  const sellingPrice = parseFloat(priceConfig.sellingPrice)
  
  if (isNaN(sellingPrice) || sellingPrice <= 0) {
    return '未配置'
  }
  
  // 获取商品折扣率
  const productDiscountRate = parseFloat(priceConfig.discountRate) || 0
  
  const memberDiscount = priceConfig.memberDiscount
  
  // 会员等级名称（根据VipLevel.php定义）
  const vipLabels = [
    '普通用户',  // 索圕0
    'VIP1',      // 索圕1
    'VIP2',      // 索圕2
    'VIP3',      // 索圕3
    'VIP4',      // 索圕4
    'VIP5'       // 索圕5
  ]
  
  const symbol = getRegionCurrencySymbol(region)
  const prices = []
  
  // 如果没有配置会员折扣，所有会员等级都显示售价
  if (!Array.isArray(memberDiscount)) {
    return `所有会员:${symbol}${sellingPrice.toFixed(2)}`
  }
  
  // 遍历数组，计算每个会员等级的价格
  memberDiscount.forEach((discount, index) => {
    if (index < vipLabels.length) {
      const memberDiscountRate = parseFloat(discount) || 0
      // 正确计算：会员价 = 售价 - (售价 × 会员折扣率)
      const memberPrice = sellingPrice - (sellingPrice * memberDiscountRate)
      prices.push(`${vipLabels[index]}:${symbol}${memberPrice.toFixed(2)}`)
    }
  })
  
  return prices.length > 0 ? prices.join(', ') : `所有会员:${symbol}${sellingPrice.toFixed(2)}`
}

// 格式化会员折扣显示
const formatMemberDiscount = (memberDiscount) => {
  if (!Array.isArray(memberDiscount)) {
    return '未配置'
  }
  
  const vipLabels = ['普通用户', 'VIP1', 'VIP2', 'VIP3', 'VIP4', 'VIP5']
  const discounts = []
  
  memberDiscount.forEach((discount, index) => {
    if (index < vipLabels.length) {
      const discountValue = parseFloat(discount) || 0
      const percentage = (discountValue * 100).toFixed(1)
      discounts.push(`${vipLabels[index]}:${percentage}%`)
    }
  })
  
  return discounts.length > 0 ? discounts.join(', ') : '未配置'
}

// 格式化供应商信息显示
const formatSupplierInfo = (supplier) => {
  if (!supplier) return '-';
  
  const username = supplier.username || '';
  const companyName = supplier.companyName || '';
  
  // 如果公司名称为空，只显示用户名
  if (!companyName) {
    return truncateText(username, 20);
  }
  
  // 组合显示 username/companyName
  const combined = `${username}/${companyName}`;
  return truncateText(combined, 20);
};

// 截断文本并添加省略号
const truncateText = (text, maxLength) => {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};

// 初始化数据加载
const initData = () => {
  loadProductData()
  loadStatistics()
  loadSuppliers()
  loadDefaultTags()
}

// 加载默认标签
const loadDefaultTags = async () => {
  try {
    const response = await fetch(`/admin${props.adminLoginPath}/product/tags`, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })

    const result = await response.json()

    if (result.success) {
      defaultTags.value = result.data || []
      console.log('加载默认标签成功:', defaultTags.value)
    } else {
      console.error('加载默认标签失败:', result.message)
    }
  } catch (error) {
    console.error('加载默认标签失败:', error)
  }
}

// 显示批量标签对话框
const showBatchTagDialog = async (action) => {
  batchTagAction.value = action
  batchTagForm.tags = []
  
  // 如果默认标签为空，先加载
  if (defaultTags.value.length === 0) {
    await loadDefaultTags()
  }
  
  batchTagDialogVisible.value = true
}

// 确认批量修改标签
const confirmBatchTag = async () => {
  if (batchTagForm.tags.length === 0) {
    ElMessage.warning('请至少选择或输入一个标签')
    return
  }

  if (selectedIds.value.length === 0) {
    ElMessage.warning('请选择要修改的商品')
    return
  }

  batchTagProcessing.value = true
  try {
    const response = await fetch(`/admin${props.adminLoginPath}/product/batch-tags`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: JSON.stringify({
        productIds: selectedIds.value,
        tags: batchTagForm.tags,
        action: batchTagAction.value
      })
    })

    const result = await response.json()

    if (result.success) {
      ElMessage.success(result.message)
      batchTagDialogVisible.value = false
      loadProductData(pagination.currentPage, pagination.itemsPerPage)
    } else {
      ElMessage.error(result.message || '操作失败')
    }
  } catch (error) {
    console.error('批量修改标签失败:', error)
    ElMessage.error('网络错误，请稍后重试')
  } finally {
    batchTagProcessing.value = false
  }
}

// 暴露方法给父组件
defineExpose({
  loadProductData,
  loadStatistics,
  initData
})

// 组件挂载时
onMounted(() => {
  if (props.autoLoad) {
    initData()
  }
})
</script>

<style scoped>
.statistics-row {
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 8px;
}

.stat-number.pending {
  color: #e6a23c;
}

.stat-number.approved {
  color: #67c23a;
}

.stat-number.rejected {
  color: #f56c6c;
}

.stat-number.draft {
  color: #909399;
}

.stat-number.offline {
  color: #909399;
}

.stat-label {
  font-size: 14px;
  color: #606266;
}

.search-card,
.operation-card,
.table-card {
  margin-bottom: 20px;
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

.supplier-info {
  display: inline-block;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  vertical-align: middle;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 3px;
  align-items: center;
  justify-content: center;
}

.no-tags {
  color: #909399;
  font-size: 14px;
}

.form-tip {
  margin-top: 8px;
  font-size: 12px;
  color: #909399;
  line-height: 1.5;
}

.discount-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.discount-details {
  font-size: 12px;
  color: #606266;
  margin-top: 3px;
}

/* 区域价格弹窗样式 */
.region-price-popover {
  max-height: 600px;
  overflow-y: auto;
}

.region-price-item {
  padding: 15px;
  border-bottom: 1px solid #ebeef5;
}

.region-price-item:last-child {
  border-bottom: none;
}

.region-name {
  margin-bottom: 10px;
  font-weight: 600;
}

.region-info {
  font-size: 13px;
  line-height: 1.8;
}

.region-info > div {
  margin-bottom: 5px;
}

.member-discount-section,
.member-prices-section {
  padding-left: 10px;
  margin-top: 5px;
  border-left: 2px solid #409eff;
}

.member-discount-detail,
.member-prices-detail {
  font-size: 12px;
  color: #606266;
  margin-top: 3px;
  word-break: break-word;
}

.popover-tip {
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid #ebeef5;
  font-size: 12px;
  color: #909399;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
}
</style>
