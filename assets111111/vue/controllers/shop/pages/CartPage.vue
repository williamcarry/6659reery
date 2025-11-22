<template>
  <div class="min-h-screen flex flex-col">
    <SiteHeader />
    <div class="flex-1 bg-slate-50">
      <div class="mx-auto w-full max-w-[1500px] md:w-[80%] md:min-w-[1150px] px-4 md:px-0 py-8">
        <div class="mb-6">
          <h1 class="text-2xl font-semibold text-slate-900 mb-4">购物车</h1>
          <div class="flex gap-0 border-b border-slate-200">
            <button
              @click="cartType = 'dropship'"
              :class="[
                'px-6 py-3 font-medium border-b-2 transition',
                cartType === 'dropship'
                  ? 'border-primary text-primary'
                  : 'border-transparent text-slate-600 hover:text-slate-900'
              ]"
            >
              一件代发
            </button>
            <button
              @click="cartType = 'wholesale'"
              :class="[
                'px-6 py-3 font-medium border-b-2 transition',
                cartType === 'wholesale'
                  ? 'border-primary text-primary'
                  : 'border-transparent text-slate-600 hover:text-slate-900'
              ]"
            >
              批发
            </button>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-12 gap-6">
          <!-- 购物车商品列表 -->
          <div class="md:col-span-7 lg:col-span-8">
            <div class="bg-white rounded-lg border border-slate-200">
              <!-- 表头 -->
              <div class="grid grid-cols-12 gap-3 p-4 bg-slate-50 border-b border-slate-200 text-sm font-medium text-slate-700">
                <div class="col-span-1">
                  <input
                    type="checkbox"
                    v-model="selectAll"
                    @change="toggleSelectAll"
                    class="w-4 h-4 accent-primary rounded"
                  />
                </div>
                <div class="col-span-5">商品</div>
                <div class="col-span-2 text-right">价格</div>
                <div class="col-span-2 text-center">数量</div>
                <div class="col-span-2 text-right">小计</div>
              </div>

              <!-- 购物车内容 -->
              <div v-if="cartItems.length > 0">
                <div v-for="(group, groupIndex) in groupedItems" :key="groupIndex">
                  <!-- 分组标题 -->
                  <div class="grid grid-cols-12 gap-3 p-3 bg-slate-100 border-b border-slate-200 items-center text-xs font-medium text-slate-600">
                    <div class="col-span-1"></div>
                    <div class="col-span-11 flex items-center justify-between">
                      <div class="flex items-center gap-2">
                        <span v-if="group.region === 'US'" class="text-lg">🇺🇸</span>
                        <span v-else-if="group.region === 'UK'" class="text-lg">🇬🇧</span>
                        <span v-else class="text-lg">🌍</span>
                        <span class="font-medium">{{ group.region }} - {{ group.shipping }} ({{ group.items.length }})</span>
                      </div>
                      <div class="flex items-center gap-4 text-slate-500 text-xs">
                        <button 
                          @click="deleteSelectedInGroup(group)"
                          class="hover:text-slate-700 transition cursor-pointer flex items-center gap-1"
                        >
                          ⊖ <span>删除选中商品({{ getSelectedCountInGroup(group) }})</span>
                        </button>
                        <button 
                          @click="selectGroup(group)"
                          :class="[
                            'transition cursor-pointer flex items-center gap-1',
                            group.items.every(item => item.selected) 
                              ? 'text-primary hover:text-red-700' 
                              : 'text-slate-500 hover:text-slate-700'
                          ]"
                        >
                          <span :class="[
                            'inline-block w-3 h-3 rounded-full border-2 transition',
                            group.items.every(item => item.selected)
                              ? 'border-primary bg-primary'
                              : 'border-slate-400 bg-transparent'
                          ]"></span>
                          <span>选中此运费方式的商品({{ group.items.length }})</span>
                        </button>
                      </div>
                    </div>
                  </div>

                  <!-- 商品行 -->
                  <div v-for="(item, itemIndex) in group.items" :key="item.id" class="grid grid-cols-12 gap-3 p-4 border-b border-slate-200 items-center text-sm bg-white hover:bg-slate-50 transition">
                    <div class="col-span-1">
                      <input
                        type="checkbox"
                        v-model="item.selected"
                        @change="updateCartItem(item.id, { isSelected: item.selected })"
                        class="w-4 h-4 accent-primary rounded"
                      />
                    </div>

                    <!-- 商品信息 -->
                    <div class="col-span-5 flex gap-3">
                      <div 
                        class="w-16 h-16 bg-slate-100 rounded flex-shrink-0 overflow-hidden cursor-pointer hover:opacity-80 transition"
                        @click="goToProductDetail(item.productId)"
                        :title="'查看商品详情'"
                      >
                        <img
                          :src="item.image"
                          :alt="item.name"
                          class="w-full h-full object-cover"
                        />
                      </div>
                      <div class="flex-1 min-w-0">
                        <div class="flex justify-between items-start gap-2">
                          <div 
                            class="text-slate-900 font-medium text-sm line-clamp-2 cursor-pointer hover:text-primary transition"
                            @click="goToProductDetail(item.productId)"
                            :title="item.name"
                          >
                            {{ item.name }}
                          </div>
                          <button
                            @click="removeItem(cartItems.indexOf(item))"
                            class="text-primary hover:text-red-700 transition text-sm font-medium flex-shrink-0 whitespace-nowrap ml-2"
                          >
                            删除
                          </button>
                        </div>
                        <div 
                          class="text-slate-500 text-xs mt-1 cursor-pointer hover:text-primary transition"
                          @click="goToProductDetail(item.productId)"
                          :title="'点击查看商品详情'"
                        >
                          SKU: {{ item.sku }}
                        </div>
                        <div class="text-slate-500 text-xs">可售库存：{{ item.availableStock }}</div>
                        <div v-if="!item.isAvailable" class="text-red-500 text-xs mt-1">
                          {{ item.unavailableReason || '商品已失效' }}
                        </div>
                      </div>
                    </div>

                    <!-- 价格 -->
                    <div class="col-span-2 text-right">
                      <div class="text-primary font-semibold text-sm">{{ item.price }}</div>
                      <div class="text-slate-500 line-through text-xs">{{ item.originalPrice }}</div>
                      
                      <!-- 商品级别价格明细 -->
                      <div class="mt-2 space-y-0.5 text-xs">
                        <!-- 会员折扣 -->
                        <div v-if="item.memberDiscount && item.memberDiscount > 0" class="text-green-600">
                          <!-- 【原有显示逻辑 - 已注释】原逻辑：使用商品自带的 currency -->
                          <!-- 会员省: -{{ item.currency }} {{ parseFloat(item.memberDiscount * item.quantity).toFixed(2) }} -->
                          <!-- 【新逻辑】使用从SiteConfig读取的网站货币符号 -->
                          会员省: -{{ siteCurrency }} {{ parseFloat(item.memberDiscount * item.quantity).toFixed(2) }}
                        </div>
                        <!-- 商品折扣 -->
                        <div v-if="item.productDiscount && item.productDiscount > 0" class="text-green-600">
                          <!-- 【原有显示逻辑 - 已注释】原逻辑：使用商品自带的 currency -->
                          <!-- 优惠: -{{ item.currency }} {{ parseFloat(item.productDiscount * item.quantity).toFixed(2) }} -->
                          <!-- 【新逻辑】使用从SiteConfig读取的网站货币符号 -->
                          优惠: -{{ siteCurrency }} {{ parseFloat(item.productDiscount * item.quantity).toFixed(2) }}
                        </div>
                        <!-- 满减(每个商品单独显示) -->
                        <div v-if="item.fullReduction && item.fullReduction > 0" class="text-green-600">
                          <!-- 【原有显示逻辑 - 已注释】原逻辑：使用商品自带的 currency -->
                          <!-- 满减: -{{ item.currency }} {{ parseFloat(item.fullReduction).toFixed(2) }} -->
                          <!-- 【新逻辑】使用从SiteConfig读取的网站货币符号 -->
                          满减: -{{ siteCurrency }} {{ parseFloat(item.fullReduction).toFixed(2) }}
                        </div>
                        <!-- 运费 -->
                        <div v-if="item.shippingFee && item.shippingFee > 0" class="text-slate-600">
                          <!-- 【原有显示逻辑 - 已注释】原逻辑：使用商品自带的 currency -->
                          <!-- 运费: +{{ item.currency }} {{ parseFloat(item.shippingFee).toFixed(2) }} -->
                          <!-- 【新逻辑】使用从SiteConfig读取的网站货币符号 -->
                          运费: +{{ siteCurrency }} {{ parseFloat(item.shippingFee).toFixed(2) }}
                        </div>
                      </div>
                    </div>

                    <!-- 数量控制 -->
                    <div class="col-span-2 flex justify-center">
                      <div class="flex flex-col items-center">
                        <div class="flex items-center border border-slate-300 rounded bg-white">
                          <button
                            @click="decrementQty(cartItems.indexOf(item))"
                            class="px-2 py-1 text-slate-600 hover:bg-slate-100 text-sm font-medium transition"
                          >
                            −
                          </button>
                          <input
                            v-model.number="item.quantity"
                            type="number"
                            :min="item.minOrderQty || 1"
                            class="w-10 text-center border-l border-r border-slate-300 py-1 outline-none text-sm"
                            @change="updateQuantity(cartItems.indexOf(item), item.quantity)"
                          />
                          <button
                            @click="incrementQty(cartItems.indexOf(item))"
                            class="px-2 py-1 text-slate-600 hover:bg-slate-100 text-sm font-medium transition"
                          >
                            +
                          </button>
                        </div>
                        <!-- 最小起订量提示 -->
                        <div v-if="item.minOrderQty && item.minOrderQty > 1" class="text-xs text-slate-500 mt-1">
                          起订：{{ item.minOrderQty }}
                        </div>
                        <!-- 错误提示 -->
                        <div v-if="item.quantityError" class="text-xs text-red-500 mt-1">
                          {{ item.quantityError }}
                        </div>
                      </div>
                    </div>

                    <!-- 小计 -->
                    <div class="col-span-2 text-right">
                      <div class="text-slate-900 font-medium text-sm">
                        <!-- 【原有显示逻辑 - 已注释】原逻辑：使用商品自带的 currency -->
                        <!-- {{ item.currency }} {{ parseFloat(item.subtotal).toFixed(2) }} -->
                        <!-- 【新逻辑】使用从SiteConfig读取的网站货币符号 -->
                        {{ siteCurrency }} {{ parseFloat(item.subtotal).toFixed(2) }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 空购物车 -->
              <div v-else class="p-12 text-center">
                <div class="flex flex-col items-center justify-center">
                  <svg
                    class="w-20 h-20 text-slate-300 mb-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"
                    ></path>
                  </svg>
                  <p class="text-slate-500 text-sm">购物车为空</p>
                  <button
                    @click="goHome"
                    class="mt-4 px-6 py-2 bg-primary text-white rounded-lg hover:bg-red-700 transition text-sm font-medium"
                  >
                    继续购物
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- 合计侧栏 -->
          <div class="md:col-span-5 lg:col-span-4">
            <div class="bg-white rounded-lg border border-slate-200 p-5 sticky top-6 h-fit">
              <h3 class="text-base font-semibold text-slate-900 mb-4 pb-4 border-b border-slate-200">
                订单汇总
              </h3>

              <!-- 统计信息 -->
              <div class="space-y-3 mb-4">
                <div class="flex justify-between text-xs text-slate-600">
                  <span>SKU(件)：</span>
                  <span class="text-slate-900 font-medium">{{ totalSkuCount }}</span>
                </div>
                <div class="flex justify-between text-xs text-slate-600">
                  <span>商品数量(件)：</span>
                  <span class="text-slate-900 font-medium">{{ totalQuantity }}</span>
                </div>
              </div>

              <!-- 费用明细 -->
              <div class="space-y-2 mb-4 pb-4 border-b border-slate-200">
                <div class="flex justify-between text-sm">
                  <span class="text-slate-600">商品金额：</span>
                  <span class="text-slate-900 font-medium">{{ productAmount }}</span>
                </div>
                
                <!-- 动态显示每一项优惠 -->
                <div v-if="priceBreakdown && priceBreakdown.length > 0" class="space-y-2">
                  <div v-for="(item, index) in priceBreakdown" :key="index" class="flex justify-between text-sm">
                    <span class="text-slate-600">{{ item.label }}：</span>
                    <span :class="item.amount.startsWith('-') ? 'text-green-600 font-medium' : 'text-slate-900 font-medium'">
                      <!-- 【原有显示逻辑 - 已注释】原逻辑：使用明细项中的 currency 字段 -->
                      <!-- {{ item.currency }} {{ item.amount }} -->
                      <!-- 【新逻辑】使用从SiteConfig读取的网站货币符号 -->
                      {{ siteCurrency }} {{ item.amount }}
                    </span>
                  </div>
                </div>
              </div>

              <!-- 应付总额 -->
              <div class="flex justify-between text-base font-semibold text-primary mb-6">
                <span>应付总额：</span>
                <span>{{ totalAmount }}</span>
              </div>

              <!-- 结算按钮 -->
              <button
                @click="goToCheckout"
                :disabled="selectedCount === 0"
                :class="[
                  'w-full px-6 py-3 rounded-lg transition font-medium text-sm mb-4',
                  selectedCount > 0
                    ? 'bg-primary text-white hover:bg-red-700 cursor-pointer'
                    : 'bg-slate-300 text-slate-500 cursor-not-allowed'
                ]"
              >
                去结算{{ selectedCount > 0 ? `(${selectedCount})` : '' }}
              </button>

              <!-- 价格说明 -->
              <div class="p-3 bg-amber-50 border border-amber-200 rounded-lg">
                <div class="flex items-start gap-2">
                  <svg class="w-4 h-4 text-amber-600 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
                  </svg>
                  <div class="text-xs text-amber-800">
                    <p class="font-medium mb-1">价格说明</p>
                    <p class="text-amber-700">点击结算后，系统会根据您的会员等级、当前折扣活动、订单数量等因素重新计算最终价格，实际支付金额以结算页面显示为准。</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <SiteFooter />
    
    <!-- 支付方式对话框 -->
    <PaymentMethodModal
      :is-open="showPaymentModal"
      :product-title="paymentModalData.productTitle"
      :product-title-en="paymentModalData.productTitleEn"
      :product-image="paymentModalData.productImage"
      :quantity="paymentModalData.quantity"
      :total-price="paymentModalData.totalPrice"
      :price-breakdown="paymentModalData.priceBreakdown"
      :product-list="paymentModalData.productList"
      :site-currency="siteCurrency"
      @close="closePaymentModal"
      @confirm="confirmPayment"
    />
    
    <!-- 订单状态监控弹窗 -->
    <OrderStatusMonitor
      :is-visible="showOrderMonitor"
      :order-no="processingOrderNo"
      @close="handleOrderMonitorClose"
      @ready="handleMercureReady"
      @payment-success="handlePaymentSuccess"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import SiteHeader from '@/components/SiteHeader.vue'
