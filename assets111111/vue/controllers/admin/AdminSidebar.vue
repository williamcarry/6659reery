<template>
  <div class="admin-sidebar">
    <el-menu
      :default-active="activeIndex"
      class="nav-menu"
      @select="handleSelect"
      :unique-opened="true"
      background-color="#2c3e50"
      text-color="#bdc3c7"
      active-text-color="#1abc9c"
    >
      <!-- 主页 -->
      <el-menu-item index="dashboard">
        <el-icon><House /></el-icon>
        <span>主页</span>
      </el-menu-item>
      <!-- 个人信息 -->
      <el-menu-item index="profile-edit">
        <el-icon><UserFilled /></el-icon>
        <span>个人信息</span>
      </el-menu-item>
      <!-- 管理员管理（仅超级管理员可见） -->
      <el-sub-menu index="admin-management" v-if="isSuperAdmin">
        <template #title>
          <el-icon><User /></el-icon>
          <span>管理员管理</span>
        </template>
        <el-menu-item index="user-list">管理员列表</el-menu-item>
        <el-menu-item index="user-roles">角色管理</el-menu-item>
      </el-sub-menu>
      
      <!-- 供应商管理 -->
      <el-sub-menu index="supplier-management" v-if="hasSupplierManagementPermission">
        <template #title>
          <el-icon><User /></el-icon>
          <span>供应商管理</span>
        </template>
        <el-menu-item index="supplier-list">供应商列表</el-menu-item>
        <el-menu-item index="supplier-create">添加供应商</el-menu-item>
      </el-sub-menu> 
      <!-- 会员管理 -->
      <el-sub-menu index="member-management" v-if="hasMemberManagementPermission">
        <template #title>
          <el-icon><User /></el-icon>
          <span>会员管理</span>
        </template>
        <el-menu-item index="member-list">会员列表</el-menu-item>
        <el-menu-item index="member-create">添加会员</el-menu-item>
      </el-sub-menu>
      <!-- 商品管理 -->
      <el-sub-menu index="product-management" v-if="hasProductManagementPermission">
        <template #title>
          <el-icon><Box /></el-icon>
          <span>商品管理</span>
        </template>
        <el-menu-item index="product-list">商品列表</el-menu-item>
      </el-sub-menu>
      <!-- 订单管理 -->
      <el-sub-menu index="order-management" v-if="hasOrderManagementPermission">
        <template #title>
          <el-icon><Box /></el-icon>
          <span>订单管理</span>
        </template>
        <el-menu-item index="order-list">订单列表</el-menu-item>
        <el-menu-item index="order-debug-tool" v-if="isSuperAdmin">订单状态调试</el-menu-item>
      </el-sub-menu>
      <!-- 财务相关 -->
      <el-sub-menu index="finance-management" v-if="hasFinanceManagementPermission">
        <template #title>
          <el-icon><Box /></el-icon>
          <span>财务相关</span>
        </template>
        <el-menu-item index="supplier-statement-list">供应商对账单</el-menu-item>
        <el-menu-item index="member-statement-list">会员对账单</el-menu-item>
        <el-menu-item index="balance-history-list">余额记录</el-menu-item>
        <el-menu-item index="recharge-list">充值记录</el-menu-item>
        <el-menu-item index="withdrawal-list">提现申请</el-menu-item>
      </el-sub-menu>
      
      <!-- 工厂直采 -->
      <el-menu-item index="product-inquiry-list" v-if="hasInquiryManagementPermission">
        <el-icon><ChatDotSquare /></el-icon>
        <span>工厂直采</span>
      </el-menu-item>
      <!-- 分隔线 -->
      <div class="menu-divider"></div>
      <!-- 网站设计标题 -->
      <div class="website-design-title">网站设计</div>
      <el-menu-item index="translation-manager" v-if="hasWebsiteMenuPermission">多语言翻译</el-menu-item>
      <el-menu-item index="product-logistics-payment-info" v-if="hasWebsiteMenuPermission">商品详情物流支付说明</el-menu-item>
      <el-menu-item index="public-resource-list" v-if="hasWebsiteMenuPermission">前端公共资源</el-menu-item>
      <el-menu-item index="site-config-list" v-if="hasWebsiteMenuPermission">网站参数</el-menu-item>
      <el-menu-item index="shipping-region-list" v-if="hasWebsiteMenuPermission">发货区域</el-menu-item>
      <el-menu-item index="logistics-company-list" v-if="hasWebsiteMenuPermission">物流公司</el-menu-item>
      <!-- 主页侧边栏子菜单 -->
      <el-sub-menu index="sidebar-menu" v-if="hasWebsiteMenuPermission">
        <template #title>
          <span>首页编辑</span>
        </template>
        <el-menu-item index="menu-category-list">一级菜单</el-menu-item>
        <el-menu-item index="menu-subcategory-list">二级菜单</el-menu-item>
        <el-menu-item index="menu-item-list">三级菜单</el-menu-item>
        <el-menu-item index="menu-promotion-list">菜单图片</el-menu-item>
        <el-menu-item index="horizontal-menu-manager">横向与楼层</el-menu-item>
        <el-menu-item index="slider-manager">首页轮播图</el-menu-item>
      </el-sub-menu>
      <!-- 帮助中心子菜单 -->
      <el-sub-menu index="help-center-menu" v-if="hasWebsiteMenuPermission">
        <template #title>
          <span>帮助中心</span>
        </template>
        <el-menu-item index="help-center-category">帮助一级分类</el-menu-item>
        <el-menu-item index="help-center-sub-category">帮助二级分类</el-menu-item>
        <el-menu-item index="help-center-faq">常见问题</el-menu-item>
        <el-menu-item index="help-center-guide">操作指引</el-menu-item>
      </el-sub-menu>
      <!-- 公告消息 -->
      <el-sub-menu index="announcement-menu" v-if="hasWebsiteMenuPermission">
        <template #title>
          <span>公告消息</span>
        </template>
        <!-- 公告消息 -->
        <el-menu-item index="site-message-list">公告消息</el-menu-item>
      </el-sub-menu>
    </el-menu>
    <!-- 滚动提示 -->
    <div class="scroll-hint"></div>
  </div>
