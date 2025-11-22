<template>
  <div class="supplier-ranking">
    <!-- 顶部操作区 -->
    <el-card style="margin-bottom: 20px">
      <el-row :gutter="20">
        <!-- 左侧：搜索供应商 -->
        <el-col :span="12">
          <el-input
            v-model="searchUsername"
            placeholder="输入供应商用户名搜索（支持模糊搜索）"
            clearable
            @keyup.enter="handleSearch"
            @clear="clearSearch"
          >
            <template #append>
              <el-button 
                type="primary" 
                @click="handleSearch"
                :loading="searchLoading"
                class="search-button"
              >
                搜索
              </el-button>
            </template>
          </el-input>
        </el-col>
        
        <!-- 右侧：筛选器 -->
        <el-col :span="12">
          <div style="display: flex; gap: 10px; justify-content: flex-end">
            <el-date-picker
              v-model="selectedMonth"
              type="month"
              placeholder="选择月份"
              format="YYYY年MM月"
              value-format="YYYY-MM"
              @change="loadRanking"
              clearable
              style="width: 180px"
            />
            
            <el-select 
              v-model="sortBy" 
              placeholder="排序方式" 
              style="width: 150px"
              @change="loadRanking"
            >
              <el-option label="销售额排序" value="sales" />
              <el-option label="订单量排序" value="orders" />
              <el-option label="商品数排序" value="products" />
            </el-select>
            
            <el-button @click="resetFilters">重置</el-button>
          </div>
        </el-col>
      </el-row>
    </el-card>
    
    <!-- 搜索结果卡片 -->
    <el-card 
      v-if="searchResult" 
      class="search-result-card" 
      shadow="always"
      style="margin-bottom: 20px; border: 2px solid #409EFF"
    >
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center">
          <div>
            <span style="margin-left: 10px; font-size: 16px; font-weight: bold">
              {{ searchResult.supplier.companyName }}
            </span>
            <el-tag size="small" style="margin-left: 10px">
              {{ searchResult.supplier.username }}
            </el-tag>
            <el-tag size="small" type="info" style="margin-left: 5px">
              ID: {{ searchResult.supplier.id }}
            </el-tag>
          </div>
          <el-button 
            type="danger" 
            :icon="Close"
            size="small"
            @click="clearSearch"
          >
            关闭
          </el-button>
        </div>
      </template>
      
      <!-- 月度核心指标 -->
      <el-row :gutter="20" style="margin-bottom: 20px">
        <el-col :span="6">
          <el-statistic 
            title="本月订单数" 
            :value="searchResult.monthlyStats.order_count || 0"
          />
        </el-col>
        <el-col :span="6">
          <el-statistic 
            title="本月销售额" 
            :value="searchResult.monthlyStats.total_sales || 0"
            :prefix="currencySymbol"
            :precision="2"
          />
        </el-col>
        <el-col :span="6">
          <el-statistic 
            title="佣金支出" 
            :value="searchResult.monthlyStats.commission || 0"
            :prefix="currencySymbol"
            :precision="2"
          />
        </el-col>
        <el-col :span="6">
          <el-statistic 
            title="净收入" 
            :value="searchResult.monthlyStats.net_income || 0"
            :prefix="currencySymbol"
            :precision="2"
          />
        </el-col>
      </el-row>
      
      <!-- 12个月趋势图 -->
      <el-divider content-position="left">近12个月销售趋势</el-divider>
      <div ref="trendChartRef" style="height: 300px"></div>
      
      <!-- 热销商品 Top 5 -->
      <el-divider content-position="left">热销商品 Top 5</el-divider>
      <el-table 
        :data="searchResult.hotProducts" 
        border
        stripe
      >
        <el-table-column type="index" label="排名" width="60" align="center">
          <template #default="{ $index }">
            <el-tag v-if="$index === 0" type="danger">🥇</el-tag>
            <el-tag v-else-if="$index === 1" type="warning">🥈</el-tag>
            <el-tag v-else-if="$index === 2" type="success">🥉</el-tag>
            <span v-else>{{ $index + 1 }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="商品名称" min-width="200" />
        <el-table-column prop="sku" label="SKU" width="120" />
        <el-table-column prop="sales_count" label="销量" width="100" align="right" />
        <el-table-column label="销售额" width="150" align="right">
          <template #default="{ row }">
            <span style="color: #67C23A; font-weight: bold">
              {{ currencySymbol }}{{ Number(row.sales_amount || 0).toLocaleString('zh-CN', { minimumFractionDigits: 2 }) }}
            </span>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 排行榜列表 -->
    <el-card v-loading="rankingLoading" element-loading-background="rgba(255, 255, 255, 0.5)">
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center">
          <span style="font-weight: bold">
            {{ selectedMonth }} 供应商销量排行榜 Top 100
          </span>
          <el-tag>共 {{ total }} 个供应商</el-tag>
        </div>
      </template>
      
      <el-table 
        :data="rankingList" 
        border
        stripe
        highlight-current-row
        @row-click="handleRowClick"
        style="cursor: pointer"
      >
        <el-table-column label="排名" width="80" align="center" fixed>
          <template #default="{ $index }">
            <el-tag v-if="$index === 0" size="large" type="danger">🥇 1</el-tag>
            <el-tag v-else-if="$index === 1" size="large" type="warning">🥈 2</el-tag>
            <el-tag v-else-if="$index === 2" size="large" type="success">🥉 3</el-tag>
            <span v-else style="font-weight: bold">{{ (currentPage - 1) * pageSize + $index + 1 }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" width="150" />
        <el-table-column prop="company_name" label="公司名称" min-width="200" show-overflow-tooltip />
        <el-table-column prop="order_count" label="订单数" width="100" align="right" />
        <el-table-column label="销售额" width="150" align="right">
          <template #default="{ row }">
            {{ currencySymbol }}{{ Number(row.total_sales || 0).toLocaleString('zh-CN', { minimumFractionDigits: 2 }) }}
          </template>
        </el-table-column>
        <el-table-column label="佣金" width="120" align="right">
          <template #default="{ row }">
            {{ currencySymbol }}{{ Number(row.commission || 0).toLocaleString('zh-CN', { minimumFractionDigits: 2 }) }}
          </template>
        </el-table-column>
        <el-table-column label="净收入" width="150" align="right">
          <template #default="{ row }">
            <span style="color: #67C23A; font-weight: bold">
              {{ currencySymbol }}{{ Number(row.net_income || 0).toLocaleString('zh-CN', { minimumFractionDigits: 2 }) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="product_count" label="商品数" width="100" align="right" />
      </el-table>
      
      <!-- 分页 -->
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @current-change="loadRanking"
        @size-change="loadRanking"
        style="margin-top: 20px; justify-content: center"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import { 
  ElCard, 
  ElRow, 
  ElCol, 
  ElInput,
  ElButton,
  ElDatePicker,
  ElSelect,
  ElOption,
  ElIcon,
  ElTag,
  ElStatistic,
  ElDivider,
  ElTable,
  ElTableColumn,
  ElPagination,
  ElMessage,
  ElLoading
} from 'element-plus'
import { Close } from '@element-plus/icons-vue'
import { vLoading } from 'element-plus/es/components/loading/src/directive'
import * as echarts from 'echarts'

const props = defineProps({
  adminLoginPath: {
    type: String,
    default: ''
  },
  autoLoad: {
    type: Boolean,
    default: false
  }
})

const searchUsername = ref('')
const searchLoading = ref(false)
const searchResult = ref(null)
const trendChartRef = ref(null)
let trendChart = null

const selectedMonth = ref(new Date().toISOString().substring(0, 7))
const sortBy = ref('sales')
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const rankingList = ref([])
const rankingLoading = ref(false)
const currencySymbol = ref('$')

const handleSearch = async () => {
  if (!searchUsername.value || searchUsername.value.trim() === '') {
    ElMessage.warning('请输入供应商用户名')
    return
  }
  
  searchLoading.value = true
  try {
    const loginPath = props.adminLoginPath || window.adminLoginPath || ''
    const response = await fetch(
      `/api/admin/stats/suppliers/search?username=${encodeURIComponent(searchUsername.value)}&month=${selectedMonth.value}`,
      {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      }
    )
    
    const result = await response.json()
    
    if (response.ok && result) {
      searchResult.value = result
      // 更新货币符号
      if (result.currencySymbol) {
        currencySymbol.value = result.currencySymbol
      }
      await nextTick()
      renderTrendChart()
    } else {
      ElMessage.error(result.error || '未找到该供应商')
      searchResult.value = null
    }
  } catch (error) {
    ElMessage.error('搜索失败: ' + error.message)
  } finally {
    searchLoading.value = false
  }
}

const clearSearch = () => {
  searchUsername.value = ''
  searchResult.value = null
  if (trendChart) {
    trendChart.dispose()
    trendChart = null
  }
}

const renderTrendChart = () => {
  if (!trendChartRef.value || !searchResult.value) return
  
  if (trendChart) {
    trendChart.dispose()
  }
  
  trendChart = echarts.init(trendChartRef.value)
  
  const trend = searchResult.value.last12MonthsTrend || []
  const months = trend.map(item => item.month || '')
  const values = trend.map(item => Number(item.total_income || 0))
  
  const option = {
    tooltip: {
      trigger: 'axis',
      formatter: (params) => {
        const param = params[0]
        return `${param.axisValue}<br/>销售额: ${currencySymbol.value}${Number(param.value).toLocaleString('zh-CN', { minimumFractionDigits: 2 })}`
      }
    },
    xAxis: {
      type: 'category',
      data: months,
      axisLabel: {
        rotate: 45
      }
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        formatter: (value) => currencySymbol.value + (value / 1000).toFixed(0) + 'k'
      }
    },
    series: [{
      data: values,
      type: 'line',
      smooth: true,
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(64, 158, 255, 0.3)' },
          { offset: 1, color: 'rgba(64, 158, 255, 0.05)' }
        ])
      },
      lineStyle: {
        color: '#409EFF',
        width: 2
      },
      itemStyle: {
        color: '#409EFF'
      }
    }],
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      containLabel: true
    }
  }
  
  trendChart.setOption(option)
}