import SiteFooter from '@/components/SiteFooter.vue'
import PaymentMethodModal from '@/components/PaymentMethodModal.vue'
import OrderStatusMonitor from '@/components/OrderStatusMonitor.vue'
import apiSignature from '../services/apiSignature.js'
import encryptionService from '../data/encryption-service.js'

// 从 window 对象获取 store 实例
const store = window.vueStore

// 检测登录状态，未登录则跳转到登录页
onMounted(async () => {
  if (!store?.state?.isLoggedIn) {
    window.location.href = '/login?redirect=/cart'
    return
  }
  // 加载购物车数据
  await loadCartData()
})

const cartType = ref('dropship')
const loading = ref(false)
const dropshipCartItems = ref([])
const wholesaleCartItems = ref([])
const orderSummary = ref(null) // 存储后端返回的订单汇总信息
const siteCurrency = ref('USD') // 网站货币符号（从SiteConfig读取）
const showPaymentModal = ref(false) // 支付方式对话框显示状态
const showOrderMonitor = ref(false) // 订单状态监控弹窗
const processingOrderNo = ref('') // 处理中的订单号
const pendingOrderData = ref(null) // 待提交的订单数据

// 监听购物车类型切换
watch(cartType, async () => {
  await loadCartData()
})

// 显示提示消息
const showMessage = (message, type = 'info') => {
  ElMessage({
    message: message,
    type: type,
    duration: 3000
  })
}

