<template>
  <div class="product-list-container" v-loading="loading" element-loading-text="数据加载中..." element-loading-background="rgba(255, 255, 255, 0.9)">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span class="header-title">商品列表</span>
          <div class="header-actions">
            <el-tooltip 
              v-if="!canAddProduct" 
              :content="getAddProductTooltip()" 
              placement="left"
            >
              <span>
                <el-button type="primary" disabled>添加商品</el-button>
              </span>
            </el-tooltip>
            <el-button v-else type="primary" @click="navigateToAdd">添加商品</el-button>
          </div>
        </div>
      </template>

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
            <div class="stat-number draft">{{ statistics.draft }}</div>
            <div class="stat-label">草稿</div>
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
            <div class="stat-label">已上架</div>
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
            <div class="stat-number offline">{{ statistics.offline }}</div>
            <div class="stat-label">已下架</div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 搜索筛选栏 -->
      <div class="search-bar">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-input
              v-model="searchParams.keyword"
              placeholder="搜索ID/SKU/SPU/商品名称/标签"
              clearable
              @keyup.enter="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </el-col>
          <el-col :span="4">
            <el-select v-model="searchParams.status" placeholder="商品状态" clearable>
              <el-option label="全部状态" value="" />
              <el-option label="草稿" value="draft" />
              <el-option label="待审核" value="pending" />
              <el-option label="已上架" value="approved" />
              <el-option label="已拒绝" value="rejected" />
              <el-option label="已下架" value="offline" />
            </el-select>
          </el-col>
          <el-col :span="4">
            <el-select v-model="searchParams.isNew" placeholder="是否新品" clearable>
              <el-option label="全部" value="" />
              <el-option label="新品" :value="true" />
              <el-option label="非新品" :value="false" />
            </el-select>
          </el-col>
          <el-col :span="4">
            <el-select v-model="searchParams.isHot" placeholder="是否热卖" clearable>
              <el-option label="全部" value="" />
              <el-option label="热卖" :value="true" />
              <el-option label="非热卖" :value="false" />
            </el-select>
          </el-col>
          <el-col :span="6">
            <el-button type="primary" @click="handleSearch" :loading="searching">搜索</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-col>
        </el-row>
      </div>

      <!-- 商品表格 -->
      <el-table
        :data="products"
        style="width: 100%; margin-top: 20px;"
        :fit="true"
        :border="true"
        :stripe="true"
        :header-cell-style="{ textAlign: 'center', backgroundColor: '#f5f7fa' }"
        :cell-style="{ textAlign: 'center' }"
      >
        <el-table-column prop="id" label="ID" min-width="80" />
        <el-table-column label="商品图片" min-width="120">
          <template #default="scope">
            <el-image
              v-if="scope && scope.row && scope.row.mainImageUrl"
              :src="scope.row.mainImageUrl"
              :preview-src-list="[scope.row.mainImageUrl]"
              :preview-teleported="true"
              fit="cover"
              style="width: 80px; height: 80px; cursor: pointer;"
            />
            <span v-else class="no-image">暂无图片</span>
          </template>
        </el-table-column>
        <el-table-column label="SKU/SPU" min-width="200" show-overflow-tooltip>
          <template #default="scope">
            <div>
              <div>SKU: {{ scope.row.sku || '-' }}</div>
              <div>SPU: {{ scope.row.spu || '-' }}</div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="title" label="商品名称" min-width="200" show-overflow-tooltip />
        <el-table-column label="分类" min-width="150">
          <template #default="scope">
            {{ (scope && scope.row && scope.row.category) || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="状态" min-width="100">
          <template #default="scope">
            <el-tag v-if="scope && scope.row" :type="getStatusType(scope.row.status)">
              {{ scope.row.statusText }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="标签" min-width="150">
          <template #default="scope">
            <template v-if="scope && scope.row && scope.row.tags && scope.row.tags.length > 0">
              <!-- 只显示自定义标签 -->
              <el-tag
                v-for="(tag, index) in scope.row.tags"
                :key="index"
                type="info"
                size="small"
                style="margin-right: 5px;"
              >
                {{ tag }}
              </el-tag>
            </template>
            <template v-else>
              <span>-</span>
            </template>
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
                style="margin-right: 5px;"
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
        <el-table-column prop="salesCount" label="销量" min-width="80" />
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
                  点击"编辑"查看详细价格配置
                </div>
              </div>
            </el-popover>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="createdAt" label="创建时间" min-width="180" />
        <el-table-column label="操作" min-width="180" fixed="right">
          <template #default="scope">
            <div class="button-group">
              <template v-if="scope && scope.row">
                <el-button 
                  type="primary" 
                  size="small" 
                  @click="handleEdit(scope.row)"
                  :disabled="scope.row.status === 'pending'"
                >
                  编辑
                </el-button>
                <el-button 
                  type="danger" 
                  size="small" 
                  @click="handleDelete(scope.row)"
                  :loading="deletingIds.has(scope.row.id)"
                  :disabled="deletingIds.has(scope.row.id)"
                >
                  {{ deletingIds.has(scope.row.id) ? '删除中...' : '删除' }}
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
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import {
  ElCard,
  ElRow,
  ElCol,
  ElInput,
  ElSelect,
  ElOption,
  ElButton,
  ElTable,
  ElTableColumn,
  ElPagination,
  ElImage,
  ElTag,
  ElMessage,
  ElMessageBox,
  ElIcon,
  ElPopover,
  ElTooltip,
  vLoading
} from 'element-plus'
import { Search, InfoFilled } from '@element-plus/icons-vue'

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
const searching = ref(false)
const products = ref([])
const statistics = ref(null)
const deletingIds = ref(new Set()) // 记录正在删除的商品ID

// 审核状态和激活状态相关
const supplierAuditStatus = ref('resubmit')
const isActive = ref(false)
const isAuditApproved = computed(() => supplierAuditStatus.value === 'approved')
const canAddProduct = computed(() => isActive.value && isAuditApproved.value)

// 获取添加商品按钮的提示文案
const getAddProductTooltip = () => {
  if (!isActive.value) {
    return '账号未激活，无法添加商品。请联系管理员激活您的账号。'
  }
  if (!isAuditApproved.value) {
    return '只有审核状态为“已通过”的供应商才能添加商品'
  }
  return ''
}

// 搜索参数
const searchParams = reactive({
  keyword: '',
  status: '',
  categoryId: '',
  subcategoryId: '',
  itemId: '',
  isNew: '',
  isHot: '',
  isPromotion: '',
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

// 加载商品数据
const loadProductData = async (page = 1, limit = 20) => {
  // 确保区域选项已加载（按需加载时也会请求）
  if (regionOptions.length === 0) {
    await loadRegionOptions()
  }
  
  // 如果是搜索操作，显示搜索按钮的loading状态
  if (page === 1 && (searchParams.keyword || searchParams.status || searchParams.isNew || searchParams.isHot)) {
    searching.value = true
  }
  
  loading.value = true
  try {
    const params = new URLSearchParams({
      page: page,
      limit: limit,
      ...searchParams
    })

    const url = `/supplier${props.supplierLoginPath}/product/list/data?${params}`

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
    const response = await fetch(`/supplier${props.supplierLoginPath}/product/statistics`, {
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

// 搜索
const handleSearch = () => {
  pagination.currentPage = 1
  loadProductData(1, pagination.itemsPerPage)
}

// 重置
const handleReset = () => {
  searchParams.keyword = ''
  searchParams.status = ''
  searchParams.categoryId = ''
  searchParams.subcategoryId = ''
  searchParams.itemId = ''
  searchParams.isNew = ''
  searchParams.isHot = ''
  searchParams.isPromotion = ''
  handleSearch()
}

// 分页大小变化
const handleSizeChange = (val) => {
  pagination.itemsPerPage = val
  loadProductData(pagination.currentPage, val)
}

// 当前页变化
const handleCurrentChange = (val) => {
  pagination.currentPage = val
  loadProductData(val, pagination.itemsPerPage)
}

// 导航到添加商品页面
const navigateToAdd = () => {
  window.dispatchEvent(new CustomEvent('navigate-to', {
    detail: { key: 'product-add' }
  }))
}

// 编辑商品（导航到编辑页面）
const handleEdit = (row) => {
  window.dispatchEvent(new CustomEvent('navigate-to', {
    detail: { key: 'product-edit', params: { id: row.id } }
  }))
}

// 删除
const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确定要删除商品“${row.title}”吗？删除后将同步清理七牛云上的图片文件。`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(async () => {
    // 添加到删除中的ID集合
    deletingIds.value.add(row.id)
    
    try {
      const response = await fetch(`/supplier${props.supplierLoginPath}/product/delete/${row.id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        }
      })

      const result = await response.json()

      if (result.success) {
        ElMessage.success(result.message || '删除成功')
        loadProductData(pagination.currentPage, pagination.itemsPerPage)
        loadStatistics()
      } else {
        ElMessage.error(result.message || '删除失败')
      }
    } catch (error) {
      console.error('删除失败:', error)
      ElMessage.error('网络错误，请稍后重试')
    } finally {
      // 从删除中的ID集合移除
      deletingIds.value.delete(row.id)
    }
  }).catch(() => {
    // 取消删除
  })
}

// 获取状态类型
const getStatusType = (status) => {
  const typeMap = {
    draft: 'info',
    pending: 'warning',
    approved: 'success',
    rejected: 'danger',
    offline: ''
  }
  return typeMap[status] || ''
}

// 从枚举类获取区域信息
let regionOptions = []

const loadRegionOptions = async () => {
  try {
    const response = await fetch(`/supplier${props.supplierLoginPath}/product/shipping-regions`, {
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
    return option?.currencySymbol || '￥'
  }
  // 后备方案
  const symbolMap = {
    'CN': '￥',
    'US': '$',
    'UK': '£',
    'PR': '€'
  }
  return symbolMap[region] || '￥'
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

// 格式化会员折扣显示
const formatMemberDiscount = (memberDiscount) => {
  if (!memberDiscount || typeof memberDiscount !== 'object') {
    return '未配置'
  }
  
  const vipLabels = {
    '0': '普通',
    '1': 'VIP1',
    '2': 'VIP2',
    '3': 'VIP3',
    '4': 'VIP4',
    '5': 'VIP5'
  }
  
  const discounts = []
  for (const [level, discount] of Object.entries(memberDiscount)) {
    if (discount && parseFloat(discount) > 0) {
      const discountPercent = (parseFloat(discount) * 100).toFixed(0)
      discounts.push(`${vipLabels[level]}:${discountPercent}%`)
    }
  }
  
  return discounts.length > 0 ? discounts.join(', ') : '未配置'
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

// 加载供应商信息（获取审核状态和激活状态）
const loadSupplierProfile = async () => {
  try {
    const response = await fetch(`/supplier${props.supplierLoginPath}/profile/data`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    
    const result = await response.json()
    
    if (result.success && result.data) {
      supplierAuditStatus.value = result.data.auditStatus || 'resubmit'
      // 正确处理布尔值，避免 false 被转换为 false
      isActive.value = result.data.isActive === true || result.data.isActive === 1
      
      console.log('[ProductList] 供应商状态:', {
        auditStatus: supplierAuditStatus.value,
        isActive: isActive.value,
        rawIsActive: result.data.isActive
      })
    }
  } catch (error) {
    console.error('加载供应商信息失败:', error)
  }
}

// 组件挂载
onMounted(() => {
  if (props.autoLoad) {
    loadSupplierProfile()
    loadProductData()
    loadStatistics()
  }
})

// 暴露方法供父组件调用（按需加载）
defineExpose({
  loadProductData,
  loadStatistics
})
</script>

<style scoped>
.product-list-container {
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

.search-bar {
  margin-bottom: 20px;
}

.no-image {
  color: #909399;
  font-size: 12px;
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

/* 多区域价格Popover样式 */
.region-price-popover {
  padding: 5px 0;
}

.region-price-item {
  padding: 10px;
  border-bottom: 1px solid #f0f0f0;
}

.region-price-item:last-child {
  border-bottom: none;
}

.region-name {
  margin-bottom: 8px;
}

.region-info {
  font-size: 12px;
  color: #606266;
  line-height: 1.8;
}

.region-info div {
  display: flex;
  align-items: center;
  gap: 5px;
}

.member-discount-section {
  display: block !important;
}

.member-discount-detail {
  padding-left: 20px;
  font-size: 11px;
  color: #909399;
  line-height: 1.6;
  margin-top: 2px;
}

.member-prices-section {
  display: block !important;
}

.member-prices-detail {
  padding-left: 20px;
  font-size: 11px;
  color: #67c23a;
  line-height: 1.6;
  margin-top: 2px;
  font-weight: 500;
}

.discount-info {
  color: #e6a23c;
  font-weight: 500;
}

.popover-tip {
  margin-top: 10px;
  padding: 8px;
  background-color: #f5f7fa;
  border-radius: 4px;
  font-size: 12px;
  color: #909399;
  display: flex;
  align-items: center;
  gap: 5px;
}

.debug-info {
  font-size: 10px;
  color: #999;
  margin-top: 5px;
}
</style>