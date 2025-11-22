<template>
  <div class="supplier-sidebar" ref="sidebar">
    <div class="scroll-hint" v-show="showScrollHint"></div>
    <el-menu
      :default-active="activeIndex"
      class="nav-menu"
      @select="handleSelect"
      :unique-opened="true"
      background-color="#7a5aa5"
      text-color="#e6e6e6"
      active-text-color="#FFD700"
    >
      <!-- 主页 -->
      <el-menu-item index="dashboard">
        <el-icon><House /></el-icon>
        <span>主页</span>
      </el-menu-item>
      
      <!-- 个人信息 -->
      <el-menu-item index="profile-edit" v-if="hasSupplierSuperRole">
        <el-icon><User /></el-icon>
        <span>个人信息</span>
      </el-menu-item>
      <!-- 子账号管理 -->
      <el-sub-menu index="sub-account" v-if="hasSupplierSuperRole">
        <template #title>
          <el-icon><UserFilled /></el-icon>
          <span>子账号管理</span>
        </template>
        <el-menu-item index="sub-account-list">
          <span>子账号列表</span>
        </el-menu-item>
      </el-sub-menu>
      <!-- 商品管理 -->
      <el-sub-menu index="product" v-if="hasSupplierSuperRole || hasSupplierProductRole">
        <template #title>
          <el-icon><Box /></el-icon>
          <span>商品管理</span>
        </template>
        <el-menu-item index="product-list">
          <span>商品列表</span>
        </el-menu-item>
        <el-menu-item index="product-add">
          <span>添加商品</span>
        </el-menu-item>
        <!-- 地址管理 -->
        <el-menu-item index="address-list">
          <span>地址管理</span>
        </el-menu-item>
      </el-sub-menu>
      <!-- 财务与VIP -->
      <el-sub-menu index="finance-vip" v-if="hasSupplierSuperRole || hasSupplierBalanceRole">
        <template #title>
          <el-icon><List /></el-icon>
          <span>财务与VIP</span>
        </template>
        <el-menu-item index="balance-vip">
          <span>余额&VIP</span>
        </el-menu-item>
        <el-menu-item index="balance-history-list">
          <span>余额记录</span>
        </el-menu-item>
        <el-menu-item index="recharge-list">
          <span>充值记录</span>
        </el-menu-item>
        <el-menu-item index="withdrawal-list">
          <span>提现申请</span>
        </el-menu-item>
      </el-sub-menu>
      
      <!-- 订单管理 -->
      <el-sub-menu index="order" v-if="hasSupplierSuperRole || hasSupplierOrderRole">
        <template #title>
          <el-icon><ShoppingCart /></el-icon>
          <span>订单管理</span>
        </template>
        <el-menu-item index="order-list">
          <span>订单列表</span>
        </el-menu-item>
      </el-sub-menu>
      
    </el-menu>
  </div>
</template>

<script>
import { 
  House, 
  Box, 
  Document, 
  List, 
  TrendCharts, 
  User,
  UserFilled,
  ShoppingCart
} from '@element-plus/icons-vue'
import {
  ElMenu,
  ElMenuItem,
  ElSubMenu,
  ElIcon
} from 'element-plus'

export default {
  name: 'SupplierSidebar',
  components: {
    House,
    Box,
    Document,
    List,
    TrendCharts,
    User,
    UserFilled,
    ShoppingCart,
    ElMenu,
    ElMenuItem,
    ElSubMenu,
    ElIcon
  },
  props: {
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
      activeIndex: 'dashboard',
      showScrollHint: false
    }
  },
  methods: {
    handleSelect(key, keyPath) {
      // 触发自定义事件，让父组件处理导航逻辑
      this.$emit('navigate', key, keyPath);
      
      // 更新激活状态
      this.activeIndex = key;
    },
    checkOverflow() {
      const sidebar = this.$refs.sidebar;
      if (sidebar) {
        // 检查内容是否溢出
        this.showScrollHint = sidebar.scrollHeight > sidebar.clientHeight;
      }
    }
  },
  mounted() {
    // 监听来自其他组件的导航事件
    window.addEventListener('navigate-to', (event) => {
      this.activeIndex = event.detail.key;
    });
    
    // 检查初始溢出状态
    this.checkOverflow();
    
    // 监听窗口大小变化
    window.addEventListener('resize', this.checkOverflow);
    
    // 使用 MutationObserver 监听内容变化
    const observer = new MutationObserver(this.checkOverflow);
    observer.observe(this.$refs.sidebar, {
      childList: true,
      subtree: true
    });
    
    // 保存观察器引用以便销毁
    this.observer = observer;
  },
  beforeUnmount() {
    // 清理事件监听器
    window.removeEventListener('resize', this.checkOverflow);
    
    // 断开观察器连接
    if (this.observer) {
      this.observer.disconnect();
    }
  }
}
</script>