// 加载购物车数据
const loadCartData = async () => {
  loading.value = true
  try {
    const params = {
      businessType: cartType.value
    }
    
    // 使用和商品详情立即购买一样的加密方式：先加密再签名
    const encryptedData = encryptionService.prepareData(params, true)
    const signedData = apiSignature.sign(encryptedData)

    const response = await fetch('/shop/api/cart/list', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify(signedData)
    })
    
    const data = await response.json()
    
    if (data.success) {
      const items = data.data.map(item => ({
        id: item.id,
        productId: item.productId,
        name: item.productName,
        nameCn: item.productNameCn,
        sku: item.sku,
        image: item.productImage,
        // 【原有显示逻辑 - 已注释】
        // 原逻辑：使用商品自带的 currency 字段
        // price: `${item.currency} ${item.sellingPrice}`,
        // originalPrice: item.originalPrice ? `${item.currency} ${item.originalPrice}` : null,
        // 【新逻辑】使用从SiteConfig读取的网站货币符号
        price: `${siteCurrency.value} ${item.sellingPrice}`,
        originalPrice: item.originalPrice ? `${siteCurrency.value} ${item.originalPrice}` : null,
        quantity: item.quantity,
        minOrderQty: item.minOrderQty || 1, // 最小起订量
        region: item.region,
        shipping: '运送方式',
        selected: item.isSelected,
        isAvailable: item.isAvailable,
        unavailableReason: item.unavailableReason,
        availableStock: item.availableStock,
        currency: item.currency,
        sellingPrice: parseFloat(item.sellingPrice),
        subtotal: parseFloat(item.subtotal),
        // 价格详情
        productDiscount: parseFloat(item.productDiscount || 0),
        memberDiscount: parseFloat(item.memberDiscount || 0),
        fullReduction: parseFloat(item.fullReduction || 0),
        shippingFee: parseFloat(item.shippingFee || 0),
        quantityError: '' // 数量错误提示
      }))
      
      // 保存后端返回的订单汇总信息
      console.log('✅ 更新订单汇总:', data.summary) // 调试日志
      orderSummary.value = data.summary
      
      // 保存网站货币符号
      if (data.siteCurrency) {
        siteCurrency.value = data.siteCurrency
      }
      
      if (cartType.value === 'dropship') {
        dropshipCartItems.value = items
      } else {
        wholesaleCartItems.value = items
      }
    }
  } catch (error) {
    console.error('加载购物车失败:', error)
    
    showMessage('加载购物车失败', 'error')
  } finally {
    loading.value = false
  }
}

