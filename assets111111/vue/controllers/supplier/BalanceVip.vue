<template>
  <div class="balance-vip-container">
    <!-- 余额统计卡片 -->
    <div class="balance-section">
      <el-row :gutter="20" class="balance-cards">
        <el-col :span="8">
          <el-card class="balance-card available-balance">
            <div class="card-icon">
              <el-icon :size="48" color="#52c41a">
                <Wallet />
              </el-icon>
            </div>
            <div class="card-content">
              <div class="card-label">可用余额</div>
              <div class="card-value">{{ formatCurrency(balanceData.balance) }}</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="balance-card frozen-balance">
            <div class="card-icon">
              <el-icon :size="48" color="#faad14">
                <Lock />
              </el-icon>
            </div>
            <div class="card-content">
              <div class="card-label">冻结余额</div>
              <div class="card-value frozen">{{ formatCurrency(balanceData.balanceFrozen) }}</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="balance-card pending-settlement">
            <div class="card-icon">
              <el-icon :size="48" color="#1890ff">
                <Clock />
              </el-icon>
            </div>
            <div class="card-content">
              <div class="card-label">订单待结算</div>
              <div class="card-value pending">{{ formatCurrency(balanceData.pendingSettlementAmount) }}</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
      
      <!-- 充值和提现按钮 -->
      <div class="balance-actions">
        <el-button @click="showRechargeDialog" class="recharge-button-action" type="primary">
          <el-icon style="margin-right: 6px;"><Wallet /></el-icon>
          充值
        </el-button>
        <el-button @click="showWithdrawDialog" class="withdraw-button-action">
          <el-icon style="margin-right: 6px;"><Download /></el-icon>
          提现
        </el-button>
      </div>
    </div>
    
    <!-- 会员信息卡片 -->
    <el-card class="membership-info-card">
      <template #header>
        <div class="card-header">
          <span class="header-title">
            <el-icon style="margin-right: 8px;"><TrophyBase /></el-icon>
            会员信息
          </span>
        </div>
      </template>
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="info-item">
            <div class="info-label">会员类型</div>
            <div class="info-value" :class="{ 'vip-active': balanceData.isMemberActive }">
              {{ membershipTypeName }}
            </div>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="info-item">
            <div class="info-label">到期时间</div>
            <div class="info-value">{{ membershipExpiredAt }}</div>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="info-item">
            <div class="info-label">佣金比例</div>
            <div class="info-value" :class="{ 'commission-free': balanceData.isMemberActive }">
              {{ commissionRateText }}
            </div>
          </div>
        </el-col>
      </el-row>
      
      <!-- 会员等级规则说明 -->
      <div class="membership-rules">
        <div class="rules-header">
          <el-icon class="rules-icon"><InfoFilled /></el-icon>
          <span class="rules-title">会员规则说明</span>
        </div>
        <div class="rules-content">
          有效期内只能升级不能降级，可购买任意等级会员延长有效期，过期后可重新选择任意等级。
        </div>
      </div>
    </el-card>
    
    <!-- 会员套餐选择 -->
    <el-card class="membership-plans-card">
      <template #header>
        <div class="card-header">
          <span class="header-title">
            <el-icon style="margin-right: 8px;"><TrophyBase /></el-icon>
            会员套餐
          </span>
          <span class="header-subtitle">开通会员，尊享特权</span>
        </div>
      </template>
      <el-row :gutter="20">
        <el-col :span="6" v-for="plan in membershipPlans" :key="plan.type">
          <div 
            class="membership-plan" 
            :class="[
              { 'active': selectedMembershipPlan === plan.type },
              `plan-${plan.type}`
            ]"
            @click="selectMembershipPlan(plan.type)"
          >
            <div class="plan-badge" v-if="plan.type === 'yearly'">推荐</div>
            <div class="plan-header">
              <div class="plan-name">{{ plan.name }}</div>
              <div class="plan-price">
                <span class="currency">{{ balanceData.currencySymbol }}</span>
                <span class="amount">{{ plan.price }}</span>
              </div>
            </div>
            <el-button 
              class="plan-button"
              type="primary"
              size="large"
              @click.stop="confirmPurchaseMembership(plan.type)"
              :loading="purchasingPlan === plan.type"
            >
              立即开通
            </el-button>
            <div class="plan-benefits">
              <div class="benefit" v-for="benefit in plan.benefits" :key="benefit">
                <el-icon color="#52c41a" class="check-icon"><CircleCheck /></el-icon>
                <span>{{ benefit }}</span>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>
    
    <!-- 提现对话框（Payoneer在线提现） -->
    <el-dialog 
      v-model="withdrawDialogVisible" 
      title="申请提现" 
      width="600px"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <div class="withdraw-dialog-content" style="padding: 0 20px;">
        <!-- 提现金额输入 -->
        <div style="margin-bottom: 24px;">
          <label style="display: block; font-size: 14px; font-weight: 500; color: #374151; margin-bottom: 8px;">
            提现金额
          </label>
          <div style="position: relative;">
            <span style="position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: #6b7280; font-size: 18px;">{{ balanceData.currencySymbol }}</span>
            <input
              v-model.number="withdrawForm.amount"
              type="number"
              min="1"
              step="0.01"
              :max="parseFloat(balanceData.balance)"
              style="width: 100%; padding: 12px 16px 12px 32px; border: 1px solid #d1d5db; border-radius: 6px; outline: none; font-size: 18px; transition: all 0.2s;"
              placeholder="请输入提现金额"
              @input="formatAmount"
              @focus="$event.target.style.borderColor='#52c41a'; $event.target.style.boxShadow='0 0 0 3px rgba(82, 196, 26, 0.1)'"
              @blur="$event.target.style.borderColor='#d1d5db'; $event.target.style.boxShadow='none'"
            />
          </div>
          <p style="margin-top: 8px; font-size: 14px; color: #52c41a;">
            可用余额：{{ formatCurrency(balanceData.balance) }}
          </p>
        </div>

        <!-- 快捷金额选择 -->
        <div style="margin-bottom: 24px;">
          <label style="display: block; font-size: 14px; font-weight: 500; color: #374151; margin-bottom: 8px;">
            快捷金额
          </label>
          <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px;">
            <button
              v-for="amount in getAvailableWithdrawAmounts()"
              :key="amount"
              @click="withdrawForm.amount = amount"
              style="padding: 8px 16px; border: 1px solid; border-radius: 6px; cursor: pointer; transition: all 0.2s; font-size: 14px; background: white;"
              :style="{
                borderColor: withdrawForm.amount === amount ? '#52c41a' : '#d1d5db',
                color: withdrawForm.amount === amount ? '#52c41a' : '#374151',
                backgroundColor: withdrawForm.amount === amount ? '#f6ffed' : 'white'
              }"
            >
              {{ balanceData.currencySymbol }}{{ amount }}
            </button>
            <button
              @click="withdrawForm.amount = parseFloat(balanceData.balance)"
              style="padding: 8px 16px; border: 1px solid; border-radius: 6px; cursor: pointer; transition: all 0.2s; font-size: 14px; background: white;"
              :style="{
                borderColor: withdrawForm.amount === parseFloat(balanceData.balance) ? '#52c41a' : '#d1d5db',
                color: withdrawForm.amount === parseFloat(balanceData.balance) ? '#52c41a' : '#374151',
                backgroundColor: withdrawForm.amount === parseFloat(balanceData.balance) ? '#f6ffed' : 'white'
              }"
            >
              全部
            </button>
          </div>
        </div>

        <!-- Payoneer账号信息 -->
        <div v-if="withdrawForm.amount > 0" style="margin-bottom: 24px; background-color: #f6ffed; padding: 16px; border-radius: 8px;">
          <div style="margin-bottom: 16px;">
            <label style="display: block; font-size: 14px; font-weight: 500; color: #374151; margin-bottom: 8px;">
              Payoneer 账号 *
            </label>
            <input
              v-model="withdrawForm.accountNumber"
              type="text"
              style="width: 100%; padding: 12px; border: 1px solid #d1d5db; border-radius: 6px; outline: none; font-size: 14px; transition: all 0.2s;"
              placeholder="请填写您的 Payoneer 账号"
              @focus="$event.target.style.borderColor='#52c41a'; $event.target.style.boxShadow='0 0 0 3px rgba(82, 196, 26, 0.1)'"
              @blur="$event.target.style.borderColor='#d1d5db'; $event.target.style.boxShadow='none'"
            />
            <p style="margin-top: 8px; font-size: 14px; color: #6b7280;">
              <svg style="display: inline-block; width: 16px; height: 16px; margin-right: 4px; vertical-align: middle;" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
              </svg>
              提现将通过 Payoneer 支付平台处理
            </p>
          </div>

          <!-- 提交按钮 -->
          <button
            @click="submitWithdraw"
            :disabled="!isOnlineWithdrawFormValid || withdrawLoading"
            class="withdraw-submit-button"
            :class="{ 'disabled': !isOnlineWithdrawFormValid || withdrawLoading }"
          >
            <svg v-if="withdrawLoading" style="animation: spin 1s linear infinite; width: 20px; height: 20px;" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle style="opacity: 0.25;" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path style="opacity: 0.75;" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 714 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>{{ withdrawLoading ? '提交中...' : '确认提现' }}</span>
          </button>
        </div>
        <div v-else style="text-align: center; padding: 32px 0; color: #6b7280;">
          请输入提现金额
        </div>
      </div>
    </el-dialog>
    
    <!-- 离线提现对话框（手动打款） -->
    <el-dialog 
      v-model="offlineWithdrawDialogVisible" 
      title="申请提现（管理员审核）" 
      width="600px"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <div class="withdraw-dialog-content" style="padding: 0 20px;">
        <!-- 提现金额输入 -->
        <div style="margin-bottom: 24px;">
          <label style="display: block; font-size: 14px; font-weight: 500; color: #374151; margin-bottom: 8px;">
            提现金额
          </label>
          <div style="position: relative;">
            <span style="position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: #6b7280; font-size: 18px;">{{ balanceData.currencySymbol }}</span>
            <input
              v-model.number="offlineWithdrawForm.amount"
              type="number"
              min="1"
              step="0.01"
              :max="parseFloat(balanceData.balance)"
              style="width: 100%; padding: 12px 16px 12px 32px; border: 1px solid #d1d5db; border-radius: 6px; outline: none; font-size: 18px; transition: all 0.2s;"
              placeholder="请输入提现金额"
              @input="formatOfflineAmount"
              @focus="$event.target.style.borderColor='#f97316'; $event.target.style.boxShadow='0 0 0 3px rgba(249, 115, 22, 0.1)'"
              @blur="$event.target.style.borderColor='#d1d5db'; $event.target.style.boxShadow='none'"
            />
          </div>
          <p style="margin-top: 8px; font-size: 14px; color: #ea580c;">
            可用余额：{{ formatCurrency(balanceData.balance) }}
          </p>
        </div>

        <!-- 快捷金额选择 -->
        <div style="margin-bottom: 24px;">
          <label style="display: block; font-size: 14px; font-weight: 500; color: #374151; margin-bottom: 8px;">
            快捷金额
          </label>
          <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px;">
            <button
              v-for="amount in getAvailableWithdrawAmounts()"
              :key="amount"
              @click="offlineWithdrawForm.amount = amount"
              style="padding: 8px 16px; border: 1px solid; border-radius: 6px; cursor: pointer; transition: all 0.2s; font-size: 14px; background: white;"
              :style="{
                borderColor: offlineWithdrawForm.amount === amount ? '#f97316' : '#d1d5db',
                color: offlineWithdrawForm.amount === amount ? '#f97316' : '#374151',
                backgroundColor: offlineWithdrawForm.amount === amount ? '#fff7ed' : 'white'
              }"
            >
              {{ balanceData.currencySymbol }}{{ amount }}
            </button>
            <button
              @click="offlineWithdrawForm.amount = parseFloat(balanceData.balance)"
              style="padding: 8px 16px; border: 1px solid; border-radius: 6px; cursor: pointer; transition: all 0.2s; font-size: 14px; background: white;"
              :style="{
                borderColor: offlineWithdrawForm.amount === parseFloat(balanceData.balance) ? '#f97316' : '#d1d5db',
                color: offlineWithdrawForm.amount === parseFloat(balanceData.balance) ? '#f97316' : '#374151',
                backgroundColor: offlineWithdrawForm.amount === parseFloat(balanceData.balance) ? '#fff7ed' : 'white'
              }"
            >
              全部
            </button>
          </div>
        </div>

        <!-- 收款信息 -->
        <div v-if="offlineWithdrawForm.amount > 0" style="margin-bottom: 24px; background-color: #fff7ed; padding: 16px; border-radius: 8px;">
          <div style="margin-bottom: 16px;">
            <label style="display: block; font-size: 14px; font-weight: 500; color: #374151; margin-bottom: 8px;">
              收款信息 *
            </label>
            <textarea
              v-model="offlineWithdrawForm.paymentInfo"
              rows="4"
              style="width: 100%; padding: 12px; border: 1px solid #d1d5db; border-radius: 6px; outline: none; resize: none; font-size: 14px; transition: all 0.2s;"
              placeholder="请填写您的收款信息（如：银行账号、支付宝账号、Payoneer账号等）"
              @focus="$event.target.style.borderColor='#f97316'; $event.target.style.boxShadow='0 0 0 3px rgba(249, 115, 22, 0.1)'"
              @blur="$event.target.style.borderColor='#d1d5db'; $event.target.style.boxShadow='none'"
            ></textarea>
            <p style="margin-top: 8px; font-size: 14px; color: #6b7280;">
              提示：请准确填写收款信息，以便管理员审核通过后能及时打款
            </p>
          </div>

          <!-- 提交按钮 -->
          <button
            @click="submitOfflineWithdraw"
            :disabled="!isOfflineWithdrawFormValid || offlineWithdrawLoading"
            class="offline-withdraw-button"
            :class="{ 'disabled': !isOfflineWithdrawFormValid || offlineWithdrawLoading }"
          >
            <svg v-if="offlineWithdrawLoading" style="animation: spin 1s linear infinite; width: 20px; height: 20px;" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle style="opacity: 0.25;" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path style="opacity: 0.75;" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>{{ offlineWithdrawLoading ? '提交中...' : '确认提现' }}</span>
          </button>
        </div>
        <div v-else style="text-align: center; padding: 32px 0; color: #6b7280;">
          请输入提现金额
        </div>
      </div>
    </el-dialog>
    
    <!-- 充值对话框 -->
    <el-dialog 
      v-model="rechargeDialogVisible" 
      title="账户充值" 
      width="600px"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <div class="recharge-dialog-content" style="padding: 0 20px;">
        <!-- 充值金额输入 -->
        <div style="margin-bottom: 24px;">
          <label style="display: block; font-size: 14px; font-weight: 500; color: #374151; margin-bottom: 8px;">
            充值金额
          </label>
          <div style="position: relative;">
            <span style="position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: #6b7280; font-size: 18px;">{{ balanceData.currencySymbol }}</span>
            <input
              v-model.number="rechargeForm.amount"
              type="number"
              min="1"
              step="0.01"
              style="width: 100%; padding: 12px 16px 12px 32px; border: 1px solid #d1d5db; border-radius: 6px; outline: none; font-size: 18px; transition: all 0.2s;"
              placeholder="请输入充值金额"
              @input="formatRechargeAmount"
              @focus="$event.target.style.borderColor='#1890ff'; $event.target.style.boxShadow='0 0 0 3px rgba(24, 144, 255, 0.1)'"
              @blur="$event.target.style.borderColor='#d1d5db'; $event.target.style.boxShadow='none'"
            />
          </div>
          <p style="margin-top: 8px; font-size: 14px; color: #1890ff;">
            当前余额：{{ formatCurrency(balanceData.balance) }}
          </p>
        </div>

        <!-- 快捷金额选择 -->
        <div style="margin-bottom: 24px;">
          <label style="display: block; font-size: 14px; font-weight: 500; color: #374151; margin-bottom: 8px;">
            快捷金额
          </label>
          <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px;">
            <button
              v-for="amount in quickRechargeAmounts"
              :key="amount"
              @click="rechargeForm.amount = amount"
              style="padding: 8px 16px; border: 1px solid; border-radius: 6px; cursor: pointer; transition: all 0.2s; font-size: 14px; background: white;"
              :style="{
                borderColor: rechargeForm.amount === amount ? '#1890ff' : '#d1d5db',
                color: rechargeForm.amount === amount ? '#1890ff' : '#374151',
                backgroundColor: rechargeForm.amount === amount ? '#e6f7ff' : 'white'
              }"
            >
              {{ balanceData.currencySymbol }}{{ amount }}
            </button>
          </div>
        </div>

        <!-- 提交按钮 -->
        <div v-if="rechargeForm.amount > 0" style="margin-bottom: 24px; background-color: #e6f7ff; padding: 16px; border-radius: 8px;">
          <p style="margin-bottom: 12px; font-size: 14px; color: #6b7280; text-align: center;">
            <svg style="display: inline-block; width: 16px; height: 16px; margin-right: 4px; vertical-align: middle;" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
            </svg>
            充值将通过 Payoneer 支付平台处理
          </p>
          <button
            @click="submitRecharge"
            :disabled="!isRechargeFormValid || rechargeLoading"
            class="recharge-submit-button"
            :class="{ 'disabled': !isRechargeFormValid || rechargeLoading }"
          >
            <svg v-if="rechargeLoading" style="animation: spin 1s linear infinite; width: 20px; height: 20px;" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle style="opacity: 0.25;" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path style="opacity: 0.75;" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>{{ rechargeLoading ? '处理中...' : '确认充值' }}</span>
          </button>
        </div>
        <div v-else style="text-align: center; padding: 32px 0; color: #6b7280;">
          请输入充值金额
        </div>
      </div>
    </el-dialog>
    
    <!-- 会员购买确认对话框 -->
    <el-dialog v-model="purchaseConfirmDialogVisible" title="确认购买会员" width="500px">
      <div v-if="purchaseConfirmData">
        <p>您即将购买 <strong>{{ purchaseConfirmData.membershipName }}</strong></p>
        <p>价格：<strong>{{ balanceData.currencySymbol }}{{ purchaseConfirmData.price }}</strong></p>
        <div v-if="purchaseConfirmData.isMemberActive">
          <p>您当前是 <strong>{{ membershipTypeMap[purchaseConfirmData.currentMembershipType] }}</strong>，有效期至 {{ purchaseConfirmData.currentMembershipExpiredAt }}</p>
          <p>本次购买将延长您的会员有效期。</p>
        </div>
        <div v-else>
          <p v-if="purchaseConfirmData.currentMembershipType && purchaseConfirmData.currentMembershipType !== 'none'">
            您当前是 <strong>{{ membershipTypeMap[purchaseConfirmData.currentMembershipType] }}</strong>，但已过期。
          </p>
          <p v-else>
            您当前没有会员。
          </p>
          <p>本次购买将为您开通新的会员。</p>
        </div>
        <p>购买后将从您的余额中扣除 <strong>{{ balanceData.currencySymbol }}{{ purchaseConfirmData.price }}</strong></p>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="purchaseConfirmDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="purchaseMembership" :loading="purchasingPlan !== ''">确认购买</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import {
  ElCard,
  ElRow,
  ElCol,
  ElButton,
  ElDialog,
  ElForm,
  ElFormItem,
  ElInput,
  ElMessage,
  ElMessageBox,
  ElTag,
  ElAlert,
  ElIcon
} from 'element-plus'
import {
  Wallet,
  Lock,
  Download,
  Clock,
  TrophyBase,
  InfoFilled,
  CircleCheck
} from '@element-plus/icons-vue'

