<template>
  <div class="order-detail-tab-container">
    <!-- 右上角刷新按钮 -->
    <div class="refresh-button-container">
      <el-button 
        type="primary" 
        :icon="Refresh" 
        circle
        :loading="detailLoading"
        @click="handleRefresh"
        title="刷新订单数据"
      />
    </div>
    
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
            <div style="display: flex; flex-direction: column; gap: 8px;">
              <div>{{ currentOrder.paymentTransactionId || '-' }}</div>
              <div v-if="currentOrder.paymentCallbackLog" style="font-size: 12px; color: #909399; padding: 8px; background: #f5f7fa; border-radius: 4px; white-space: pre-wrap; line-height: 1.6;">
                <div style="color: #606266; font-weight: 500; margin-bottom: 4px;">支付回调日志：</div>
                {{ currentOrder.paymentCallbackLog }}
              </div>
            </div>
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
        <el-descriptions :column="1" border>
          <el-descriptions-item label="收货信息" label-class-name="desc-label">
            <div style="font-size: 14px; color: #303133;">
              {{ currentOrder.receiverAddress || '-' }}，{{ currentOrder.receiverName }}，{{ currentOrder.receiverPhone }}，邮编：{{ currentOrder.receiverZipcode || '-' }}
            </div>
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
        <el-table :data="orderItems" border stripe ref="orderItemsTable" :span-method="arraySpanMethod" :default-sort="{prop: 'id', order: 'ascending'}" style="width: 100%">
          <el-table-column label="序号" width="60" align="center">
            <template #default="scope">
              <span v-if="!scope.row.isLogisticsRow && !scope.row.isRefundReasonRow">{{ scope.row.displayIndex }}</span>
            </template>
          </el-table-column>
          <el-table-column label="商品信息" min-width="280" align="left">
            <template #header>
              <span>商品信息</span>
            </template>
            <template #default="scope">
              <!-- 物流信息行 -->
              <div v-if="scope.row.isLogisticsRow" style="font-size: 13px; padding: 10px; background: #f5f7fa; line-height: 2; width: 100%;">
                <div style="margin-bottom: 8px;">
                  <span style="color: #606266; font-weight: 500; font-size: 13px;">订单项状态：</span>
                  <el-tag :type="getOrderStatusTagType(scope.row.parentOrderStatus)" size="small" style="margin-right: 12px;">
                    {{ getOrderStatusText(scope.row.parentOrderStatus) }}
                  </el-tag>
                  <span style="color: #606266; font-weight: 500; font-size: 13px;">退款状态：</span>
                  <el-tag v-if="scope.row.parentRefundStatus !== 'none'" :type="getRefundStatusTagType(scope.row.parentRefundStatus)" size="small" style="margin-right: 12px;">
                    {{ getRefundStatusText(scope.row.parentRefundStatus) }}
                  </el-tag>
                  <span v-else style="color: #909399; margin-right: 12px;">无</span>
                </div>
                <div style="margin-bottom: 6px;">
                  <span style="margin: 0 4px; color: #dcdfe6;">|</span>
                  <span style="color: #606266; font-weight: 600; font-size: 14px;">发货物流：</span>
                  <span v-if="scope.row.logisticsCompany || scope.row.logisticsNo" style="font-size: 13px;">
                    {{ scope.row.logisticsCompany?.name_zh || scope.row.logisticsCompany?.name_en || '-' }}
                    <el-link 
                      v-if="scope.row.logisticsNo" 
                      type="primary" 
                      @click="handleTrackExpress(scope.row.logisticsNo)"
                      style="margin-left: 4px; cursor: pointer; font-size: 13px; font-weight: 600;"
                    >
                      {{ scope.row.logisticsNo }}
                      <el-icon><View /></el-icon>
                    </el-link>
                    <span v-else style="color: #909399;">-</span>
                  </span>
                  <span v-else style="color: #909399;">未发货</span>
                </div>
                <!-- 发货物流最新动态 -->
                <div v-if="scope.row.latestLogisticsMessage" style="padding-left: 20px; color: #67c23a; font-size: 13px; font-weight: 500; margin-bottom: 6px; line-height: 1.6;">
                  <el-icon style="vertical-align: middle; font-size: 14px;"><Clock /></el-icon>
                  <span style="margin-left: 6px; font-weight: 600;">{{ scope.row.latestLogisticsTime }}</span>
                  <span style="margin-left: 10px;">{{ scope.row.latestLogisticsMessage }}</span>
                </div>
                <div>
                  <span style="margin: 0 4px; color: #dcdfe6;">|</span>
                  <span style="color: #606266; font-weight: 600; font-size: 14px;">退货物流：</span>
                  <span v-if="scope.row.refundLogisticsCompany || scope.row.refundLogisticsNo" style="font-size: 13px;">
                    {{ scope.row.refundLogisticsCompany?.name_zh || scope.row.refundLogisticsCompany?.name_en || '-' }}
                    <el-link 
                      v-if="scope.row.refundLogisticsNo" 
                      type="warning" 
                      @click="handleTrackExpress(scope.row.refundLogisticsNo)"
                      style="margin-left: 4px; cursor: pointer; font-size: 13px; font-weight: 600;"
                    >
                      {{ scope.row.refundLogisticsNo }}
                      <el-icon><View /></el-icon>
                    </el-link>
                    <span v-else style="color: #909399;">-</span>
                  </span>
                  <span v-else style="color: #909399;">无</span>
                </div>
                <!-- 退货物流最新动态 -->
                <div v-if="scope.row.latestRefundLogisticsMessage" style="padding-left: 20px; color: #e6a23c; font-size: 13px; font-weight: 500; line-height: 1.6;">
                  <el-icon style="vertical-align: middle; font-size: 14px;"><Clock /></el-icon>
                  <span style="margin-left: 6px; font-weight: 600;">{{ scope.row.latestRefundLogisticsTime }}</span>
                  <span style="margin-left: 10px;">{{ scope.row.latestRefundLogisticsMessage }}</span>
                </div>
              </div>
              <!-- 退款原因行 -->
              <div v-else-if="scope.row.isRefundReasonRow" style="font-size: 12px; padding: 8px; background: #fef0f0; color: #f56c6c; line-height: 1.6; width: 100%;">
                <span style="font-weight: 500;">退款原因：</span>{{ scope.row.refundReason }}
              </div>
              <!-- 商品信息行 -->
              <div v-else style="display: flex; gap: 12px; align-items: center;">
                <div style="flex-shrink: 0;">
                  <el-image
                    v-if="scope.row.productThumbnail"
                    :src="scope.row.signedThumbnailUrl || getImageUrl(scope.row.productThumbnail)"
                    :preview-src-list="[scope.row.signedThumbnailUrl || getImageUrl(scope.row.productThumbnail)]"
                    :initial-index="0"
                    fit="cover"
                    style="width: 60px; height: 60px; border-radius: 4px; cursor: pointer;"
                    preview-teleported
                  />
                  <div v-else style="width: 60px; height: 60px; background: #f5f7fa; border-radius: 4px; display: flex; align-items: center; justify-content: center;">
                    <span style="color: #909399; font-size: 12px;">无图</span>
                  </div>
                </div>
                <div style="flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 4px;">
                  <div 
                    style="font-size: 14px; color: #409eff; font-weight: 500; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; cursor: pointer;" 
                    :title="scope.row.productTitle + ' (点击查看商品详情)'"
                    @click="goToProductDetail(scope.row.productId)"
                  >
                    {{ scope.row.productTitle }}
                  </div>
                  <div 
                    style="font-size: 12px; color: #409eff; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; cursor: pointer;" 
                    :title="scope.row.productSku + ' (点击查看商品详情)'"
                    @click="goToProductDetail(scope.row.productId)"
                  >
                    SKU: {{ scope.row.productSku }}
                  </div>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="供应商&发货区" width="140" align="center">
            <template #header>
              <span>供应商&发货区</span>
            </template>
            <template #default="scope">
              <div v-if="!scope.row.isLogisticsRow && !scope.row.isRefundReasonRow" style="display: flex; flex-direction: column; gap: 4px; align-items: center;">
                <div 
                  style="font-size: 13px; color: #409eff; font-weight: 500; cursor: pointer; text-decoration: underline;"
                  :title="'点击查看供应商详情'"
                  @click="handleViewSupplier(scope.row.supplierId)"
                >
                  {{ scope.row.supplierName }}
                </div>
                <el-tag type="primary" size="small">{{ scope.row.shippingRegion || '-' }}</el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="商品价格" width="120" align="center">
            <template #header>
              <span>商品价格</span>
            </template>
            <template #default="scope">
              <div style="display: flex; flex-direction: column; gap: 2px; align-items: center;">
                <div style="font-size: 14px; color: #303133; font-weight: 600;">
                  <span style="font-size: 12px; color: #909399; font-weight: normal;">售价</span>
                  {{ currencySymbol }}{{ scope.row.unitPrice }}
                </div>
                <div v-if="scope.row.originalUnitPrice" style="font-size: 12px; color: #909399; text-decoration: line-through;">
                  <span style="text-decoration: none;">原价</span>
                  {{ currencySymbol }}{{ scope.row.originalUnitPrice }}
                </div>
                <div v-else style="font-size: 12px; color: #909399;">-</div>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="价格明细" width="200" align="left">
            <template #header>
              <span>价格明细</span>
            </template>
            <template #default="scope">
              <div style="display: flex; flex-direction: column; gap: 3px; padding: 8px 0; font-size: 13px; line-height: 1.4;">
                <div style="display: flex; align-items: center; gap: 8px;">
                  <span style="color: #909399; font-size: 12px;">实付</span>
                  <span style="color: #67c23a; font-weight: bold;">{{ currencySymbol }}{{ scope.row.actualUnitPrice }}</span>
                  <span style="color: #909399;">×</span>
                  <span style="color: #303133; font-weight: 600;">{{ scope.row.quantity }}</span>
                  <span style="color: #909399; font-size: 12px;">数量</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                  <span style="color: #909399;">+</span>
                  <span style="color: #e6a23c; font-weight: 600;">{{ currencySymbol }}{{ scope.row.shippingFee }}</span>
                  <span style="color: #909399; font-size: 12px;">运费</span>
                </div>
                <div style="border-top: 1px dashed #dcdfe6; margin: 2px 0;"></div>
                <div style="display: flex; align-items: center; gap: 8px;">
                  <span style="color: #606266; font-size: 12px;">支付总价：</span>
                  <span style="font-weight: bold; color: #f56c6c; font-size: 14px;">{{ currencySymbol }}{{ scope.row.subtotalAmount }}</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px; margin-top: 4px;">
                  <span style="color: #909399; font-size: 12px;">物流方式：</span>
                  <el-tag :type="scope.row.shippingMethod === 'STANDARD_SHIPPING' ? 'success' : 'warning'" size="small">
                    {{ getShippingMethodText(scope.row.shippingMethod) }}
                  </el-tag>
                </div>
              </div>
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
          <el-table-column label="佣金&收入" width="280" align="center">
            <template #header>
              <span>佣金&收入</span>
            </template>
            <template #default="scope">
              <div style="display: flex; flex-direction: column; gap: 3px; padding: 8px 0; font-size: 13px; line-height: 1.4; align-items: flex-start;">
                <div style="display: flex; align-items: center; gap: 8px;">
                  <span style="color: #909399; font-size: 12px;">实付</span>
                  <span style="color: #67c23a; font-weight: bold;">{{ currencySymbol }}{{ scope.row.actualUnitPrice }}</span>
                  <span style="color: #909399;">×</span>
                  <span style="color: #303133; font-weight: 600;">{{ scope.row.quantity }}</span>
                  <span style="color: #909399; font-size: 12px;">数量</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                  <span style="color: #909399;">-</span>
                  <span style="color: #e6a23c; font-weight: 600;">{{ currencySymbol }}{{ scope.row.commissionAmount }}</span>
                  <span style="color: #909399; font-size: 12px;">平台收入</span>
                </div>
                <div style="border-top: 1px dashed #dcdfe6; margin: 2px 0; width: 100%;"></div>
                <div style="display: flex; align-items: center; gap: 8px;">
                  <span style="color: #606266; font-size: 12px;">供应商收入：</span>
                  <span style="font-weight: bold; color: #67c23a; font-size: 14px;">{{ currencySymbol }}{{ scope.row.supplierIncome }}</span>
                </div>
                <div style="font-size: 11px; color: #909399; margin-top: 2px;">
                  <span>佣金比例：</span>
                  <el-tag :type="scope.row.commissionRate === '0.0000' ? 'success' : 'warning'" size="small">
                    {{ formatCommissionRate(scope.row.commissionRate) }}
                  </el-tag>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="220" align="center" fixed="right">
            <template #default="scope">
              <!-- 确认收货并完成退款按钮 -->
              <div v-if="scope.row.orderStatus === 'refunding' && scope.row.refundStatus === 'buyer_shipped'" style="display: flex; flex-direction: column; align-items: center; gap: 6px;">
                <el-button
                  type="warning"
                  size="small"
                  @click="handleConfirmRefundReceived(scope.row)"
                >
                  确认收货并完成退款
                </el-button>
                <div style="font-size: 11px; color: #909399; line-height: 1.4; text-align: center; max-width: 200px;">
                  <div style="margin-bottom: 2px;">
                    <el-icon style="font-size: 12px; vertical-align: middle;"><InfoFilled /></el-icon>
                    供应商在15天内未处理，管理员有权强制执行
                  </div>
                  <div v-if="scope.row.refundBuyerShippedTime" style="color: #f56c6c; font-weight: 500;">
                    截止：{{ getRefundDeadline(scope.row.refundBuyerShippedTime) }}
                  </div>
                </div>
              </div>
              <span v-else style="color: #909399; font-size: 12px;">-</span>
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
    
    <!-- 快递查询弹窗 -->
    <ExpressTrackingDialog ref="expressTrackingDialog" />
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { 
  ElCard,
  ElDescriptions,
  ElDescriptionsItem,
  ElTag,
  ElTable,
  ElTableColumn,
  ElImage,
  ElInput,
  ElButton,
  ElTooltip,
  ElIcon,
  ElMessage,
  ElMessageBox,
  ElLink,
  vLoading
} from 'element-plus'
import { Document, Money, Location, Goods, EditPen, QuestionFilled, InfoFilled, Refresh, View, Clock } from '@element-plus/icons-vue'
import ExpressTrackingDialog from './ExpressTrackingDialog.vue'