// 根据当前模式返回对应的购物车数据
const cartItems = computed(() => {
  return cartType.value === 'dropship' ? dropshipCartItems.value : wholesaleCartItems.value
})

const selectAll = ref(false)

const groupedItems = computed(() => {
  const groups = {}
  const items = cartItems.value

  items.forEach((item) => {
    const key = `${item.region}-${item.shipping}`
    if (!groups[key]) {
      groups[key] = {
        region: item.region,
        shipping: item.shipping || '标准配送',
        items: [],
      }
    }
    groups[key].items.push(item)
  })

  return Object.values(groups)
})

const totalSkuCount = computed(() => {
  return cartItems.value.filter(item => item.selected && item.isAvailable).length
})

// ✅ 前端实时计算选中商品的总数量
const totalQuantity = computed(() => {
  return cartItems.value
    .filter(item => item.selected && item.isAvailable)
    .reduce((sum, item) => sum + item.quantity, 0)
})

// 商品金额（直接使用后端返回的数据）
const productAmount = computed(() => {
  if (!orderSummary.value) return 'USD 0.00'
  // 【原有显示逻辑 - 已注释】
  // 原逻辑：使用后端返回的 currency 字段
  // const currency = orderSummary.value.currency || 'USD'
  // const amount = orderSummary.value.productAmount || '0.00'
  // return `${currency} ${amount}`
  
  // 【新逻辑】使用从SiteConfig读取的网站货币符号
  const amount = orderSummary.value.productAmount || '0.00'
  return `${siteCurrency.value} ${amount}`
})

