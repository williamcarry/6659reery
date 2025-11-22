<template>
  <div class="sales-stats" v-loading="loading" element-loading-text="加载中..." element-loading-background="rgba(255, 255, 255, 0.5)">
    <el-card style="margin-bottom: 20px">
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center">
          <span>销售统计</span>
          <el-radio-group v-model="period" size="small" @change="loadData">
            <el-radio-button label="last_7_days">最近7天</el-radio-button>
            <el-radio-button label="last_30_days">最近30天</el-radio-button>
            <el-radio-button label="last_3_months">最近3个月</el-radio-button>
          </el-radio-group>
        </div>
      </template>
      
      <!-- 销售趋势图 -->
      <div ref="salesTrendChartRef" style="height: 400px"></div>
    </el-card>
    
    <el-row :gutter="20">
      <!-- 商品销售排行 Top 10 -->
      <el-col :span="12">
        <el-card>
          <template #header>热销商品 Top 10</template>
          <el-table :data="topProducts" stripe max-height="400">
            <el-table-column type="index" label="排名" width="60" align="center">
              <template #default="{ $index }">
                <el-tag v-if="$index === 0" type="danger" size="small">🥇</el-tag>
                <el-tag v-else-if="$index === 1" type="warning" size="small">🥈</el-tag>
                <el-tag v-else-if="$index === 2" type="success" size="small">🥉</el-tag>
                <span v-else>{{ $index + 1 }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="product_name" label="商品名称" min-width="150" show-overflow-tooltip />
            <el-table-column prop="total_quantity" label="销量" width="80" align="right" />
            <el-table-column label="销售额" width="120" align="right">
              <template #default="{ row }">
                {{ currencySymbol }}{{ Number(row.total_sales || 0).toLocaleString('zh-CN', { minimumFractionDigits: 2 }) }}
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      
      <!-- 订单状态分布 -->
      <el-col :span="12">
        <el-card>
          <template #header>订单状态分布</template>
          <div ref="orderStatusChartRef" style="height: 400px"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import { ElCard, ElRow, ElCol, ElRadioGroup, ElRadioButton, ElTable, ElTableColumn, ElTag, ElMessage, ElLoading } from 'element-plus'
import { vLoading } from 'element-plus/es/components/loading/src/directive'
import * as echarts from 'echarts'

const props = defineProps({
  supplierLoginPath: {
    type: String,
    default: ''
  },
  autoLoad: {
    type: Boolean,
    default: false
  }
})

const period = ref('last_30_days')
const loading = ref(false)
const topProducts = ref([])
const orderStatusData = ref([])
const currencySymbol = ref('¥') // 默认货币符号

const salesTrendChartRef = ref(null)
const orderStatusChartRef = ref(null)
let salesTrendChart = null
let orderStatusChart = null

const loadData = async () => {
  loading.value = true
  try {
    const loginPath = props.supplierLoginPath || window.supplierLoginPath || ''
    const response = await fetch(`/api/supplier/stats/sales/trend?period=${period.value}`)
    const salesResult = await response.json()
    
    // 从后端获取货币符号
    if (salesResult.currencySymbol) {
      currencySymbol.value = salesResult.currencySymbol
    }
    
    const salesData = salesResult.data || salesResult
    
    await nextTick()
    renderSalesTrendChart(salesData)
    
    const productResponse = await fetch(`/api/supplier/stats/products/ranking?period=${period.value}&type=sales&limit=10`)
    const productResult = await productResponse.json()
    
    // 同步货币符号
    if (productResult.currencySymbol) {
      currencySymbol.value = productResult.currencySymbol
    }
    
    topProducts.value = productResult.data || productResult || []
    
    const statusResponse = await fetch(`/api/supplier/stats/sales/category?period=${period.value}`)
    const statusData = await statusResponse.json()
    orderStatusData.value = statusData || []
    
    await nextTick()
    renderOrderStatusChart()
  } catch (error) {
    ElMessage.error('加载销售统计数据失败: ' + error.message)
  } finally {
    loading.value = false
  }
}

const renderSalesTrendChart = (data) => {
  if (!salesTrendChartRef.value) return
  
  // 检查DOM是否可见且有宽度
  if (salesTrendChartRef.value.clientWidth === 0) {
    // 延迟初始化，等待DOM完全渲染，最多重试50次
    const retryCount = data._retryCount || 0
    if (retryCount < 50) {
      data._retryCount = retryCount + 1
      setTimeout(() => renderSalesTrendChart(data), 100)
    }
    return
  }
  
  if (salesTrendChart) {
    salesTrendChart.dispose()
  }
  
  salesTrendChart = echarts.init(salesTrendChartRef.value)
  
  const dates = (data || []).map(item => item.date || item.created_at || '')
  const orderCounts = (data || []).map(item => Number(item.order_count || 0))
  const salesAmounts = (data || []).map(item => Number(item.sales_amount || item.supplier_income || 0))
  
  const option = {
    title: {
      text: '销售趋势分析',
      left: 'center',
      top: 10,
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      },
      formatter: function(params) {
        let result = params[0].axisValue + '<br/>'
        params.forEach(item => {
          if (item.seriesName === '订单数量') {
            result += item.marker + item.seriesName + ': ' + item.value + ' 件<br/>'
          } else {
            result += item.marker + item.seriesName + ': ' + currencySymbol.value + item.value.toLocaleString('zh-CN', { minimumFractionDigits: 2 }) + '<br/>'
          }
        })
        return result
      }
    },
    legend: {
      data: ['订单数量', '销售额'],
      top: 40
    },
    xAxis: {
      type: 'category',
      data: dates,
      axisLabel: {
        rotate: 45
      }
    },
    yAxis: [
      {
        type: 'value',
        name: '订单数量(件)',
        position: 'left',
        axisLabel: {
          formatter: '{value}'
        },
        splitLine: {
          show: true,
          lineStyle: {
            type: 'dashed',
            color: '#E4E7ED'
          }
        }
      },
      {
        type: 'value',
        name: '销售额(元)',
        position: 'right',
        axisLabel: {
          formatter: function(value) {
            if (value >= 10000) {
              return currencySymbol.value + (value / 10000).toFixed(1) + 'w'
            } else if (value >= 1000) {
              return currencySymbol.value + (value / 1000).toFixed(1) + 'k'
            } else {
              return currencySymbol.value + value.toFixed(0)
            }
          }
        },
        splitLine: {
          show: false
        }
      }
    ],
    series: [
      {
        name: '订单数量',
        type: 'bar',
        data: orderCounts,
        itemStyle: {
          color: '#409EFF',
          borderRadius: [4, 4, 0, 0]
        },
        barWidth: '40%',
        label: {
          show: true,
          position: 'top',
          formatter: '{c}',
          fontSize: 10,
          color: '#606266'
        }
      },
      {
        name: '销售额',
        type: 'line',
        yAxisIndex: 1,
        data: salesAmounts,
        smooth: true,
        lineStyle: {
          color: '#67C23A',
          width: 3
        },
        itemStyle: {
          color: '#67C23A',
          borderWidth: 2,
          borderColor: '#fff'
        },
        symbol: 'circle',
        symbolSize: 8,
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(103, 194, 58, 0.3)' },
            { offset: 1, color: 'rgba(103, 194, 58, 0.05)' }
          ])
        },
        label: {
          show: true,
          position: 'top',
          formatter: function(params) {
            const value = params.value
            if (value >= 10000) {
              return currencySymbol.value + (value / 10000).toFixed(1) + 'w'
            } else if (value >= 1000) {
              return currencySymbol.value + (value / 1000).toFixed(1) + 'k'
            } else {
              return currencySymbol.value + value.toFixed(0)
            }
          },
          fontSize: 10,
          color: '#67C23A'
        }
      }
    ],
    grid: {
      left: '3%',
      right: '5%',
      bottom: '15%',
      top: '22%',
      containLabel: true
    }
  }
  
  salesTrendChart.setOption(option)
}

