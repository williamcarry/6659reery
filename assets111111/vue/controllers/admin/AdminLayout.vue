<template>
  <el-container class="admin-layout">
    <!-- 顶部 Banner -->
    <el-header class="admin-header">
      <div class="header-content">
        <div class="logo">
          <h1>{{ headerTitle }}</h1>
        </div>
        <div class="user-info" @click="editProfile">
          <span style="display: inline-block;margin-right: 10px;">欢迎，{{ userName }}!</span>
          <el-button v-if="isCurrentUserSuperAdmin" class="cache-clear-btn" @click.stop="clearCache" :loading="clearingCache">清理缓存</el-button>
          <el-button class="logout-btn" @click.stop="logout">退出</el-button>
        </div>
      </div>
    </el-header>
    
    <admin-sidebar 
      @navigate="handleNavigation" 
      :is-super-admin="isCurrentUserSuperAdmin"
      :user-roles="currentAdmin.roles || []"
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
            <h2>欢迎，{{ userName }}!</h2>
            
            <!-- 平台数据概览 -->
            <platform-dashboard 
              ref="platformDashboard"
              :admin-login-path="adminLoginPath"
              :auto-load="true"
            />
            
            <!-- 供应商销量排行榜 -->
            <div style="margin-top: 20px">
              <supplier-ranking 
                ref="supplierRanking"
                :admin-login-path="adminLoginPath"
                :auto-load="true"
              />
            </div>
          </div>
        </div>
        
        <!-- 管理员列表 -->
        <div :class="['content-tab', { 'active': activeTag === 'user-list' }]" id="user-list-tab">
          <admin-list 
            :admins="adminListData"
            :is-current-user-super-admin="isCurrentUserSuperAdmin"
            :roles="adminRoleListData"
            @reload-admin-list="reloadAdminListData"
          />
        </div>
        
        <!-- 添加管理员 -->
        <div :class="['content-tab', { 'active': activeTag === 'user-create' }]" id="user-create-tab">
          <admin-profile-edit 
            :is-create-mode="true"
            :submit-url="adminCreateUrl"
          />
        </div>
        
        <!-- 角色管理 -->
        <div :class="['content-tab', { 'active': activeTag === 'user-roles' }]" id="user-roles-tab">
          <role-list 
            :roles="roleListData"
            :permissions="permissionListData"
            @reload-role-list="reloadRoleListData"
          />
        </div>
        <!-- 个人信息 -->
        <div :class="['content-tab', { 'active': activeTag === 'profile-edit' }]" id="profile-edit-tab">
          <admin-profile-edit 
            :admin="currentAdmin"
            :submit-url="adminProfileUrl"
            :is-create-mode="false"
          />
        </div> 
        <!-- 一级分类 -->
        <div :class="['content-tab', { 'active': activeTag === 'menu-category-list' }]" id="menu-category-list-tab">
          <menu-category-tab :admin-login-path="adminLoginPath" ref="menuCategoryTab" :auto-load="false" />
        </div>
        
        <!-- 二级分类 -->
        <div :class="['content-tab', { 'active': activeTag === 'menu-subcategory-list' }]" id="menu-subcategory-list-tab">
          <menu-subcategory-tab :admin-login-path="adminLoginPath" ref="menuSubcategoryTab" :auto-load="false" />
        </div>
        
        <!-- 三级分类 -->
        <div :class="['content-tab', { 'active': activeTag === 'menu-item-list' }]" id="menu-item-list-tab">
          <menu-item-tab :admin-login-path="adminLoginPath" ref="menuItemTab" :auto-load="false" />
        </div>
        
        <!-- 促销菜单 -->
        <div :class="['content-tab', { 'active': activeTag === 'menu-promotion-list' }]" id="menu-promotion-list-tab">
          <promotion-menu-tab :admin-login-path="adminLoginPath" ref="promotionMenuTab" :auto-load="false" />
        </div>
        
        <!-- 网站参数 -->
        <div :class="['content-tab', { 'active': activeTag === 'site-config-list' }]" id="site-config-list-tab">
          <site-config-manager :admin-login-path="adminLoginPath" ref="siteConfigManager" :auto-load="false" />
        </div>
        
        <!-- 多语言翻译 -->
        <div :class="['content-tab', { 'active': activeTag === 'translation-manager' }]" id="translation-manager-tab">
          <translation-manager :admin-login-path="adminLoginPath" ref="translationManager" :auto-load="false" />
        </div>
        
        <!-- 前端公共资源 -->
        <div :class="['content-tab', { 'active': activeTag === 'public-resource-list' }]" id="public-resource-list-tab">
          <public-resource-list :admin-login-path="adminLoginPath" ref="publicResourceList" :auto-load="false" />
        </div>
        
        <!-- 供应商列表 -->
        <div :class="['content-tab', { 'active': activeTag === 'supplier-list' }]" id="supplier-list-tab">
          <supplier-list :admin-login-path="adminLoginPath" ref="supplierList" :auto-load="false" />
        </div>
        
        <!-- 添加供应商 -->
        <div :class="['content-tab', { 'active': activeTag === 'supplier-create' }]" id="supplier-create-tab">
          <supplier-create :admin-login-path="adminLoginPath" @supplier-created="reloadSupplierList" />
        </div>
        
        <!-- 查看供应商 -->
        <div :class="['content-tab', { 'active': activeTag === 'supplier-view' }]" id="supplier-view-tab">
          <supplier-view-tab :admin-login-path="adminLoginPath" :supplier-id="currentSupplierId" :return-to="supplierViewReturnTo" ref="supplierViewTab" :auto-load="false" />
        </div>
        
        <!-- 编辑供应商 -->
        <div :class="['content-tab', { 'active': activeTag === 'supplier-edit' }]" id="supplier-edit-tab">
          <supplier-edit-tab :admin-login-path="adminLoginPath" :supplier-id="currentSupplierId" ref="supplierEditTab" :auto-load="false" />
        </div>
        
        <!-- 供应商对账单 -->
        <div :class="['content-tab', { 'active': activeTag === 'supplier-statement' }]" id="supplier-statement-tab">
          <supplier-statement-tab :admin-login-path="adminLoginPath" :supplier-id="currentSupplierId" ref="supplierStatementTab" :auto-load="false" />
        </div>
        
        <!-- 供应商对账单列表 -->
        <div :class="['content-tab', { 'active': activeTag === 'supplier-statement-list' }]" id="supplier-statement-list-tab">
          <supplier-statement-list :admin-login-path="adminLoginPath" ref="supplierStatementList" :auto-load="false" />
        </div>
        
        <!-- 商品列表 -->
        <div :class="['content-tab', { 'active': activeTag === 'product-list' }]" id="product-list-tab">
          <product-list :admin-login-path="adminLoginPath" ref="productList" :auto-load="false" />
        </div>
        
        <!-- 查看商品 -->
        <div :class="['content-tab', { 'active': activeTag === 'product-view' }]" id="product-view-tab">
          <product-view :admin-login-path="adminLoginPath" :product-id="currentProductId" :return-to="productViewReturnTo" ref="productView" :auto-load="false" />
        </div>
        
        <!-- 会员列表 -->
        <div :class="['content-tab', { 'active': activeTag === 'member-list' }]" id="member-list-tab">
          <member-list :admin-login-path="adminLoginPath" ref="memberList" :auto-load="false" />
        </div>
        
        <!-- 会员对账单 -->
        <div :class="['content-tab', { 'active': activeTag === 'member-statement' }]" id="member-statement-tab">
          <member-statement-tab :admin-login-path="adminLoginPath" :member-id="currentMemberId" ref="memberStatementTab" :auto-load="false" />
        </div>
        
        <!-- 会员对账单列表 -->
        <div :class="['content-tab', { 'active': activeTag === 'member-statement-list' }]" id="member-statement-list-tab">
          <member-statement-list :admin-login-path="adminLoginPath" ref="memberStatementList" :auto-load="false" />
        </div>
        
        <!-- 添加会员 -->
        <div :class="['content-tab', { 'active': activeTag === 'member-create' }]" id="member-create-tab">
          <member-create :admin-login-path="adminLoginPath" @member-created="reloadMemberList" />
        </div>
        
        <!-- 查看会员 -->
        <div :class="['content-tab', { 'active': activeTag === 'member-view' }]" id="member-view-tab">
          <member-view-tab :admin-login-path="adminLoginPath" :member-id="currentMemberId" ref="memberViewTab" :auto-load="false" />
        </div>
        
        <!-- 编辑会员 -->
        <div :class="['content-tab', { 'active': activeTag === 'member-edit' }]" id="member-edit-tab">
          <member-edit-tab :admin-login-path="adminLoginPath" :member-id="currentMemberId" ref="memberEditTab" :auto-load="false" />
        </div>
        
        <!-- 物流公司 -->
        <div :class="['content-tab', { 'active': activeTag === 'logistics-company-list' }]" id="logistics-company-list-tab">
          <logistics-company-list :admin-login-path="adminLoginPath" ref="logisticsCompanyList" :auto-load="false" />
        </div>
        
        <!-- 添加物流公司 -->
        <div :class="['content-tab', { 'active': activeTag === 'logistics-company-create' }]" id="logistics-company-create-tab">
          <logistics-company-create :admin-login-path="adminLoginPath" @logistics-company-created="reloadLogisticsCompanyList" />
        </div>
        
        <!-- 编辑物流公司 -->
        <div :class="['content-tab', { 'active': activeTag === 'logistics-company-edit' }]" id="logistics-company-edit-tab">
          <logistics-company-edit :admin-login-path="adminLoginPath" :logistics-company-id="currentLogisticsCompanyId" ref="logisticsCompanyEdit" :auto-load="false" />
        </div>
        
        <!-- 余额变化记录 -->
        <div :class="['content-tab', { 'active': activeTag === 'balance-history-list' }]" id="balance-history-list-tab">
          <balance-history-list :admin-login-path="adminLoginPath" ref="balanceHistoryList" :auto-load="false" />
        </div>
        
        <!-- 充值记录 -->
        <div :class="['content-tab', { 'active': activeTag === 'recharge-list' }]" id="recharge-list-tab">
          <recharge-list :admin-login-path="adminLoginPath" ref="rechargeList" :auto-load="false" />
        </div>
        
        <!-- 提现申请 -->
        <div :class="['content-tab', { 'active': activeTag === 'withdrawal-list' }]" id="withdrawal-list-tab">
          <withdrawal-list :admin-login-path="adminLoginPath" ref="withdrawalList" :auto-load="false" />
        </div>
        
        <!-- 工厂直采 -->
        <div :class="['content-tab', { 'active': activeTag === 'product-inquiry-list' }]" id="product-inquiry-list-tab">
          <product-inquiry-list :admin-login-path="adminLoginPath" ref="productInquiryList" :auto-load="false" />
        </div>
        
        <!-- 编辑工厂直采 -->
        <div :class="['content-tab', { 'active': activeTag === 'product-inquiry-edit' }]" id="product-inquiry-edit-tab">
          <product-inquiry-edit-tab :admin-login-path="adminLoginPath" :inquiry-id="currentInquiryId" ref="productInquiryEditTab" :auto-load="false" />
        </div>
        
        <!-- 订单列表 -->
        <div :class="['content-tab', { 'active': activeTag === 'order-list' }]" id="order-list-tab">
          <order-list :admin-login-path="adminLoginPath" ref="orderList" :auto-load="false" />
        </div>
        
        <!-- 订单详情 -->
        <div :class="['content-tab', { 'active': activeTag === 'order-detail' }]" id="order-detail-tab">
          <order-detail-tab :admin-login-path="adminLoginPath" :order-id="currentOrderId" ref="orderDetail" :auto-load="false" />
        </div>
        
        <!-- 常见问题 -->
        <div :class="['content-tab', { 'active': activeTag === 'help-center-faq' }]" id="help-center-faq-tab">
          <help-center-faq-list :admin-login-path="adminLoginPath" ref="helpCenterFaqList" :auto-load="false" />
        </div>
        
        <!-- 操作指引 -->
        <div :class="['content-tab', { 'active': activeTag === 'help-center-guide' }]" id="help-center-guide-tab">
          <help-center-guide-list :admin-login-path="adminLoginPath" ref="helpCenterGuideList" :auto-load="false" />
        </div>
        
        <!-- 问题分类 -->
        <div :class="['content-tab', { 'active': activeTag === 'help-center-category' }]" id="help-center-category-tab">
          <help-category-list :admin-login-path="adminLoginPath" ref="helpCategoryList" :auto-load="false" />
        </div>
        
        <!-- 二级分类 -->
        <div :class="['content-tab', { 'active': activeTag === 'help-center-sub-category' }]" id="help-center-sub-category-tab">
          <help-sub-category-list :admin-login-path="adminLoginPath" ref="helpSubCategoryList" :auto-load="false" />
        </div>
        
        <!-- 公告消息列表 -->
        <div :class="['content-tab', { 'active': activeTag === 'site-message-list' }]" id="site-message-list-tab">
          <site-message-list :admin-login-path="adminLoginPath" ref="siteMessageList" :auto-load="false" />
        </div>
        
        <!-- 添加公告消息 -->
        <div :class="['content-tab', { 'active': activeTag === 'site-message-create' }]" id="site-message-create-tab">
          <site-message-create :admin-login-path="adminLoginPath" @site-message-created="reloadSiteMessageList" />
        </div>
        
        <!-- 编辑公告消息 -->
        <div :class="['content-tab', { 'active': activeTag === 'site-message-edit' }]" id="site-message-edit-tab">
          <site-message-edit :admin-login-path="adminLoginPath" :message-id="currentSiteMessageId" ref="siteMessageEdit" :auto-load="false" />
        </div>
        
        <!-- 横向与楼层菜单 -->
        <div :class="['content-tab', { 'active': activeTag === 'horizontal-menu-manager' }]" id="horizontal-menu-manager-tab">
          <horizontal-menu-manager :admin-login-path="adminLoginPath" ref="horizontalMenuManager" :auto-load="false" />
        </div>
        
        <!-- 首页轮播图 -->
        <div :class="['content-tab', { 'active': activeTag === 'slider-manager' }]" id="slider-manager-tab">
          <slider-manager :admin-login-path="adminLoginPath" ref="sliderManager" :auto-load="false" />
        </div>
        
        <!-- 商品详情物流支付说明 -->
        <div :class="['content-tab', { 'active': activeTag === 'product-logistics-payment-info' }]" id="product-logistics-payment-info-tab">
          <product-logistics-payment-info-edit :admin-login-path="adminLoginPath" ref="productLogisticsPaymentInfoEdit" :auto-load="false" />
        </div>
        
        <!-- 发货区域 -->
        <div :class="['content-tab', { 'active': activeTag === 'shipping-region-list' }]" id="shipping-region-list-tab">
          <shipping-region-list :admin-login-path="adminLoginPath" ref="shippingRegionList" :auto-load="false" />
        </div>
        
        <!-- 订单状态调试工具 -->
        <div :class="['content-tab', { 'active': activeTag === 'order-debug-tool' }]" id="order-debug-tool-tab">
          <order-debug-tool-tab :admin-login-path="adminLoginPath" :auto-load="false" />
        </div>

      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import AdminSidebar from './AdminSidebar.vue'
