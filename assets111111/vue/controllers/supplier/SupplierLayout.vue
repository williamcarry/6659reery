<template>
  <el-container class="supplier-layout">
    <!-- 顶部 Banner -->
    <el-header class="supplier-header">
      <div class="header-content">
        <div class="logo">
          <h1>{{ headerTitle }}<span v-if="customerId" class="customer-id-badge">{{ customerId }}</span></h1>
        </div>
        <div class="supplier-info" @click="editProfile" v-if="hasSupplierSuperRole">
          <span style="display: inline-block;margin-right: 10px;">欢迎，{{ supplierName }}!</span>
          <el-button class="logout-btn" @click.stop="logout">退出</el-button>
        </div>
        <div class="supplier-info-no-click" v-else>
          <span style="display: inline-block;margin-right: 10px;">欢迎，{{ supplierName }}!</span>
          <el-button class="logout-btn" @click.stop="logout">退出</el-button>
        </div>
      </div>
    </el-header>
    
    <supplier-sidebar 
      @navigate="handleNavigation" 
      :has-supplier-super-role="hasSupplierSuperRole"
      :has-supplier-balance-role="hasSupplierBalanceRole"
      :has-supplier-product-role="hasSupplierProductRole"
    />
    
    <el-container class="content-container">
      <el-header class="tags-view">
        <el-tag
          v-for="tag in tags"
          :key="tag.key"
          :type="activeTag === tag.key ? 'success' : 'info'"
          :closable="tag.key !== 'dashboard'"
          @click="switchToTab(tag.key)"
          @close="closeTab(tag.key)"
          class="tag-item"
        >
          {{ tag.title }}
        </el-tag>
      </el-header>
      
      <el-main class="content-wrapper">
        <!-- 主页内容 -->
        <div :class="['content-tab', { 'active': activeTag === 'dashboard' }]" id="dashboard-tab">
          <div class="dashboard-content">
            <h2>欢迎，{{ supplierName }}!</h2>
            
            <!-- 供应商数据概览 -->
            <supplier-dashboard-component 
              ref="supplierDashboard"
              :supplier-login-path="supplierLoginPath"
              :auto-load="true"
            />
            
            <!-- 销售与财务统计 -->
            <div style="margin-top: 20px">
              <el-tabs type="border-card" class="stats-tabs" @tab-click="handleTabClick" v-model="activeStatsTab">
                <el-tab-pane label="销售统计" name="sales" :lazy="false">
                  <sales-stats 
                    ref="salesStats"
                    :supplier-login-path="supplierLoginPath"
                    :auto-load="true"
                  />
                </el-tab-pane>
                
                <el-tab-pane label="财务统计" name="finance" :lazy="false">
                  <finance-stats 
                    ref="financeStats"
                    :supplier-login-path="supplierLoginPath"
                    :auto-load="false"
                  />
                </el-tab-pane>
              </el-tabs>
            </div>
          </div>
        </div>
        
        <!-- 个人信息 -->
        <div :class="['content-tab', { 'active': activeTag === 'profile-edit' }]" id="profile-edit-tab" v-if="hasSupplierSuperRole">
          <supplier-profile-edit 
            :supplier-login-path="supplierLoginPath"
            ref="profileEdit"
            :auto-load="false"
          />
        </div>

        <!-- 子账号列表 -->
        <div :class="['content-tab', { 'active': activeTag === 'sub-account-list' }]" id="sub-account-list-tab" v-if="hasSupplierSuperRole">
          <supplier-sub-account-list 
            :supplier-login-path="supplierLoginPath" 
            ref="subAccountList" 
            :auto-load="false" 
          />
        </div>
        
        <!-- 余额&VIP -->
        <div :class="['content-tab', { 'active': activeTag === 'balance-vip' }]" id="balance-vip-tab" v-if="hasSupplierSuperRole || hasSupplierBalanceRole">
          <balance-vip 
            :supplier-login-path="supplierLoginPath" 
            ref="balanceVip" 
            :auto-load="false" 
          />
        </div>
        
        <!-- 余额记录 -->
        <div :class="['content-tab', { 'active': activeTag === 'balance-history-list' }]" id="balance-history-list-tab" v-if="hasSupplierSuperRole || hasSupplierBalanceRole">
          <balance-history-list 
            :supplier-login-path="supplierLoginPath" 
            ref="balanceHistoryList" 
            :auto-load="false" 
          />
        </div>
        
        <!-- 充值记录 -->
        <div :class="['content-tab', { 'active': activeTag === 'recharge-list' }]" id="recharge-list-tab" v-if="hasSupplierSuperRole || hasSupplierBalanceRole">
          <recharge-list 
            :supplier-login-path="supplierLoginPath" 
            ref="rechargeList" 
            :auto-load="false" 
          />
        </div>
        
        <!-- 提现申请 -->
        <div :class="['content-tab', { 'active': activeTag === 'withdrawal-list' }]" id="withdrawal-list-tab" v-if="hasSupplierSuperRole || hasSupplierBalanceRole">
          <withdrawal-list 
            :supplier-login-path="supplierLoginPath" 
            ref="withdrawalList" 
            :auto-load="false" 
          />
        </div>
        
        <!-- 商品列表 -->
        <div :class="['content-tab', { 'active': activeTag === 'product-list' }]" id="product-list-tab" v-if="hasSupplierSuperRole || hasSupplierProductRole">
          <product-list 
            :supplier-login-path="supplierLoginPath" 
            ref="productList" 
            :auto-load="false" 
          />
        </div>
        
        <!-- 添加商品 -->
        <div :class="['content-tab', { 'active': activeTag === 'product-add' }]" id="product-add-tab" v-if="hasSupplierSuperRole || hasSupplierProductRole">
          <product-add 
            :supplier-login-path="supplierLoginPath" 
            ref="productAdd" 
            :auto-load="false" 
          />
        </div>
        
        <!-- 编辑商品 -->
        <div :class="['content-tab', { 'active': activeTag === 'product-edit' }]" id="product-edit-tab" v-if="hasSupplierSuperRole || hasSupplierProductRole">
          <product-edit 
            :supplier-login-path="supplierLoginPath" 
            :product-id="editingProductId"
            ref="productEdit" 
            :auto-load="false" 
          />
        </div>
        
        <!-- 地址管理 -->
        <div :class="['content-tab', { 'active': activeTag === 'address-list' }]" id="address-list-tab" v-if="hasSupplierSuperRole || hasSupplierProductRole">
          <address-list 
            :supplier-login-path="supplierLoginPath" 
            ref="addressList" 
            :auto-load="false" 
          />
        </div>
        
        <!-- 订单列表 -->
        <div :class="['content-tab', { 'active': activeTag === 'order-list' }]" id="order-list-tab" v-if="hasSupplierSuperRole || hasSupplierOrderRole">
          <order-list 
            :supplier-login-path="supplierLoginPath" 
            ref="orderList" 
            :auto-load="false" 
          />
        </div>
        
        <!-- 订单详情 -->
        <div :class="['content-tab', { 'active': activeTag === 'order-detail' }]" id="order-detail-tab" v-if="hasSupplierSuperRole || hasSupplierOrderRole">
          <order-detail-tab 
            :supplier-login-path="supplierLoginPath" 
            :order-id="currentOrderId"
            ref="orderDetail" 
            :auto-load="false" 
          />
        </div>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import SupplierSidebar from './SupplierSidebar.vue'