</template>

<script>
import {
  House,
  User,
  Box,
  Document,
  UserFilled,
  Setting,
  Menu,
  ChatDotSquare
} from '@element-plus/icons-vue'
import {
  ElMenu,
  ElMenuItem,
  ElSubMenu,
  ElIcon
} from 'element-plus'

export default {
  name: 'AdminSidebar',
  components: {
    House,
    User,
    Box,
    Document,
    UserFilled,
    Setting,
    Menu,
    ChatDotSquare,
    ElMenu,
    ElMenuItem,
    ElSubMenu,
    ElIcon
  },
  props: {
    isSuperAdmin: {
      type: Boolean,
      default: false
    },
    userRoles: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      activeIndex: 'dashboard'
    }
  },
  computed: {
    // 检查用户是否具有会员管理权限
    hasMemberManagementPermission() {
      return this.isSuperAdmin || this.userRoles.includes('ROLE_ADMIN_MEMBER');
    },
    // 检查用户是否具有供应商管理权限
    hasSupplierManagementPermission() {
      return this.isSuperAdmin || this.userRoles.includes('ROLE_ADMIN_SUPPLIER');
    },
    // 检查用户是否具有商品管理权限
    hasProductManagementPermission() {
      return this.isSuperAdmin || this.userRoles.includes('ROLE_ADMIN_PRODUCT');
    },
    // 检查用户是否具有网站菜单管理权限
    hasWebsiteMenuPermission() {
      return this.isSuperAdmin || this.userRoles.includes('ROLE_ADMIN_SITEMENU');
    },
    // 检查用户是否具有财务管理权限
    hasFinanceManagementPermission() {
      return this.isSuperAdmin || this.userRoles.includes('ROLE_ADMIN_BALANCE');
    },
    // 检查用户是否具有订单管理权限
    hasOrderManagementPermission() {
      return this.isSuperAdmin || this.userRoles.includes('ROLE_ADMIN_ORDER');
    },
    // 检查用户是否具有工厂直采管理权限
    hasInquiryManagementPermission() {
      return this.isSuperAdmin || this.userRoles.includes('ROLE_ADMIN_INQUIRY');
    }
  },
  methods: {
    handleSelect(key, keyPath) {
      // 触发自定义事件，让父组件处理导航逻辑
      this.$emit('navigate', key, keyPath);

      // 更新激活状态
      this.activeIndex = key;

      // 延迟检测溢出，因为菜单可能会展开或收起
      setTimeout(() => {
        this.checkOverflow();
      }, 300);
    },

    // 检测侧边栏内容是否溢出
    checkOverflow() {
      this.$nextTick(() => {
        const sidebar = this.$el;
        const menu = sidebar.querySelector('.nav-menu');

        if (sidebar && menu) {
          // 检查是否有垂直滚动条
          if (menu.scrollHeight > menu.clientHeight) {
            sidebar.classList.add('overflowing');
          } else {
            sidebar.classList.remove('overflowing');
          }
        }
      });
    }
  },
  mounted() {
    // 监听来自其他组件的导航事件
    window.addEventListener('navigate-to', (event) => {
      this.activeIndex = event.detail.key;
    });

    // 检测侧边栏是否溢出
    this.checkOverflow();

    // 监听窗口大小变化
    window.addEventListener('resize', this.checkOverflow);
  },
  beforeUnmount() {
    // 清理事件监听器
    window.removeEventListener('resize', this.checkOverflow);
  }
}
</script>