// 费用明细（直接使用后端返回的数据）
const priceBreakdown = computed(() => {
  return orderSummary.value?.priceBreakdown || []
})

// 应付总额（直接使用后端返回的数据）
const totalAmount = computed(() => {
  if (!orderSummary.value) {
    console.log('⚠️ orderSummary 为空') // 调试日志
    return 'USD 0.00'
  }
  // 【原有显示逻辑 - 已注释】
  // 原逻辑：使用后端返回的 currency 字段
  // const currency = orderSummary.value.currency || 'USD'
  // const amount = orderSummary.value.totalAmount || '0.00'
  // console.log('✅ 计算总额:', `${currency} ${amount}`) // 调试日志
  // return `${currency} ${amount}`
  
  // 【新逻辑】使用从SiteConfig读取的网站货币符号
  const amount = orderSummary.value.totalAmount || '0.00'
  console.log('✅ 计算总额:', `${siteCurrency.value} ${amount}`) // 调试日志
  return `${siteCurrency.value} ${amount}`
})

const toggleSelectAll = async () => {
  const items = cartType.value === 'dropship' ? dropshipCartItems.value : wholesaleCartItems.value
  const ids = items.map(item => item.id)
  
  try {
    const params = {
      ids,
      isSelected: selectAll.value
    }
    
    // 先加密再签名
    const encryptedData = encryptionService.prepareData(params, true)
    const signedData = apiSignature.sign(encryptedData)

    const response = await fetch('/shop/api/cart/batch-select', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify(signedData)
    })
    
    const result = await response.json()
    
    if (result.success) {
      await loadCartData()
    }
  } catch (error) {
    console.error('批量选中失败:', error)
    showMessage('操作失败', 'error')
  }
}

const incrementQty = async (index) => {
  const items = cartType.value === 'dropship' ? dropshipCartItems.value : wholesaleCartItems.value
  const item = items[index]
  item.quantityError = '' // 清除错误提示
  await updateCartItem(item.id, { quantity: item.quantity + 1 })
}

const decrementQty = async (index) => {
  const items = cartType.value === 'dropship' ? dropshipCartItems.value : wholesaleCartItems.value
  const item = items[index]
  const minQty = item.minOrderQty || 1
  
  // 前端拦截：如果当前数量小于等于最小起订量，不允许减少
  if (item.quantity <= minQty) {
    item.quantityError = `最小起订数量为：${minQty}`
    showMessage(`最小起订数量为：${minQty}`, 'warning')
    return // 阻止调用后端 API
  }
  
  item.quantityError = '' // 清除错误提示
  await updateCartItem(item.id, { quantity: item.quantity - 1 })
}

const updateQuantity = async (index, qty) => {
  const items = cartType.value === 'dropship' ? dropshipCartItems.value : wholesaleCartItems.value
  const item = items[index]
  const minQty = item.minOrderQty || 1
  const newQty = Math.max(minQty, parseInt(qty) || minQty) // 确保不小于最小起订量
  
  // 如果输入的数量小于最小起订量，显示错误提示
  if (parseInt(qty) < minQty) {
    item.quantityError = `最小起订数量为：${minQty}`
    showMessage(`最小起订数量为：${minQty}`, 'warning')
    // 仍然调用API，但使用修正后的数量
  } else {
    item.quantityError = ''
  }
  
  await updateCartItem(item.id, { quantity: newQty })
}