export default {
  name: 'BalanceVip',
  components: {
    ElCard,
    ElRow,
    ElCol,
    ElButton,
    ElDialog,
    ElForm,
    ElFormItem,
    ElInput,
    ElTag,
    ElAlert,
    ElIcon,
    Wallet,
    Lock,
    Download,
    Clock,
    TrophyBase,
    InfoFilled,
    CircleCheck
  },
  props: {
    supplierLoginPath: {
      type: String,
      default: ''
    },
    // 添加autoLoad属性以支持按需加载
    autoLoad: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {

// 数据
const balanceData = ref({
  balance: '0.00',
  balanceFrozen: '0.00',
  pendingSettlementAmount: '0.00',
  membershipType: 'none',
  membershipExpiredAt: null,
  commissionRate: null,
  commissionRatePercentage: null,
  originalCommissionRate: null,
  originalCommissionRatePercentage: null,
  isMemberActive: false,
  membershipPrices: {},
  defaultPaymentInfo: '', // 默认收款信息
  currencySymbol: '$' // 货币符号，默认美元符号
})

// 提现配置
const withdrawalConfig = ref({
  withdrawalMode: 'offline',
  isOnlinePayment: false,
  isOfflinePayment: true
})

// 在线提现对话框
const withdrawDialogVisible = ref(false)
const withdrawLoading = ref(false)
const withdrawForm = ref({
  amount: '',
  accountNumber: '' // Payoneer 账号
})
const withdrawFormRef = ref(null)

// 离线提现对话框
const offlineWithdrawDialogVisible = ref(false)
const offlineWithdrawLoading = ref(false)
const offlineWithdrawForm = ref({
  amount: '',
  paymentInfo: ''
})
const offlineWithdrawFormRef = ref(null)

// 快捷金额选项
const quickAmounts = [10, 20, 50, 100, 200, 500, 1000, 2000]
const quickRechargeAmounts = [10, 20, 50, 100, 200, 500, 1000, 2000]

// 充值对话框
const rechargeDialogVisible = ref(false)
const rechargeLoading = ref(false)
const rechargeForm = ref({
  amount: ''
})
const rechargeFormRef = ref(null)

// 会员购买
const selectedMembershipPlan = ref('')
const purchasingPlan = ref('')
const purchaseConfirmDialogVisible = ref(false)
const purchaseConfirmData = ref(null)

// 会员类型映射
const membershipTypeMap = {
  'none': '无会员',
  'monthly': '月会员',
  'quarterly': '季度会员',
  'half_yearly': '半年会员',
  'yearly': '年会员'
}

// 会员计划
const membershipPlans = computed(() => {
  const prices = balanceData.value.membershipPrices || {};
  return [
    {
      type: 'monthly',
      name: '月会员',
      price: prices.monthly || '...',
      benefits: ['免佣金', '优先客服', '专属活动']
    },
    {
      type: 'quarterly',
      name: '季度会员',
      price: prices.quarterly || '...',
      benefits: ['免佣金', '优先客服', '专属活动', '月度报告']
    },
    {
      type: 'half_yearly',
      name: '半年会员',
      price: prices.half_yearly || '...',
      benefits: ['免佣金', '优先客服', '专属活动', '月度报告', '定制服务']
    },
    {
      type: 'yearly',
      name: '年会员',
      price: prices.yearly || '...',
      benefits: ['免佣金', '优先客服', '专属活动', '月度报告', '定制服务', '一对一顾问']
    }
  ];
})

// 提现表单验证规则
const withdrawRules = {
  amount: [
    { required: true, message: '请输入提现金额', trigger: 'blur' },
    { type: 'number', min: 10, message: '提现金额不能小于 10 元', trigger: 'blur' },
    { 
      validator: (rule, value, callback) => {
        if (value && !/^\d+(\.\d{1,2})?$/.test(value.toString())) {
          callback(new Error('提现金额最多保留两位小数'));
        } else {
          callback();
        }
      }, 
      trigger: 'blur' 
    }
  ],
  accountNumber: [
    { required: true, message: '请填写 Payoneer 账号', trigger: 'blur' },
    { min: 3, message: 'Payoneer 账号至少 3 个字符', trigger: 'blur' }
  ]
}

// 离线提现表单验证规则
const offlineWithdrawRules = {
  amount: [
    { required: true, message: '请输入提现金额', trigger: 'blur' },
    { type: 'number', min: 10, message: '提现金额不能小于 10 元', trigger: 'blur' },
    { 
      validator: (rule, value, callback) => {
        if (value && !/^\d+(\.\d{1,2})?$/.test(value.toString())) {
          callback(new Error('提现金额最多保留两位小数'));
        } else {
          callback();
        }
      }, 
      trigger: 'blur' 
    }
  ],
  paymentInfo: [
    { required: true, message: '请填写收款信息', trigger: 'blur' },
    { min: 10, message: '收款信息至少 10 个字符', trigger: 'blur' }
  ]
}

// 充值表单验证规则
const rechargeRules = {
  amount: [
    { required: true, message: '请输入充值金额', trigger: 'blur' },
    { type: 'number', min: 10, message: '充值金额不能小于 10 元', trigger: 'blur' },
    { 
      validator: (rule, value, callback) => {
        if (value && !/^\d+(\.\d{1,2})?$/.test(value.toString())) {
          callback(new Error('充值金额最多保留两位小数'));
        } else {
          callback();
        }
      }, 
      trigger: 'blur' 
    }
  ]
}

// 计算属性
const membershipTypeName = computed(() => {
  return membershipTypeMap[balanceData.value.membershipType] || '无会员'
})

const membershipExpiredAt = computed(() => {
  if (balanceData.value.membershipExpiredAt) {
    return balanceData.value.membershipExpiredAt
  }
  return '未开通'
})

const commissionRateText = computed(() => {
  // 检查是否为活跃会员
  if (balanceData.value.isMemberActive) {
    return '免佣金（VIP特权）'
  }
  
  // 如果有有效的佣金比例，显示该比例
  if (balanceData.value.commissionRatePercentage !== null) {
    return balanceData.value.commissionRatePercentage + '%'
  }
  
  // 如果会员不活跃但有自定义佣金比例，显示自定义比例
  if (balanceData.value.originalCommissionRate !== null) {
    const rate = parseFloat(balanceData.value.originalCommissionRate) * 100;
    return rate.toFixed(2) + '%';
  }
  
  // 如果都没有设置，显示未设置
  return '未设置'
})

// 格式化货币
const formatCurrency = (value) => {
  if (value === null || value === undefined) return balanceData.value.currencySymbol + '0.00'
  return balanceData.value.currencySymbol + parseFloat(value).toFixed(2)
}

// 格式化金额，保留两位小数
const formatAmount = (value) => {
  if (value && typeof value === 'number') {
    withdrawForm.value.amount = parseFloat(value.toFixed(2));
  }
}

// 获取可用的提现快捷金额
const getAvailableWithdrawAmounts = () => {
  const balance = parseFloat(balanceData.value.balance || 0)
  return quickAmounts.filter(amount => amount <= balance)
}

// 离线提现表单验证
const isOfflineWithdrawFormValid = computed(() => {
  if (offlineWithdrawForm.value.amount <= 0 || offlineWithdrawForm.value.amount > parseFloat(balanceData.value.balance)) {
    return false
  }
  if (!offlineWithdrawForm.value.paymentInfo || offlineWithdrawForm.value.paymentInfo.trim() === '') {
    return false
  }
  return true
})

// 在线提现表单验证
const isOnlineWithdrawFormValid = computed(() => {
  if (withdrawForm.value.amount <= 0 || withdrawForm.value.amount > parseFloat(balanceData.value.balance)) {
    return false
  }
  if (!withdrawForm.value.accountNumber || withdrawForm.value.accountNumber.trim().length < 3) {
    return false
  }
  return true
})

// 充值表单验证
const isRechargeFormValid = computed(() => {
  if (rechargeForm.value.amount <= 0) {
    return false
  }
  if (!/^\d+(\.\d{1,2})?$/.test(rechargeForm.value.amount.toString())) {
    return false
  }
  return true
})

// 格式化离线提现金额
const formatOfflineAmount = (value) => {
  if (value && typeof value === 'number') {
    offlineWithdrawForm.value.amount = parseFloat(value.toFixed(2));
  }
}

// 提交离线提现申请
const submitOfflineWithdraw = async () => {
  // 手动验证表单
  if (!isOfflineWithdrawFormValid.value) {
    ElMessage.warning('请填写完整的提现信息')
    return
  }
  
  offlineWithdrawLoading.value = true
  try {
    const amount = parseFloat(offlineWithdrawForm.value.amount).toFixed(2);
    
    const response = await fetch(`/supplier${props.supplierLoginPath}/balance-vip/withdraw-offline`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        amount: amount,
        paymentInfo: offlineWithdrawForm.value.paymentInfo.trim()
      })
    })
    
    const result = await response.json()
    
    if (result.success) {
      ElMessage.success(result.message)
      offlineWithdrawDialogVisible.value = false
      // 重置表单
      offlineWithdrawForm.value.amount = ''
      offlineWithdrawForm.value.paymentInfo = ''
      // 重新加载数据
      await loadBalanceVipData()
    } else {
      ElMessage.error(result.message || '提现失败')
    }
  } catch (error) {
    ElMessage.error('网络错误：' + error.message)
  } finally {
    offlineWithdrawLoading.value = false
  }
}