const props = defineProps({
  adminLoginPath: {
    type: String,
    default: ''
  },
  orderId: {
    type: Number,
    default: null
  }
})

const currentOrder = ref(null)
const orderItems = ref([])
const remarkText = ref('')
const orderItemsTable = ref(null)
const detailLoading = ref(false)
const expressTrackingDialog = ref(null)
const currencySymbol = ref('$')

/**
 * 表格单元格合并方法
 * 物流信息行和退款原因行需要跨越所有列
 */
const arraySpanMethod = ({ row, column, rowIndex, columnIndex }) => {
  // 物流信息行：跨越所有列
  if (row.isLogisticsRow) {
    if (columnIndex === 1) {
      // 商品信息列显示内容，并跨越所有列
      return { rowspan: 1, colspan: 10 }
    } else {
      // 其他列隐藏
      return { rowspan: 0, colspan: 0 }
    }
  }
  
  // 退款原因行：跨越所有列
  if (row.isRefundReasonRow) {
    if (columnIndex === 1) {
      // 商品信息列显示内容，并跨越所有列
      return { rowspan: 1, colspan: 10 }
    } else {
      // 其他列隐藏
      return { rowspan: 0, colspan: 0 }
    }
  }
  
  // 普通商品行：不合并
  return { rowspan: 1, colspan: 1 }
}

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
    'partial_shipped': '',
    'mixed': 'info'
  }
  return typeMap[status] || 'info'
}

