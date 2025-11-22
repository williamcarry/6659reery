<template>
  <div class="finance-stats" v-loading="loading" element-loading-text="加载中..." element-loading-background="rgba(255, 255, 255, 0.5)">
    <el-row :gutter="20" style="margin-bottom: 20px">
      <el-col :span="8">
        <el-card shadow="hover">
          <el-statistic title="本月订单总收入" :value="monthlyStats.totalIncome" :prefix="currencySymbol" :precision="2" />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <el-statistic title="本月佣金支出" :value="monthlyStats.commission" :prefix="currencySymbol" :precision="2" />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <el-statistic title="本月净收入" :value="monthlyStats.netIncome" :prefix="currencySymbol" :precision="2" />
        </el-card>
      </el-col>
    </el-row>
    
    <el-card>
      <template #header>近12个月收入趋势</template>
      <div ref="incomeTrendChartRef" style="height: 400px"></div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { ElCard, ElRow, ElCol, ElStatistic, ElMessage, ElLoading } from 'element-plus'
import { vLoading } from 'element-plus/es/components/loading/src/directive'
import * as echarts from 'echarts'

const props = defineProps({
  supplierLoginPath: { type: String, default: '' },
  autoLoad: { type: Boolean, default: false }
})

const monthlyStats = ref({ totalIncome: 0, commission: 0, netIncome: 0 })
const loading = ref(false)
const incomeTrendChartRef = ref(null)
const currencySymbol = ref('¥') // 默认货币符号
let incomeTrendChart = null

const loadData = async () => {
  loading.value = true
  try {
    const loginPath = props.supplierLoginPath || window.supplierLoginPath || ''
    const response = await fetch(`/api/supplier/stats/finance/trend?period=last_12_months`)
    const result = await response.json()
    
    // 从后端获取货币符号
    if (result.currencySymbol) {
      currencySymbol.value = result.currencySymbol
    }
    
    const data = result.data || result
    
    if (data && Array.isArray(data)) {
      const latest = data[data.length - 1] || {}
      monthlyStats.value = {
        totalIncome: Number(latest.total_income || latest.revenue || 0),
        commission: Number(latest.total_commission || latest.commission || 0),
        netIncome: Number(latest.net_income || 0)
      }
      
      await nextTick()
      renderIncomeTrendChart(data)
    }
  } catch (error) {
    ElMessage.error('加载财务统计数据失败')
  } finally {
    loading.value = false
  }
}

const renderIncomeTrendChart = (data) => {
  if (!incomeTrendChartRef.value) return
  
  // 检查DOM是否可见且有宽度
  if (incomeTrendChartRef.value.clientWidth === 0) {
    // 延迟初始化，等待DOM完全渲染
    setTimeout(() => renderIncomeTrendChart(data), 100)
    return
  }
  
  if (incomeTrendChart) incomeTrendChart.dispose()
  
  incomeTrendChart = echarts.init(incomeTrendChartRef.value)
  
  const months = data.map(item => item.month || '')
  const incomes = data.map(item => Number(item.total_income || item.revenue || 0))
  const commissions = data.map(item => Number(item.total_commission || item.commission || 0))
  const netIncomes = data.map(item => Number(item.net_income || 0))
  
  const option = {
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    legend: { data: ['总收入', '佣金支出', '净收入'], top: 10 },
    xAxis: { type: 'category', data: months },
    yAxis: { type: 'value', axisLabel: { formatter: (value) => currencySymbol.value + (value / 1000).toFixed(0) + 'k' } },
    series: [
      { name: '总收入', type: 'bar', data: incomes, itemStyle: { color: '#409EFF' } },
      { name: '佣金支出', type: 'bar', data: commissions, itemStyle: { color: '#E6A23C' } },
      { name: '净收入', type: 'line', data: netIncomes, smooth: true, lineStyle: { color: '#67C23A', width: 3 } }
    ],
    grid: { left: '3%', right: '4%', bottom: '10%', containLabel: true }
  }
  
  incomeTrendChart.setOption(option)
}

onMounted(() => { if (props.autoLoad) loadData() })
defineExpose({ loadData })
</script>