// 更新购物车项
const updateCartItem = async (id, data) => {
  // 记录原始状态，用于失败时恢复
  const items = cartType.value === 'dropship' ? dropshipCartItems.value : wholesaleCartItems.value
  const item = items.find(i => i.id === id)
  const originalData = item ? { ...item } : null
  
  try {
    const params = {
      ...data
    }
    
    // 先加密再签名
    const encryptedData = encryptionService.prepareData(params, true)
    const signedData = apiSignature.sign(encryptedData)

    const response = await fetch(`/shop/api/cart/update/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify(signedData)
    })
    
    const result = await response.json()
    
    if (result.success) {
      // 成功后重新加载数据（会触发价格重新计算）
      await loadCartData()
    } else {
      // 处理后端返回的错误（包括最小起订量校验失败）
      const errorMsg = result.message || '更新失败'
      showMessage(errorMsg, 'error')
      
      // 如果是选中状态更新失败，恢复原始状态
      if (originalData && item) {
        item.selected = originalData.selected
      }
      
      // 重新加载数据以恢复原来的值
      await loadCartData()
    }
  } catch (error) {
    console.error('更新购物车失败:', error)
    showMessage('更新失败', 'error')
    
    // 如果是选中状态更新失败，恢复原始状态
    if (originalData && item) {
      item.selected = originalData.selected
    }
    
    // 重新加载数据以恢复原来的值
    await loadCartData()
  }
}

const removeItem = async (index) => {
  const items = cartType.value === 'dropship' ? dropshipCartItems.value : wholesaleCartItems.value
  const item = items[index]
  
  try {
    const params = {}
    
    // 先加密再签名
    const encryptedData = encryptionService.prepareData(params, true)
    const signedData = apiSignature.sign(encryptedData)

    const queryString = new URLSearchParams(signedData).toString()
    const response = await fetch(`/shop/api/cart/delete/${item.id}?${queryString}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include'
    })
    
    const result = await response.json()
    
    if (result.success) {
      showMessage('已删除')
      await loadCartData()
    }
  } catch (error) {
    console.error('删除失败:', error)
    showMessage('删除失败', 'error')
  }
}

const goHome = () => {
  window.location.href = '/'
}

// 跳转到商品详情页（新标签页打开）
const goToProductDetail = (productId) => {
  if (productId) {
    window.open(`/shop/item/${productId}`, '_blank')
  }
}

// 获取分组中选中的商品数量
const getSelectedCountInGroup = (group) => {
  return group.items.filter(item => item.selected).length
}

// 选中/取消选中分组（切换模式）
const selectGroup = async (group) => {
  const ids = group.items.map(item => item.id)
  
  // 判断当前分组是否全部选中：如果全部选中则取消，否则全选
  const allSelected = group.items.every(item => item.selected)
  const isSelected = !allSelected
  
  try {
    const params = {
      ids,
      isSelected
    }
    
    // 先加密再签名
    const encryptedData = encryptionService.prepareData(params, true)
    const signedData = apiSignature.sign(encryptedData)

    const response = await fetch('/shop/api/cart/batch-select', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify(signedData)
    })
    
    const result = await response.json()
    
    if (result.success) {
      await loadCartData()
    }
  } catch (error) {
    console.error('批量选中失败:', error)
    showMessage('操作失败', 'error')
  }
}

// 删除分组中选中的商品
const deleteSelectedInGroup = async (group) => {
  const ids = group.items.filter(item => item.selected).map(item => item.id)
  
  if (ids.length === 0) {
    showMessage('请先选择要删除的商品', 'warning')
    return
  }
  
  try {
    const params = {
      ids
    }
    
    // 先加密再签名
    const encryptedData = encryptionService.prepareData(params, true)
    const signedData = apiSignature.sign(encryptedData)

    const response = await fetch('/shop/api/cart/batch-delete', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify(signedData)
    })
    
    const result = await response.json()
    
    if (result.success) {
      showMessage(`已删除 ${result.data.deletedCount} 个商品`)
      await loadCartData()
    }
  } catch (error) {
    console.error('批量删除失败:', error)
    showMessage('删除失败', 'error')
  }
}

// 去结算（重新获取最新价格后再打开支付对话框）
const goToCheckout = async () => {
  const selected = cartItems.value.filter(item => item.selected && item.isAvailable)
  if (selected.length === 0) {
    showMessage('请先选择要结算的商品', 'warning')
    return
  }
  
  // ❗ 重要：点击结算时，重新调用后端获取最新价格
  console.log('📊 去结算前，重新获取最新价格...')
  loading.value = true
  try {
    await loadCartData() // 重新加载购物车数据，会更新 orderSummary
    console.log('✅ 最新价格获取成功:', orderSummary.value)
    // 打开支付方式对话框
    showPaymentModal.value = true
  } catch (error) {
    console.error('❌ 获取最新价格失败:', error)
    showMessage('获取最新价格失败，请重试', 'error')
  } finally {
    loading.value = false
  }
}

// 选中的商品数量
const selectedCount = computed(() => {
  return cartItems.value.filter(item => item.selected && item.isAvailable).length
})

