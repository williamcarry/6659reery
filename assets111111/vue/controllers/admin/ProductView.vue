<template>
  <div class="product-view" v-loading="loading" element-loading-text="正在加载商品信息，请稍候..." element-loading-background="rgba(255, 255, 255, 0.9)">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-button type="primary" :icon="Back" @click="goBack">返回</el-button>
            <span style="margin-left: 15px;">查看商品</span>
          </div>
          <el-icon v-if="loading" class="loading-icon is-loading">
            <Loading />
          </el-icon>
        </div>
      </template>
      
      <el-form :model="formData" label-width="120px" :disabled="true">
        <!-- 基本信息 -->
        <el-divider content-position="left">基本信息</el-divider>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="SKU">
              <el-input v-model="formData.sku" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="SPU">
              <el-input v-model="formData.spu" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="商品名称">
          <el-input v-model="formData.title" />
        </el-form-item>
        
        <el-form-item label="英文名称">
          <el-input v-model="formData.titleEn" />
        </el-form-item>
        
        <el-form-item label="商品主图">
          <div class="image-preview-list">
            <div v-for="(image, index) in mainImages" :key="`main-image-${index}`" class="image-item">
              <el-image
                :src="image.url"
                fit="cover"
                style="width: 178px; height: 178px; border-radius: 6px"
                :preview-src-list="mainImageUrls"
                preview-teleported
                @click="handleImagePreview(index)"
              >
                <template #error>
                  <div class="image-slot">
                    <el-icon><Picture /></el-icon>
                  </div>
                </template>
              </el-image>
            </div>
          </div>
        </el-form-item>
        
        <!-- 商品详情图 -->
        <el-form-item label="商品详情图" v-if="detailImages && detailImages.length > 0">
          <div class="image-preview-list">
            <div v-for="(image, index) in detailImages" :key="`detail-image-${index}`" class="image-item">
              <el-image
                :src="image.url"
                fit="cover"
                style="width: 178px; height: 178px; border-radius: 6px"
                :preview-src-list="detailImageUrls"
                preview-teleported
                @click="handleDetailImagePreview(index)"
              >
                <template #error>
                  <div class="image-slot">
                    <el-icon><Picture /></el-icon>
                  </div>
                </template>
              </el-image>
            </div>
          </div>
        </el-form-item>
        
        <!-- 分类信息 -->
        <el-divider content-position="left">分类信息</el-divider>
        
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="一级分类">
              <el-input v-model="formData.categoryName" readonly />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="二级分类">
              <el-input v-model="formData.subcategoryName" readonly />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="三级分类">
              <el-input v-model="formData.itemName" readonly />
            </el-form-item>
          </el-col>
        </el-row>
        
        <!-- 商品属性 -->
        <el-divider content-position="left">商品属性</el-divider>
        
        <el-form-item label="品牌">
          <el-input v-model="formData.brand" />
        </el-form-item>
        
        <el-row :gutter="20">
          <el-col :span="6">
            <el-form-item label="长度(cm)">
              <el-input :value="formatToTwoDecimals(formData.length)" />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="宽度(cm)">
              <el-input :value="formatToTwoDecimals(formData.width)" />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="高度(cm)">
              <el-input :value="formatToTwoDecimals(formData.height)" />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="重量(g)">
              <el-input :value="formatToTwoDecimals(formData.weight)" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <!-- 包装信息 -->
        <el-divider content-position="left">包装信息</el-divider>
        
        <el-row :gutter="20">
          <el-col :span="6">
            <el-form-item label="包装长度(cm)">
              <el-input :value="formatToTwoDecimals(formData.packageLength)" />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="包装宽度(cm)">
              <el-input :value="formatToTwoDecimals(formData.packageWidth)" />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="包装高度(cm)">
              <el-input :value="formatToTwoDecimals(formData.packageHeight)" />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="包装重量(g)">
              <el-input :value="formatToTwoDecimals(formData.packageWeight)" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <!-- 商品标签 -->
        <el-form-item label="商品标签">
          <el-select
            v-model="formData.tags"
            multiple
            filterable
            style="width: 100%"
          >
            <el-option
              v-for="tag in allTags"
              :key="tag"
              :label="tag"
              :value="tag"
            />
          </el-select>
        </el-form-item>
        
        <!-- 发货区域 -->
        <el-form-item label="发货区域">
          <div v-if="formData.shippingRegions && formData.shippingRegions.length > 0" style="display: flex; gap: 8px; flex-wrap: wrap;">
            <el-tag
              v-for="(region, index) in formData.shippingRegions"
              :key="index"
              type="success"
              size="large"
            >
              {{ getRegionLabel(region) }}
            </el-tag>
          </div>
          <span v-else style="color: #909399;">未设置</span>
        </el-form-item>
        
        <!-- 多区域配置展示 -->
        <el-divider content-position="left">多区域价格设置</el-divider>
        
        <el-tabs v-model="activeRegion" type="border-card" v-if="formData.shippingRegions.length > 0">
          <el-tab-pane v-for="region in formData.shippingRegions" :key="region" :label="getRegionLabel(region)" :name="region">
            <div class="region-config-panel" v-if="formData.regionConfigs && formData.regionConfigs[region]">
              <!-- 价格配置 -->
              <h4 style="margin: 0 0 15px; color: #409EFF;">💰 价格配置</h4>
              <el-row :gutter="20" v-if="formData.regionConfigs[region].price">
                <el-col :span="12">
                  <el-form-item label="业务类型">
                    <el-input :value="formData.regionConfigs[region].price.businessType === 'dropship' ? '一件代发' : '批发'" readonly />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="币种">
                    <!-- 注释掉原有逻辑：显示各区域自己的币种 -->
                    <!-- <el-input :value="formData.regionConfigs[region].price.currency" readonly /> -->
                    <!-- 新逻辑：统一显示网站配置的币种代码（USD/CNY等） -->
                    <el-input :value="siteCurrency" readonly />
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-row :gutter="20" v-if="formData.regionConfigs[region].price">
                <el-col :span="8">
                  <el-form-item label="原价">
                    <el-input :value="formatToTwoDecimals(formData.regionConfigs[region].price.originalPrice)" readonly />
                  </el-form-item>
                </el-col>
                <el-col :span="8">
                  <el-form-item label="折扣率(%)">
                    <el-input :value="formatToPercentage(formData.regionConfigs[region].price.discountRate)" readonly>
                      <template #append>%</template>
                    </el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="8">
                  <el-form-item label="售价">
                    <el-input :value="formatToTwoDecimals(formData.regionConfigs[region].price.sellingPrice)" readonly />
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-row :gutter="20" v-if="formData.regionConfigs[region].price">
                <el-col :span="12">
                  <el-form-item label="最小起订量">
                    <el-input :value="formatToInteger(formData.regionConfigs[region].price.minWholesaleQuantity)" readonly />
                  </el-form-item>
                </el-col>
              </el-row>
              
              <!-- 会员折扣配置 -->
              <h4 style="margin: 20px 0 15px; color: #409EFF;">👥 会员折扣配置</h4>
              <div class="member-discount-container" v-if="formData.regionConfigs[region].price && formData.regionConfigs[region].price.memberDiscount">
                <el-row :gutter="20">
                  <el-col :span="8" v-for="level in vipLevels" :key="level.value">
                    <el-form-item :label="level.label">
                      <el-input :value="formatToPercentage(formData.regionConfigs[region].price.memberDiscount[level.value])" readonly>
                        <template #append>%</template>
                      </el-input>
                      <div class="member-price" v-if="calculateRegionMemberPrice(region, level.value) !== null">
                        实际售价：{{ getRegionCurrencySymbol(region) }}{{ calculateRegionMemberPrice(region, level.value) }}
                      </div>
                    </el-form-item>
                  </el-col>
                </el-row>
              </div>
              
              <!-- 满减活动配置 -->
              <h4 style="margin: 20px 0 15px; color: #409EFF;">🎁 满减活动配置</h4>
              <el-form-item label="活动状态">
                <el-tag v-if="formData.regionConfigs[region].discountRule && formData.regionConfigs[region].discountRule.enabled" type="success" size="large">已启用</el-tag>
                <el-tag v-else type="info" size="large">未启用</el-tag>
              </el-form-item>
              
              <template v-if="formData.regionConfigs[region].discountRule && formData.regionConfigs[region].discountRule.enabled">
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="满减条件">
                      <el-input :value="formatToTwoDecimals(formData.regionConfigs[region].discountRule.minAmount)" readonly />
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="减免金额">
                      <el-input :value="formatToTwoDecimals(formData.regionConfigs[region].discountRule.discountAmount)" readonly />
                    </el-form-item>
                  </el-col>
                </el-row>
              </template>
              
              <!-- 运费配置 -->
              <h4 style="margin: 20px 0 15px; color: #409EFF;">🚚 运费配置</h4>
              <el-row :gutter="20" v-if="formData.regionConfigs[region].shipping">
                <el-col :span="12">
                  <el-form-item label="物流方式">
                    <el-input :value="formData.regionConfigs[region].shipping.shippingMethod === 'STANDARD_SHIPPING' ? '标准物流' : '自提'" readonly />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="币种">
                    <!-- 注释掉原有逻辑：显示各区域自己的币种 -->
                    <!-- <el-input :value="formData.regionConfigs[region].shipping.currency" readonly /> -->
                    <!-- 新逻辑：统一显示网站配置的币种代码（USD/CNY等） -->
                    <el-input :value="siteCurrency" readonly />
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-row :gutter="20" v-if="formData.regionConfigs[region].shipping">
                <el-col :span="8">
                  <el-form-item label="首件运费">
                    <el-input :value="formatToTwoDecimals(formData.regionConfigs[region].shipping.shippingPrice)" readonly />
                  </el-form-item>
                </el-col>
                <el-col :span="8">
                  <el-form-item label="续件运费">
                    <el-input :value="formatToTwoDecimals(formData.regionConfigs[region].shipping.additionalPrice)" readonly />
                  </el-form-item>
                </el-col>
                <el-col :span="8">
                  <el-form-item label="参考时效">
                    <el-input :value="formData.regionConfigs[region].shipping.deliveryTime || '-'" readonly />
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-form-item label="承运商" v-if="formData.regionConfigs[region].shipping">
                <el-input 
                  v-if="formData.regionConfigs[region].shipping.carriers && formData.regionConfigs[region].shipping.carriers.length > 0"
                  :value="formData.regionConfigs[region].shipping.carriers.join(', ')"
                  readonly
                />
                <el-input v-else value="无" readonly />
              </el-form-item>
              
              <el-form-item label="发货地址" v-if="formData.regionConfigs[region].shipping">
                <el-input 
                  :value="formData.regionConfigs[region].shipping.shippingAddress || '未设置'" 
                  type="textarea"
                  :rows="3"
                  readonly
                />
              </el-form-item>
              
              <el-form-item label="退货地址" v-if="formData.regionConfigs[region].shipping">
                <el-input 
                  :value="formData.regionConfigs[region].shipping.returnAddress || '未设置'" 
                  type="textarea"
                  :rows="3"
                  readonly
                />
              </el-form-item>
              
              <!-- 库存配置 -->
              <h4 style="margin: 20px 0 15px; color: #409EFF;">📦 库存配置</h4>
              <el-row :gutter="20" v-if="formData.regionConfigs[region].stock">
                <el-col :span="12">
                  <el-form-item label="可售库存">
                    <el-input :value="formatToInteger(formData.regionConfigs[region].stock.availableStock)" readonly />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="库存预警线">
                    <el-input :value="formatToInteger(formData.regionConfigs[region].stock.alertStockLine)" readonly />
                  </el-form-item>
                </el-col>
              </el-row>
            </div>
          </el-tab-pane>
        </el-tabs>
        
        <!-- 是否限量 -->
        <el-form-item label="是否限量">
          <el-tag v-if="formData.isLimited" type="danger" size="large">限量</el-tag>
          <el-tag v-else type="info" size="large">不限量</el-tag>
        </el-form-item>
        
        <!-- 业务类型 -->
        <el-divider content-position="left">业务类型</el-divider>
        
        <el-form-item label="支持业务">
          <el-checkbox v-model="formData.supportDropship">一件代发</el-checkbox>
          <el-checkbox v-model="formData.supportWholesale">批发</el-checkbox>
          <el-checkbox v-model="formData.supportCircleBuy">圈货</el-checkbox>
          <el-checkbox v-model="formData.supportSelfPickup">自提</el-checkbox>
        </el-form-item>
        
        <!-- 商品详情 -->
        <el-divider content-position="left">商品详情</el-divider>
        
        <el-form-item label="" class="full-width-editor" style="width: 100%!important;">
          <div class="rich-content-preview" style="width: 100%; height: 100%;" v-html="formData.richContent"></div>
        </el-form-item>
        
        <!-- 审核信息 -->
        <el-divider content-position="left">审核信息</el-divider>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="商品状态">
              <el-tag :type="getStatusTagType(formData.status)">
                {{ getStatusText(formData.status) }}
              </el-tag>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="审核人">
              <el-input v-model="formData.auditedBy" readonly />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="审核时间">
              <el-input v-model="formData.auditedAt" readonly />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="首次上架时间">
              <el-input v-model="formData.publishDate" readonly />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="审核备注">
          <el-input
            v-model="formData.auditRemark"
            type="textarea"
            :rows="4"
            readonly
          />
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { ref, reactive, onMounted, defineProps, defineExpose, computed } from 'vue'
import {
  ElCard,
  ElForm,
  ElFormItem,
  ElInput,
  ElSelect,
  ElOption,
  ElButton,
  ElRow,
  ElCol,
  ElDivider,
  ElCheckbox,
  ElMessage,
  ElImage,
  ElIcon,
  ElTag,
  ElTabs,
  ElTabPane,
  vLoading
} from 'element-plus'
import { Picture, Loading, Back } from '@element-plus/icons-vue'