import SupplierProfileEdit from './SupplierProfileEdit.vue'
import SupplierSubAccountList from './SupplierSubAccountList.vue'
import BalanceHistoryList from './BalanceHistoryList.vue'
import BalanceVip from './BalanceVip.vue'
import RechargeList from './RechargeList.vue'
import WithdrawalList from './WithdrawalList.vue'
import ProductList from './ProductList.vue'
import ProductAdd from './ProductAdd.vue'
import ProductEdit from './ProductEdit.vue'
import AddressList from './AddressList.vue'
import OrderList from './OrderList.vue'
import OrderDetailTab from './OrderDetailTab.vue'
import SupplierDashboardComponent from './SupplierDashboard.vue'
import SalesStats from './SalesStats.vue'
import FinanceStats from './FinanceStats.vue'
import {
  ElContainer,
  ElHeader,
  ElMain,
  ElTag,
  ElButton,
  ElTabs,
  ElTabPane
} from 'element-plus'

export default {
  name: 'SupplierLayout',
  components: {
    SupplierSidebar,
    SupplierProfileEdit,
    SupplierSubAccountList,
    BalanceHistoryList,
    BalanceVip,
    RechargeList,
    WithdrawalList,
    ProductList,
    ProductAdd,
    ProductEdit,
    AddressList,
    OrderList,
    OrderDetailTab,
    SupplierDashboardComponent,
    SalesStats,
    FinanceStats,
    ElContainer,
    ElHeader,
    ElMain,
    ElTag,
    ElButton,
    ElTabs,
    ElTabPane
  },
  props: {
    currentSupplier: {
      type: Object,
      default: () => ({
        username: '',
        email: '',
        contactPerson: '',
        companyName: '',
        customerId: ''
      })
    },
    supplierLoginPath: {
      type: String,
      default: ''
    },
    // 添加供应商超级角色属性
    hasSupplierSuperRole: {
      type: Boolean,
      default: false
    },
    // 添加供应商余额角色属性
    hasSupplierBalanceRole: {
      type: Boolean,
      default: false
    },
    // 添加供应商商品角色属性
    hasSupplierProductRole: {
      type: Boolean,
      default: false
    },
    // 添加供应商订单角色属性
    hasSupplierOrderRole: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      headerTitle: '供应商后台',
      customerId: '', // 客户ID
      activeTag: 'dashboard',
      activeStatsTab: 'sales',
      supplierName: '', // 默认为空
      editingProductId: null, // 用于编辑商品的ID
      currentOrderId: null, // 当前查看的订单ID
      tags: [
        { key: 'dashboard', title: '主页' }
      ],
      tagTitles: {
        'dashboard': '主页',
        'profile-edit': '个人信息',
        'product-list': '商品列表',
        'product-add': '添加商品',
        'product-edit': '编辑商品',
        'sub-account-list': '子账号列表',
        'balance-vip': '余额&VIP',
        'balance-history-list': '余额记录',
        'recharge-list': '充值记录',
        'withdrawal-list': '提现申请',
        'address-list': '地址管理',
        'order-list': '订单列表',
        'order-detail': '订单详情'
      }
    }
  },
  methods: {
    handleNavigation(key, keyPath) {
      console.log('Navigation triggered with key:', key); // 调试信息
      // 添加标签页
      this.addTab(key);
      
      // 切换到该标签页
      this.switchToTab(key);
      
      // 根据标签页类型加载相应数据
      this.loadTabData(key);
    },
    
    addTab(key) {
      console.log('Adding tab with key:', key); // 调试信息
      // 如果标签页已存在，直接返回
      if (this.tags.some(tag => tag.key === key)) {
        console.log('Tab already exists:', key); // 调试信息
        return;
      }
      
      // 添加新标签页
      this.tags.push({
        key: key,
        title: this.tagTitles[key] || key
      });
      
      console.log('Added new tab:', key, 'Updated tags:', this.tags); // 调试信息
      
      // 强制更新以确保视图刷新
      this.$forceUpdate();
    },
    
    // 根据标签页类型加载数据
    loadTabData(key) {
      // 可以在这里添加按需加载数据的逻辑
      // 例如，对于需要从后端获取数据的标签页，可以在这里添加相应的加载逻辑
      switch (key) {
        case 'dashboard':
          // 刷新主页统计数据
          if (this.$refs.supplierDashboard) {
            this.$refs.supplierDashboard.loadData();
          }
          if (this.$refs.salesStats) {
            this.$refs.salesStats.loadData();
          }
          if (this.$refs.financeStats) {
            this.$refs.financeStats.loadData();
          }
          break;
        case 'profile-edit':
          // 按需加载个人信息数据
          if (this.$refs.profileEdit && this.hasSupplierSuperRole) {
            this.$refs.profileEdit.loadProfileData();
          }
          break;
        case 'sub-account-list':
          // 按需加载子账号列表数据
          if (this.$refs.subAccountList && this.hasSupplierSuperRole) {
            this.$refs.subAccountList.loadSubAccountData();
          }
          break;
        case 'balance-vip':
          // 按需加载余额&VIP数据
          if (this.$refs.balanceVip && (this.hasSupplierSuperRole || this.hasSupplierBalanceRole)) {
            this.$refs.balanceVip.loadBalanceVipData();
          }
          break;
        case 'balance-history-list':
          // 按需加载余额记录数据
          if (this.$refs.balanceHistoryList && (this.hasSupplierSuperRole || this.hasSupplierBalanceRole)) {
            this.$refs.balanceHistoryList.loadBalanceHistoryData();
          }
          break;
        case 'recharge-list':
          // 按需加载充值记录数据
          if (this.$refs.rechargeList && (this.hasSupplierSuperRole || this.hasSupplierBalanceRole)) {
            this.$refs.rechargeList.loadRechargeData();
          }
          break;
        case 'withdrawal-list':
          // 按需加载提现申请数据
          if (this.$refs.withdrawalList && (this.hasSupplierSuperRole || this.hasSupplierBalanceRole)) {
            this.$refs.withdrawalList.loadWithdrawalData();
          }
          break;
        case 'product-list':
          // 按需加载商品列表数据
          if (this.$refs.productList && (this.hasSupplierSuperRole || this.hasSupplierProductRole)) {
            this.$refs.productList.loadProductData();
            this.$refs.productList.loadStatistics();
          }
          break;
        case 'product-add':
          // 按需加载添加商品数据（初始化分类等）
          if (this.$refs.productAdd && (this.hasSupplierSuperRole || this.hasSupplierProductRole)) {
            this.$refs.productAdd.initData();
          }
          break;
        case 'product-edit':
          // 按需加载编辑商品数据
          console.log('Loading product edit data, refs:', this.$refs); // 调试信息
          if (this.$refs.productEdit && (this.hasSupplierSuperRole || this.hasSupplierProductRole)) {
            console.log('ProductEdit component found, calling initData'); // 调试信息
            // 检查initData方法是否存在
            if (typeof this.$refs.productEdit.initData === 'function') {
              this.$refs.productEdit.initData();
            } else {
              console.error('ProductEdit component does not have initData method'); // 调试信息
            }
          } else {
            console.log('ProductEdit component not found or user lacks permissions'); // 调试信息
          }
          break;
        case 'address-list':
          // 按需加载地址列表数据
          if (this.$refs.addressList && (this.hasSupplierSuperRole || this.hasSupplierProductRole)) {
            this.$refs.addressList.loadAddressData();
          }
          break;
        case 'order-list':
          // 按需加载订单列表数据
          if (this.$refs.orderList && (this.hasSupplierSuperRole || this.hasSupplierOrderRole)) {
            this.$refs.orderList.loadOrderData();
          }
          break;
        case 'order-detail':
          // 按需加载订单详情数据
          if (this.$refs.orderDetail && (this.hasSupplierSuperRole || this.hasSupplierOrderRole)) {
            this.$refs.orderDetail.initData();
          }
          break;
        default:
          // 其他标签页不需要预加载数据
          break;
      }
    },
    
    switchToTab(key) {
      console.log('Switching to tab:', key); // 调试信息
      this.activeTag = key;
      console.log('Active tab is now:', this.activeTag); // 调试信息
      
      // 强制更新以确保视图刷新
      this.$forceUpdate();
    },
    
    closeTab(key) {
      // 不能关闭主页标签
      if (key === 'dashboard') {
        return;
      }
      
      // 找到要关闭的标签索引
      const index = this.tags.findIndex(tag => tag.key === key);
      if (index === -1) {
        return;
      }
      
      // 删除标签
      this.tags.splice(index, 1);
      
      // 如果关闭的是当前激活的标签，则切换到合适的标签页
      if (this.activeTag === key) {
        // 特殊处理：如果关闭的是商品编辑页，则返回商品列表
        if (key === 'product-edit') {
          // 检查商品列表标签是否存在
          const productListExists = this.tags.some(tag => tag.key === 'product-list');
          if (productListExists) {
            this.activeTag = 'product-list';
          } else {
            // 如果商品列表标签不存在，则切换到主页
            this.activeTag = 'dashboard';
          }
        } else if (key === 'product-add') {
          // 特殊处理：如果关闭的是添加商品页，也返回商品列表
          const productListExists = this.tags.some(tag => tag.key === 'product-list');
          if (productListExists) {
            this.activeTag = 'product-list';
          } else {
            this.activeTag = 'dashboard';
          }
        } else if (key === 'order-detail') {
          // 特殊处理：如果关闭的是订单详情页，则返回订单列表
          const orderListExists = this.tags.some(tag => tag.key === 'order-list');
          if (orderListExists) {
            this.activeTag = 'order-list';
          } else {
            this.activeTag = 'dashboard';
          }
        } else {
          // 其他情况，切换到主页
          this.activeTag = 'dashboard';
        }
      }
      
      // 强制更新以确保视图刷新
      this.$forceUpdate();
    },
    
    logout() {
      // 实现退出登录逻辑
      window.location.href = '/logout'; // 需要根据实际的退出登录路由调整
    },
    
    editProfile() {
      // 只有具有 ROLE_SUPPLIER_SUPER 权限的用户才能编辑个人信息
      if (this.hasSupplierSuperRole) {
        // 添加个人信息标签页并切换到该标签页
        this.addTab('profile-edit');
        this.switchToTab('profile-edit');
        // 加载数据
        this.loadTabData('profile-edit');
      }
    },
    
    // 处理统计Tab切换
    handleTabClick(tab) {
      if (tab.paneName === 'sales' && this.$refs.salesStats) {
        // 切换到销售统计时，延迟50ms后重新加载数据，确保Tab已完全显示
        setTimeout(() => {
          if (this.$refs.salesStats) {
            this.$refs.salesStats.loadData()
          }
        }, 50)
      } else if (tab.paneName === 'finance' && this.$refs.financeStats) {
        // 切换到财务统计时，延迟50ms后加载数据
        setTimeout(() => {
          if (this.$refs.financeStats) {
            this.$refs.financeStats.loadData()
          }
        }, 50)
      }
    }
  },
  mounted() {
    // 从props中获取当前供应商信息
    // 设置显示的供应商名，明确使用username字段
    this.supplierName = this.currentSupplier.username || '';
    
    // 设置客户ID
    this.customerId = this.currentSupplier.customerId || '';
    
    // 如果仍然没有供应商名，则使用默认值
    if (!this.supplierName) {
      this.supplierName = '供应商';
    }
    
    // 设置全局supplierLoginPath变量
    if (this.supplierLoginPath) {
      window.supplierLoginPath = this.supplierLoginPath;
    }
    
    // 监听navigate-to事件
    window.addEventListener('navigate-to', (event) => {
      const { key, params } = event.detail;
      
      // 特殊处理编辑商品事件
      if (key === 'product-edit' && params && params.id) {
        // 设置要编辑的商品ID
        this.editingProductId = params.id;
        
        // 添加并切换到编辑商品标签页
        this.addTab('product-edit');
        this.switchToTab('product-edit');
        
        // 使用setTimeout确保DOM更新完成后再加载数据
        setTimeout(() => {
          // 加载数据
          this.loadTabData('product-edit');
        }, 100);
      } else {
        // 处理其他导航事件
        this.handleNavigation(key);
      }
    });
    
    // 监听关闭当前标签页事件
    window.addEventListener('close-current-tab', () => {
      // 关闭当前激活的标签页
      this.closeTab(this.activeTag);
    });
    
    // 监听查看订单详情事件
    window.addEventListener('navigate-to-order-detail', (event) => {
      // 支持传入 orderId 或 orderNo
      const orderId = event.detail.orderId;
      const orderNo = event.detail.orderNo;
      
      if (orderNo) {
        // 如果传入的是订单号，先切换到订单列表并搜索
        this.addTab('order-list');
        this.switchToTab('order-list');
        this.$nextTick(() => {
          if (this.$refs.orderList) {
            // 设置搜索条件为订单号并搜索
            this.$refs.orderList.searchByOrderNo(orderNo);
          }
        });
      } else if (orderId) {
        // 如果传入的是订单ID（兼容旧逻辑）
        this.currentOrderId = orderId;
        this.addTab('order-detail');
        this.switchToTab('order-detail');
        this.$nextTick(() => {
          this.loadTabData('order-detail');
        });
      }
    });
  }
}
</script>