// 加载数据
const loadBalanceVipData = async () => {
  try {
    const response = await fetch(`/supplier${props.supplierLoginPath}/balance-vip/data`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    
    const result = await response.json()
    
    if (result.success) {
      // 更新balanceData，确保包含membershipPrices
      balanceData.value = {
        ...balanceData.value,
        ...result.data,
        membershipPrices: result.data.membershipPrices || {}
      }
    } else {
      ElMessage.error(result.message || '获取数据失败')
    }
  } catch (error) {
    ElMessage.error('网络错误：' + error.message)
  }
}

// 加载提现配置
const loadWithdrawalConfig = async () => {
  try {
    const response = await fetch(`/supplier${props.supplierLoginPath}/balance-vip/withdrawal-config`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    
    const result = await response.json()
    
    if (result.success && result.data) {
      withdrawalConfig.value = result.data
    }
  } catch (error) {
    console.error('加载提现配置失败:', error)
    // 默认使用离线模式
    withdrawalConfig.value = {
      withdrawalMode: 'offline',
      isOnlinePayment: false,
      isOfflinePayment: true
    }
  }
}

// 显示提现对话框
const showWithdrawDialog = async () => {
  // 先加载配置
  await loadWithdrawalConfig()
  
  // 检查余额
  const balance = parseFloat(balanceData.value.balance || 0)
  if (balance <= 0) {
    ElMessage.warning('余额不足，无法提现')
    return
  }
  
  if (withdrawalConfig.value.isOnlinePayment) {
    // 在线提现（Payoneer）
    withdrawForm.value.amount = ''
    withdrawForm.value.accountNumber = ''
    withdrawDialogVisible.value = true
  } else if (withdrawalConfig.value.isOfflinePayment) {
    // 离线提现（手动打款）
    offlineWithdrawForm.value.amount = ''
    // 填充默认收款信息
    offlineWithdrawForm.value.paymentInfo = balanceData.value.defaultPaymentInfo || ''
    offlineWithdrawDialogVisible.value = true
  }
}

// 提交提现申请
const submitWithdraw = async () => {
  // 手动验证表单
  if (!isOnlineWithdrawFormValid.value) {
    ElMessage.warning('请填写完整的提现信息')
    return
  }
  
  withdrawLoading.value = true
  try {
    // 确保金额格式化为两位小数
    const amount = parseFloat(withdrawForm.value.amount).toFixed(2);
    
    const response = await fetch(`/supplier${props.supplierLoginPath}/balance-vip/withdraw`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        amount: amount,
        accountNumber: withdrawForm.value.accountNumber.trim()
      })
    })
    
    const result = await response.json()
    
    if (result.success) {
      ElMessage.success(result.message)
      withdrawDialogVisible.value = false
      // 重置表单
      withdrawForm.value.amount = ''
      withdrawForm.value.accountNumber = ''
      // 重新加载数据
      await loadBalanceVipData()
    } else {
      ElMessage.error(result.message || '提现失败')
    }
  } catch (error) {
    ElMessage.error('网络错误：' + error.message)
  } finally {
    withdrawLoading.value = false
  }
}