export default {
  name: 'ProductView',
  components: {
    ElCard,
    ElForm,
    ElFormItem,
    ElInput,
    ElSelect,
    ElOption,
    ElButton,
    ElRow,
    ElCol,
    ElDivider,
    ElCheckbox,
    ElImage,
    ElIcon,
    ElTag,
    ElTabs,
    ElTabPane,
    Picture,
    Loading,
    Back
  },
  directives: {
    loading: vLoading
  },
  props: {
    adminLoginPath: {
      type: String,
      required: true
    },
    productId: {
      type: [Number, String],
      default: null
    },
    returnTo: {
      type: String,
      default: 'product-list' // 默认返回商品列表
    },
    autoLoad: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    const loading = ref(false)
    
    // 当前活动区域
    const activeRegion = ref('')
    
    // 网站币种和货币符号
    const siteCurrency = ref('USD') // 币种代码（如USD）
    const siteCurrencySymbol = ref('$') // 货币符号（如$）
    
    // 发货区域选项
    const shippingRegionOptions = ref([])
    
    // 分类数据
    const categories = ref([])
    const subcategories = ref([])
    const items = ref([])
    
    // 物流公司数据
    const logisticsCompanies = ref([])
    
    // 所有标签选项
    const allTags = ref([
      '热卖', '新品', '促销', '推荐', '限时特价'
    ])

    // 会员等级信息
    const vipLevels = ref([
      { value: '0', label: '普通用户' },
      { value: '1', label: 'VIP1' },
      { value: '2', label: 'VIP2' },
      { value: '3', label: 'VIP3' },
      { value: '4', label: 'VIP4' },
      { value: '5', label: 'VIP5' }
    ]);

    // 加载会员等级信息
    const loadVipLevels = async () => {
      try {
        const response = await fetch(`/admin${props.adminLoginPath}/product/vip-levels`, {
          method: 'GET',
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          }
        });

        const result = await response.json();

        if (result.success) {
          // 转换数据格式以匹配前端代码
          vipLevels.value = result.data.map(level => ({
            value: level.value.toString(),
            label: level.label
          }));
        }
      } catch (error) {
        console.error('加载会员等级信息失败:', error);
        // 如果加载失败，使用默认值
        vipLevels.value = [
          { value: '0', label: '普通用户' },
          { value: '1', label: 'VIP1' },
          { value: '2', label: 'VIP2' },
          { value: '3', label: 'VIP3' },
          { value: '4', label: 'VIP4' },
          { value: '5', label: 'VIP5' }
        ];
      }
    };

    // 加载物流公司数据
    const loadLogisticsCompanies = async () => {
      try {
        const response = await fetch(`/admin${props.adminLoginPath}/product/logistics-companies`, {
          method: 'GET',
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          }
        });

        const result = await response.json();

        if (result.success) {
          logisticsCompanies.value = result.data || []
        }
      } catch (error) {
        console.error('加载物流公司数据失败:', error);
      }
    };

    // 表单数据
    const formData = reactive({
      id: null,
      sku: '',
      spu: '',
      title: '',
      titleEn: '',
      categoryId: '',
      categoryName: '',
      subcategoryId: '',
      subcategoryName: '',
      itemId: '',
      itemName: '',
      brand: '',
      length: null,
      width: null,
      height: null,
      weight: null,
      packageLength: null,
      packageWidth: null,
      packageHeight: null,
      packageWeight: null,
      tags: [],
      shippingRegions: [],  // 发货区域
      regionConfigs: {},  // 多区域配置
      isLimited: false,
      supportDropship: true,
      supportWholesale: false,
      supportCircleBuy: false,
      supportSelfPickup: false,
      alertStockLine: 10,
      richContent: '',
      status: 'draft',
      auditRemark: '',
      auditedBy: '',
      auditedAt: '',
      publishDate: '',
      // 满减活动
      enableDiscount: false,
      minAmount: null,
      discountAmount: null,
      // 库存信息
      stock: {
        availableStock: 0,
        warehouseCode: 'WH001',
        warehouseName: '默认仓库',
        warehouseAddress: ''
      },
      // 价格信息
      price: {
        currency: 'CNY',
        businessType: 'dropship',
        originalPrice: null,
        sellingPrice: null,
        discountRate: 0,
        memberDiscount: {
          '0': 0, // 普通会员
          '1': 0, // VIP1
          '2': 0, // VIP2
          '3': 0, // VIP3
          '4': 0, // VIP4
          '5': 0  // VIP5
        },
        minWholesaleQuantity: null
      },
      // 物流信息
      shipping: {
        shippingMethod: 'standard',
        currency: 'CNY',
        shippingPrice: '0.00',
        deliveryTime: '3-5天',
        carriers: []
      }
    })

    // 主图数据
    const mainImages = ref([])
    
    // 详情图数据
    const detailImages = ref([])
    
    // 主图URL数组（用于预览）
    const mainImageUrls = computed(() => {
      return mainImages.value.map(image => image.url)
    })
    
    // 详情图URL数组（用于预览）
    const detailImageUrls = computed(() => {
      return detailImages.value.map(image => image.url)
    })

    // 数字格式化函数 - 保留两位小数
    const formatToTwoDecimals = (value) => {
      if (value === null || value === undefined || value === '') return '-'
      const num = parseFloat(value)
      return isNaN(num) ? '-' : num.toFixed(2)
    }

    // 整数格式化函数
    const formatToInteger = (value) => {
      if (value === null || value === undefined || value === '') return '-'
      const num = parseFloat(value)
      return isNaN(num) ? '-' : Math.floor(num)
    }

    // 百分比格式化函数
    const formatToPercentage = (value) => {
      if (value === null || value === undefined || value === '') return '0%'
      const num = parseFloat(value)
      return isNaN(num) ? '0%' : num.toFixed(1) + '%'
    }

    // 加载分类数据
    const loadCategories = async () => {
      try {
        const response = await fetch(`/admin${props.adminLoginPath}/product/categories`, {
          method: 'GET',
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          }
        })

        const result = await response.json()

        if (result.success) {
          categories.value = result.data || []
        }
      } catch (error) {
        console.error('加载分类数据失败:', error)
      }
    }

    // 处理一级分类变化
    const handleCategoryChange = async (categoryId) => {
      formData.subcategoryId = ''
      formData.itemId = ''
      subcategories.value = []
      items.value = []

      if (!categoryId) return

      try {
        const response = await fetch(`/admin${props.adminLoginPath}/product/subcategories/${categoryId}`, {
          method: 'GET',
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          }
        })

        const result = await response.json()

        if (result.success) {
          subcategories.value = result.data || []
        }
      } catch (error) {
        console.error('加载子分类数据失败:', error)
      }
    }

    // 处理二级分类变化
    const handleSubcategoryChange = async (subcategoryId) => {
      formData.itemId = ''
      items.value = []

      if (!subcategoryId) return

      try {
        const response = await fetch(`/admin${props.adminLoginPath}/product/items/${subcategoryId}`, {
          method: 'GET',
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          }
        })

        const result = await response.json()

        if (result.success) {
          items.value = result.data || []
        }
      } catch (error) {
        console.error('加载商品项数据失败:', error)
      }
    }

    // 加载商品详情数据
    const loadProductDetail = async (productId = null) => {
      // 使用传入的productId或props.productId
      const id = productId || props.productId
      
      // 如果没有商品ID，等待一段时间后重试（处理异步设置的情况）
      if (!id) {
        // 等待100ms后重试
        await new Promise(resolve => setTimeout(resolve, 100))
        
        // 再次检查props.productId
        if (!props.productId) {
          ElMessage.error('商品ID缺失')
          loading.value = false
          return
        }
        
        // 使用更新后的productId
        return loadProductDetail(props.productId)
      }

      loading.value = true
      try {
        const response = await fetch(`/admin${props.adminLoginPath}/product/detail/${id}`, {
          method: 'GET',
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          }
        })

        const result = await response.json()

        if (result.success) {
          const product = result.data

          // 更新网站币种和货币符号
          if (result.siteCurrency) {
            siteCurrency.value = result.siteCurrency
          }
          if (result.currencySymbol) {
            siteCurrencySymbol.value = result.currencySymbol
          }

          // 先加载分类数据
          await loadCategories()

          // 填充表单数据
          Object.assign(formData, {
            id: product.id,
            sku: product.sku,
            spu: product.spu,
            title: product.title,
            titleEn: product.titleEn || '',
            categoryId: product.categoryId || '',
            categoryName: product.categoryName || '',
            subcategoryId: product.subcategoryId || '',
            subcategoryName: product.subcategoryName || '',
            itemId: product.itemId || '',
            itemName: product.itemName || '',
            brand: product.brand || '',
            length: product.length,
            width: product.width,
            height: product.height,
            weight: product.weight,
            packageLength: product.packageLength,
            packageWidth: product.packageWidth,
            packageHeight: product.packageHeight,
            packageWeight: product.packageWeight,
            tags: product.tags || [],
            shippingRegions: product.shippingRegions || [],  // 发货区域
            isLimited: product.isLimited || false,
            supportDropship: product.supportDropship,
            supportWholesale: product.supportWholesale,
            supportCircleBuy: product.supportCircleBuy,
            supportSelfPickup: product.supportSelfPickup,
            alertStockLine: product.alertStockLine || 10,
            richContent: product.richContent || '',
            status: product.status,
            auditRemark: product.auditRemark || '',
            auditedBy: product.auditedBy || '',
            auditedAt: product.auditedAt || '',
            publishDate: product.publishDate || '',
            // 满减活动
            enableDiscount: product.enableDiscount || false,
            minAmount: product.minAmount || null,
            discountAmount: product.discountAmount || null
          })

          // 填充库存信息
          if (product.stock) {
            Object.assign(formData.stock, product.stock)
          }

          // 填充价格信息
          if (product.price) {
            formData.price.currency = product.price.currency || 'CNY'
            formData.price.businessType = product.price.businessType || 'dropship'
            formData.price.originalPrice = product.price.originalPrice
            formData.price.sellingPrice = product.price.sellingPrice
            formData.price.discountRate = product.price.discountRate ? product.price.discountRate * 100 : 0
            formData.price.minWholesaleQuantity = product.price.minWholesaleQuantity
            
            // 填充会员折扣
            if (product.price.memberDiscount) {
              Object.keys(formData.price.memberDiscount).forEach(key => {
                formData.price.memberDiscount[key] = product.price.memberDiscount[key] ? product.price.memberDiscount[key] * 100 : 0
              })
            }
          }

          // 填充物流信息
          if (product.shipping) {
            Object.assign(formData.shipping, product.shipping)
          }
          
          // 填充多区域配置
          if (product.regionConfigs) {
            formData.regionConfigs = product.regionConfigs
            // 设置默认活动区域为第一个区域
            if (formData.shippingRegions.length > 0) {
              activeRegion.value = formData.shippingRegions[0]
            }
          }

          // 处理主图数据
          if (product.mainImages && Array.isArray(product.mainImages) && product.mainImages.length > 0) {
            mainImages.value = product.mainImages.map(img => ({
              url: img.url || ''
            }))
          } else if (product.mainImage || product.mainImageKey) {
            // 兼容旧数据格式
            const mainImageUrl = product.mainImage || product.mainImageKey
            mainImages.value = [{
              url: mainImageUrl
            }]
          } else {
            mainImages.value = []
          }
          
          // 处理详情图数据
          if (product.detailImages && Array.isArray(product.detailImages) && product.detailImages.length > 0) {
            detailImages.value = product.detailImages.map(img => ({
              url: img.url || ''
            }))
          } else {
            detailImages.value = []
          }
          
          // 立即隐藏loading，让页面先显示出来
          loading.value = false

          // 如果有一级分类，加载二级分类（异步，不阻塞显示）
          if (formData.categoryId) {
            handleCategoryChange(formData.categoryId)
          }

          // 如果有二级分类，加载三级分类（异步，不阻塞显示）
          if (formData.subcategoryId) {
            handleSubcategoryChange(formData.subcategoryId)
          }
        } else {
          ElMessage.error(result.message || '加载商品详情失败')
          loading.value = false
        }
      } catch (error) {
        console.error('加载商品详情失败:', error)
        ElMessage.error('网络错误，请稍后重试')
        loading.value = false
      }
    }

    // 图片预览处理
    const handleImagePreview = (index) => {
      // Element Plus 的 el-image 组件会自动处理预览功能
      // 这里可以添加额外的处理逻辑（如果需要）
      console.log('预览主图，索引：', index)
    }
    
    // 详情图预览处理
    const handleDetailImagePreview = (index) => {
      // Element Plus 的 el-image 组件会自动处理预览功能
      // 这里可以添加额外的处理逻辑（如果需要）
      console.log('预览详情图，索引：', index)
    }

    // 获取状态标签类型
    const getStatusTagType = (status) => {
      const typeMap = {
        'draft': 'info',
        'pending': 'warning',
        'approved': 'success',
        'rejected': 'danger',
        'offline': ''
      }
      return typeMap[status] || 'info'
    }

    // 获取状态文本
    const getStatusText = (status) => {
      const statusMap = {
        'draft': '草稿',
        'pending': '待审核',
        'approved': '已通过',
        'rejected': '已拒绝',
        'offline': '已下架'
      }
      return statusMap[status] || status
    }

    // 初始化数据加载
    const initData = async () => {
      await loadShippingRegions();
      loadProductDetail();
      loadVipLevels(); // 加载会员等级信息
      loadLogisticsCompanies(); // 加载物流公司信息
    }
    
    // 加载发货区域选项
    const loadShippingRegions = async () => {
      try {
        const response = await fetch(`/admin${props.adminLoginPath}/product/shipping-regions`, {
          method: 'GET',
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          }
        });

        const result = await response.json();

        if (result.success) {
          shippingRegionOptions.value = result.data || [];
        }
      } catch (error) {
        console.error('加载发货区域选项失败:', error);
      }
    }
    
    // 获取区域显示名称
    const getRegionLabel = (regionCode) => {
      const region = shippingRegionOptions.value.find(r => r.value === regionCode)
      return region ? region.label : regionCode
    }
    
    // 获取区域货币符号
    const getRegionCurrencySymbol = (regionCode) => {
      const region = shippingRegionOptions.value.find(r => r.value === regionCode)
      return region ? region.currencySymbol : siteCurrencySymbol.value
    }
    
    // 计算区域会员价格
    const calculateRegionMemberPrice = (regionCode, vipLevel) => {
      if (!formData.regionConfigs || !formData.regionConfigs[regionCode] || !formData.regionConfigs[regionCode].price) {
        return null
      }
      
      const priceConfig = formData.regionConfigs[regionCode].price
      const sellingPrice = parseFloat(priceConfig.sellingPrice)
      
      if (isNaN(sellingPrice)) {
        return null
      }
      
      const memberDiscount = priceConfig.memberDiscount || {}
      const discount = parseFloat(memberDiscount[vipLevel]) || 0
      const validDiscount = Math.max(0, Math.min(90, discount))
      const memberPrice = sellingPrice * (1 - validDiscount / 100)
      
      return memberPrice.toFixed(2)
    }

    // 计算会员价格
    const memberPrices = computed(() => {
      const prices = {}
      const sellingPrice = parseFloat(formData.price.sellingPrice)
      
      if (isNaN(sellingPrice)) {
        // 如果售价无效，所有会员价都设为null
        for (let i = 0; i <= 5; i++) {
          prices[i] = null
        }
        return prices
      }
      
      // 计算每个会员等级的实际售价
      for (let i = 0; i <= 5; i++) {
        const discount = parseFloat(formData.price.memberDiscount[i]) || 0
        // 确保折扣率在0-90范围内
        const validDiscount = Math.max(0, Math.min(90, discount))
        // 计算实际售价：售价 * (1 - 折扣率/100)
        const memberPrice = sellingPrice * (1 - validDiscount / 100)
        prices[i] = memberPrice.toFixed(2)
      }
      
      return prices
    })

    // 组件挂载时
    onMounted(() => {
      if (props.autoLoad) {
        initData()
      }
    })

    // 返回按钮处理
    const goBack = () => {
      // 触发自定义事件，通知父组件关闭当前标签页并返回来源页
      window.dispatchEvent(new CustomEvent('product-view-go-back', {
        detail: { returnTo: props.returnTo }
      }))
    }

    return {
      loading,
      activeRegion,
      siteCurrency,
      siteCurrencySymbol,
      shippingRegionOptions,
      categories,
      subcategories,
      items,
      logisticsCompanies,
      allTags,
      formData,
      mainImages,
      detailImages,
      mainImageUrls,
      detailImageUrls,
      loadCategories,
      handleCategoryChange,
      handleSubcategoryChange,
      loadProductDetail,
      handleImagePreview,
      handleDetailImagePreview,
      getStatusTagType,
      getStatusText,
      initData,
      memberPrices,
      vipLevels,
      formatToTwoDecimals,
      formatToInteger,
      formatToPercentage,
      getRegionLabel,
      getRegionCurrencySymbol,
      calculateRegionMemberPrice,
      goBack,
      Back
    }
  }
}
</script>