// 支付对话框相关数据
const paymentModalData = computed(() => {
  const selected = cartItems.value.filter(item => item.selected && item.isAvailable)
  if (selected.length === 0 || !orderSummary.value) {
    return {
      productTitle: '',
      productTitleEn: '',
      productImage: '',
      quantity: 0,
      totalPrice: '',
      priceBreakdown: [],
      productList: null
    }
  }

  // 获取第一个商品的信息作为展示（单商品模式兼容）
  const firstItem = selected[0]
  const selectedQuantity = selected.reduce((sum, item) => sum + item.quantity, 0)
  
  // 构建价格明细数组
  const breakdown = []
  
  // 商品金额
  breakdown.push({
    label: '商品金额',
    amount: parseFloat(orderSummary.value.productAmount),
    // 【原有显示逻辑 - 已注释】原逻辑:使用后端返回的 currency 字段
    // currency: orderSummary.value.currency
    // 【新逻辑】使用从SiteConfig读取的网站货币符号
    currency: siteCurrency.value
  })
  
  // 从priceBreakdown中提取各项优惠
  if (orderSummary.value.priceBreakdown && orderSummary.value.priceBreakdown.length > 0) {
    orderSummary.value.priceBreakdown.forEach(item => {
      const amount = parseFloat(item.amount.replace(/[+-]/g, ''))
      breakdown.push({
        label: item.label,
        amount: item.amount.startsWith('-') ? -amount : amount,
        // 【原有显示逻辑 - 已注释】原逻辑:使用后端返回的 currency 字段
        // currency: item.currency
        // 【新逻辑】使用从SiteConfig读取的网站货币符号
        currency: siteCurrency.value
      })
    })
  }
  
  console.log('✅ 价格明细数据:', breakdown) // 调试日志
  
  // 构建商品列表（用于多商品折叠展示）
  const productList = selected.map(item => {
    // 使用商品的 subtotal（小计）作为价格
    const itemPrice = item.subtotal || 0
    return {
      title: item.nameCn || item.name,
      image: item.image,
      quantity: item.quantity,
      // 【原有显示逻辑 - 已注释】原逻辑:使用商品自带的 currency
      // price: `${item.currency} ${parseFloat(itemPrice).toFixed(2)}`
      // 【新逻辑】使用从SiteConfig读取的网站货币符号
      price: `${siteCurrency.value} ${parseFloat(itemPrice).toFixed(2)}`
    }
  })
  
  return {
    productTitle: selected.length > 1 
      ? `${firstItem.nameCn} 等${selected.length}件商品`
      : firstItem.nameCn,
    productTitleEn: selected.length > 1
      ? `${firstItem.name} and ${selected.length - 1} more items`
      : firstItem.name,
    productImage: firstItem.image,
    quantity: selectedQuantity,
    // 【原有显示逻辑 - 已注释】原逻辑:使用后端返回的 currency 字段
    // totalPrice: `${orderSummary.value.currency} ${orderSummary.value.totalAmount}`,
    // 【新逻辑】使用从SiteConfig读取的网站货币符号
    totalPrice: `${siteCurrency.value} ${orderSummary.value.totalAmount}`,
    priceBreakdown: breakdown,
    productList: productList  // 传递商品列表
  }
})

// 关闭支付对话框
const closePaymentModal = () => {
  showPaymentModal.value = false
}

// 确认支付
const confirmPayment = async (data) => {
  console.log('选择的地址ID:', data.addressId)
  
  // 获取地址ID
  const addressId = data.addressId
  
  // 关闭支付方式弹窗
  showPaymentModal.value = false
  
  // 步骤1：生成订单号
  const orderNo = 'ORD' + Date.now() + Math.random().toString(36).substr(2, 6).toUpperCase()
  
  // 步骤2：准备请求数据（不立即提交）
  const selectedItems = cartItems.value.filter(item => item.selected && item.isAvailable)
  
  // ❗ 重要：使用最新的 orderSummary 中的总价
  // orderSummary 在 goToCheckout() 时已经重新从后端获取，确保是最新价格
  const latestTotalAmount = parseFloat(orderSummary.value.totalAmount)
  const latestCurrency = orderSummary.value.currency
  
  console.log('📊 提交订单使用的价格:', {
    totalAmount: latestTotalAmount,
    currency: latestCurrency,
    orderSummary: orderSummary.value
  })
  
  // ❗ 重要：支付方式为空，等待订单生成后再填写
  const requestData = {
    orderNo: orderNo,
    businessType: cartType.value,
    items: selectedItems.map(item => ({
      productId: item.productId,
      sku: item.sku,
      quantity: item.quantity,
      region: item.region,
      businessType: cartType.value  // 添加业务类型，保证后端能正确验证价格
    })),
    paymentMethod: '',  // 支付方式留空
    customerId: store.state.user?.id,
    totalAmount: latestTotalAmount,  // 使用最新价格
    currency: latestCurrency,  // 使用最新货币
    addressId: addressId  // 添加地址ID
  }
  
  // 保存待提交的订单数据
  pendingOrderData.value = { orderNo, requestData }
  
  // 步骤3：显示订单状态监控弹窗（会立即建立 Mercure 连接）
  processingOrderNo.value = orderNo
  showOrderMonitor.value = true
  
  // 步骤4：等待 Mercure 连接就绪后，handleMercureReady 会被触发，然后才提交订单
  console.log('等待 Mercure 连接就绪...')
}