// 格式化充值金额，保留两位小数
const formatRechargeAmount = (value) => {
  if (value && typeof value === 'number') {
    rechargeForm.value.amount = parseFloat(value.toFixed(2));
  }
}

// 显示充值对话框
const showRechargeDialog = () => {
  rechargeForm.value.amount = ''
  rechargeDialogVisible.value = true
}

// 提交充值申请
const submitRecharge = async () => {
  // 手动验证表单
  if (!isRechargeFormValid.value) {
    ElMessage.warning('请填写有效的充值金额')
    return
  }
  
  rechargeLoading.value = true
  try {
    // 确保金额格式化为两位小数
    const amount = parseFloat(rechargeForm.value.amount).toFixed(2);
    
    const response = await fetch(`/supplier${props.supplierLoginPath}/balance-vip/recharge`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        amount: amount
      })
    })
    
    const result = await response.json()
    
    if (result.success) {
      // 跳转到 Payoneer 支付页面
      window.location.href = result.paymentUrl
    } else {
      ElMessage.error(result.message || '充值失败')
    }
  } catch (error) {
    ElMessage.error('网络错误：' + error.message)
  } finally {
    rechargeLoading.value = false
  }
}

// 选择会员计划
const selectMembershipPlan = (planType) => {
  selectedMembershipPlan.value = planType
}