<style scoped>
.product-view {
  padding: 20px;
}

.box-card {
  max-width: 1200px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  font-size: 16px;
}

.header-left {
  display: flex;
  align-items: center;
}

.loading-icon {
  margin-left: 10px;
  font-size: 18px;
  color: #409eff;
}

.loading-icon.is-loading {
  animation: rotating 2s linear infinite;
}

@keyframes rotating {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

:deep(.el-form-item__label) {
  font-weight: 500;
}

:deep(.el-divider__text) {
  font-weight: bold;
  color: #303133;
}

.image-preview-list {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.image-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.image-slot {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background: #f5f7fa;
  color: #909399;
}

.member-discount-container {
  width: 100%;
}

/* 富文本编辑器铺满内容区域 */
.full-width-editor {
  width: 100%;
}

.full-width-editor :deep(.el-form-item__content) {
  width: 100% !important;
  margin-left: 0 !important;
}

.member-price {
  font-size: 12px;
  color: #67c23a;
  margin-top: 5px;
  font-weight: bold;
}

.rich-content-preview {
  min-height: 200px;
  padding: 15px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background-color: #fff;
}

.region-config-panel {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.region-config-panel h4 {
  margin: 0 0 15px;
  color: #409EFF;
  font-size: 16px;
  font-weight: 600;
}

:deep(.el-tabs__item) {
  font-weight: 500;
}

:deep(.el-tabs__item.is-active) {
  color: #409EFF;
  font-weight: 600;
}
</style>