const loadRanking = async () => {
  // 如果月份为空，使用当前月份
  if (!selectedMonth.value) {
    selectedMonth.value = new Date().toISOString().substring(0, 7)
  }
  
  rankingLoading.value = true
  try {
    const loginPath = props.adminLoginPath || window.adminLoginPath || ''
    const response = await fetch(
      `/api/admin/stats/suppliers/monthly-ranking?month=${selectedMonth.value}&page=${currentPage.value}&limit=${pageSize.value}&sortBy=${sortBy.value}`,
      {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      }
    )
    
    const result = await response.json()
    
    if (result && result.list && Array.isArray(result.list)) {
      rankingList.value = result.list
      total.value = Math.min(result.list.length, 100)
      // 更新货币符号
      if (result.currencySymbol) {
        currencySymbol.value = result.currencySymbol
      }
    } else if (Array.isArray(result)) {
      // 兼容旧格式（直接是数组）
      rankingList.value = result
      total.value = Math.min(result.length, 100)
    } else {
      console.error('排行榜数据格式错误:', result)
      ElMessage.error('加载排行榜失败：数据格式错误')
      rankingList.value = []
      total.value = 0
    }
  } catch (error) {
    ElMessage.error('加载排行榜失败: ' + error.message)
  } finally {
    rankingLoading.value = false
  }
}

const handleRowClick = (row) => {
  searchUsername.value = row.username
  handleSearch()
}

const resetFilters = () => {
  selectedMonth.value = new Date().toISOString().substring(0, 7)
  sortBy.value = 'sales'
  currentPage.value = 1
  loadRanking()
}

watch(() => searchResult.value, () => {
  if (searchResult.value) {
    nextTick(() => {
      renderTrendChart()
    })
  }
})

onMounted(() => {
  if (props.autoLoad) {
    loadRanking()
  }
})

defineExpose({
  loadRanking
})
</script>

<style scoped>
.supplier-ranking {
  padding: 0;
}

/* 搜索按钮样式增强 */
.search-button {
  background-color: #409EFF !important;
  border-color: #409EFF !important;
  color: white !important;
  font-weight: bold;
  min-width: 80px;
  height: 100%;
  font-size: 14px;
}

/* 确保按钮内所有元素文字都是白色 */
.search-button :deep(span) {
  color: white !important;
}

.search-button:hover {
  background-color: #66b1ff !important;
  border-color: #66b1ff !important;
}

.search-button:active {
  background-color: #3a8ee6 !important;
  border-color: #3a8ee6 !important;
}

.search-result-card {
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