<style scoped>
.supplier-sidebar {
  width: 200px;
  background: #7a5aa5;
  color: white;
  overflow-y: auto;
  font-size: 14px;
  flex-shrink: 0;
  position: fixed;
  top: 60px;
  left: 0;
  bottom: 0;
  height: calc(100vh - 60px);
  
  /* 自定义滚动条样式 */
  scrollbar-width: thin;
  scrollbar-color: #FFD700 #7a5aa5;
}

.supplier-sidebar::-webkit-scrollbar {
  width: 3px;
}

.supplier-sidebar::-webkit-scrollbar-track {
  background: #7a5aa5;
}

.supplier-sidebar::-webkit-scrollbar-thumb {
  background-color: #FFD700;
  border-radius: 2px;
}

.supplier-sidebar::-webkit-scrollbar-thumb:hover {
  background-color: #e6c100;
}

/* 菜单项基础样式 */
.nav-menu :deep(.el-menu-item) {
  background-color: #7a5aa5 !important;
  color: #e6e6e6 !important;
  height: 45px;
  line-height: 45px;
  transition: all 0.3s ease;
}

/* 菜单项悬停效果 */
.nav-menu :deep(.el-menu-item:hover) {
  background-color: #8268bf !important;
  color: #ffffff !important;
}

/* 菜单项激活状态样式（移除左边框） */
.nav-menu :deep(.el-menu-item.is-active) {
  background-color: #8268bf !important;
  color: #FFD700 !important;
  border-left: none !important; /* 移除左边框 */
}

/* 子菜单标题基础样式 */
.nav-menu :deep(.el-sub-menu__title) {
  background-color: #7a5aa5 !important;
  color: #e6e6e6 !important;
  height: 45px;
  line-height: 45px;
  transition: all 0.3s ease;
}

/* 子菜单标题悬停效果 */
.nav-menu :deep(.el-sub-menu__title:hover) {
  background-color: #8268bf !important;
  color: #ffffff !important;
}

/* 子菜单展开状态标题样式 */
.nav-menu :deep(.el-sub-menu.is-opened .el-sub-menu__title) {
  background-color: #8268bf !important;
  color: #FFD700 !important;
  border-left: none !important; /* 移除左边框 */
}

/* 子菜单激活状态标题样式 */
.nav-menu :deep(.el-sub-menu.is-active .el-sub-menu__title) {
  background-color: #8268bf !important;
  color: #FFD700 !important;
  border-left: none !important; /* 移除左边框 */
}

/* 子菜单滚动样式 */
.nav-menu :deep(.el-menu--inline) {
  max-height: 300px;
  overflow-y: auto;
  /* 美化滚动条 */
  scrollbar-width: thin;
  scrollbar-color: #FFD700 #7a5aa5;
  background-color: #8268bf !important;
}

.nav-menu :deep(.el-menu--inline::-webkit-scrollbar) {
  width: 4px;
}

.nav-menu :deep(.el-menu--inline::-webkit-scrollbar-track) {
  background: #7a5aa5;
}

.nav-menu :deep(.el-menu--inline::-webkit-scrollbar-thumb) {
  background-color: #FFD700;
  border-radius: 2px;
}

.nav-menu :deep(.el-menu--inline::-webkit-scrollbar-thumb:hover) {
  background-color: #e6c100;
}

/* 子菜单项样式 */
.nav-menu :deep(.el-menu--inline .el-menu-item) {
  background-color: #8268bf !important;
  color: #e6e6e6 !important;
  height: 40px;
  line-height: 40px;
  padding-left: 48px !important;
}

/* 子菜单项悬停效果 */
.nav-menu :deep(.el-menu--inline .el-menu-item:hover) {
  background-color: #8a75c7 !important;
  color: #ffffff !important;
}

/* 子菜单项激活状态样式 */
.nav-menu :deep(.el-menu--inline .el-menu-item.is-active) {
  background-color: #8a75c7 !important;
  color: #FFD700 !important;
  border-left: none !important; /* 移除左边框 */
}

/* 滚动提示 */
.scroll-hint {
  position: absolute;
  right: 5px;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 30px;
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
  opacity: 0;
  transition: opacity 0.3s;
  pointer-events: none;
  z-index: 100;
}

.supplier-sidebar:hover .scroll-hint {
  opacity: 1;
}

.nav-menu {
  border-right: none;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .supplier-sidebar {
    width: 60px;
  }
  
  :deep(.el-menu--collapse) {
    width: 60px;
  }
  
  :deep(.el-menu--collapse .el-sub-menu__title span),
  :deep(.el-menu--collapse .el-menu-item span) {
    display: none;
  }
  
  :deep(.el-menu--collapse .el-sub-menu__title .el-sub-menu__icon-arrow),
  :deep(.el-menu--collapse .el-menu-item .el-icon) {
    margin-right: 0;
  }
}
</style>