// 确认购买会员
const confirmPurchaseMembership = async (planType) => {
  purchasingPlan.value = planType
  try {
    const response = await fetch(`/supplier${props.supplierLoginPath}/balance-vip/purchase-membership-confirm`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        membershipType: planType
      })
    })
    
    const result = await response.json()
    
    if (result.success) {
      purchaseConfirmData.value = result.data
      purchaseConfirmDialogVisible.value = true
    } else {
      ElMessage.error(result.message || '获取确认信息失败')
    }
  } catch (error) {
    ElMessage.error('网络错误：' + error.message)
  } finally {
    purchasingPlan.value = ''
  }
}

// 购买会员
const purchaseMembership = async () => {
  if (!purchaseConfirmData.value) return
  
  const planType = purchaseConfirmData.value.membershipType
  purchasingPlan.value = planType
  purchaseConfirmDialogVisible.value = false
  
  try {
    const response = await fetch(`/supplier${props.supplierLoginPath}/balance-vip/purchase-membership`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        membershipType: planType
      })
    })
    
    const result = await response.json()
    
    if (result.success) {
      ElMessage.success(result.message)
      // 重新加载数据
      await loadBalanceVipData()
    } else {
      ElMessage.error(result.message || '购买失败')
    }
  } catch (error) {
    ElMessage.error('网络错误：' + error.message)
  } finally {
    purchasingPlan.value = ''
    purchaseConfirmData.value = null
  }
}

    // 组件挂载时根据autoLoad属性决定是否自动加载数据
    onMounted(() => {
      if (props.autoLoad) {
        loadBalanceVipData()
        loadWithdrawalConfig() // 加载提现配置
      }
    })

    // 暴露方法给父组件
    return {
      balanceData,
      withdrawalConfig,
      withdrawDialogVisible,
      withdrawLoading,
      withdrawForm,
      offlineWithdrawDialogVisible,
      offlineWithdrawLoading,
      offlineWithdrawForm,
      rechargeDialogVisible,
      rechargeLoading,
      rechargeForm,
      selectedMembershipPlan,
      purchasingPlan,
      purchaseConfirmDialogVisible,
      purchaseConfirmData,
      membershipTypeMap,
      membershipPlans,
      membershipTypeName,
      membershipExpiredAt,
      commissionRateText,
      formatCurrency,
      formatAmount,
      getAvailableWithdrawAmounts,
      isOfflineWithdrawFormValid,
      isOnlineWithdrawFormValid,
      isRechargeFormValid,
      formatOfflineAmount,
      submitOfflineWithdraw,
      loadBalanceVipData,
      loadWithdrawalConfig,
      showWithdrawDialog,
      submitWithdraw,
      formatRechargeAmount,
      showRechargeDialog,
      submitRecharge,
      selectMembershipPlan,
      confirmPurchaseMembership,
      purchaseMembership,
      quickRechargeAmounts
    }
  }
}
</script>