import AdminList from './AdminList.vue'
import RoleList from './RoleList.vue'
import AdminProfileEdit from './AdminProfileEdit.vue'
import MenuCategoryTab from './MenuCategoryTab.vue'
import MenuSubcategoryTab from './MenuSubcategoryTab.vue'
import MenuItemTab from './MenuItemTab.vue'
import PromotionMenuTab from './PromotionMenuTab.vue'
import SupplierList from './SupplierList.vue'
import SupplierCreate from './SupplierCreate.vue'
import ProductList from './ProductList.vue'
import ProductView from './ProductView.vue'
import SupplierViewTab from './SupplierViewTab.vue'
import SupplierEditTab from './SupplierEditTab.vue'
import SupplierStatementTab from './SupplierStatementTab.vue'
import SupplierStatementList from './SupplierStatementList.vue'
import MemberStatementTab from './MemberStatementTab.vue'
import MemberStatementList from './MemberStatementList.vue'
import MemberList from './MemberList.vue'
import MemberCreate from './MemberCreate.vue'
import MemberViewTab from './MemberViewTab.vue'
import MemberEditTab from './MemberEditTab.vue'
import SiteConfigManager from './SiteConfigManager.vue'
import PublicResourceList from './PublicResourceList.vue'
import BalanceHistoryList from './BalanceHistoryList.vue'
import RechargeList from './RechargeList.vue'
import WithdrawalList from './WithdrawalList.vue'
import ProductInquiryList from './ProductInquiryList.vue'
import ProductInquiryEditTab from './ProductInquiryEditTab.vue'
import OrderList from './OrderList.vue'
import OrderDetailTab from './OrderDetailTab.vue'
import LogisticsCompanyList from './LogisticsCompanyList.vue'
import LogisticsCompanyCreate from './LogisticsCompanyCreate.vue'
import LogisticsCompanyEdit from './LogisticsCompanyEdit.vue'
import HelpCenterFaqList from './HelpCenterFaqList.vue'
import HelpCenterGuideList from './HelpCenterGuideList.vue'
import HelpCategoryList from './HelpCategoryList.vue'
import HelpSubCategoryList from './HelpSubCategoryList.vue'
import SiteMessageList from './SiteMessageList.vue'
import SiteMessageCreate from './SiteMessageCreate.vue'
import SiteMessageEdit from './SiteMessageEdit.vue'
import TranslationManager from './TranslationManager.vue'
import HorizontalMenuManager from './HorizontalMenuManager.vue'
import SliderManager from './SliderManager.vue'
import ProductLogisticsPaymentInfoEdit from './ProductLogisticsPaymentInfoEdit.vue'