// 关闭订单监控弹窗
const handleOrderMonitorClose = () => {
  console.log('🚪 关闭订单监控弹窗')
  showOrderMonitor.value = false
  
  // 延迟清空所有状态，避免关闭动画时看到状态变化
  setTimeout(() => {
    console.log('🧹 清空订单相关状态')
    processingOrderNo.value = ''
    pendingOrderData.value = null
    // OrderStatusMonitor 组件会在自己的 close() 方法中调用 cleanupConnection()
  }, 300)
}

// Mercure 连接就绪后的回调
const handleMercureReady = async () => {
  console.log('🔌 === handleMercureReady 开始执行 ===')
  console.log('🔌 Mercure 连接已就绪，开始提交订单')
  
  if (!pendingOrderData.value) {
    console.warn('❌ 没有待提交的订单数据')
    return
  }
  
  const { orderNo, requestData } = pendingOrderData.value
  console.log('🔌 订单号:', orderNo)
  console.log('🔌 原始请求数据:', requestData)
  
  try {
    // 使用加密服务加密整个JSON对象
    console.log('🔌 开始加密请求数据...')
    const encryptedData = encryptionService.prepareData(requestData, true)
    console.log('🔌 加密后数据:', encryptedData)
    
    // 生成API签名
    console.log('🔌 生成API签名...')
    const signedData = apiSignature.sign(encryptedData)
    console.log('🔌 签名后数据:', signedData)
    
    console.log('🔌 发送购物车结算请求（加密+签名）:', signedData)
    
    // 调用后端 API
    console.log('🔌 开始调用 /shop/api/cart/checkout')
    const response = await fetch('/shop/api/cart/checkout', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      credentials: 'include',
      body: JSON.stringify(signedData)
    })
    
    console.log('🔌 响应状态:', response.status, response.statusText)
    const result = await response.json()
    console.log('🔌 后端返回结果:', result)
    
    if (!result.success) {
      // 订单创建失败
      console.error('❌ 订单创建失败:', result)
      showOrderMonitor.value = false
      processingOrderNo.value = ''
      pendingOrderData.value = null
      
      ElMessage.error(result.message || '结算失败，请重试')
      console.error('❌ 订单创建失败:', result)
    } else {
      console.log('✅ 订单创建成功，等待 Mercure 消息更新状态')
    }
    // 成功的话，等待 Mercure 消息更新状态
    
    // 清空待提交数据
    pendingOrderData.value = null
    console.log('🔌 === handleMercureReady 执行结束 ===')
    
  } catch (error) {
    console.error('❌ 提交订单失败:', error)
    console.error('❌ 异常堆栈:', error.stack)
    
    showOrderMonitor.value = false
    processingOrderNo.value = ''
    pendingOrderData.value = null
    ElMessage.error('网络错误，请重试')
  }
}

// 重试支付
const handleRetryPayment = () => {
  console.log('🔄 重新支付')
  showOrderMonitor.value = false
  
  setTimeout(() => {
    console.log('🧹 清空订单状态，准备重新支付')
    processingOrderNo.value = ''
    pendingOrderData.value = null
    showPaymentModal.value = true // 重新打开支付方式对话框
  }, 300)
}

// 查看订单
const handleViewOrder = () => {
  console.log('📋 查看订单')
  showOrderMonitor.value = false
  
  // 清空状态后跳转
  setTimeout(() => {
    processingOrderNo.value = ''
    pendingOrderData.value = null
    // 跳转到订单详情页
    window.location.href = '/user/orders'
  }, 100)
}

// 继续购物
const handleContinueShopping = () => {
  console.log('🛍️ 继续购物')
  showOrderMonitor.value = false
  
  setTimeout(() => {
    console.log('🧹 清空订单状态')
    processingOrderNo.value = ''
    pendingOrderData.value = null
    // 刷新购物车数据
    loadCartData()
  }, 300)
}

// 支付成功后的处理
const handlePaymentSuccess = async () => {
  console.log('🎉 支付成功，刷新购物车')
  
  // 关闭监控弹窗
  showOrderMonitor.value = false
  
  // 清空状态
  setTimeout(() => {
    processingOrderNo.value = ''
    pendingOrderData.value = null
  }, 300)
  
  // 注意：不在这里显示成功提示，因为 OrderStatusMonitor 组件已经显示了
  
  // 重新加载购物车数据
  await loadCartData()
}
</script>

<style scoped>
input[type='number']::-webkit-outer-spin-button,
input[type='number']::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type='number'] {
  -moz-appearance: textfield;
}
</style>