<style scoped>
.balance-vip-container {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

/* 离线提现按钮样式 */
.offline-withdraw-button {
  width: 100%;
  padding: 12px 16px;
  background-color: #f97316;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 16px;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.offline-withdraw-button:hover:not(.disabled) {
  background-color: #ea580c;
}

.offline-withdraw-button.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 旋转动画 */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* 余额区域容器 */
.balance-section {
  position: relative;
  margin-bottom: 24px;
}

/* 余额卡片 */
.balance-cards {
  margin-bottom: 0;
}

.balance-card {
  cursor: default;
  transition: all 0.3s ease;
  border-radius: 12px;
  overflow: hidden;
  height: 140px;
}

.balance-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.balance-card :deep(.el-card__body) {
  display: flex;
  align-items: center;
  padding: 24px;
  gap: 20px;
}

.available-balance {
  background: linear-gradient(135deg, #f0f9ff 0%, #e6f7ff 100%);
  border: 1px solid #91d5ff;
}

.frozen-balance {
  background: linear-gradient(135deg, #fffbe6 0%, #fff7e6 100%);
  border: 1px solid #ffe58f;
}

.pending-settlement {
  background: linear-gradient(135deg, #e6f7ff 0%, #d9f0ff 100%);
  border: 1px solid #91d5ff;
}

.withdraw-card {
  background: linear-gradient(135deg, #fffbe6 0%, #fff7e6 100%);
  border: 1px solid #ffe58f;
}

.card-icon {
  flex-shrink: 0;
}

.card-content {
  flex: 1;
}

.card-label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 12px;
  font-weight: 500;
}

.card-value {
  font-size: 32px;
  font-weight: 700;
  color: #52c41a;
  line-height: 1.2;
}

.card-value.frozen {
  color: #faad14;
}

.card-value.pending {
  color: #1890ff;
}

/* 充值和提现按钮区域 */
.balance-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 16px;
}

/* 充值按钮样式 */
.recharge-button-action {
  height: 44px;
  padding: 0 24px;
  font-size: 15px;
  font-weight: 600;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #faad14 0%, #fa8c16 100%);
  border: none;
  color: white;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(250, 173, 20, 0.3);
}

.recharge-button-action:hover {
  background: linear-gradient(135deg, #ffc53d 0%, #ffa940 100%);
  box-shadow: 0 6px 16px rgba(250, 173, 20, 0.5);
  transform: translateY(-2px);
}

.recharge-button-action:active {
  transform: translateY(0);
}

/* 提现按钮样式 */
.withdraw-button-action {
  height: 44px;
  padding: 0 24px;
  font-size: 15px;
  font-weight: 600;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #52c41a 0%, #389e0d 100%);
  border: none;
  color: white;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(82, 196, 26, 0.3);
}

.withdraw-button-action:hover {
  background: linear-gradient(135deg, #73d13d 0%, #52c41a 100%);
  box-shadow: 0 6px 16px rgba(82, 196, 26, 0.5);
  transform: translateY(-2px);
}

.withdraw-button-action:active {
  transform: translateY(0);
}

/* 会员信息卡片 */
.membership-info-card {
  margin-bottom: 24px;
  border-radius: 12px;
}

.membership-info-card :deep(.el-card__header) {
  background: linear-gradient(135deg, #f9f0ff 0%, #f0e6ff 100%);
  border-bottom: 1px solid #d3adf7;
  padding: 20px 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  display: flex;
  align-items: center;
}

.header-subtitle {
  font-size: 14px;
  color: #909399;
}

.info-item {
  text-align: center;
  padding: 20px;
  background: #fafafa;
  border-radius: 8px;
  transition: all 0.3s;
}

.info-item:hover {
  background: #f0f0f0;
}

.info-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 12px;
}

.info-value {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

.info-value.vip-active {
  color: #52c41a;
}

.info-value.commission-free {
  color: #52c41a;
  font-weight: 700;
}

.no-vip {
  color: #909399;
}

/* 会员等级规则说明 */
.membership-rules {
  background: linear-gradient(135deg, #f0f9ff 0%, #e6f7ff 100%);
  border: 1px solid #91d5ff;
  border-radius: 12px;
  padding: 20px;
  margin-top: 20px;
  box-shadow: 0 4px 12px rgba(24, 144, 255, 0.1);
  transition: all 0.3s ease;
}

.membership-rules:hover {
  box-shadow: 0 6px 16px rgba(24, 144, 255, 0.15);
  transform: translateY(-2px);
}

.rules-header {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
}

.rules-icon {
  font-size: 20px;
  color: #1890ff;
  margin-right: 8px;
}

.rules-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.rules-content {
  text-align: center;
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
  padding: 0 10px;
}

/* 会员套餐卡片 */
.membership-plans-card {
  border-radius: 12px;
}

.membership-plans-card :deep(.el-card__header) {
  background: linear-gradient(135deg, #fff7e6 0%, #fff1db 100%);
  border-bottom: 1px solid #ffd591;
  padding: 20px 24px;
}

.membership-plan {
  position: relative;
  background: #ffffff;
  border: 2px solid #e8e8e8;
  border-radius: 16px;
  padding: 28px 24px;
  transition: all 0.3s ease;
  cursor: pointer;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.membership-plan:hover {
  border-color: #1890ff;
  box-shadow: 0 8px 24px rgba(24, 144, 255, 0.15);
  transform: translateY(-6px);
}

.membership-plan.active {
  border-color: #1890ff;
  box-shadow: 0 8px 32px rgba(24, 144, 255, 0.25);
  background: linear-gradient(135deg, #e6f7ff 0%, #f0f9ff 100%);
}

.plan-badge {
  position: absolute;
  top: -1px;
  right: 24px;
  background: linear-gradient(135deg, #fa8c16 0%, #fa541c 100%);
  color: #fff;
  padding: 4px 16px;
  border-radius: 0 0 12px 12px;
  font-size: 12px;
  font-weight: 600;
  box-shadow: 0 4px 8px rgba(250, 140, 22, 0.3);
}

.plan-header {
  text-align: center;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 2px solid #f0f0f0;
}

.plan-name {
  font-size: 22px;
  font-weight: 700;
  color: #303133;
  margin-bottom: 16px;
}

.plan-price {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 4px;
}

.currency {
  font-size: 20px;
  font-weight: 600;
  color: #fa8c16;
}

.amount {
  font-size: 40px;
  font-weight: 700;
  color: #fa8c16;
  line-height: 1;
}

.plan-button {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 24px;
  margin-bottom: 24px;
  background: linear-gradient(135deg, #1890ff 0%, #096dd9 100%);
  border: none;
  transition: all 0.3s;
}

.plan-button:hover {
  background: linear-gradient(135deg, #40a9ff 0%, #1890ff 100%);
  box-shadow: 0 6px 16px rgba(24, 144, 255, 0.4);
  transform: translateY(-2px);
}

.plan-yearly .plan-button {
  background: linear-gradient(135deg, #fa8c16 0%, #fa541c 100%);
}

.plan-yearly .plan-button:hover {
  background: linear-gradient(135deg, #ffa940 0%, #fa8c16 100%);
  box-shadow: 0 6px 16px rgba(250, 140, 22, 0.4);
}

.plan-benefits {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.benefit {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
}

.check-icon {
  flex-shrink: 0;
}

.dialog-footer {
  text-align: right;
}

/* 充值和提现对话框按钮样式 */
.recharge-submit-button,
.withdraw-submit-button {
  width: 100%;
  padding: 12px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 16px;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: white;
}

.recharge-submit-button {
  background-color: #1890ff;
}

.recharge-submit-button:hover:not(.disabled) {
  background-color: #40a9ff;
  box-shadow: 0 4px 12px rgba(24, 144, 255, 0.4);
}

.withdraw-submit-button {
  background-color: #52c41a;
}

.withdraw-submit-button:hover:not(.disabled) {
  background-color: #73d13d;
  box-shadow: 0 4px 12px rgba(82, 196, 26, 0.4);
}

.recharge-submit-button.disabled,
.withdraw-submit-button.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 快捷金额按钮悬停效果 */
button:hover {
  opacity: 0.9;
}

/* 对话框样式优化 */
.recharge-dialog-content,
.withdraw-dialog-content {
  max-height: 70vh;
  overflow-y: auto;
}

/* 滚动条样式 */
.recharge-dialog-content::-webkit-scrollbar,
.withdraw-dialog-content::-webkit-scrollbar {
  width: 6px;
}

.recharge-dialog-content::-webkit-scrollbar-track,
.withdraw-dialog-content::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.recharge-dialog-content::-webkit-scrollbar-thumb,
.withdraw-dialog-content::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 3px;
}

.recharge-dialog-content::-webkit-scrollbar-thumb:hover,
.withdraw-dialog-content::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>
