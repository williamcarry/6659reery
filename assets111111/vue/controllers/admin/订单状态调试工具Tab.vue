<template>
  <div class="order-debug-tool">
    <el-card class="header-card">
      <template #header>
        <div class="card-header">
          <span>订单状态调试工具</span>
        </div>
      </template>
      
      <!-- 危险操作区 -->
      <el-alert 
        title="危险操作区" 
        type="error" 
        :closable="false"
        style="margin-bottom: 20px"
      >
        <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 10px">
          <el-button type="danger" @click="showClearOrdersDialog" :loading="processing">
            <el-icon><Delete /></el-icon> 清空全部订单
          </el-button>
          <el-button type="danger" @click="showClearBalanceDialog" :loading="processing">
            <el-icon><Delete /></el-icon> 清空全部余额记录
          </el-button>
        </div>
      </el-alert>

      <el-form :inline="true" class="search-form">
        <el-form-item label="查询用户">
          <el-input 
            v-model="searchValue" 
            placeholder="请输入用户ID/客户号/用户名/邮箱" 
            clearable
            style="width: 300px"
            @keyup.enter="loadOrders"
          >
            <template #prepend>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadOrders" :loading="loading">
            查询订单
          </el-button>
        </el-form-item>
      </el-form>

      <!-- 供应商查询 -->
      <el-divider />
      <el-form :inline="true" class="search-form">
        <el-form-item label="查询供应商">
          <el-input 
            v-model="supplierSearchValue" 
            placeholder="请输入供应商ID/客户号/用户名/邮箱" 
            clearable
            style="width: 300px"
            @keyup.enter="loadSupplier"
          >
            <template #prepend>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="success" @click="loadSupplier" :loading="supplierLoading">
            查询供应商
          </el-button>
        </el-form-item>
      </el-form>
      
      <el-alert 
        v-if="!searchValue && !supplierSearchValue" 
        title="支持查询方式：用户ID（数字）、客户号（CUSTXXXXXXXX）、用户名、邮箱" 
        type="info" 
        :closable="false"
        style="margin-top: 10px"
      />
    </el-card>

    <!-- 供应商信息卡片 -->
    <el-card v-if="supplier" class="supplier-card">
      <template #header>
        <div class="card-header">
          <span>供应商信息</span>
        </div>
      </template>
      <el-descriptions :column="3" border>
        <el-descriptions-item label="供应商ID">{{ supplier.id }}</el-descriptions-item>
        <el-descriptions-item label="客户号">{{ supplier.customerId }}</el-descriptions-item>
        <el-descriptions-item label="用户名">{{ supplier.username }}</el-descriptions-item>
        <el-descriptions-item label="邮箱">{{ supplier.email }}</el-descriptions-item>
        <el-descriptions-item label="供应商类型">
          <el-tag :type="supplier.supplierType === 'company' ? 'warning' : 'success'">
            {{ supplier.supplierType === 'company' ? '公司' : '个人' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="公司/姓名">{{ supplier.companyName || supplier.individualName || '-' }}</el-descriptions-item>
        <el-descriptions-item label="联系人">{{ supplier.contactPerson || '-' }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ supplier.contactPhone || '-' }}</el-descriptions-item>
        <el-descriptions-item label="账户余额">
          <span style="color: #67c23a; font-weight: bold">￥{{ supplier.balance }}</span>
          <el-button 
            size="small" 
            type="success" 
            @click="showSupplierBalanceDialog"
            style="margin-left: 10px"
          >
            <el-icon><Edit /></el-icon> 修改余额
          </el-button>
        </el-descriptions-item>
        <el-descriptions-item label="冻结余额">
          <span style="color: #e6a23c; font-weight: bold">￥{{ supplier.balanceFrozen }}</span>
          <el-button 
            size="small" 
            type="warning" 
            @click="showSupplierFrozenBalanceDialog"
            style="margin-left: 10px"
          >
            <el-icon><Edit /></el-icon> 修改冻结余额
          </el-button>
        </el-descriptions-item>
        <el-descriptions-item label="待结算金额">
          <span style="color: #409eff; font-weight: bold">￥{{ supplier.pendingSettlementAmount || '0.00' }}</span>
          <el-button 
            size="small" 
            type="primary" 
            @click="showSupplierPendingDialog"
            style="margin-left: 10px"
          >
            <el-icon><Edit /></el-icon> 修改待结算金额
          </el-button>
        </el-descriptions-item>
      </el-descriptions>
    </el-card>

    <!-- 用户信息卡片 -->
    <el-card v-if="customer" class="customer-card">
      <template #header>
        <div class="card-header">
          <span>用户信息</span>
        </div>
      </template>
      <el-descriptions :column="3" border>
        <el-descriptions-item label="用户ID">{{ customer.id }}</el-descriptions-item>
        <el-descriptions-item label="客户号">{{ customer.customerId }}</el-descriptions-item>
        <el-descriptions-item label="用户名">{{ customer.username }}</el-descriptions-item>
        <el-descriptions-item label="邮箱">{{ customer.email }}</el-descriptions-item>
        <el-descriptions-item label="真实姓名">{{ customer.realName || '-' }}</el-descriptions-item>
        <el-descriptions-item label="手机">{{ customer.mobile || '-' }}</el-descriptions-item>
        <el-descriptions-item label="会员类型">
          <el-tag :type="customer.customerType === 'company' ? 'warning' : 'success'">
            {{ customer.customerType === 'company' ? '企业' : '个人' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="账户余额">
          <span style="color: #67c23a; font-weight: bold">￥{{ customer.balance }}</span>
          <el-button 
            size="small" 
            type="success" 
            @click="showBalanceDialog"
            style="margin-left: 10px"
          >
            <el-icon><Edit /></el-icon> 修改余额
          </el-button>
        </el-descriptions-item>
        <el-descriptions-item label="冻结余额">
          <span style="color: #e6a23c; font-weight: bold">￥{{ customer.frozenBalance }}</span>
          <el-button 
            size="small" 
            type="warning" 
            @click="showFrozenBalanceDialog"
            style="margin-left: 10px"
          >
            <el-icon><Edit /></el-icon> 修改冻结余额
          </el-button>
        </el-descriptions-item>
        <el-descriptions-item label="累计消费" :span="3">
          <span style="color: #f56c6c; font-weight: bold">￥{{ customer.consumptionAmount }}</span>
        </el-descriptions-item>
      </el-descriptions>
    </el-card>

    <div v-if="orders.length > 0" class="orders-container">
      <el-card v-for="order in orders" :key="order.id" class="order-card">
        <template #header>
          <div class="order-header">
            <div class="order-info">
              <span class="order-no">订单号: {{ order.orderNo }}</span>
              <el-tag :type="order.items.length > 1 ? 'warning' : 'info'" size="small">
                {{ order.items.length > 1 ? '多商品订单' : '单商品订单' }} ({{ order.items.length }}个商品)
              </el-tag>
            </div>
            <div class="order-meta">
              <span class="order-total">订单总额: ¥{{ order.totalAmount }}</span>
              <span class="order-time">{{ order.createdAt }}</span>
            </div>
          </div>
        </template>

        <el-table :data="order.items" border stripe>
          <el-table-column type="expand">
            <template #default="scope">
              <div class="item-detail">
                <el-descriptions :column="2" border size="small">
                  <el-descriptions-item label="订单项ID">{{ scope.row.id }}</el-descriptions-item>
                  <el-descriptions-item label="购买数量">{{ scope.row.quantity }}</el-descriptions-item>
                  <el-descriptions-item label="供应商">
                    {{ scope.row.supplierName }} (ID: {{ scope.row.supplierId }})
                  </el-descriptions-item>
                  <el-descriptions-item label="供应商余额">
                    ¥{{ scope.row.supplierBalance }}
                  </el-descriptions-item>
                  <el-descriptions-item label="供应商冻结余额">
                    ¥{{ scope.row.supplierFrozenBalance }}
                  </el-descriptions-item>
                  <el-descriptions-item label="供应商收入">
                    ¥{{ scope.row.supplierIncome }}
                  </el-descriptions-item>
                  <el-descriptions-item label="平台佣金">
                    ¥{{ scope.row.commissionAmount }}
                  </el-descriptions-item>
                  <el-descriptions-item label="发货时间">
                    {{ scope.row.shippedTime || '-' }}
                  </el-descriptions-item>
                  <el-descriptions-item label="收货时间">
                    {{ scope.row.receivedTime || '-' }}
                  </el-descriptions-item>
                  <el-descriptions-item label="物流公司">
                    {{ scope.row.logisticsCompany || '-' }}
                  </el-descriptions-item>
                  <el-descriptions-item label="物流单号">
                    {{ scope.row.logisticsNo || '-' }}
                  </el-descriptions-item>
                  <el-descriptions-item label="退款时间">
                    {{ scope.row.refundTime || '-' }}
                  </el-descriptions-item>
                  <el-descriptions-item label="退款金额">
                    {{ scope.row.refundAmount || '-' }}
                  </el-descriptions-item>
                  <el-descriptions-item label="退款原因" :span="2">
                    {{ scope.row.refundReason || '-' }}
                  </el-descriptions-item>
                  <el-descriptions-item label="退货截止时间" :span="2">
                    {{ scope.row.returnDeadline || '-' }}
                    <el-tag v-if="scope.row.isWithinReturnPeriod" type="success" size="small">
                      可退货
                    </el-tag>
                    <el-tag v-else-if="scope.row.returnDeadline" type="info" size="small">
                      已过期
                    </el-tag>
                  </el-descriptions-item>
                </el-descriptions>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column type="index" label="序号" width="60" align="center" />
          <el-table-column prop="productName" label="商品名称" min-width="200" />
          <el-table-column label="供应商" width="150">
            <template #default="scope">
              <div>
                <div>{{ scope.row.supplierName }}</div>
                <el-tag size="small" type="info">ID: {{ scope.row.supplierId }}</el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="quantity" label="数量" width="80" align="center" />
          <el-table-column prop="subtotalAmount" label="订单金额" width="120">
            <template #default="scope">
              ¥{{ scope.row.subtotalAmount }}
            </template>
          </el-table-column>
          <el-table-column prop="orderStatus" label="订单状态" width="120">
            <template #default="scope">
              <el-tag :type="getStatusType(scope.row.orderStatus)">
                {{ scope.row.orderStatusText }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="refundStatus" label="退款状态" width="120">
            <template #default="scope">
              <el-tag v-if="scope.row.refundStatus !== 'none'" type="warning">
                {{ scope.row.refundStatusText }}
              </el-tag>
              <span v-else>-</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="300" fixed="right">
            <template #default="scope">
              <div class="action-buttons">
                <el-button
                  v-for="(label, action) in scope.row.nextPossibleActions"
                  :key="action"
                  size="small"
                  :type="getActionButtonType(action)"
                  @click="handleAction(scope.row, action)"
                >
                  {{ label }}
                </el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>
        
        <!-- 订单汇总信息 -->
        <div class="order-summary" v-if="order.items.length > 1">
          <el-divider />
          <el-descriptions :column="4" size="small" border>
            <el-descriptions-item label="商品总数">
              {{ order.items.reduce((sum, item) => sum + item.quantity, 0) }} 件
            </el-descriptions-item>
            <el-descriptions-item label="订单总额">
              <span class="highlight-price">¥{{ order.totalAmount }}</span>
            </el-descriptions-item>
            <el-descriptions-item label="涉及供应商">
              {{ getUniqueSuppliers(order.items).length }} 个
            </el-descriptions-item>
            <el-descriptions-item label="供应商列表">
              <el-tag 
                v-for="supplier in getUniqueSuppliers(order.items)" 
                :key="supplier.id"
                size="small"
                style="margin-right: 5px"
              >
                {{ supplier.name }}
              </el-tag>
            </el-descriptions-item>
          </el-descriptions>
        </div>
      </el-card>
    </div>

    <el-empty v-else-if="!loading && searched" description="未找到订单数据" />

    <!-- 修改供应商余额对话框 -->
    <el-dialog v-model="supplierBalanceDialogVisible" title="修改供应商余额" width="500px">
      <el-form :model="supplierBalanceForm" label-width="140px">
        <el-form-item label="当前余额">
          <el-input v-model="supplier.balance" disabled>
            <template #prepend>￥</template>
          </el-input>
        </el-form-item>
        <el-form-item label="当前冻结余额">
          <el-input v-model="supplier.balanceFrozen" disabled>
            <template #prepend>￥</template>
          </el-input>
        </el-form-item>
        <el-form-item label="当前待结算金额">
          <el-input :value="supplier.pendingSettlementAmount || '0.00'" disabled>
            <template #prepend>￥</template>
          </el-input>
        </el-form-item>
        <el-form-item label="余额类型">
          <el-radio-group v-model="supplierBalanceForm.balanceType" @change="calculateSupplierNewBalance">
            <el-radio value="balance">可用余额</el-radio>
            <el-radio value="frozen">冻结余额</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="操作类型">
          <el-radio-group v-model="supplierBalanceForm.type" @change="calculateSupplierNewBalance">
            <el-radio value="add">增加</el-radio>
            <el-radio value="deduct">减少</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="金额">
          <el-input 
            v-model="supplierBalanceForm.amount" 
            type="number" 
            placeholder="请输入金额"
            @input="calculateSupplierNewBalance"
          >
            <template #prepend>￥</template>
          </el-input>
        </el-form-item>
        <el-form-item :label="supplierBalanceForm.balanceType === 'balance' ? '变更后余额' : '变更后冻结余额'">
          <el-input :value="supplierNewBalance" disabled>
            <template #prepend>￥</template>
          </el-input>
        </el-form-item>
        <el-form-item label="备注">
          <el-input 
            v-model="supplierBalanceForm.description" 
            type="textarea" 
            placeholder="请输入变更原因或备注"
            :rows="3"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="supplierBalanceDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmSupplierBalanceChange" :loading="processing">
          确定修改
        </el-button>
      </template>
    </el-dialog>

    <!-- 修改供应商待结算金额对话框 -->
    <el-dialog v-model="supplierPendingDialogVisible" title="修改供应商待结算金额" width="500px">
      <el-form :model="supplierPendingForm" label-width="140px">
        <el-form-item label="当前余额">
          <el-input v-model="supplier.balance" disabled>
            <template #prepend>￥</template>
          </el-input>
        </el-form-item>
        <el-form-item label="当前冻结余额">
          <el-input v-model="supplier.balanceFrozen" disabled>
            <template #prepend>￥</template>
          </el-input>
        </el-form-item>
        <el-form-item label="当前待结算金额">
          <el-input :value="supplier.pendingSettlementAmount || '0.00'" disabled>
            <template #prepend>￥</template>
          </el-input>
        </el-form-item>
        <el-form-item label="操作类型">
          <el-radio-group v-model="supplierPendingForm.type" @change="calculateSupplierPendingBalance">
            <el-radio value="add">增加</el-radio>
            <el-radio value="deduct">减少</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="金额">
          <el-input 
            v-model="supplierPendingForm.amount" 
            type="number" 
            placeholder="请输入金额"
            @input="calculateSupplierPendingBalance"
          >
            <template #prepend>￥</template>
          </el-input>
        </el-form-item>
        <el-form-item label="变更后待结算金额">
          <el-input :value="supplierPendingBalance" disabled>
            <template #prepend>￥</template>
          </el-input>
        </el-form-item>
        <el-form-item label="备注">
          <el-input 
            v-model="supplierPendingForm.description" 
            type="textarea" 
            placeholder="请输入变更原因或备注（如：调试修正待结算金额）"
            :rows="3"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="supplierPendingDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmSupplierPendingChange" :loading="processing">
          确定修改
        </el-button>
      </template>
    </el-dialog>

    <!-- 修改会员余额对话框 -->
    <el-dialog v-model="balanceDialogVisible" title="修改会员余额" width="500px">
      <el-form :model="balanceForm" label-width="120px">
        <el-form-item label="当前余额">
          <el-input v-model="customer.balance" disabled>
            <template #prepend>￥</template>
          </el-input>
        </el-form-item>
        <el-form-item label="当前冻结余额">
          <el-input v-model="customer.frozenBalance" disabled>
            <template #prepend>￥</template>
          </el-input>
        </el-form-item>
        <el-form-item label="余额类型">
          <el-radio-group v-model="balanceForm.balanceType" @change="calculateNewBalance">
            <el-radio value="balance">可用余额</el-radio>
            <el-radio value="frozen">冻结余额</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="操作类型">
          <el-radio-group v-model="balanceForm.type" @change="calculateNewBalance">
            <el-radio value="add">增加</el-radio>
            <el-radio value="deduct">减少</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="金额">
          <el-input 
            v-model="balanceForm.amount" 
            type="number" 
            placeholder="请输入金额"
            @input="calculateNewBalance"
          >
            <template #prepend>￥</template>
          </el-input>
        </el-form-item>
        <el-form-item :label="balanceForm.balanceType === 'balance' ? '变更后余额' : '变更后冻结余额'">
          <el-input :value="newBalance" disabled>
            <template #prepend>￥</template>
          </el-input>
        </el-form-item>
        <el-form-item label="备注">
          <el-input 
            v-model="balanceForm.description" 
            type="textarea" 
            placeholder="请输入变更原因或备注"
            :rows="3"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="balanceDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmBalanceChange" :loading="processing">
          确定修改
        </el-button>
      </template>
    </el-dialog>

    <!-- 操作参数对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form :model="actionParams" label-width="120px">
        <el-form-item v-if="currentAction === 'markAsShipped'" label="物流公司">
          <el-input v-model="actionParams.logisticsCompany" placeholder="如:顺丰速运" />
        </el-form-item>
        <el-form-item v-if="currentAction === 'markAsShipped'" label="物流单号">
          <el-input v-model="actionParams.trackingNo" placeholder="如:SF123456789" />
        </el-form-item>
        <el-form-item v-if="['cancelOrder', 'applyRefund'].includes(currentAction)" label="原因">
          <el-input 
            v-model="actionParams.reason" 
            type="textarea" 
            :placeholder="currentAction === 'cancelOrder' ? '取消原因' : '退款原因'" 
          />
        </el-form-item>
        <el-form-item v-if="currentAction === 'applyRefund'" label="退款金额">
          <el-input v-model="actionParams.amount" placeholder="留空表示全额退款" type="number" />
        </el-form-item>
        <el-form-item v-if="currentAction === 'rejectRefund'" label="拒绝原因">
          <el-input 
            v-model="actionParams.reason" 
            type="textarea" 
            placeholder="拒绝退款的原因" 
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmAction" :loading="processing">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive } from 'vue';
import { 
  ElMessage, 
  ElMessageBox,
  ElCard,
  ElForm,
  ElFormItem,
  ElInput,
  ElButton,
  ElAlert,
  ElDescriptions,
  ElDescriptionsItem,
  ElTag,
  ElTable,
  ElTableColumn,
  ElEmpty,
  ElDialog,
  ElIcon,
  ElDivider,
  ElRadio,
  ElRadioGroup
} from 'element-plus';
import { Delete, Search, Edit } from '@element-plus/icons-vue';

export default {
  name: 'OrderDebugToolTab',
  components: {
    ElCard,
    ElForm,
    ElFormItem,
    ElInput,
    ElButton,
    ElAlert,
    ElDescriptions,
    ElDescriptionsItem,
    ElTag,
    ElTable,
    ElTableColumn,
    ElEmpty,
    ElDialog,
    ElIcon,
    ElDivider,
    ElRadio,
    ElRadioGroup,
    Search,
    Edit,
    Delete
  },
  props: {
    adminLoginPath: {
      type: String,
      default: ''
    },
    autoLoad: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    const supplierSearchValue = ref('');
    const supplier = ref(null);
    const supplierLoading = ref(false);
    const supplierBalanceDialogVisible = ref(false);
    const supplierPendingDialogVisible = ref(false);
    const supplierBalanceForm = reactive({
      balanceType: 'balance',
      type: 'add',
      amount: '',
      description: ''
    });
    const supplierPendingForm = reactive({
      type: 'add',
      amount: '',
      description: ''
    });
    const supplierNewBalance = ref('0.00');
    const supplierPendingBalance = ref('0.00');

    const searchValue = ref('');
    const customer = ref(null);
    const orders = ref([]);
    const loading = ref(false);
    const processing = ref(false);
    const searched = ref(false);
    const dialogVisible = ref(false);
    const dialogTitle = ref('');
    const currentAction = ref('');
    const currentOrderItem = ref(null);
    const actionParams = reactive({
      logisticsCompany: '顺丰速运',
      trackingNo: '',
      reason: '',
      amount: ''
    });

    const balanceDialogVisible = ref(false);
    const balanceForm = reactive({
      balanceType: 'balance',
      type: 'add',
      amount: '',
      description: ''
    });
    const newBalance = ref('0.00');

    const loadOrders = async () => {
      if (!searchValue.value) {
        ElMessage.warning('请输入查询条件（用户ID/客户号/用户名/邮箱）');
        return;
      }

      loading.value = true;
      searched.value = false;
      try {
        const response = await fetch(`/admin${props.adminLoginPath}/order-debug/search-orders`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
          },
          body: JSON.stringify({
            searchValue: searchValue.value
          })
        });
        
        const data = await response.json();
        
        if (data.success) {
          customer.value = data.data.customer;
          orders.value = data.data.orders;
          searched.value = true;
          if (orders.value.length === 0) {
            ElMessage.info('该用户暂无订单');
          } else {
            ElMessage.success(`找到 ${orders.value.length} 个订单`);
          }
        } else {
          ElMessage.error(data.message || '查询失败');
          customer.value = null;
          orders.value = [];
        }
      } catch (error) {
        ElMessage.error('查询失败: ' + error.message);
        customer.value = null;
        orders.value = [];
      } finally {
        loading.value = false;
      }
    };

    const handleAction = (orderItem, action) => {
      currentOrderItem.value = orderItem;
      currentAction.value = action;

      // 重置参数
      actionParams.logisticsCompany = '顺丰速运';
      actionParams.trackingNo = 'SF' + Date.now();
      actionParams.reason = '';
      actionParams.amount = '';

      // 需要参数的操作显示对话框
      const needsDialog = ['markAsShipped', 'cancelOrder', 'applyRefund', 'rejectRefund'];
      if (needsDialog.includes(action)) {
        const titles = {
          markAsShipped: '标记发货',
          cancelOrder: '取消订单',
          applyRefund: '申请退款',
          rejectRefund: '拒绝退款'
        };
        dialogTitle.value = titles[action];
        dialogVisible.value = true;
      } else {
        // 不需要参数的操作直接确认
        const messages = {
          confirmPayment: '确认支付',
          confirmReceived: '确认收货',
          approveRefund: '同意退款',
          completeRefund: '完成退款'
        };
        ElMessageBox.confirm(`确定要执行"${messages[action]}"操作吗?`, '确认操作', {
          type: 'warning'
        }).then(() => {
          executeAction(action, orderItem.id, {});
        }).catch(() => {});
      }
    };

    const confirmAction = () => {
      const params = { ...actionParams };
      dialogVisible.value = false;
      executeAction(currentAction.value, currentOrderItem.value.id, params);
    };

    const executeAction = async (action, orderItemId, params) => {
      processing.value = true;
      try {
        const response = await fetch(`/admin${props.adminLoginPath}/order-debug/process-action`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
          },
          body: JSON.stringify({
            orderItemId,
            action,
            params
          })
        });

        const data = await response.json();

        if (data.success) {
          ElMessage.success(data.message);
          // 重新加载订单数据
          await loadOrders();
        } else {
          ElMessage.error(data.message || '操作失败');
        }
      } catch (error) {
        ElMessage.error('操作失败: ' + error.message);
      } finally {
        processing.value = false;
      }
    };

    const getStatusType = (status) => {
      const types = {
        pending_payment: 'info',
        paid: 'warning',
        shipped: 'primary',
        completed: 'success',
        cancelled: 'info',
        refunding: 'warning',
        refunded: 'danger'
      };
      return types[status] || '';
    };

    const getActionButtonType = (action) => {
      const types = {
        paid: 'success',
        shipped: 'primary',
        completed: 'success',
        cancelled: 'danger',
        refunding: 'warning',
        approved: 'success',
        rejected: 'danger',
        refunded: 'warning'
      };
      return types[action] || 'primary';
    };

    const getUniqueSuppliers = (items) => {
      const suppliersMap = new Map();
      items.forEach(item => {
        if (item.supplierId && !suppliersMap.has(item.supplierId)) {
          suppliersMap.set(item.supplierId, {
            id: item.supplierId,
            name: item.supplierName
          });
        }
      });
      return Array.from(suppliersMap.values());
    };

    const showBalanceDialog = () => {
      balanceForm.balanceType = 'balance';
      balanceForm.type = 'add';
      balanceForm.amount = '';
      balanceForm.description = '';
      newBalance.value = customer.value.balance;
      balanceDialogVisible.value = true;
    };

    const showFrozenBalanceDialog = () => {
      balanceForm.balanceType = 'frozen';
      balanceForm.type = 'add';
      balanceForm.amount = '';
      balanceForm.description = '';
      newBalance.value = customer.value.frozenBalance;
      balanceDialogVisible.value = true;
    };

    const calculateSupplierNewBalance = () => {
      if (!supplier.value || !supplierBalanceForm.amount) {
        if (supplierBalanceForm.balanceType === 'balance') {
          supplierNewBalance.value = supplier.value?.balance || '0.00';
        } else {
          supplierNewBalance.value = supplier.value?.balanceFrozen || '0.00';
        }
        return;
      }

      const currentValue = supplierBalanceForm.balanceType === 'balance'
        ? (parseFloat(supplier.value.balance) || 0)
        : (parseFloat(supplier.value.balanceFrozen) || 0);
      const changeAmount = parseFloat(supplierBalanceForm.amount) || 0;

      if (supplierBalanceForm.type === 'add') {
        supplierNewBalance.value = (currentValue + changeAmount).toFixed(2);
      } else {
        supplierNewBalance.value = (currentValue - changeAmount).toFixed(2);
      }
    };

    const showSupplierBalanceDialog = () => {
      supplierBalanceForm.balanceType = 'balance';
      supplierBalanceForm.type = 'add';
      supplierBalanceForm.amount = '';
      supplierBalanceForm.description = '';
      supplierNewBalance.value = supplier.value.balance;
      supplierBalanceDialogVisible.value = true;
    };

    const showSupplierFrozenBalanceDialog = () => {
      supplierBalanceForm.balanceType = 'frozen';
      supplierBalanceForm.type = 'add';
      supplierBalanceForm.amount = '';
      supplierBalanceForm.description = '';
      supplierNewBalance.value = supplier.value.balanceFrozen;
      supplierBalanceDialogVisible.value = true;
    };

    const showSupplierPendingDialog = () => {
      supplierPendingForm.type = 'add';
      supplierPendingForm.amount = '';
      supplierPendingForm.description = '';
      supplierPendingBalance.value = supplier.value.pendingSettlementAmount || '0.00';
      supplierPendingDialogVisible.value = true;
    };

    const confirmSupplierBalanceChange = async () => {
      if (!supplierBalanceForm.amount || parseFloat(supplierBalanceForm.amount) <= 0) {
        ElMessage.warning('请输入有效的金额');
        return;
      }

      if (!supplierBalanceForm.description) {
        ElMessage.warning('请输入变更原因或备注');
        return;
      }

      processing.value = true;
      try {
        const response = await fetch(`/admin${props.adminLoginPath}/order-debug/change-supplier-balance`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
          },
          body: JSON.stringify({
            supplierId: supplier.value.id,
            balanceType: supplierBalanceForm.balanceType,
            type: supplierBalanceForm.type,
            amount: supplierBalanceForm.amount,
            description: supplierBalanceForm.description
          })
        });

        const data = await response.json();

        if (data.success) {
          ElMessage.success(data.message);
          supplierBalanceDialogVisible.value = false;
          // 重新加载供应商数据以刷新余额
          await loadSupplier();
        } else {
          ElMessage.error(data.message || '修改失败');
        }
      } catch (error) {
        ElMessage.error('修改失败: ' + error.message);
      } finally {
        processing.value = false;
      }
    };

    const calculateSupplierPendingBalance = () => {
      if (!supplier.value || !supplierPendingForm.amount) {
        supplierPendingBalance.value = supplier.value?.pendingSettlementAmount || '0.00';
        return;
      }

      const currentValue = parseFloat(supplier.value.pendingSettlementAmount) || 0;
      const changeAmount = parseFloat(supplierPendingForm.amount) || 0;

      if (supplierPendingForm.type === 'add') {
        supplierPendingBalance.value = (currentValue + changeAmount).toFixed(2);
      } else {
        supplierPendingBalance.value = (currentValue - changeAmount).toFixed(2);
      }
    };

    const confirmSupplierPendingChange = async () => {
      if (!supplierPendingForm.amount || parseFloat(supplierPendingForm.amount) <= 0) {
        ElMessage.warning('请输入有效的金额');
        return;
      }

      if (!supplierPendingForm.description) {
        ElMessage.warning('请输入变更原因或备注');
        return;
      }

      processing.value = true;
      try {
        const response = await fetch(`/admin${props.adminLoginPath}/order-debug/change-supplier-pending`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
          },
          body: JSON.stringify({
            supplierId: supplier.value.id,
            type: supplierPendingForm.type,
            amount: supplierPendingForm.amount,
            description: supplierPendingForm.description
          })
        });

        const data = await response.json();

        if (data.success) {
          ElMessage.success(data.message);
          supplierPendingDialogVisible.value = false;
          // 重新加载供应商数据以刷新余额
          await loadSupplier();
        } else {
          ElMessage.error(data.message || '修改失败');
        }
      } catch (error) {
        ElMessage.error('修改失败: ' + error.message);
      } finally {
        processing.value = false;
      }
    };

    const loadSupplier = async () => {
      if (!supplierSearchValue.value) {
        ElMessage.warning('请输入查询条件（供应商ID/客户号/用户名/邮箱）');
        return;
      }

      supplierLoading.value = true;
      try {
        const response = await fetch(`/admin${props.adminLoginPath}/order-debug/search-supplier`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
          },
          body: JSON.stringify({
            searchValue: supplierSearchValue.value
          })
        });
        
        const data = await response.json();
        
        if (data.success) {
          supplier.value = data.data;
          ElMessage.success('查询成功');
        } else {
          ElMessage.error(data.message || '查询失败');
          supplier.value = null;
        }
      } catch (error) {
        ElMessage.error('查询失败: ' + error.message);
        supplier.value = null;
      } finally {
        supplierLoading.value = false;
      }
    };

    const showClearOrdersDialog = () => {
      ElMessageBox.confirm(
        '此操作将清空所有订单和订单详情记录，此操作不可恢复！确定要继续吗？',
        '危险操作警告',
        {
          confirmButtonText: '确定清空',
          cancelButtonText: '取消',
          type: 'error',
          confirmButtonClass: 'el-button--danger'
        }
      ).then(async () => {
        processing.value = true;
        try {
          const response = await fetch(`/admin${props.adminLoginPath}/order-debug/clear-all-orders`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({ confirm: true })
          });

          const data = await response.json();

          if (data.success) {
            ElMessage.success(data.message);
            // 清空当前显示的订单
            orders.value = [];
            customer.value = null;
            searched.value = false;
          } else {
            ElMessage.error(data.message || '清空失败');
          }
        } catch (error) {
          ElMessage.error('清空失败: ' + error.message);
        } finally {
          processing.value = false;
        }
      }).catch(() => {});
    };

    const showClearBalanceDialog = () => {
      ElMessageBox.confirm(
        '此操作将清空所有余额记录，并将所有会员和供应商余额重置为0，同时清空供应商待结算金额，此操作不可恢复！确定要继续吗？',
        '危险操作警告',
        {
          confirmButtonText: '确定清空',
          cancelButtonText: '取消',
          type: 'error',
          confirmButtonClass: 'el-button--danger'
        }
      ).then(async () => {
        processing.value = true;
        try {
          const response = await fetch(`/admin${props.adminLoginPath}/order-debug/clear-all-balance-history`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({ confirm: true })
          });

          const data = await response.json();

          if (data.success) {
            ElMessage.success(data.message);
            // 如果当前有显示的会员或供应商，刷新其余额
            if (customer.value) {
              customer.value.balance = '0.00';
              customer.value.frozenBalance = '0.00';
            }
            if (supplier.value) {
              supplier.value.balance = '0.00';
              supplier.value.balanceFrozen = '0.00';
              supplier.value.pendingSettlementAmount = '0.00';
            }
          } else {
            ElMessage.error(data.message || '清空失败');
          }
        } catch (error) {
          ElMessage.error('清空失败: ' + error.message);
        } finally {
          processing.value = false;
        }
      }).catch(() => {});
    };

    const calculateNewBalance = () => {
      if (!customer.value || !balanceForm.amount) {
        if (balanceForm.balanceType === 'balance') {
          newBalance.value = customer.value?.balance || '0.00';
        } else {
          newBalance.value = customer.value?.frozenBalance || '0.00';
        }
        return;
      }

      const currentValue = balanceForm.balanceType === 'balance' 
        ? (parseFloat(customer.value.balance) || 0)
        : (parseFloat(customer.value.frozenBalance) || 0);
      const changeAmount = parseFloat(balanceForm.amount) || 0;

      if (balanceForm.type === 'add') {
        newBalance.value = (currentValue + changeAmount).toFixed(2);
      } else {
        newBalance.value = (currentValue - changeAmount).toFixed(2);
      }
    };

    const confirmBalanceChange = async () => {
      if (!balanceForm.amount || parseFloat(balanceForm.amount) <= 0) {
        ElMessage.warning('请输入有效的金额');
        return;
      }

      if (!balanceForm.description) {
        ElMessage.warning('请输入变更原因或备注');
        return;
      }

      processing.value = true;
      try {
        const response = await fetch(`/admin${props.adminLoginPath}/order-debug/change-customer-balance`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
          },
          body: JSON.stringify({
            customerId: customer.value.id,
            balanceType: balanceForm.balanceType,
            type: balanceForm.type,
            amount: balanceForm.amount,
            description: balanceForm.description
          })
        });

        const data = await response.json();

        if (data.success) {
          ElMessage.success(data.message);
          balanceDialogVisible.value = false;
          // 重新加载订单数据以刷新余额
          await loadOrders();
        } else {
          ElMessage.error(data.message || '修改失败');
        }
      } catch (error) {
        ElMessage.error('修改失败: ' + error.message);
      } finally {
        processing.value = false;
      }
    };

    return {
      supplierSearchValue,
      supplier,
      supplierLoading,
      supplierBalanceDialogVisible,
      supplierPendingDialogVisible,
      supplierBalanceForm,
      supplierPendingForm,
      supplierNewBalance,
      supplierPendingBalance,
      loadSupplier,
      showSupplierBalanceDialog,
      showSupplierFrozenBalanceDialog,
      showSupplierPendingDialog,
      calculateSupplierNewBalance,
      calculateSupplierPendingBalance,
      confirmSupplierBalanceChange,
      confirmSupplierPendingChange,
      showClearOrdersDialog,
      showClearBalanceDialog,
      searchValue,
      customer,
      orders,
      loading,
      processing,
      searched,
      dialogVisible,
      dialogTitle,
      currentAction,
      actionParams,
      loadOrders,
      handleAction,
      confirmAction,
      getStatusType,
      getActionButtonType,
      getUniqueSuppliers,
      balanceDialogVisible,
      balanceForm,
      newBalance,
      showBalanceDialog,
      showFrozenBalanceDialog,
      calculateNewBalance,
      confirmBalanceChange
    };
  }
};
</script>

<style scoped>
.order-debug-tool {
  padding: 20px;
}

.header-card {
  margin-bottom: 20px;
}

.customer-card {
  margin-bottom: 20px;
}

.supplier-card {
  margin-bottom: 20px;
}

.card-header {
  font-size: 18px;
  font-weight: bold;
}

.search-form {
  margin: 0;
}

.orders-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.order-card {
  width: 100%;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
}

.order-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.order-meta {
  display: flex;
  align-items: center;
  gap: 20px;
}

.order-no {
  font-weight: bold;
  color: #409eff;
  font-size: 16px;
}

.order-total {
  color: #f56c6c;
  font-weight: bold;
  font-size: 15px;
}

.order-time {
  color: #909399;
  font-size: 13px;
}

.item-detail {
  padding: 20px;
  background-color: #f5f7fa;
}

.action-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.action-buttons .el-button {
  margin: 0;
}

.order-summary {
  margin-top: 15px;
}

.highlight-price {
  color: #f56c6c;
  font-weight: bold;
  font-size: 16px;
}
</style>