<style scoped>
.admin-sidebar {
  width: 200px;
  background: #2c3e50;
  color: white;
  overflow-y: auto;
  font-size: 14px;
  flex-shrink: 0;
  position: fixed;
  top: 60px;
  left: 0;
  bottom: 0;
  height: calc(100vh - 60px);
  /* 美化滚动条 */
  scrollbar-width: thin;
  scrollbar-color: #1abc9c #2c3e50;
}

/* Webkit浏览器滚动条样式 */
.admin-sidebar::-webkit-scrollbar {
  width: 3px;
}

.admin-sidebar::-webkit-scrollbar-track {
  background: #2c3e50;
}

.admin-sidebar::-webkit-scrollbar-thumb {
  background-color: #1abc9c;
  border-radius: 2px;
}

.admin-sidebar::-webkit-scrollbar-thumb:hover {
  background-color: #16a085;
}

.nav-menu {
  border-right: none;
  /* 确保菜单内容可以滚动 */
  max-height: calc(100vh - 80px);
  overflow-y: auto;
}

/* 菜单项基础样式 */
.nav-menu :deep(.el-menu-item) {
  background-color: #2c3e50 !important;
  color: #bdc3c7 !important;
  height: 45px;
  line-height: 45px;
  transition: all 0.3s ease;
}

/* 菜单项悬停效果 */
.nav-menu :deep(.el-menu-item:hover) {
  background-color: #34495e !important;
  color: #ecf0f1 !important;
}

/* 菜单项激活状态样式（移除左边框） */
.nav-menu :deep(.el-menu-item.is-active) {
  background-color: #34495e !important;
  color: #1abc9c !important;
  border-left: none !important; /* 移除左边框 */
}

/* 子菜单标题基础样式 */
.nav-menu :deep(.el-sub-menu__title) {
  background-color: #2c3e50 !important;
  color: #bdc3c7 !important;
  height: 45px;
  line-height: 45px;
  transition: all 0.3s ease;
}

/* 子菜单标题悬停效果 */
.nav-menu :deep(.el-sub-menu__title:hover) {
  background-color: #34495e !important;
  color: #ecf0f1 !important;
}

/* 子菜单展开状态标题样式 */
.nav-menu :deep(.el-sub-menu.is-opened .el-sub-menu__title) {
  background-color: #34495e !important;
  color: #1abc9c !important;
  border-left: none !important; /* 移除左边框 */
}

/* 子菜单激活状态标题样式 */
.nav-menu :deep(.el-sub-menu.is-active .el-sub-menu__title) {
  background-color: #34495e !important;
  color: #1abc9c !important;
  border-left: none !important; /* 移除左边框 */
}

/* 子菜单滚动样式 */
.nav-menu :deep(.el-menu--inline) {
  max-height: 300px;
  overflow-y: auto;
  /* 美化滚动条 */
  scrollbar-width: thin;
  scrollbar-color: #1abc9c #2c3e50;
  background-color: #34495e !important;
}

.nav-menu :deep(.el-menu--inline::-webkit-scrollbar) {
  width: 4px;
}

.nav-menu :deep(.el-menu--inline::-webkit-scrollbar-track) {
  background: #2c3e50;
}

.nav-menu :deep(.el-menu--inline::-webkit-scrollbar-thumb) {
  background-color: #1abc9c;
  border-radius: 2px;
}

.nav-menu :deep(.el-menu--inline::-webkit-scrollbar-thumb:hover) {
  background-color: #16a085;
}

/* 子菜单项样式 */
.nav-menu :deep(.el-menu--inline .el-menu-item) {
  background-color: #34495e !important;
  color: #bdc3c7 !important;
  height: 40px;
  line-height: 40px;
  padding-left: 48px !important;
}

/* 子菜单项悬停效果 */
.nav-menu :deep(.el-menu--inline .el-menu-item:hover) {
  background-color: #3d566e !important;
  color: #ecf0f1 !important;
}

/* 子菜单项激活状态样式 */
.nav-menu :deep(.el-menu--inline .el-menu-item.is-active) {
  background-color: #3d566e !important;
  color: #1abc9c !important;
  border-left: none !important; /* 移除左边框 */
}

/* 分隔线样式 */
.menu-divider {
  height: 1px;
  background-color: #3d566e;
  margin: 10px 15px;
}

/* 网站设计标题样式 */
.website-design-title {
  padding: 12px 20px;
  color: #1abc9c;
  font-weight: 600;
  font-size: 14px;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  background-color: rgba(44, 62, 80, 0.7);
  margin: 10px 10px 5px;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* 滚动提示样式 */
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

.admin-sidebar:hover .scroll-hint {
  opacity: 1;
}

/* 当内容溢出时才显示滚动提示 */
.admin-sidebar.overflowing .scroll-hint {
  opacity: 0.7;
}

.admin-sidebar.overflowing:hover .scroll-hint {
  opacity: 1;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .admin-sidebar {
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
  
  /* 移动端隐藏网站设计标题文字 */
  .website-design-title {
    display: none;
  }
}
</style>