const renderOrderStatusChart = () => {
  if (!orderStatusChartRef.value) return
  
  // 检查DOM是否可见且有宽度
  if (orderStatusChartRef.value.clientWidth === 0) {
    // 延迟初始化，等待DOM完全渲染
    setTimeout(() => renderOrderStatusChart(), 100)
    return
  }
  
  if (orderStatusChart) {
    orderStatusChart.dispose()
  }
  
  orderStatusChart = echarts.init(orderStatusChartRef.value)
  
  const statusMap = {
    'paid': '已支付',
    'shipped': '已发货',
    'completed': '已完成',
    'refunding': '退款中',
    'cancelled': '已取消'
  }
  
  const chartData = (orderStatusData.value || []).map(item => ({
    name: statusMap[item.order_status] || item.order_status || item.category_name || '其他',
    value: Number(item.order_count || item.order_count || 0)
  }))
  
  const option = {
    title: {
      text: '订单状态分布',
      left: 'center',
      top: 10,
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      top: 45
    },
    series: [
      {
        name: '订单状态',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          formatter: '{b}: {d}%'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        data: chartData
      }
    ]
  }
  
  orderStatusChart.setOption(option)
}

onMounted(() => {
  if (props.autoLoad) {
    loadData()
  }
})

defineExpose({
  loadData
})
</script>

<style scoped>
.sales-stats {
  padding: 0;
}
</style>