// 获取支付状态文本
const getPaymentStatusText = (status) => {
  const statusMap = {
    'unpaid': '未支付',
    'paid': '已支付',
    'refunded': '已退款'
  }
  return statusMap[status] || status
}

// 获取支付状态标签类型
const getPaymentStatusTagType = (status) => {
  const typeMap = {
    'unpaid': 'warning',
    'paid': 'success',
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

/**
 * 查询物流信息（获取最新一条）
 */
const fetchLatestExpressInfo = async (expressNo) => {
  if (!expressNo) return null
  
  try {
    const response = await fetch(`/api/common/express/track?expressNo=${encodeURIComponent(expressNo)}`, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    
    const result = await response.json()
    
    if (result.success && result.data && result.data.traces && result.data.traces.length > 0) {
      // 返回最新的一条物流信息（已经按时间降序排列）
      const latest = result.data.traces[0]
      return {
        time: latest.time,
        description: latest.description
      }
    }
  } catch (error) {
    console.error('查询物流信息失败:', error)
  }
  
  return null
}

// 初始化数据
const initData = async () => {
  if (!props.orderId) {
    ElMessage.error('订单ID不存在')
    return
  }

  // 显示加载状态
  detailLoading.value = true
  
  try {
    // 加载订单详情
    const detailResponse = await fetch(`/admin${props.adminLoginPath}/order/${props.orderId}`, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    
    const detailResult = await detailResponse.json()
    
    if (!detailResult.success) {
      ElMessage.error(detailResult.message || '加载订单详情失败')
      return
    }
    
    currentOrder.value = detailResult.data
    remarkText.value = currentOrder.value.sellerRemark || ''
    
    // 更新货币符号
    if (detailResult.currencySymbol) {
      currencySymbol.value = detailResult.currencySymbol
    }
    
    // 加载订单明细
    const itemsResponse = await fetch(`/admin${props.adminLoginPath}/order/${props.orderId}/items`, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    
    const itemsResult = await itemsResponse.json()
    
    if (itemsResult.success) {
      // 处理订单项数据，为每个商品添加物流信息行和退款原因行
      const expandedItems = []
      let displayIndex = 1
      
      for (const item of itemsResult.data) {
        // 为每个商品异步获取签名图片URL
        if (item.productThumbnail) {
          item.signedThumbnailUrl = await getSignedUrl(item.productThumbnail)
        }
        
        // 添加显示索引
        item.displayIndex = displayIndex++
        
        // 1. 添加商品主行
        expandedItems.push(item)
        
        // 查询发货物流和退货物流的最新信息
        let latestLogisticsInfo = null
        let latestRefundLogisticsInfo = null
        
        if (item.logisticsNo) {
          latestLogisticsInfo = await fetchLatestExpressInfo(item.logisticsNo)
        }
        
        if (item.refundLogisticsNo) {
          latestRefundLogisticsInfo = await fetchLatestExpressInfo(item.refundLogisticsNo)
        }
        
        // 2. 添加物流信息行
        expandedItems.push({
          isLogisticsRow: true,
          id: `logistics_${item.id}`,
          parentOrderStatus: item.orderStatus,  // 添加父级订单状态
          parentRefundStatus: item.refundStatus,  // 添加父级退款状态
          logisticsCompany: item.logisticsCompany,
          logisticsNo: item.logisticsNo,
          refundLogisticsCompany: item.refundLogisticsCompany,
          refundLogisticsNo: item.refundLogisticsNo,
          // 添加最新物流信息
          latestLogisticsTime: latestLogisticsInfo?.time || null,
          latestLogisticsMessage: latestLogisticsInfo?.description || null,
          latestRefundLogisticsTime: latestRefundLogisticsInfo?.time || null,
          latestRefundLogisticsMessage: latestRefundLogisticsInfo?.description || null
        })
        
        // 3. 如果有退款原因，添加退款原因行
        if (item.refundReason) {
          expandedItems.push({
            isRefundReasonRow: true,
            id: `refund_reason_${item.id}`,
            refundReason: item.refundReason
          })
        }
      }
      
      orderItems.value = expandedItems
    }
    
    // 等待DOM更新后初始化表格拖动
    await nextTick()
    setTimeout(() => {
      initTableDrag()
    }, 500)
  } catch (error) {
    ElMessage.error('加载订单详情失败: ' + error.message)
  } finally {
    // 关闭加载状态
    detailLoading.value = false
  }
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

// 跳转到商品详情
const goToProductDetail = (productId) => {
  if (!productId) {
    ElMessage.warning('商品ID不存在')
    return
  }
  
  // 触发自定义事件，通知父组件打开新标签页，并设置返回地址为订单详情
  window.dispatchEvent(new CustomEvent('navigate-to-product-view', {
    detail: { 
      productId,
      returnTo: 'order-detail' // 设置返回地址为订单详情
    }
  }))
}

// 查看供应商详情
const handleViewSupplier = (supplierId) => {
  if (!supplierId) {
    ElMessage.warning('供应商ID不存在')
    return
  }
  
  // 触发自定义事件，通知父组件打开供应商详情页，并设置返回地址为订单详情
  window.dispatchEvent(new CustomEvent('navigate-to-supplier-view', {
    detail: { 
      supplierId,
      returnTo: 'order-detail' // 设置返回地址为订单详情
    }
  }))
}

/**
 * 计算退款截止日期（买家发货时间 + 15天）
 * @param {string} refundBuyerShippedTime - 买家退货发货时间
 * @returns {string} 格式化的截止日期
 */
const getRefundDeadline = (refundBuyerShippedTime) => {
  if (!refundBuyerShippedTime) return '-'
  
  try {
    const shippedDate = new Date(refundBuyerShippedTime)
    const deadline = new Date(shippedDate)
    deadline.setDate(deadline.getDate() + 15)
    
    // 格式化为 YYYY-MM-DD HH:mm
    const year = deadline.getFullYear()
    const month = String(deadline.getMonth() + 1).padStart(2, '0')
    const day = String(deadline.getDate()).padStart(2, '0')
    const hours = String(deadline.getHours()).padStart(2, '0')
    const minutes = String(deadline.getMinutes()).padStart(2, '0')
    
    return `${year}-${month}-${day} ${hours}:${minutes}`
  } catch (error) {
    console.error('计算截止日期失败:', error)
    return '-'
  }
}

/**
 * 查看快递物流信息
 */
const handleTrackExpress = (expressNo) => {
  if (!expressNo) {
    ElMessage.warning('快递单号为空')
    return
  }
  expressTrackingDialog.value.open(expressNo)
}

/**
 * 管理员确认收到退货并完成退款
 * 
 * 业务逻辑：
 * 1. 检查订单项状态：orderStatus = 'refunding' && refundStatus = 'buyer_shipped'
 * 2. 检查15天缓冲期：refund_buyer_shipped_time + 15天 <= 当前时间
 * 3. 如果未超过15天：显示提示，告知剩余天数
 * 4. 如果已超过15天：确认后调用 completeRefund() 完成退款
 */
const handleConfirmRefundReceived = async (orderItem) => {
  try {
    // 确认操作
    await ElMessageBox.confirm(
      `请确认是否已收到买家的退货商品？
商品：${orderItem.productTitle}
SKU：${orderItem.productSku}
退款金额：￥${orderItem.refundAmount}

确认后将会：
1. 检查是否超过15天缓冲期
2. 如果超过15天，将自动完成退款
3. 从供应商待结算金额扣除
4. 退款给买家
5. 恢复库存`,
      '确认收货并完成退款',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning',
        dangerouslyUseHTMLString: true
      }
    )
    
    // 调用API
    const response = await fetch(`/admin${props.adminLoginPath}/order/confirm-refund-received/${orderItem.id}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    
    const result = await response.json()
    
    if (result.success) {
      ElMessage.success(result.message)
      // 重新加载订单数据
      await initData()
    } else {
      // 如果是未超过15天的提示，显示详细信息
      ElMessageBox.alert(
        result.message,
        '提示',
        {
          confirmButtonText: '知道了',
          type: 'warning',
          dangerouslyUseHTMLString: true
        }
      )
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败: ' + (error.message || error))
    }
  }
}

// 刷新订单数据
const handleRefresh = async () => {
  try {
    ElMessage.info('正在刷新订单数据...')
    await initData()
    ElMessage.success('订单数据已刷新')
  } catch (error) {
    ElMessage.error('刷新失败: ' + (error.message || error))
  }
}

defineExpose({
  initData
})
</script>

<style scoped>
.order-detail-tab-container {
  position: relative;
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100%;
}

.order-detail {
  max-width: 1600px;
  margin: 0 auto;
}

.detail-card {
  margin-bottom: 20px;
}

.detail-card-header {
  display: flex;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
}

.detail-card-header .el-icon {
  margin-right: 8px;
  font-size: 18px;
  color: #409eff;
}

.order-no-text {
  font-weight: 600;
  color: #409eff;
}

.amount-highlight {
  color: #409eff;
}

.discount-text {
  color: #f56c6c;
}

.paid-amount {
  color: #67c23a;
}

:deep(.desc-label) {
  background-color: #f5f7fa !important;
  font-weight: 500;
}

.refresh-button-container {
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 100;
}

.refresh-button-container .el-button {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.refresh-button-container .el-button:hover {
  transform: scale(1.05);
  transition: transform 0.2s;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .refresh-button-container {
    top: 10px;
    right: 10px;
  }
}
</style>