<style scoped>
.supplier-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100vw;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

.supplier-header {
  background-color: #8268BF;
  color: white;
  padding: 0 20px;
  height: 60px;
  line-height: 60px;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  border-bottom: 1px solid #6a5a9e;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo h1 {
  margin: 0;
  font-size: 20px;
  font-weight: normal;
}

.customer-id-badge {
  margin-left: 10px;
  padding: 2px 8px;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  font-size: 14px;
  font-weight: normal;
}

.supplier-info {
  display: flex;
  align-items: center;
  gap: 15px;
  cursor: pointer; /* 手型光标 */
}

.supplier-info-no-click {
  display: flex;
  align-items: center;
  gap: 15px;
}

.supplier-info span {
  font-size: 14px;
  text-decoration: underline; /* 下划线 */
}

.supplier-info:hover span {
  background: rgba(255, 255, 255, 0.1);
}

/* 退出按钮样式 */
.logout-btn {
  background-color: #e67e22;
  border-color: #e67e22;
  color: white;
  padding: 5px 10px;
  font-size: 12px;
  border-radius: 3px;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background-color: #d35400;
  border-color: #d35400;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.logout-btn:active {
  transform: translateY(0);
}

.content-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  margin-left: 200px;
  margin-top: 60px;
  height: calc(100vh - 60px);
}

.tags-view {
  background: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
  padding: 0.25rem 0.5rem;
  font-size: 12px;
  flex-shrink: 0;
  position: fixed;
  top: 60px;
  left: 200px;
  right: 0;
  height: 40px;
  z-index: 999;
  overflow-x: auto;
  display: flex;
  align-items: center;
}

.tag-item {
  margin-right: 0.25rem;
  cursor: pointer;
}

.content-wrapper {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  background: #ffffff;
  margin-top: 40px;
  height: calc(100vh - 100px);
}

.content-tab {
  display: none;
}

.content-tab.active {
  display: block;
}

/* 统计Tabs样式优化 */
.stats-tabs :deep(.el-tabs__item) {
  padding: 0 30px !important;
  font-size: 15px;
  font-weight: 500;
}

.stats-tabs :deep(.el-tabs__nav) {
  margin-left: 10px;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .content-container {
    margin-left: 60px;
  }
  
  .tags-view {
    left: 60px;
  }
}
</style>