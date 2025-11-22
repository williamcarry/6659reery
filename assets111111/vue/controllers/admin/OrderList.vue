<template>
  <div class="order-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2 class="page-title">
        <el-icon class="title-icon"><ShoppingCart /></el-icon>
        订单管理
      </h2>
      <div class="header-actions">
        <el-button type="primary" @click="refreshData" :icon="Refresh">
          刷新数据
        </el-button>
      </div>
    </div>
    
    <!-- 搜索和筛选区域 -->
    <el-card class="filter-card">
      <div class="filter-header">
        <el-icon class="filter-icon"><Search /></el-icon>
        <span class="filter-title">筛选条件</span>
      </div>
      <el-form :model="searchForm" class="search-form" label-position="left" label-width="100px">
        <el-row :gutter="20" align="middle">
          <el-col :span="6" :xs="24">
            <el-form-item label="订单号">
              <el-input v-model="searchForm.orderNo" placeholder="请输入订单号" clearable />
            </el-form-item>
          </el-col>
          <el-col :span="6" :xs="24">
            <el-form-item label="买家用户名">
              <el-input v-model="searchForm.customerUsername" placeholder="请输入买家用户名" clearable />
            </el-form-item>
          </el-col>
          <el-col :span="6" :xs="24">
            <el-form-item label="订单状态">
              <el-select v-model="searchForm.orderStatus" placeholder="请选择状态" clearable style="width: 100%;">
                <el-option label="全部" value="" />
                <el-option label="待支付" value="pending_payment" />
                <el-option label="已支付" value="paid" />
                <el-option label="已发货" value="shipped" />
                <el-option label="已完成" value="completed" />
                <el-option label="已取消" value="cancelled" />
                <el-option label="退款中" value="refunding" />
                <el-option label="已退款" value="refunded" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="6" :xs="24" class="action-col">
            <el-form-item label=" ">
              <div class="form-actions">
                <el-button type="primary" @click="searchOrders" :icon="Search">
                  搜索
                </el-button>
                <el-button @click="resetSearch" :icon="RefreshLeft">
                  重置
                </el-button>
              </div>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-card>
    
    <!-- 订单列表表格 -->
    <el-card class="table-card">
      <template #header>
        <div class="table-header">
          <div class="table-header-title">
            <el-icon class="table-icon"><List /></el-icon>
            订单列表
          </div>
          <div class="table-header-info">
            共 {{ pagination.totalItems }} 条记录
          </div>
        </div>
      </template>
      
      <el-table 
        :data="orders" 
        class="order-table" 
        v-loading="loading"
        :fit="true"
        :border="false"
        :header-cell-style="{ textAlign: 'center' }"
        :cell-style="{ textAlign: 'center' }"
        :stripe="true"
        empty-text="暂无订单记录"
      >
        <el-table-column label="序号" width="60" fixed>
          <template #default="scope">
            {{ (pagination.currentPage - 1) * pagination.itemsPerPage + scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column prop="orderNo" label="订单号" min-width="180" show-overflow-tooltip fixed>
          <template #default="scope">
            <span 
              @click="copyOrderNo(scope.row.orderNo)"
              style="color: #409eff; font-weight: 600; text-decoration: underline; text-decoration-style: dotted; cursor: pointer; display: inline-block; min-width: 100px;"
            >
              {{ scope.row.orderNo }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="customerUsername" label="买家" min-width="120" show-overflow-tooltip />
        <el-table-column prop="totalAmount" label="订单总额" min-width="120" sortable>
          <template #default="scope">
            <span class="amount-text">{{ currencySymbol }}{{ scope.row.totalAmount }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="orderStatus" label="订单聚合状态" min-width="120">
          <template #default="scope">
            <el-tag :type="getOrderStatusTagType(scope.row.orderStatus)">
              {{ getOrderStatusText(scope.row.orderStatus) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="paymentStatus" label="支付状态" min-width="100">
          <template #default="scope">
            <el-tag :type="getPaymentStatusTagType(scope.row.paymentStatus)">
              {{ getPaymentStatusText(scope.row.paymentStatus) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="shippingStatus" label="物流聚合状态" min-width="120">
          <template #default="scope">
            <el-tag :type="getShippingStatusTagType(scope.row.shippingStatus)">
              {{ getShippingStatusText(scope.row.shippingStatus) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="paymentMethod" label="支付方式" min-width="100">
          <template #default="scope">
            {{ getPaymentMethodText(scope.row.paymentMethod) }}
          </template>
        </el-table-column>
        <el-table-column prop="createdAt" label="下单时间" min-width="160" sortable>
          <template #default="scope">
            <div class="time-cell">
              <div class="date">{{ formatDate(scope.row.createdAt) }}</div>
              <div class="time">{{ formatTime(scope.row.createdAt) }}</div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="scope">
            <div class="button-group">
              <el-button
                type="primary"
                size="small"
                @click="viewOrderDetail(scope.row)"
              >
                查看详情
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
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

    <!-- 订单详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="订单详情"
      width="90%"
      :close-on-click-modal="false"
    >
      <div class="order-detail" v-if="currentOrder" v-loading="detailLoading" element-loading-text="正在加载订单详情...">
        <!-- 订单基本信息 -->
        <el-card class="detail-card">
          <template #header>
            <div class="detail-card-header">
              <el-icon><Document /></el-icon>
              <span>订单信息</span>
            </div>
          </template>
          <el-descriptions :column="3" border>
            <el-descriptions-item label="订单号" label-class-name="desc-label">
              <span class="order-no-text">{{ currentOrder.orderNo }}</span>
            </el-descriptions-item>
            <el-descriptions-item label="下单时间" label-class-name="desc-label">
              {{ currentOrder.createdAt }}
            </el-descriptions-item>
            <el-descriptions-item label="订单聚合状态" label-class-name="desc-label">
              <el-tag :type="getOrderStatusTagType(currentOrder.orderStatus)">
                {{ getOrderStatusText(currentOrder.orderStatus) }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="买家用户名" label-class-name="desc-label">
              {{ currentOrder.customer.username }}
            </el-descriptions-item>
            <el-descriptions-item label="买家邮箱" label-class-name="desc-label">
              {{ currentOrder.customer.email }}
            </el-descriptions-item>
            <el-descriptions-item label="买家手机" label-class-name="desc-label">
              {{ currentOrder.customer.mobile || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="物流方式" label-class-name="desc-label" :span="3">
              <el-tag :type="currentOrder.shippingMethod === 'STANDARD_SHIPPING' ? 'success' : 'warning'">
                {{ getShippingMethodText(currentOrder.shippingMethod) }}
              </el-tag>
              <el-tooltip content="STANDARD_SHIPPING-标准物流, SELF_PICKUP-自提" placement="top">
                <el-icon style="margin-left: 5px; cursor: help;"><QuestionFilled /></el-icon>
              </el-tooltip>
            </el-descriptions-item>
            <el-descriptions-item label="供应商" :span="3" label-class-name="desc-label">
              <el-tag v-if="!currentOrder.supplierIds || currentOrder.supplierIds.length === 0" type="info">无供应商</el-tag>
              <el-tag v-else-if="currentOrder.supplierIds.length === 1" type="success">ID: {{ currentOrder.supplierIds[0] }}</el-tag>
              <div v-else>
                <el-tag v-for="supplierId in currentOrder.supplierIds" :key="supplierId" type="success" style="margin-right: 5px;">
                  ID: {{ supplierId }}
                </el-tag>
                <el-tooltip content="此订单包含多个供应商的商品" placement="top">
                  <el-icon style="margin-left: 5px; cursor: help;"><QuestionFilled /></el-icon>
                </el-tooltip>
              </div>
            </el-descriptions-item>
          </el-descriptions>
        </el-card>

        <!-- 金额信息 -->
        <el-card class="detail-card">
          <template #header>
            <div class="detail-card-header">
              <el-icon><Money /></el-icon>
              <span>金额信息</span>
            </div>
          </template>
          <el-descriptions :column="3" border>
            <el-descriptions-item label="商品总金额" label-class-name="desc-label">
              <div style="display: flex; flex-direction: column; align-items: flex-start;">
                <span class="amount-highlight" style="font-size: 18px; font-weight: bold;">{{ currencySymbol }}{{ currentOrder.productAmount }}</span>
                <span style="color: #909399; font-size: 12px; margin-top: 4px;">商品原价总和</span>
              </div>
            </el-descriptions-item>
            <el-descriptions-item label="运费" label-class-name="desc-label">
              <div style="display: flex; flex-direction: column; align-items: flex-start;">
                <span class="amount-highlight" style="font-size: 18px; font-weight: bold;">{{ currencySymbol }}{{ currentOrder.shippingFee }}</span>
                <span style="color: #909399; font-size: 12px; margin-top: 4px;">运费</span>
              </div>
            </el-descriptions-item>
            <el-descriptions-item label="优惠金额" label-class-name="desc-label">
              <div style="display: flex; flex-direction: column; align-items: flex-start;">
                <span class="discount-text" style="font-size: 18px; font-weight: bold;">-{{ currencySymbol }}{{ currentOrder.discountAmount }}</span>
                <span style="color: #909399; font-size: 12px; margin-top: 4px;">优惠金额</span>
              </div>
            </el-descriptions-item>
            <el-descriptions-item label="折扣明细" :span="3" label-class-name="desc-label">
              <div v-if="currentOrder.discountDetails" style="display: flex; gap: 15px; flex-wrap: wrap;">
                <div style="display: flex; align-items: center;">
                  <el-tag type="info" size="small">商品折扣：{{ currencySymbol }}{{ currentOrder.discountDetails.product_discount_amount || '0.00' }}</el-tag>
                </div>
                <div style="display: flex; align-items: center;">
                  <el-tag type="success" size="small">会员折扣：{{ currencySymbol }}{{ currentOrder.discountDetails.member_discount_amount || '0.00' }}</el-tag>
                </div>
                <div style="display: flex; align-items: center;">
                  <el-tag type="warning" size="small">满减优惠：{{ currencySymbol }}{{ currentOrder.discountDetails.full_reduction_amount || '0.00' }}</el-tag>
                </div>
                <div style="display: flex; align-items: center;">
                  <el-tag type="danger" size="small">总折扣：{{ currencySymbol }}{{ currentOrder.discountDetails.total_discount_amount || '0.00' }}</el-tag>
                </div>
              </div>
              <span v-else style="color: #909399;">无折扣</span>
            </el-descriptions-item>
            <el-descriptions-item label="订单总额" label-class-name="desc-label">
              <div style="display: flex; flex-direction: column; align-items: flex-start;">
                <span class="amount-highlight" style="font-size: 18px; font-weight: bold;">{{ currencySymbol }}{{ currentOrder.totalAmount }}</span>
                <span style="color: #909399; font-size: 12px; margin-top: 4px;">订单总额</span>
              </div>
            </el-descriptions-item>
            <el-descriptions-item label="实付金额" label-class-name="desc-label">
              <div style="display: flex; flex-direction: column; align-items: flex-start;">
                <span class="paid-amount" style="font-size: 18px; font-weight: bold;">{{ currencySymbol }}{{ currentOrder.paidAmount }}</span>
                <span style="color: #909399; font-size: 12px; margin-top: 4px;">实付金额</span>
              </div>
            </el-descriptions-item>
            <el-descriptions-item label="支付方式" label-class-name="desc-label">
              {{ getPaymentMethodText(currentOrder.paymentMethod) }}
            </el-descriptions-item>
            <el-descriptions-item label="支付状态" label-class-name="desc-label">
              <el-tag :type="getPaymentStatusTagType(currentOrder.paymentStatus)">
                {{ getPaymentStatusText(currentOrder.paymentStatus) }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="支付时间" :span="2" label-class-name="desc-label">
              {{ currentOrder.paymentTime || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="支付流水号" :span="3" label-class-name="desc-label">
              {{ currentOrder.paymentTransactionId || '-' }}
            </el-descriptions-item>
          </el-descriptions>
        </el-card>

        <!-- 收货信息 -->
        <el-card class="detail-card">
          <template #header>
            <div class="detail-card-header">
              <el-icon><Location /></el-icon>
              <span>收货信息</span>
            </div>
          </template>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="收货人" label-class-name="desc-label">
              {{ currentOrder.receiverName }}
            </el-descriptions-item>
            <el-descriptions-item label="联系电话" label-class-name="desc-label">
              {{ currentOrder.receiverPhone }}
            </el-descriptions-item>
            <el-descriptions-item label="收货地址" :span="2" label-class-name="desc-label">
              {{ currentOrder.receiverAddress || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="邮编" label-class-name="desc-label">
              {{ currentOrder.receiverZipcode || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="物流聚合状态" label-class-name="desc-label">
              <el-tag :type="getShippingStatusTagType(currentOrder.shippingStatus)">
                {{ getShippingStatusText(currentOrder.shippingStatus) }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="物流公司" label-class-name="desc-label">
              {{ currentOrder.logisticsCompany || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="物流单号" label-class-name="desc-label">
              {{ currentOrder.logisticsNo || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="发货时间" :span="2" label-class-name="desc-label">
              {{ currentOrder.shippedTime || '-' }}
            </el-descriptions-item>
          </el-descriptions>
        </el-card>

        <!-- 订单明细 -->
        <el-card class="detail-card">
          <template #header>
            <div class="detail-card-header">
              <el-icon><Goods /></el-icon>
              <span>订单明细</span>
            </div>
          </template>
          <el-table :data="orderItems" border stripe ref="orderItemsTable">
            <el-table-column label="序号" width="60" align="center">
              <template #default="scope">
                {{ scope.$index + 1 }}
              </template>
            </el-table-column>
            <el-table-column label="商品图片" width="100" align="center">
              <template #default="scope">
                <el-image
                  v-if="scope.row.productThumbnail"
                  :src="scope.row.signedThumbnailUrl || getImageUrl(scope.row.productThumbnail)"
                  :preview-src-list="[scope.row.signedThumbnailUrl || getImageUrl(scope.row.productThumbnail)]"
                  :initial-index="0"
                  fit="cover"
                  style="width: 60px; height: 60px; border-radius: 4px; cursor: pointer;"
                  preview-teleported
                />
                <span v-else style="color: #909399; font-size: 12px;">无图片</span>
              </template>
            </el-table-column>
            <el-table-column prop="productSku" label="商品SKU" width="140" show-overflow-tooltip />
            <el-table-column prop="productTitle" label="商品名称" min-width="200" show-overflow-tooltip />
            <el-table-column label="发货区域" width="100" align="center">
              <template #header>
                <span>发货区域</span>
              </template>
              <template #default="scope">
                <el-tag type="primary" size="small">{{ scope.row.shippingRegion || '-' }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="supplierName" label="供应商" width="120" show-overflow-tooltip />
            <el-table-column label="商品原价" width="120" align="right">
              <template #header>
                <span>商品原价</span>
              </template>
              <template #default="scope">
                <span v-if="scope.row.originalUnitPrice" style="color: #909399; text-decoration: line-through;">{{ currencySymbol }}{{ scope.row.originalUnitPrice }}</span>
                <span v-else style="color: #909399;">-</span>
              </template>
            </el-table-column>
            <el-table-column label="商品售价" width="120" align="right">
              <template #header>
                <span>商品售价</span>
              </template>
              <template #default="scope">
                {{ currencySymbol }}{{ scope.row.unitPrice }}
              </template>
            </el-table-column>
            <el-table-column label="实付价格" width="120" align="right">
              <template #header>
                <span>实付价格</span>
              </template>
              <template #default="scope">
                <span style="color: #67c23a; font-weight: bold;">{{ currencySymbol }}{{ scope.row.actualUnitPrice }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="quantity" label="数量" width="80" align="center" />
            <el-table-column label="商品运费" width="120" align="right">
              <template #header>
                <span>商品运费</span>
              </template>
              <template #default="scope">
                {{ currencySymbol }}{{ scope.row.shippingFee }}
              </template>
            </el-table-column>
            <el-table-column label="支付总价" width="120" align="right">
              <template #header>
                <span>支付总价</span>
              </template>
              <template #default="scope">
                <span style="font-weight: bold;">{{ currencySymbol }}{{ scope.row.subtotalAmount }}</span>
              </template>
            </el-table-column>
            <el-table-column label="折扣明细" width="300" align="center">
              <template #header>
                <span>折扣明细</span>
              </template>
              <template #default="scope">
                <div v-if="scope.row.discountDetails" style="display: flex; flex-direction: column; gap: 5px; align-items: flex-start;">
                  <el-tag v-if="parseFloat(scope.row.discountDetails.product_discount_amount || 0) > 0" type="info" size="small">
                    商品折扣: {{ currencySymbol }}{{ scope.row.discountDetails.product_discount_amount }}
                  </el-tag>
                  <el-tag v-if="scope.row.discountDetails.member_discount_rate" type="success" size="small">
                    会员折扣: {{ formatDiscountRate(scope.row.discountDetails.member_discount_rate) }} / {{ currencySymbol }}{{ scope.row.discountDetails.member_discount_amount }}
                  </el-tag>
                  <el-tag v-if="parseFloat(scope.row.discountDetails.full_reduction_amount || 0) > 0" type="warning" size="small">
                    满减: {{ currencySymbol }}{{ scope.row.discountDetails.full_reduction_amount }}
                  </el-tag>
                  <el-tag type="danger" size="small">
                    总折扣: {{ currencySymbol }}{{ scope.row.discountDetails.total_discount_amount || '0.00' }}
                  </el-tag>
                </div>
                <span v-else style="color: #909399; font-size: 12px;">无折扣</span>
              </template>
            </el-table-column>
            <el-table-column label="佣金比例" width="100" align="center">
              <template #header>
                <span>佣金比例</span>
              </template>
              <template #default="scope">
                <el-tag :type="scope.row.commissionRate === '0.0000' ? 'success' : 'warning'" size="small">
                  {{ formatCommissionRate(scope.row.commissionRate) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="平台收入" width="120" align="right">
              <template #header>
                <span>平台收入</span>
              </template>
              <template #default="scope">
                <span style="color: #e6a23c;">{{ currencySymbol }}{{ scope.row.commissionAmount }}</span>
              </template>
            </el-table-column>
            <el-table-column label="供应商收入" width="140" align="right">
              <template #header>
                <span>供应商收入</span>
              </template>
              <template #default="scope">
                <span style="color: #67c23a; font-weight: bold;">{{ currencySymbol }}{{ scope.row.supplierIncome }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="orderStatus" label="订单项状态" width="200" align="center">
              <template #default="scope">
                <div style="display: flex; flex-direction: column; gap: 5px; align-items: center;">
                  <el-tag :type="getOrderStatusTagType(scope.row.orderStatus)" size="small">
                    {{ getOrderStatusText(scope.row.orderStatus) }}
                  </el-tag>
                  <!-- 显示退款原因（仅在 applying 或 refunding 状态时显示） -->
                  <div v-if="(scope.row.orderStatus === 'refunding' || scope.row.refundStatus === 'applying') && scope.row.refundReason" 
                       style="font-size: 12px; color: #606266; max-width: 180px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                    退款原因：{{ scope.row.refundReason }}
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column label="物流信息" width="200" align="center">
              <template #default="scope">
                <div v-if="scope.row.logisticsCompany || scope.row.logisticsNo" style="display: flex; flex-direction: column; gap: 5px; align-items: flex-start;">
                  <div v-if="scope.row.logisticsCompany" style="font-size: 12px;">
                    <span style="color: #606266;">物流公司：</span>
                    <span style="color: #303133; font-weight: 500;">{{ scope.row.logisticsCompany.name_zh || scope.row.logisticsCompany.name_en || '-' }}</span>
                  </div>
                  <div v-if="scope.row.logisticsNo" style="font-size: 12px;">
                    <span style="color: #606266;">物流单号：</span>
                    <span style="color: #409eff; font-weight: 500;">{{ scope.row.logisticsNo }}</span>
                  </div>
                  <div v-if="scope.row.shippedTime" style="font-size: 12px; color: #909399;">
                    {{ scope.row.shippedTime }}
                  </div>
                </div>
                <span v-else style="color: #909399; font-size: 12px;">未发货</span>
              </template>
            </el-table-column>
            <el-table-column prop="refundStatus" label="退款状态" width="100" align="center">
              <template #default="scope">
                <el-tag v-if="scope.row.refundStatus !== 'none'" :type="getRefundStatusTagType(scope.row.refundStatus)" size="small">
                  {{ getRefundStatusText(scope.row.refundStatus) }}
                </el-tag>
                <span v-else style="color: #909399;">-</span>
              </template>
            </el-table-column>
          </el-table>
          <div v-loading="detailLoading" element-loading-text="正在加载..." style="min-height: 100px;">
            <div style="margin-top: 10px; padding: 10px; background-color: #f5f7fa; border-radius: 4px;">
              <div style="color: #606266; font-size: 13px; line-height: 1.6;">
                <strong style="color: #303133;">说明：</strong>
                <span>供应商收入 = 纯商品金额 - 平台收入（<span style="color: #e6a23c; font-weight: 500;">不包含运费，运费供应商自行承担</span>）</span>
              </div>
            </div>
          </div>
        </el-card>

        <!-- 备注信息 -->
        <el-card class="detail-card">
          <template #header>
            <div class="detail-card-header">
              <el-icon><EditPen /></el-icon>
              <span>备注信息</span>
            </div>
          </template>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="买家留言" label-class-name="desc-label">
              {{ currentOrder.buyerMessage || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="卖家备注" label-class-name="desc-label">
              <el-input
                v-model="remarkText"
                type="textarea"
                :rows="3"
                placeholder="请输入卖家备注（内部备注，买家不可见）"
              />
              <el-button 
                type="primary" 
                size="small" 
                @click="saveRemark"
                style="margin-top: 10px;"
              >
                保存备注
              </el-button>
            </el-descriptions-item>
            <el-descriptions-item label="完成时间" label-class-name="desc-label">
              {{ currentOrder.completedTime || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="取消时间" label-class-name="desc-label">
              {{ currentOrder.cancelledTime || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="取消原因" label-class-name="desc-label">
              {{ currentOrder.cancelReason || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="更新时间" label-class-name="desc-label">
              {{ currentOrder.updatedAt }}
            </el-descriptions-item>
          </el-descriptions>
        </el-card>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, defineExpose, nextTick } from 'vue'
import {
  ElCard,
  ElTable,
  ElTableColumn,
  ElButton,
  ElForm,
  ElFormItem,
  ElInput,
  ElSelect,
  ElOption,
  ElTag,
  ElMessage,
  ElPagination,
  ElRow,
  ElCol,
  ElIcon,
  ElDialog,
  ElDescriptions,
  ElDescriptionsItem,
  ElTooltip,
  ElImage,
  vLoading
} from 'element-plus'
import {
  ShoppingCart,
  Search,
  Refresh,
  RefreshLeft,
  List,
  Document,
  Money,
  Location,
  Goods,
  EditPen,
  QuestionFilled
} from '@element-plus/icons-vue'

// 定义组件属性
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

// 定义响应式数据
const orders = ref([])
const loading = ref(false)
const currencySymbol = ref('$')
const pagination = ref({
  currentPage: 1,
  totalPages: 1,
  totalItems: 0,
  itemsPerPage: 20
})

// 搜索表单
const searchForm = ref({
  orderNo: '',
  customerUsername: '',
  orderStatus: '',
  paymentStatus: ''
})

// 订单详情相关
const detailDialogVisible = ref(false)
const currentOrder = ref(null)
const orderItems = ref([])
const remarkText = ref('')
const orderItemsTable = ref(null)
const detailLoading = ref(false)  // 订单详情加载状态

// 获取订单状态文本
const getOrderStatusText = (status) => {
  const statusMap = {
    'pending_payment': '待支付',
    'paid': '已支付',
    'shipped': '已发货',
    'completed': '已完成',
    'cancelled': '已取消',
    'refunding': '退款中',
    'refunded': '已退款',
    'partial_shipped': '部分发货',
    'mixed': '混合状态'
  }
  return statusMap[status] || status
}

// 获取订单状态标签类型
const getOrderStatusTagType = (status) => {
  const typeMap = {
    'pending_payment': 'warning',
    'paid': 'success',
    'shipped': 'primary',
    'completed': 'success',
    'cancelled': 'info',
    'refunding': 'warning',
    'refunded': 'danger',
    'partial_shipped': '',  // 默认蓝色
    'mixed': 'info'
  }
  return typeMap[status] || 'info'
}

// 获取支付状态文本
const getPaymentStatusText = (status) => {
  const statusMap = {
    'unpaid': '未支付',
    'paid': '已支付',
    'cancelled': '已取消',
    'refunded': '已退款'
  }
  return statusMap[status] || status
}

// 获取支付状态标签类型
const getPaymentStatusTagType = (status) => {
  const typeMap = {
    'unpaid': 'warning',
    'paid': 'success',
    'cancelled': 'info',
    'refunded': 'danger'
  }
  return typeMap[status] || 'info'
}

// 获取物流状态文本
const getShippingStatusText = (status) => {
  const statusMap = {
    'unshipped': '未发货',
    'shipped': '已发货',
    'received': '已收货',
    'partial_shipped': '部分发货'
  }
  return statusMap[status] || status
}

// 获取物流状态标签类型
const getShippingStatusTagType = (status) => {
  const typeMap = {
    'unshipped': 'info',
    'shipped': 'primary',
    'received': 'success',
    'partial_shipped': ''
  }
  return typeMap[status] || 'info'
}

// 获取支付方式文本
const getPaymentMethodText = (method) => {
  const methodMap = {
    'balance': '余额支付',
    'alipay': '支付宝',
    'wechat': '微信',
    'paypal': 'PayPal'
  }
  return methodMap[method] || method || '-'
}

// 获取物流方式文本
const getShippingMethodText = (method) => {
  const methodMap = {
    'STANDARD_SHIPPING': '标准物流',
    'SELF_PICKUP': '自提'
  }
  return methodMap[method] || method || '-'
}

// 获取退款状态文本
const getRefundStatusText = (status) => {
  const statusMap = {
    'none': '无退款',
    'applying': '申请中',
    'approved': '商家同意',
    'buyer_shipped': '买家已发货',
    'completed': '已完成',
    'rejected': '已拒绝'
  }
  return statusMap[status] || status
}

// 获取退款状态标签类型
const getRefundStatusTagType = (status) => {
  const typeMap = {
    'none': 'info',
    'applying': 'warning',
    'approved': 'primary',
    'buyer_shipped': '',
    'completed': 'success',
    'rejected': 'danger'
  }
  return typeMap[status] || 'info'
}

// 格式化佣金比例
const formatCommissionRate = (rate) => {
  if (rate === null || rate === undefined) return '-'
  const numRate = parseFloat(rate)
  if (numRate === 0) return '0% (免佣)'
  return (numRate * 100).toFixed(2) + '%'
}

// 格式化折扣率
const formatDiscountRate = (rate) => {
  if (rate === null || rate === undefined) return '-'
  const numRate = parseFloat(rate)
  if (numRate === 0) return '0%'
  return (numRate * 100).toFixed(2) + '%'
}

// 获取图片URL（带签名）
const getImageUrl = (qiniuKey) => {
  if (!qiniuKey) return ''
  
  // 如果已经是完整URL，直接返回
  if (qiniuKey.startsWith('http://') || qiniuKey.startsWith('https://')) {
    return qiniuKey
  }
  
  // 如果是七牛云key，返回拼接的域名URL
  const qiniuDomain = window.QINIU_DOMAIN || 'http://qiniu.difeng1688.com'
  return `${qiniuDomain}/${qiniuKey}`
}

// 获取签名URL（异步）
const getSignedUrl = async (qiniuKey) => {
  if (!qiniuKey) return ''
  
  // 如果已经是完整URL，直接返回
  if (qiniuKey.startsWith('http://') || qiniuKey.startsWith('https://')) {
    return qiniuKey
  }
  
  try {
    // 调用后端接口获取签名 URL
    const response = await fetch(`/admin${props.adminLoginPath}/order/qiniu/sign-url`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: JSON.stringify({ key: qiniuKey })
    })
    
    const result = await response.json()
    
    if (result.success && result.data) {
      return result.data.signedUrl || result.data
    }
  } catch (error) {
    console.error('获取签名 URL 失败:', error)
  }
  
  // 如果签名失败，返回原 URL
  return getImageUrl(qiniuKey)
}

// 加载订单数据
const loadOrderData = async (page = 1, limit = 20) => {
  loading.value = true
  try {
    const params = new URLSearchParams({
      page: page,
      limit: limit,
      orderNo: searchForm.value.orderNo,
      customerUsername: searchForm.value.customerUsername,
      orderStatus: searchForm.value.orderStatus,
      paymentStatus: searchForm.value.paymentStatus
    })
    
    const url = `/admin${props.adminLoginPath}/order/list?${params}`
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    
    const result = await response.json()
    
    if (result.success) {
      orders.value = result.data
      pagination.value = result.pagination
      // 更新货币符号
      if (result.currencySymbol) {
        currencySymbol.value = result.currencySymbol
      }
    } else {
      ElMessage.error(result.message || '加载数据失败')
    }
  } catch (error) {
    ElMessage.error('加载数据失败: ' + error.message)
  } finally {
    loading.value = false
  }
}

// 查看订单详情
const viewOrderDetail = async (order) => {
  // 触发导航事件，打开订单详情tab页
  window.dispatchEvent(new CustomEvent('navigate-to-order-detail', {
    detail: {
      orderId: order.id
    }
  }))
}

// 复制订单号
const copyOrderNo = async (orderNo) => {
  try {
    // 使用 Clipboard API
    if (navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(orderNo)
      ElMessage.success('已复制')
    } else {
      // 降级方案：使用 textarea
      const textarea = document.createElement('textarea')
      textarea.value = orderNo
      textarea.style.position = 'fixed'
      textarea.style.opacity = '0'
      document.body.appendChild(textarea)
      textarea.select()
      document.execCommand('copy')
      document.body.removeChild(textarea)
      ElMessage.success('已复制')
    }
  } catch (error) {
    console.error('复制失败:', error)
    ElMessage.error('复制失败')
  }
}

// 初始化表格拖动功能
const initTableDrag = () => {
  if (!orderItemsTable.value) {
    console.log('表格 ref 不存在')
    return
  }
  
  // 获取表格容器
  const tableEl = orderItemsTable.value.$el
  if (!tableEl) {
    console.log('表格元素不存在')
    return
  }
  
  // 获取表格 body wrapper
  const bodyWrapper = tableEl.querySelector('.el-table__body-wrapper')
  
  if (!bodyWrapper) {
    console.log('表格 body wrapper 不存在')
    return
  }
  
  console.log('初始化表格拖动功能', bodyWrapper)
  
  let isDown = false
  let startX = 0
  let scrollLeft = 0
  
  // 设置样式 - 确保可以滚动
  bodyWrapper.style.cursor = 'grab'
  bodyWrapper.style.overflowX = 'auto'
  bodyWrapper.style.userSelect = 'none'
  
  // 移除可能存在的旧事件
  bodyWrapper.onmousedown = null
  bodyWrapper.onmouseleave = null  
  bodyWrapper.onmouseup = null
  bodyWrapper.onmousemove = null
  
  bodyWrapper.addEventListener('mousedown', (e) => {
    // 如果点击的是按钮、图片等互动元素，不启动拖动
    const target = e.target
    if (target.closest('button') || target.closest('a') || target.closest('.el-button') ||
        target.closest('.el-tag') || target.closest('.el-image') || target.closest('img')) {
      return
    }
    
    isDown = true
    bodyWrapper.style.cursor = 'grabbing'
    startX = e.pageX - bodyWrapper.offsetLeft
    scrollLeft = bodyWrapper.scrollLeft
    e.preventDefault()
  }, { passive: false })
  
  bodyWrapper.addEventListener('mouseleave', () => {
    isDown = false
    bodyWrapper.style.cursor = 'grab'
  })
  
  bodyWrapper.addEventListener('mouseup', () => {
    isDown = false
    bodyWrapper.style.cursor = 'grab'
  })
  
  bodyWrapper.addEventListener('mousemove', (e) => {
    if (!isDown) return
    e.preventDefault()
    const x = e.pageX - bodyWrapper.offsetLeft
    const walk = (x - startX) * 2
    bodyWrapper.scrollLeft = scrollLeft - walk
  }, { passive: false })
  
  console.log('表格拖动功能已绑定')
}

// 保存备注
const saveRemark = async () => {
  try {
    const response = await fetch(`/admin${props.adminLoginPath}/order/${currentOrder.value.id}/remark`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: JSON.stringify({
        sellerRemark: remarkText.value
      })
    })
    
    const result = await response.json()
    
    if (result.success) {
      ElMessage.success('备注保存成功')
      currentOrder.value.sellerRemark = remarkText.value
    } else {
      ElMessage.error(result.message || '保存备注失败')
    }
  } catch (error) {
    ElMessage.error('保存备注失败: ' + error.message)
  }
}

// 刷新数据
const refreshData = () => {
  loadOrderData(pagination.value.currentPage, pagination.value.itemsPerPage)
}

// 搜索订单
const searchOrders = () => {
  pagination.value.currentPage = 1
  loadOrderData(1, pagination.value.itemsPerPage)
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    orderNo: '',
    customerUsername: '',
    orderStatus: '',
    paymentStatus: ''
  }
  pagination.value.currentPage = 1
  loadOrderData(1, pagination.value.itemsPerPage)
}

// 处理分页大小变化
const handleSizeChange = (val) => {
  pagination.value.itemsPerPage = val
  loadOrderData(pagination.value.currentPage, val)
}

// 处理当前页变化
const handleCurrentChange = (val) => {
  pagination.value.currentPage = val
  loadOrderData(val, pagination.value.itemsPerPage)
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

// 格式化时间
const formatTime = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// 根据订单号搜索订单（从余额记录跳转时使用）
const searchByOrderNo = (orderNo) => {
  if (!orderNo) {
    ElMessage.warning('订单号为空')
    return
  }
  // 设置搜索条件
  searchForm.value.orderNo = orderNo
  searchForm.value.customerUsername = ''
  searchForm.value.orderStatus = ''
  searchForm.value.paymentStatus = ''
  // 执行搜索
  pagination.value.currentPage = 1
  loadOrderData(1, pagination.value.itemsPerPage)
}

// 组件挂载时加载数据
onMounted(() => {
  if (props.autoLoad) {
    loadOrderData()
  }
})

// 暴露方法给父组件调用
defineExpose({
  loadOrderData,
  searchByOrderNo
})
</script>

<style scoped>
.order-container {
  width: 100%;
  max-width: 2000px;
  box-sizing: border-box;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  width: 100%;
}

.page-title {
  font-size: 24px;
  font-weight: bold;
  margin: 0;
  display: flex;
  align-items: center;
}

.title-icon {
  margin-right: 10px;
  vertical-align: middle;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.filter-card {
  margin-bottom: 20px;
  width: 100%;
}

.filter-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.filter-icon {
  margin-right: 10px;
  vertical-align: middle;
}

.filter-title {
  font-size: 18px;
  font-weight: bold;
  display: flex;
  align-items: center;
}

.search-form {
  width: 100%;
}

.search-form :deep(.el-form-item) {
  margin-bottom: 0;
  display: flex;
  align-items: center;
}

.search-form :deep(.el-form-item__label) {
  width: 100px;
  margin-right: 10px;
  margin-bottom: 0;
  text-align: right;
  flex-shrink: 0;
}

.search-form :deep(.el-form-item__content) {
  width: calc(100% - 110px);
  display: flex;
  align-items: center;
}

.action-col {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.form-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.table-card {
  width: 100%;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.table-header-title {
  font-size: 18px;
  font-weight: bold;
  display: flex;
  align-items: center;
}

.table-icon {
  margin-right: 10px;
  vertical-align: middle;
}

.table-header-info {
  font-size: 14px;
  color: #909399;
}

.order-table {
  width: 100% !important;
  font-size: 14px;
}

.order-table :deep(.el-table__header th) {
  background-color: #f5f7fa;
  color: #606266;
  font-weight: bold;
}

.order-table :deep(.el-table__body td) {
  transition: background-color 0.3s;
}

.order-table :deep(.el-table__row:hover) {
  background-color: #f5f7fa;
}

.order-table :deep(.el-table__row:hover td) {
  background-color: #f5f7fa !important;
}

.time-cell {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.date {
  font-size: 14px;
  color: #303133;
}

.time {
  font-size: 12px;
  color: #909399;
}

.amount-text {
  font-weight: bold;
  color: #f56c6c;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  width: 100%;
}

/* 订单详情样式 */
.order-detail {
  max-height: 70vh;
  overflow-y: auto;
}

.detail-card {
  margin-bottom: 20px;
}

.detail-card-header {
  display: flex;
  align-items: center;
  font-weight: bold;
}

.detail-card-header .el-icon {
  margin-right: 8px;
}

.paid-amount {
  font-weight: bold;
  color: #f56c6c;
  font-size: 16px;
}

.amount-highlight {
  font-weight: bold;
  color: #409eff;
}

.discount-text {
  font-weight: bold;
  color: #67c23a;
}

.order-no-text {
  font-weight: 600;
  color: #303133;
  font-size: 15px;
}

/* 描述列表样式 */
:deep(.desc-label) {
  background-color: #fafafa !important;
  font-weight: 600 !important;
  color: #606266 !important;
}

/* 订单号链接样式 */
.order-table :deep(.order-no-link) {
  font-weight: 600;
  color: #409eff !important;
  text-decoration: underline;
  text-decoration-style: dotted;
}

.order-table :deep(.order-no-link:hover) {
  color: #66b1ff !important;
  text-decoration-style: solid;
}
</style>