import ShippingRegionList from './ShippingRegionList.vue'
import OrderDebugToolTab from './订单状态调试工具Tab.vue'
import PlatformDashboard from './PlatformDashboard.vue'
import SupplierRanking from './SupplierRanking.vue'

import {
  ElContainer,
  ElHeader,
  ElMain,
  ElTag,
  ElButton
} from 'element-plus'

export default {
  name: 'AdminLayout',
  components: {
    AdminSidebar,
    AdminList,
    RoleList,
    AdminProfileEdit,
    MenuCategoryTab,
    MenuSubcategoryTab,
    MenuItemTab,
    PromotionMenuTab,
    SupplierList,
    SupplierCreate,
    ProductList,
    ProductView,
    SupplierViewTab,
    SupplierEditTab,
    SupplierStatementTab,
    SupplierStatementList,
    MemberStatementTab,
    MemberStatementList,
    MemberList,
    MemberCreate,
    MemberViewTab,
    MemberEditTab,
    SiteConfigManager,
    PublicResourceList,
    BalanceHistoryList,
    RechargeList,
    WithdrawalList,
    ProductInquiryList,
    ProductInquiryEditTab,
    OrderList,
    OrderDetailTab,
    LogisticsCompanyList,
    LogisticsCompanyCreate,
    LogisticsCompanyEdit,
    HelpCenterFaqList,
    HelpCenterGuideList,
    HelpCategoryList,
    HelpSubCategoryList,
    SiteMessageList,
    SiteMessageCreate,
    SiteMessageEdit,
    TranslationManager,
    HorizontalMenuManager,
    SliderManager,
    ProductLogisticsPaymentInfoEdit,

    ShippingRegionList,
    OrderDebugToolTab,
    PlatformDashboard,
    SupplierRanking,
    ElContainer,
    ElHeader,
    ElMain,
    ElTag,
    ElButton
  },
  props: {
    currentAdmin: {
      type: Object,
      default: () => ({
        username: '',
        email: '',
        mark: ''
      })
    },
    adminLoginPath: {
      type: String,
      default: ''
    },
    adminProfileUrl: {
      type: String,
      default: ''
    },
    adminCreateUrl: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      headerTitle: '总后台',
      activeTag: 'dashboard',
      userName: '', // 默认为空
      isCurrentUserSuperAdmin: false, // 是否为超级管理员
      tags: [
        { key: 'dashboard', title: '主页' }
      ],
      tagTitles: {
        'dashboard': '主页',
        'user-list': '管理员列表',
        'user-create': '添加管理员',
        'user-roles': '角色管理',
        'profile-edit': '个人信息',
        'supplier-list': '供应商列表',
        'supplier-create': '添加供应商',
        'supplier-view': '查看供应商',
        'supplier-edit': '编辑供应商',
        'supplier-statement': '供应商对账单',
        'supplier-statement-list': '供应商对账单列表',
        'member-statement': '会员对账单',
        'member-statement-list': '会员对账单列表',
        'product-list': '商品列表',
        'product-view': '查看商品',
        'member-list': '会员列表',
        'member-create': '添加会员',
        'member-view': '查看会员',
        'member-edit': '编辑会员',
        'menu-category-list': '一级分类',
        'menu-subcategory-list': '二级分类',
        'menu-item-list': '三级分类',
        'menu-promotion-list': '促销菜单',
        'site-config-list': '网站参数',
        'public-resource-list': '前端公共资源',
        'logistics-company-list': '物流公司',
        'logistics-company-create': '添加物流公司',
        'logistics-company-edit': '编辑物流公司',
        'balance-history-list': '余额变化记录',
        'recharge-list': '充值记录',
        'withdrawal-list': '提现申请',
        'product-inquiry-list': '工厂直采',
        'product-inquiry-edit': '编辑询价单',
        'order-list': '订单列表',
        'order-detail': '订单详情',
        'help-center-faq': '常见问题',
        'help-center-guide': '操作指引',
        'help-center-category': '问题分类',
        'help-center-sub-category': '二级分类',
        'site-message-list': '公告消息',
        'site-message-create': '添加公告消息',
        'site-message-edit': '编辑公告消息',
        'translation-manager': '多语言翻译',
        'horizontal-menu-manager': '横向与楼层',
        'slider-manager': '首页轮播图',
        'product-logistics-payment-info': '商品详情物流支付说明',
        'shipping-region-list': '发货区域',
        'order-debug-tool': '订单状态调试工具'
      },
      adminListData: [], // 添加管理员列表数据
      adminRoleListData: [], // 添加管理员角色列表数据
      roleListData: [], // 添加角色列表数据
      permissionListData: [], // 添加权限列表数据
      withdrawalList: null, // 提现申请列表引用
      currentProductId: null, // 当前查看的商品ID
      productViewReturnTo: 'product-list', // 商品查看页面返回地址
      currentSupplierId: null, // 当前查看/编辑的供应商ID
      supplierViewReturnTo: 'supplier-list', // 供应商查看页面返回地址
      currentMemberId: null, // 当前查看的会员ID
      currentLogisticsCompanyId: null, // 当前编辑的物流公司ID
      currentSiteMessageId: null,
      currentOrderId: null, // 当前查看的订单ID
      currentInquiryId: 0, // 当前编辑的询价单ID (默认0而不是null)
      clearingCache: false
    }
  },
  methods: {
    handleNavigation(key, keyPath) {
      // 添加标签页
      this.addTab(key);
      
      // 切换到该标签页
      this.switchToTab(key);
      
      // 根据标签页类型加载相应数据
      this.loadTabData(key);
    },
    
    addTab(key) {
      // 如果标签页已存在，直接返回
      if (this.tags.some(tag => tag.key === key)) {
        return;
      }
      
      // 添加新标签页
      this.tags.push({
        key: key,
        title: this.tagTitles[key] || key
      });
      
      // 强制更新以确保视图刷新
      this.$forceUpdate();
    },
    
    // 根据标签页类型加载数据就是按需加载
    loadTabData(key) {
      switch (key) {
        case 'dashboard':
          // 刷新主页统计数据
          if (this.$refs.platformDashboard) {
            this.$refs.platformDashboard.loadData();
          }
          if (this.$refs.supplierRanking) {
            this.$refs.supplierRanking.loadRanking();
          }
          break;
        case 'user-list':
          this.fetchAdminListData();
          break;
        case 'user-roles':
          this.fetchRoleListData();
          break;
        case 'menu-category-list':
          // 按需加载一级分类数据
          if (this.$refs.menuCategoryTab) {
            this.$refs.menuCategoryTab.loadCategoryData();
          }
          break;
        case 'menu-subcategory-list':
          // 按需加载二级分类数据
          if (this.$refs.menuSubcategoryTab) {
            this.$refs.menuSubcategoryTab.loadSubcategoryData();
          }
          break;
        case 'menu-item-list':
          // 按需加载三级分类数据
          if (this.$refs.menuItemTab) {
            this.$refs.menuItemTab.loadItemData();
          }
          break;
        case 'menu-promotion-list':
          // 按需加载促销菜单数据
          if (this.$refs.promotionMenuTab) {
            this.$refs.promotionMenuTab.loadPromotionData();
          }
          break;
        case 'site-config-list':
          // 按需加载网站参数数据
          if (this.$refs.siteConfigManager) {
            this.$refs.siteConfigManager.loadConfigData();
          }
          break;
        case 'public-resource-list':
          // 按需加载前端公共资源数据
          if (this.$refs.publicResourceList) {
            this.$refs.publicResourceList.loadResourceData();
          }
          break;
        case 'logistics-company-list':
          // 按需加载物流公司列表数据
          if (this.$refs.logisticsCompanyList) {
            this.$refs.logisticsCompanyList.loadLogisticsCompanyData();
          }
          break;
        case 'logistics-company-edit':
          // 按需加载物流公司编辑数据
          if (this.$refs.logisticsCompanyEdit) {
            this.$refs.logisticsCompanyEdit.initData();
          }
          break;
        case 'supplier-list':
          // 按需加载供应商列表数据
          if (this.$refs.supplierList) {
            this.$refs.supplierList.loadSupplierData();
          }
          break;
        case 'member-list':
          // 按需加载会员列表数据
          if (this.$refs.memberList) {
            this.$refs.memberList.loadMemberData();
          }
          break;
        case 'member-view':
          // 按需加载会员查看数据
          if (this.$refs.memberViewTab) {
            this.$refs.memberViewTab.initData();
          }
          break;
        case 'member-edit':
          // 按需加载会员编辑数据
          if (this.$refs.memberEditTab) {
            this.$refs.memberEditTab.initData();
          }
          break;
        case 'balance-history-list':
          // 按需加载余额变化记录数据
          if (this.$refs.balanceHistoryList) {
            this.$refs.balanceHistoryList.loadBalanceHistoryData();
          }
          break;
        case 'recharge-list':
          // 按需加载充值记录数据
          if (this.$refs.rechargeList) {
            this.$refs.rechargeList.loadRechargeData();
          }
          break;
        case 'withdrawal-list':
          // 按需加载提现申请数据
          if (this.$refs.withdrawalList) {
            this.$refs.withdrawalList.loadWithdrawalData();
          }
          break;
        case 'product-inquiry-list':
          // 按需加载工厂直采数据
          if (this.$refs.productInquiryList) {
            this.$refs.productInquiryList.loadInquiryData();
          }
          break;
        case 'product-inquiry-edit':
          // 按需加载询价单编辑数据
          if (this.$refs.productInquiryEditTab) {
            this.$refs.productInquiryEditTab.loadInquiry();
          }
          break;
        case 'order-list':
          // 按需加载订单列表数据
          if (this.$refs.orderList) {
            this.$refs.orderList.loadOrderData();
          }
          break;
        case 'order-detail':
          // 按需加载订单详情数据
          if (this.$refs.orderDetail) {
            this.$refs.orderDetail.initData();
          }
          break;
        case 'help-center-faq':
          // 按需加载常见问题数据
          if (this.$refs.helpCenterFaqList) {
            this.$refs.helpCenterFaqList.loadQuestionData();
          }
          break;
        case 'help-center-guide':
          // 按需加载操作指引数据
          if (this.$refs.helpCenterGuideList) {
            this.$refs.helpCenterGuideList.loadGuideData();
          }
          break;
        case 'help-center-category':
          // 按需加载问题分类数据
          if (this.$refs.helpCategoryList) {
            this.$refs.helpCategoryList.loadCategoryData();
          }
          break;
        case 'help-center-sub-category':
          // 按需加载二级分类数据
          if (this.$refs.helpSubCategoryList) {
            this.$refs.helpSubCategoryList.loadSubCategoryData();
          }
          break;
        case 'withdrawal-list':
          // 按需加载提现申请数据
          if (this.$refs.withdrawalList) {
            this.$refs.withdrawalList.loadWithdrawalData();
          }
          break;
        case 'product-list':
          // 按需加载商品列表数据
          if (this.$refs.productList) {
            this.$refs.productList.loadProductData();
            this.$refs.productList.loadStatistics();
          }
          break;
        case 'product-view':
          // 按需加载商品查看数据
          if (this.$refs.productView) {
            this.$refs.productView.initData();
          }
          break;
        case 'supplier-view':
          // 按需加载供应商查看数据
          if (this.$refs.supplierViewTab) {
            this.$refs.supplierViewTab.initData();
          }
          break;
        case 'supplier-edit':
          // 按需加载供应商编辑数据
          if (this.$refs.supplierEditTab) {
            this.$refs.supplierEditTab.initData();
          }
          break;
        case 'supplier-statement':
          // 按需加载供应商对账单数据
          if (this.$refs.supplierStatementTab) {
            this.$refs.supplierStatementTab.initData();
          }
          break;
        case 'supplier-statement-list':
          // 按需加载供应商对账单列表数据
          if (this.$refs.supplierStatementList) {
            this.$refs.supplierStatementList.loadSupplierData();
          }
          break;
        case 'member-statement':
          // 按需加载会员对账单数据
          if (this.$refs.memberStatementTab) {
            this.$refs.memberStatementTab.initData();
          }
          break;
        case 'member-statement-list':
          // 按需加载会员对账单列表数据
          if (this.$refs.memberStatementList) {
            this.$refs.memberStatementList.loadMemberData();
          }
          break;
        case 'site-message-list':
          // 按需加载公告消息列表数据
          if (this.$refs.siteMessageList) {
            this.$refs.siteMessageList.loadMessageData();
          }
          break;
        case 'site-message-edit':
          // 按需加载公告消息编辑数据
          if (this.$refs.siteMessageEdit) {
            this.$refs.siteMessageEdit.loadMessageData();
          }
          break;
        case 'translation-manager':
          // 按需加载多语言翻译数据
          if (this.$refs.translationManager) {
            this.$refs.translationManager.loadTranslationFiles();
          }
          break;
        case 'horizontal-menu-manager':
          // 按需加载横向与楼层菜单数据
          if (this.$refs.horizontalMenuManager) {
            this.$refs.horizontalMenuManager.loadMenuData();
          }
          break;
        case 'slider-manager':
          // 按需加载首页轮播图数据
          if (this.$refs.sliderManager) {
            this.$refs.sliderManager.loadSliders();
          }
          break;
        case 'product-logistics-payment-info':
          // 按需加载商品详情物流支付说明数据
          if (this.$refs.productLogisticsPaymentInfoEdit) {
            this.$refs.productLogisticsPaymentInfoEdit.loadData();
          }
          break;
        case 'shipping-region-list':
          // 按需加载发货区域列表数据
          if (this.$refs.shippingRegionList) {
            this.$refs.shippingRegionList.loadShippingRegionData();
          }
          break;

        // 可以在这里添加其他标签页的数据加载逻辑
        default:
          // 其他标签页不需要预加载数据
          break;
      }
    },
    
    // 获取管理员列表数据
    fetchAdminListData() {
      console.log('Fetching admin list data'); // 调试信息
      
      // 构造请求URL
      const url = `/admin${this.adminLoginPath}/user/list/tab`;
      
      // 发送AJAX请求获取数据
      fetch(url, {
        method: 'GET',
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        if (data.admins) {
          this.adminListData = data.admins;
        }
        if (data.roles) {
          this.adminRoleListData = data.roles;
        }
      })
      .catch(error => {
        console.error('Error fetching admin list data:', error);
      });
    },
    
    // 获取角色列表数据
    fetchRoleListData() {
      console.log('Fetching role list data'); // 调试信息
      
      // 构造请求URL
      const url = `/admin${this.adminLoginPath}/role/list/tab`;
      
      // 发送AJAX请求获取数据
      fetch(url, {
        method: 'GET',
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        if (data.roles) {
          this.roleListData = data.roles;
        }
        if (data.permissions) {
          this.permissionListData = data.permissions;
        }
      })
      .catch(error => {
        console.error('Error fetching role list data:', error);
      });
    },
    
    // 重新加载管理员列表数据（供子组件调用）
    reloadAdminListData() {
      this.fetchAdminListData();
    },
    
    // 重新加载角色列表数据（供子组件调用）
    reloadRoleListData() {
      this.fetchRoleListData();
    },
    
    // 重新加载供应商列表（供子组件调用）
    reloadSupplierList() {
      // 这里可以添加重新加载供应商列表的逻辑
    },
    
    // 重新加载会员列表（供子组件调用）
    reloadMemberList() {
      // 这里可以添加重新加载会员列表的逻辑
    },
    
    // 重新加载物流公司列表（供子组件调用）
    reloadLogisticsCompanyList() {
      // 这里可以添加重新加载物流公司列表的逻辑
      if (this.$refs.logisticsCompanyList) {
        this.$refs.logisticsCompanyList.loadLogisticsCompanyData();
      }
    },
    
    // 重新加载公告消息列表数据
    reloadSiteMessageList() {
      // 刷新公告消息列表
      if (this.$refs.siteMessageList) {
        this.$refs.siteMessageList.loadMessageData();
      }
      // 关闭创建标签页
      this.closeTab('site-message-create');
      // 切换到站内信列表标签页
      this.switchToTab('site-message-list');
    },
    
    switchToTab(key) {
      this.activeTag = key;
      
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
        // 特殊处理：如果关闭的是商品查看页，则返回商品列表
        if (key === 'product-view') {
          // 检查商品列表标签是否存在
          const productListExists = this.tags.some(tag => tag.key === 'product-list');
          if (productListExists) {
            this.activeTag = 'product-list';
          } else {
            // 如果商品列表标签不存在，则切换到主页
            this.activeTag = 'dashboard';
          }
        } else if (key === 'member-view' || key === 'member-edit') {
          // 如果关闭的是会员查看/编辑页，则返回会员列表
          const memberListExists = this.tags.some(tag => tag.key === 'member-list');
          if (memberListExists) {
            this.activeTag = 'member-list';
          } else {
            this.activeTag = 'dashboard';
          }
        } else if (key === 'order-detail') {
          // 如果关闭的是订单详情页，则返回订单列表
          const orderListExists = this.tags.some(tag => tag.key === 'order-list');
          if (orderListExists) {
            this.activeTag = 'order-list';
          } else {
            this.activeTag = 'dashboard';
          }
        } else if (key === 'supplier-statement') {
          // 如果关闭的是供应商对账单页，则返回供应商对账单列表
          const supplierStatementListExists = this.tags.some(tag => tag.key === 'supplier-statement-list');
          if (supplierStatementListExists) {
            this.activeTag = 'supplier-statement-list';
          } else {
            this.activeTag = 'dashboard';
          }
        } else if (key === 'member-statement') {
          // 如果关闭的是会员对账单页，则返回会员对账单列表
          const memberStatementListExists = this.tags.some(tag => tag.key === 'member-statement-list');
          if (memberStatementListExists) {
            this.activeTag = 'member-statement-list';
          } else {
            this.activeTag = 'dashboard';
          }
        } else if (key === 'product-inquiry-edit') {
          // 如果关闭的是询价单编辑页，则返回工厂直采列表
          const inquiryListExists = this.tags.some(tag => tag.key === 'product-inquiry-list');
          if (inquiryListExists) {
            this.activeTag = 'product-inquiry-list';
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
      // 添加个人信息标签页并切换到该标签页
      this.addTab('profile-edit');
      this.switchToTab('profile-edit');
    },
    
    // 查看会员详情
    viewMember(memberId) {
      // 设置当前查看的会员ID
      this.currentMemberId = memberId;
      
      // 添加会员查看标签页并切换到该标签页
      this.addTab('member-view');
      this.switchToTab('member-view');
      
      // 按需加载会员数据
      this.$nextTick(() => {
        this.loadTabData('member-view');
      });
    },
    
    // 编辑会员
    editMember(memberId) {
      // 设置当前编辑的会员ID
      this.currentMemberId = memberId;
      
      // 添加会员编辑标签页并切换到该标签页
      this.addTab('member-edit');
      this.switchToTab('member-edit');
      
      // 按需加载会员数据
      this.$nextTick(() => {
        this.loadTabData('member-edit');
      });
    },
    
    // 查看商品详情
    viewProduct(productId, returnTo) {
      // 设置当前查看的商品ID
      this.currentProductId = productId;
      
      // 记录来源页面，默认返回商品列表
      this.productViewReturnTo = returnTo || 'product-list';
      
      // 添加商品查看标签页并切换到该标签页
      this.addTab('product-view');
      this.switchToTab('product-view');
      
      // 按需加载商品数据
      this.$nextTick(() => {
        this.loadTabData('product-view');
      });
    },
    
    // 查看供应商详情
    viewSupplier(supplierId, returnTo) {
      // 设置当前查看的供应商ID
      this.currentSupplierId = supplierId;
      
      // 记录来源页面，默认返回供应商列表
      this.supplierViewReturnTo = returnTo || 'supplier-list';
      
      // 添加供应商查看标签页并切换到该标签页
      this.addTab('supplier-view');
      this.switchToTab('supplier-view');
      
      // 按需加载供应商数据
      this.$nextTick(() => {
        this.loadTabData('supplier-view');
      });
    },
    
    // 编辑供应商
    editSupplier(supplierId) {
      // 设置当前编辑的供应商ID
      this.currentSupplierId = supplierId;
      
      // 添加供应商编辑标签页并切换到该标签页
      this.addTab('supplier-edit');
      this.switchToTab('supplier-edit');
      
      // 按需加载供应商数据
      this.$nextTick(() => {
        this.loadTabData('supplier-edit');
      });
    },
    
    // 编辑物流公司
    editLogisticsCompany(companyId) {
      // 设置当前编辑的物流公司ID
      this.currentLogisticsCompanyId = companyId;
      
      // 添加物流公司编辑标签页并切换到该标签页
      this.addTab('logistics-company-edit');
      this.switchToTab('logistics-company-edit');
      
      // 按需加载物流公司数据
      this.$nextTick(() => {
        this.loadTabData('logistics-company-edit');
      });
    },
    
    // 查看公告消息详情
    viewSiteMessage(messageId) {
      // 设置当前查看的公告消息 ID
      this.currentSiteMessageId = messageId;
      
      // 添加公告消息查看标签页并切换到该标签页
      this.addTab('site-message-view');
      this.switchToTab('site-message-view');
      
      // 按需加载公告消息数据
      this.$nextTick(() => {
        this.loadTabData('site-message-view');
      });
    },
    
    // 编辑公告消息
    editSiteMessage(messageId) {
      // 设置当前编辑的公告消息 ID
      this.currentSiteMessageId = messageId;
      
      // 添加公告消息编辑标签页并切换到该标签页
      this.addTab('site-message-edit');
      this.switchToTab('site-message-edit');
      
      // 按需加载公告消息数据
      this.$nextTick(() => {
        this.loadTabData('site-message-edit');
      });
    },
    
    // 编辑询价单
    editInquiry(inquiryId) {
      // 设置当前编辑的询价单ID
      this.currentInquiryId = inquiryId;
      
      // 添加询价单编辑标签页并切换到该标签页
      this.addTab('product-inquiry-edit');
      this.switchToTab('product-inquiry-edit');
      
      // 按需加载询价单数据
      this.$nextTick(() => {
        this.loadTabData('product-inquiry-edit');
      });
    },
    
    clearCache() {
      // 弹出确认对话框
      if (!confirm('系统缓存会自动定时刷新，通常无需手动清理。\n\n确定要立即清理缓存并重新加载数据吗？')) {
        return; // 用户取消操作
      }
      
      this.clearingCache = true;
      // 使用正确的路径，包含adminLoginPath
      fetch(`/admin${this.adminLoginPath}/cache/clear`, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(response => {
        if (!response.ok) {
          // 尝试解析错误响应
          return response.json().then(errorData => {
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
          }).catch(() => {
            // 如果无法解析JSON，使用默认错误消息
            throw new Error(`HTTP error! status: ${response.status}`);
          });
        }
        return response.json();
      })
      .then(data => {
        console.log('Cache cleared:', data);
        if (data && data.success) {
          // 使用简单的alert显示成功提示
          alert(data.message || '缓存已清理');
        } else if (data && data.error) {
          // 使用简单的alert显示错误提示
          alert(data.error || '清理缓存失败');

        } else {
          // 使用简单的alert显示错误提示
          alert('清理缓存失败');
        }
      })
      .catch(error => {
        console.error('Error clearing cache:', error);
        // 使用简单的alert显示错误提示
        alert('清理缓存失败: ' + error.message);
      })
      .finally(() => {
        this.clearingCache = false;
      });
    }
  },
  mounted() {
    // 从props中获取当前管理员信息
    // 设置显示的用户名，明确使用username字段
    this.userName = this.currentAdmin.username || '';
    
    // 如果仍然没有用户名，则使用默认值
    if (!this.userName) {
      this.userName = '管理员';
    }
    
    // 检查当前用户是否为超级管理员
    if (this.currentAdmin && this.currentAdmin.roles) {
      this.isCurrentUserSuperAdmin = this.currentAdmin.roles.includes('ROLE_SUPER_ADMIN');
    }
    
    // 设置全局adminLoginPath变量
    if (this.adminLoginPath) {
      window.adminLoginPath = this.adminLoginPath;
    }
    
    // 监听查看商品详情事件
    window.addEventListener('navigate-to-product-view', (event) => {
      const productId = event.detail.productId;
      const returnTo = event.detail.returnTo; // 获取来源页面
      this.viewProduct(productId, returnTo);
    });
    
    // 监听查看会员详情事件
    window.addEventListener('open-member-view-tab', (event) => {
      const memberId = event.detail.memberId;
      this.viewMember(memberId);
    });
    
    // 监听编辑会员事件
    window.addEventListener('open-member-edit-tab', (event) => {
      const memberId = event.detail.memberId;
      this.editMember(memberId);
    });
    
    // 监听会员保存成功事件
    window.addEventListener('member-save-success', () => {
      // 刷新会员列表
      if (this.$refs.memberList) {
        this.$refs.memberList.loadMemberData();
      }
      // 关闭编辑标签页
      this.closeTab('member-edit');
      // 切换到会员列表标签页
      this.switchToTab('member-list');
    });
    
    // 监听查看供应商详情事件
    window.addEventListener('navigate-to-supplier-view', (event) => {
      const supplierId = event.detail.supplierId;
      const returnTo = event.detail.returnTo || 'supplier-list'; // 获取来源，默认返回供应商列表
      this.viewSupplier(supplierId, returnTo);
    });
    
    // 监听编辑供应商事件
    window.addEventListener('navigate-to-supplier-edit', (event) => {
      const supplierId = event.detail.supplierId;
      this.editSupplier(supplierId);
    });
    
    // 监听供应商保存成功事件
    window.addEventListener('supplier-save-success', () => {
      // 刷新供应商列表
      if (this.$refs.supplierList) {
        this.$refs.supplierList.loadSupplierData();
      }
      // 关闭编辑标签页
      this.closeTab('supplier-edit');
      // 切换到供应商列表标签页
      this.switchToTab('supplier-list');
    });
    
    // 监听编辑物流公司事件
    window.addEventListener('navigate-to-logistics-company-edit', (event) => {
      const companyId = event.detail.companyId;
      this.editLogisticsCompany(companyId);
    });
    
    // 监听关闭当前标签页事件
    window.addEventListener('close-current-tab', () => {
      // 关闭当前激活的标签页
      this.closeTab(this.activeTag);
    });
    
    // 监听导航到指定页面事件
    window.addEventListener('navigate-to', (event) => {
      const key = event.detail.key;
      // 切换到指定标签页
      this.switchToTab(key);
    });
    
    // 监听商品查看页返回事件
    window.addEventListener('product-view-go-back', (event) => {
      const returnTo = event.detail.returnTo;
      // 关闭商品查看标签页
      this.closeTab('product-view');
      // 返回来源页面
      this.switchToTab(returnTo);
    });
    
    // 监听编辑公告消息事件
    window.addEventListener('navigate-to-site-message-edit', (event) => {
      const messageId = event.detail.messageId;
      this.editSiteMessage(messageId);
    });
    
    // 监听创建公告消息事件
    window.addEventListener('navigate-to-site-message-create', () => {
      // 添加公告消息创建标签页并切换到该标签页
      this.addTab('site-message-create');
      this.switchToTab('site-message-create');
    });
    
    // 监听返回公告消息列表事件
    window.addEventListener('navigate-to-site-message-list', () => {
      // 切换到公告消息列表标签页
      this.switchToTab('site-message-list');
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
    
    // 监听查看供应商对账单事件
    window.addEventListener('navigate-to-supplier-statement', (event) => {
      const supplierId = event.detail.supplierId;
      this.currentSupplierId = supplierId;
      this.addTab('supplier-statement');
      this.switchToTab('supplier-statement');
      this.$nextTick(() => {
        this.loadTabData('supplier-statement');
      });
    });
    
    // 监听查看会员对账单事件
    window.addEventListener('navigate-to-member-statement', (event) => {
      const memberId = event.detail.memberId;
      this.currentMemberId = memberId;
      this.addTab('member-statement');
      this.switchToTab('member-statement');
      this.$nextTick(() => {
        this.loadTabData('member-statement');
      });
    });
    
    // 监听编辑询价单事件
    window.addEventListener('open-inquiry-edit-tab', (event) => {
      const inquiryId = event.detail.inquiryId;
      this.editInquiry(inquiryId);
    });
  }
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100vw;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

.admin-header {
  background-color: #2c3e50;
  color: white;
  padding: 0 20px;
  height: 60px;
  line-height: 60px;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
  cursor: pointer; /* 手型光标 */
}

.user-info span {
  font-size: 14px;
  text-decoration: underline; /* 下划线 */
}

.user-info:hover span {
  color: #1abc9c; /* 悬停时的颜色变化 */
}

/* 清理缓存按钮样式 */
.cache-clear-btn {
  background-color: #3498db;
  border-color: #3498db;
  color: white;
  padding: 5px 10px;
  font-size: 12px;
  border-radius: 3px;
  transition: all 0.3s ease;
}

.cache-clear-btn:hover {
  background-color: #2980b9;
  border-color: #2980b9;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.cache-clear-btn:active {
  transform: translateY(0);
}

/* 退出按钮样式 */
.logout-btn {
  background-color: #e74c3c;
  border-color: #e74c3c;
  color: white;
  padding: 5px 10px;
  font-size: 12px;
  border-radius: 3px;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background-color: #c0392b;
  border-color: #c0392b;
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
  background: #f5f5f5;
  border-bottom: 1px solid #ddd;
  padding: 0.5rem 1rem;
  font-size: 14px;
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
  margin-right: 0.5rem;
  cursor: pointer;
}

.content-wrapper {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  background: #ecf0f1;
  margin-top: 40px;
  height: calc(100vh - 100px);
}

.content-tab {
  display: none;
}

.content-tab.active {
  display: block;
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