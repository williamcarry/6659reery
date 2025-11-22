<template>
  <div class="product-edit" v-loading="loading" element-loading-text="数据加载中..." element-loading-background="rgba(255, 255, 255, 0.9)">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>编辑商品</span>
        </div>
      </template>
      
      <el-form :model="formData" :rules="formRules" ref="formRef" label-width="120px">
        <!-- 基本信息 -->
        <el-divider content-position="left">基本信息</el-divider>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="SKU" prop="sku">
              <el-input v-model="formData.sku" placeholder="自动生成或手动输入" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="SPU" prop="spu">
              <el-input v-model="formData.spu" placeholder="自动生成或手动输入" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="商品名称" prop="title">
          <el-input v-model="formData.title" placeholder="请输入商品名称" />
        </el-form-item>
        
        <el-form-item label="英文名称">
          <el-input v-model="formData.titleEn" placeholder="请输入英文名称" />
          <div class="form-item-tip">如不填写英文名称，网站将默认显示中文名称</div>
        </el-form-item>
        
        <!-- 主图上传 -->
        <el-form-item label="商品主图" prop="mainImage">
          <file-upload
            v-model="formData.mainImage"
            :supplier-login-path="supplierLoginPath"
            endpoint-type="product-main"
            accept="image/*"
            :max-size="5"
            @upload-success="handleMainImageUpload"
          />
         
        </el-form-item>
         <div class="form-item-tip" style="text-align: center;">主图必须是正方形图片（如800x800），最小尺寸600x600，系统会自动生成350x350的缩略图用于列表展示</div>
        <!-- 详情图上传 -->
        <el-form-item label="商品详情图" style="margin-top: 20px;">
          <div class="image-upload-list">
            <div v-for="(image, index) in formData.detailImages" :key="`detail-image-${index}`" class="image-item">
              <file-upload
                :model-value="image.previewUrl || image.key"
                @update:model-value="updateDetailImageKey(index, $event)"
                :supplier-login-path="supplierLoginPath"
                endpoint-type="product"
                accept="image/*"
                :max-size="5"
                class="image-upload-item"
              />
              <div class="image-info">
                <el-checkbox v-model="image.canBeMain">
                  可作为主图
                </el-checkbox>
              </div>
            </div>
            <div v-if="formData.detailImages.length < 10" class="image-item">
              <file-upload
                :key="`new-detail-upload-${newDetailUploadKey}`"
                v-model="newDetailImageKey"
                :supplier-login-path="supplierLoginPath"
                endpoint-type="product"
                accept="image/*"
                :max-size="5"
                class="image-upload-item"
                @upload-success="addNewDetailImage"
              />
            </div>
          </div>
        </el-form-item>
         <div class="form-item-tip" style="text-align: center;">最多可上传10张详情图，最小尺寸600x600，建议尺寸：800x800px，支持JPG、PNG格式，大小不超过5MB。勾选"可作为主图"表示该图片可以替换当前主图</div>
        <!-- 分类信息 -->
        <el-divider content-position="left">分类信息</el-divider>
        
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="一级分类" prop="categoryId" required>
              <el-select v-model="formData.categoryId" placeholder="请选择分类" @change="handleCategoryChange" clearable>
                <el-option
                  v-for="category in categories"
                  :key="category.id"
                  :label="category.name"
                  :value="category.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="二级分类" prop="subcategoryId" required>
              <el-select v-model="formData.subcategoryId" placeholder="请选择子分类" @change="handleSubcategoryChange" clearable :disabled="!formData.categoryId">
                <el-option
                  v-for="subcategory in subcategories"
                  :key="subcategory.id"
                  :label="subcategory.name"
                  :value="subcategory.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="三级分类" prop="itemId" required>
              <el-select v-model="formData.itemId" placeholder="请选择商品项" clearable :disabled="!formData.subcategoryId">
                <el-option
                  v-for="item in items"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <!-- 商品属性 -->
        <el-divider content-position="left">商品属性</el-divider>
        
        <el-form-item label="品牌">
          <el-input v-model="formData.brand" placeholder="请输入品牌" />
        </el-form-item>
        
        <el-row :gutter="20">
          <el-col :span="6">
            <el-form-item label="长度(cm)">
              <el-input v-model.number="formData.length" type="number" placeholder="长度" />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="宽度(cm)">
              <el-input v-model.number="formData.width" type="number" placeholder="宽度" />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="高度(cm)">
              <el-input v-model.number="formData.height" type="number" placeholder="高度" />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="重量(g)">
              <el-input v-model.number="formData.weight" type="number" placeholder="重量" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <!-- 包装信息 -->
        <el-divider content-position="left">包装信息</el-divider>
        
        <el-row :gutter="20">
          <el-col :span="6">
            <el-form-item label="包装长度(cm)">
              <el-input v-model.number="formData.packageLength" type="number" placeholder="包装长度" />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="包装宽度(cm)">
              <el-input v-model.number="formData.packageWidth" type="number" placeholder="包装宽度" />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="包装高度(cm)">
              <el-input v-model.number="formData.packageHeight" type="number" placeholder="包装高度" />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="包装重量(g)">
              <el-input v-model.number="formData.packageWeight" type="number" placeholder="包装重量" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <!-- 商品标签 -->
        <el-form-item label="商品标签">
          <el-select
            v-model="formData.tags"
            multiple
            filterable
            allow-create
            default-first-option
            placeholder="请输入商品标签，可创建新标签"
            style="width: 100%"
          >
            <el-option 
              v-for="tag in productTags" 
              :key="tag" 
              :label="tag" 
              :value="tag" 
            />
          </el-select>
        </el-form-item>
        
        <!-- 是否限量 -->
        <el-form-item label="是否限量">
          <el-select v-model="formData.isLimited" placeholder="请选择是否限量" style="width: 200px">
            <el-option label="不限量" :value="false" />
            <el-option label="限量" :value="true" />
          </el-select>
          <div class="form-item-tip">设置为限量商品后，商品将在前端显示"限量"标识</div>
        </el-form-item>
        
        <!-- 业务类型 -->
        <el-divider content-position="left">业务类型</el-divider>
        
        <el-form-item label="支持业务">
          <el-checkbox v-model="formData.supportDropship">一件代发</el-checkbox>
          <el-checkbox v-model="formData.supportWholesale">批发</el-checkbox>
          <el-checkbox v-model="formData.supportCircleBuy">圈货</el-checkbox>
          <el-checkbox v-model="formData.supportSelfPickup">自提</el-checkbox>
        </el-form-item>
        
        <!-- 发货区域 -->
        <el-form-item label="发货区域" prop="shippingRegions">
          <el-select
            v-model="formData.shippingRegions"
            multiple
            placeholder="请选择发货区域（最多8个）"
            style="width: 100%"
            :multiple-limit="8"
          >
            <el-option
              v-for="region in shippingRegionOptions"
              :key="region.value"
              :label="region.label"
              :value="region.value"
            />
          </el-select>
          <div class="form-item-tip">⚠️ 请选择该商品可以发货的区域，可多选，<strong>最多可选择8个区域</strong></div>
          <el-alert 
            title="重要提示" 
            type="info" 
            :closable="false" 
            show-icon
            style="margin-top: 10px;"
          >
            <template #default>
              <ul style="margin: 0; padding-left: 20px;">
                <li><strong>网站前台展示规则：</strong> 商品的价格、库存等信息将显示<strong>首个发货区域</strong>的数据。例如，选择了“中国”和“美国”，则前台显示“中国”区域的价格和库存。</li>
                <li><strong>区域选择限制：</strong> 最多可选择8个发货区域，超过数量将无法继续添加。</li>
              </ul>
            </template>
          </el-alert>
        </el-form-item>
        
        <!-- 多区域价格设置 -->
        <el-divider content-position="left">多区域价格设置</el-divider>
        <div class="form-item-tip">
          💡 您需要为每个发货区域单独配置价格、折扣、会员折扣、满减和运费信息
        </div>

        <el-tabs v-model="activeRegion" type="border-card" v-if="formData.shippingRegions.length > 0">
          <el-tab-pane v-for="region in formData.shippingRegions" :key="region" :label="getRegionLabel(region)" :name="region">
            <div class="region-config-panel" v-if="formData.regionConfigs[region]">
              <h4>💰 价格配置</h4>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="业务类型">
                    <el-select v-model="formData.regionConfigs[region].price.businessType" placeholder="请选择业务类型">
                      <el-option label="一件代发" value="dropship" />
                      <el-option label="批发" value="wholesale" />
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="原价" required>
                    <el-input 
                      v-model.number="formData.regionConfigs[region].price.originalPrice" 
                      type="number" 
                      step="0.01"
                      placeholder="请输入原价"
                      @input="(val) => formData.regionConfigs[region].price.originalPrice = parseFloat(parseFloat(val).toFixed(2))"
                    >
                      <template #prepend>{{ getRegionCurrencySymbol(region) }}</template>
                    </el-input>
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="折扣率(%)">
                    <el-input 
                      v-model.number="formData.regionConfigs[region].price.discountRate" 
                      type="number" 
                      placeholder="请输入折扣率(0-90)" 
                      min="0" 
                      max="90"
                    >
                      <template #append>%</template>
                    </el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="售价">
                    <el-input 
                      :model-value="calculateSellingPrice(region)" 
                      type="number" 
                      placeholder="根据原价和折扣自动计算" 
                      readonly
                    >
                      <template #prepend>{{ getRegionCurrencySymbol(region) }}</template>
                    </el-input>
                    <div class="form-item-tip">根据原价和折扣率自动计算</div>
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="最小起订量">
                    <el-input 
                      v-model.number="formData.regionConfigs[region].price.minWholesaleQuantity" 
                      type="number" 
                      placeholder="请输入最小起订量" 
                    />
                  </el-form-item>
                </el-col>
              </el-row>

              <h4>👥 会员折扣配置</h4>
              <div class="member-discount-container">
                <el-row :gutter="20">
                  <el-col :span="8" v-for="level in vipLevels" :key="level.value">
                    <el-form-item :label="level.label">
                      <el-input 
                        v-model.number="formData.regionConfigs[region].price.memberDiscount[level.value]" 
                        type="number" 
                        placeholder="0" 
                        min="0" 
                        max="90"
                      >
                        <template #append>%</template>
                      </el-input>
                      <div class="member-price">
                        实际售价：{{ getRegionCurrencySymbol(region) }}{{ calculateMemberPrice(region, level.value) }}
                      </div>
                    </el-form-item>
                  </el-col>
                </el-row>
              </div>
              <div class="form-item-tip">会员折扣范围：0-90%，以售价为基础计算</div>

              <h4>🎁 满减活动配置</h4>
              <el-form-item label="启用满减活动">
                <el-switch v-model="formData.regionConfigs[region].discountRule.enabled" />
                <div class="form-item-tip">开启后可设置满减优惠活动</div>
              </el-form-item>

              <template v-if="formData.regionConfigs[region].discountRule.enabled">
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="满减条件" required>
                      <template #label>
                        <span class="required-label">满减条件</span>
                      </template>
                      <el-input 
                        v-model.number="formData.regionConfigs[region].discountRule.minAmount" 
                        type="number" 
                        step="0.01"
                        placeholder="如：100"
                        @input="(val) => formData.regionConfigs[region].discountRule.minAmount = parseFloat(parseFloat(val).toFixed(2))"
                      >
                        <template #prepend>{{ getRegionCurrencySymbol(region) }}</template>
                      </el-input>
                      <div class="form-item-tip">满足此金额可享受减免优惠</div>
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="减免金额" required>
                      <template #label>
                        <span class="required-label">减免金额</span>
                      </template>
                      <el-input 
                        v-model.number="formData.regionConfigs[region].discountRule.discountAmount" 
                        type="number" 
                        step="0.01"
                        placeholder="如：20"
                        @input="(val) => formData.regionConfigs[region].discountRule.discountAmount = parseFloat(parseFloat(val).toFixed(2))"
                      >
                        <template #prepend>{{ getRegionCurrencySymbol(region) }}</template>
                      </el-input>
                      <div class="form-item-tip">满足条件后可减免的金额</div>
                    </el-form-item>
                  </el-col>
                </el-row>
              </template>

              <h4>🚚 运费配置</h4>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="物流方式">
                    <el-select v-model="formData.regionConfigs[region].shipping.shippingMethod" placeholder="请选择物流方式">
                      <el-option label="标准物流" value="STANDARD_SHIPPING" />
                      <el-option label="自提" value="SELF_PICKUP" />
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="首件运费">
                    <el-input 
                      v-model.number="formData.regionConfigs[region].shipping.shippingPrice" 
                      type="number" 
                      step="0.01"
                      placeholder="请输入首件运费"
                      @input="(val) => formData.regionConfigs[region].shipping.shippingPrice = parseFloat(parseFloat(val).toFixed(2))"
                    >
                      <template #prepend>{{ getRegionCurrencySymbol(region) }}</template>
                    </el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="续件运费">
                    <el-input 
                      v-model.number="formData.regionConfigs[region].shipping.additionalPrice" 
                      type="number" 
                      step="0.01"
                      placeholder="请输入续件运费"
                      @input="(val) => formData.regionConfigs[region].shipping.additionalPrice = parseFloat(parseFloat(val).toFixed(2))"
                    >
                      <template #prepend>{{ getRegionCurrencySymbol(region) }}</template>
                    </el-input>
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="参考时效">
                    <el-input v-model="formData.regionConfigs[region].shipping.deliveryTime" placeholder="如：3-5天" />
                  </el-form-item>
                </el-col>
              </el-row>

              <el-form-item label="承运商">
                <el-select 
                  v-model="formData.regionConfigs[region].shipping.carriers" 
                  multiple 
                  placeholder="请选择承运商" 
                  style="width: 100%;" 
                  filterable
                >
                  <el-option 
                    v-for="company in logisticsCompanies" 
                    :key="company.id" 
                    :label="company.name + ' / ' + company.nameEn" 
                    :value="company.name + ' / ' + company.nameEn" 
                  />
                </el-select>
              </el-form-item>
              
              <!-- 新增：发货地址 -->
              <el-form-item label="发货地址">
                <el-input 
                  v-model="formData.regionConfigs[region].shipping.shippingAddress" 
                  type="textarea" 
                  :rows="3" 
                  placeholder="请输入该区域的发货地址或从地址列表中选择"
                />
                <div style="margin-top: 10px;">
                  <el-button type="primary" @click="loadSupplierAddresses('shipping', region)" size="small">
                    从地址列表中选择发货地址
                  </el-button>
                </div>
                <div class="form-item-tip">该区域商品的发货地址</div>
              </el-form-item>

              <!-- 新增：退货地址 -->
              <el-form-item label="退货地址">
                <el-input 
                  v-model="formData.regionConfigs[region].shipping.returnAddress" 
                  type="textarea" 
                  :rows="3" 
                  placeholder="请输入该区域的退货地址或从地址列表中选择"
                />
                <div style="margin-top: 10px;">
                  <el-button type="primary" @click="loadSupplierAddresses('return', region)" size="small">
                    从地址列表中选择退货地址
                  </el-button>
                </div>
                <div class="form-item-tip">该区域商品的退货地址</div>
              </el-form-item>
              
              <!-- 库存设置 -->
              <h4 style="margin: 20px 0 15px; color: #409EFF;">📦 库存配置</h4>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="可售库存">
                    <el-input 
                      v-model.number="formData.regionConfigs[region].stock.availableStock" 
                      type="number" 
                      placeholder="请输入可售库存数量" 
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="库存预警线">
                    <el-input 
                      v-model.number="formData.regionConfigs[region].stock.alertStockLine" 
                      type="number" 
                      placeholder="当库存低于此值时预警" 
                    />
                    <div class="form-item-tip">当库存低于此值时系统会发送预警通知</div>
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="仓库代码">
                    <el-input 
                      v-model="formData.regionConfigs[region].stock.warehouseCode" 
                      placeholder="请输入仓库代码" 
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="仓库名称">
                    <el-input 
                      v-model="formData.regionConfigs[region].stock.warehouseName" 
                      placeholder="请输入仓库名称" 
                    />
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-form-item label="仓库地址">
                <el-input 
                  v-model="formData.regionConfigs[region].stock.warehouseAddress" 
                  type="textarea" 
                  :rows="2" 
                  placeholder="请输入仓库地址" 
                />
              </el-form-item>
            </div>
          </el-tab-pane>
        </el-tabs>

        <el-alert 
          v-if="formData.shippingRegions.length === 0" 
          title="请先选择发货区域" 
          type="warning" 
          :closable="false" 
          show-icon
        >
          <template #default>
            <p>请在上方「业务类型」区域中选择发货区域，然后配置每个区域的价格信息。</p>
          </template>
        </el-alert>

        <!-- 商品详情 -->
        <el-divider content-position="left">商品详情</el-divider>
        
        <el-form-item label="" class="full-width-editor">
          <rich-text-editor
            v-model="formData.richContent"
            :supplier-login-path="supplierLoginPath"
            placeholder="请输入商品详细内容..."
            height="500px"
          />
        </el-form-item>
        
        <!-- 提交状态 -->
        <el-divider content-position="left">提交状态</el-divider>
        
        <el-form-item label="商品状态" prop="status">
          <!-- 如果是已审核状态，只显示不可编辑 -->
          <template v-if="formData.status === 'approved'">
            <el-tag type="success" size="large">已审核</el-tag>
            <div class="form-item-tip">该商品已通过审核</div>
          </template>
          <!-- 其他状态可以选择 -->
          <template v-else>
            <el-radio-group v-model="formData.status">
              <el-radio label="draft">保存为草稿</el-radio>
              <el-radio label="approved">发布</el-radio>
            </el-radio-group>
            <div class="form-item-tip">草稿状态可以继续编辑，发布后商品将直接上架</div>
          </template>
        </el-form-item>
        
        <!-- 提交按钮 -->
        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">更新</el-button>
          <el-button @click="handleCancel">取消</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 地址选择对话框 -->
      <el-dialog
        v-model="addressDialogVisible"
        :title="addressDialogType === 'shipping' ? '选择发货地址' : '选择退货地址'"
        width="600px"
        @close="handleAddressDialogClose"
      >
        <el-table
          :data="supplierAddresses"
          style="width: 100%"
          max-height="400"
          @row-click="handleAddressSelect"
        >
          <el-table-column prop="address" label="地址" show-overflow-tooltip />
          <el-table-column prop="typeText" label="类型" width="120">
            <template #default="scope">
              <el-tag 
                :type="scope.row && scope.row.type === 'shipping' ? 'success' : 'warning'"
              >
                {{ scope.row ? (scope.row.typeText || scope.row.type) : '' }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="addressDialogVisible = false">取消</el-button>
          </span>
        </template>
      </el-dialog>
    </el-card>
  </div>
</template>

<script>
import { ref, reactive, onMounted, defineProps, defineExpose, watch, computed } from 'vue'
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
  ElRadio,
  ElRadioGroup,
  ElCheckbox,
  ElSwitch,
  ElMessage,
  ElMessageBox,
  ElIcon,
  ElDialog,
  ElTable,
  ElTableColumn,
  ElTag,
  ElTabs,
  ElTabPane,
  ElAlert,
  ElLoading
} from 'element-plus'
import FileUpload from './FileUpload.vue'
import RichTextEditor from './RichTextEditor.vue'

export default {
  name: 'ProductEdit',
  directives: {
    loading: ElLoading.directive
  },
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
    ElRadio,
    ElRadioGroup,
    ElCheckbox,
    ElSwitch,
    ElIcon,
    ElDialog,
    ElTable,
    ElTableColumn,
    ElTag,
    ElTabs,
    ElTabPane,
    ElAlert,
    FileUpload,
    RichTextEditor
  },
  props: {
    supplierLoginPath: {
      type: String,
      required: true
    },
    productId: {
      type: [Number, String, null],
      default: null
    },
    autoLoad: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    const loading = ref(false)
    const submitting = ref(false)
    const formRef = ref(null)
    const activeRegion = ref('') // 当前激活的区域 Tab
    const newDetailImageKey = ref('') // 用于新增详情图的临时key
    const newDetailUploadKey = ref(0) // 用于强制刷新新的详情图上传组件
    // 删除旧的未使用变量
    // const newImageKey = ref('')
    // const newImageAltText = ref('')
    // const isNewImageMain = ref(false)
    // const newUploadKey = ref(0)

    // 分类数据
    const categories = ref([])
    const subcategories = ref([])
    const items = ref([])

    // 物流公司数据
    const logisticsCompanies = ref([])

    // 商品标签数据
    const productTags = ref([])
    
    // 发货区域选项
    const shippingRegionOptions = ref([])

    // 供应商地址数据
    const supplierAddresses = ref([])
    const addressDialogVisible = ref(false)
    const addressDialogType = ref('shipping') // 'shipping' 或 'return'
    const selectedAddress = ref('')
    const currentRegionForAddress = ref('') // 当前选择地址的区域

    // 表单数据
    const formData = reactive({
      id: null,
      sku: '',
      spu: '',
      title: '',
      titleEn: '',
      mainImage: '',  // 主图key
      thumbnailImage: '',  // 缩略图key
      detailImages: [], // 详情图数组 [{key: '', canBeMain: false}]
      categoryId: '',
      subcategoryId: '',
      itemId: '',
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
      isLimited: false,
      supportDropship: true,
      supportWholesale: false,
      supportCircleBuy: false,
      supportSelfPickup: false,
      shippingRegions: [],  // 发货区域
      richContent: '',
      status: 'draft',
      // 多区域配置：价格、满减、运费和库存
      regionConfigs: {} // { 'CN': { price: {...}, discountRule: {...}, shipping: {...}, stock: {...} }, 'US': {...} }
    })

    // 监听发货区域变化，自动初始化/删除配置
    watch(() => formData.shippingRegions, (newRegions, oldRegions) => {
      // 为新增区域初始化配置
      newRegions.forEach(region => {
        if (!formData.regionConfigs[region]) {
          formData.regionConfigs[region] = createRegionConfig(region)
        }
      })
      
      // 删除移除区域的配置
      Object.keys(formData.regionConfigs).forEach(region => {
        if (!newRegions.includes(region)) {
          delete formData.regionConfigs[region]
        }
      })
      
      // 切换激活的Tab
      if (!newRegions.includes(activeRegion.value) && newRegions.length > 0) {
        activeRegion.value = newRegions[0]
      } else if (newRegions.length === 0) {
        activeRegion.value = ''
      }
    }, { deep: true })

    // 创建区域默认配置
    const createRegionConfig = (region) => {
      const currency = getRegionCurrency(region)
      return {
        price: {
          currency: currency,
          businessType: 'dropship',
          originalPrice: null,
          discountRate: 0,
          memberDiscount: { '0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0 },
          minWholesaleQuantity: null
        },
        discountRule: {
          enabled: false,
          minAmount: null,
          discountAmount: null
        },
        shipping: {
          shippingMethod: 'STANDARD_SHIPPING',
          currency: currency,
          shippingPrice: 0,
          additionalPrice: 0,
          deliveryTime: '3-5天',
          carriers: [],
          shippingAddress: '',  // 新增：发货地址
          returnAddress: ''     // 新增：退货地址
        },
        stock: {  // 新增：库存配置
          availableStock: 0,           // 可售库存
          alertStockLine: 10,          // 库存预警线
          warehouseCode: '',           // 仓库代码
          warehouseName: '',           // 仓库名称
          warehouseAddress: ''         // 仓库地址
        }
      }
    }

    // 从枚举类获取区域信息
    let regionOptions = []

    const loadRegionOptions = async () => {
      try {
        const response = await fetch(`/supplier${props.supplierLoginPath}/product/shipping-regions`, {
          method: 'GET',
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          }
        })
        const result = await response.json()
        if (result.success) {
          regionOptions = result.data
        } else {
          // 如果后端返回错误（例如数据库中没有发货区域配置）
          ElMessage.error(result.message || '加载发货区域失败')
          regionOptions = []
        }
      } catch (error) {
        console.error('加载区域选项失败:', error)
        ElMessage.error('加载发货区域失败，请刷新页面重试')
        regionOptions = []
      }
    }

    // 处理主图上传成功
    const handleMainImageUpload = (response) => {
      console.log('[ProductEdit] 主图上传成功:', response)
      if (response && response.success) {
        formData.mainImage = response.mainImageKey
        formData.thumbnailImage = response.thumbnailKey
      } else {
        if (response && response.message && response.message.includes('正方形')) {
          ElMessage.error('主图必须是正方形图片，请重新选择!')
        } else {
          ElMessage.error(response.message || '主图上传失败')
        }
      }
    }

    // 更新详情图key
    const updateDetailImageKey = (index, newKey) => {
      console.log(`[ProductEdit] 更新详情图[${index}] key:`, newKey);
      if (formData.detailImages[index]) {
        formData.detailImages[index].key = newKey;
      }
    }

    // 添加新详情图
    const addNewDetailImage = (response) => {
      console.log('[ProductEdit] addNewDetailImage called with response:', response);
      
      if (!response || !response.success) {
        console.error('[ProductEdit] 详情图上传失败:', response)
        return
      }
      
      if (formData.detailImages.length >= 10) {
        ElMessage.warning('最多只能上传10张详情图')
        return
      }
      
      const newImage = {
        key: response.key,
        previewUrl: response.previewUrl || response.url || '',
        canBeMain: false
      }
      
      formData.detailImages.push(newImage)
      newDetailImageKey.value = ''
      newDetailUploadKey.value++
    }

    // 获取区域对应的币种
    const getRegionCurrency = (region) => {
      // 先从 regionOptions 查找
      if (regionOptions.length > 0) {
        const option = regionOptions.find(r => r.value === region)
        if (option) {
          return option.currency
        }
      }
      
      // 如果 regionOptions 中没有，尝试从商品的 regionConfigs 中获取
      if (formData.regionConfigs[region] && formData.regionConfigs[region].price) {
        return formData.regionConfigs[region].price.currency || 'CNY'
      }
      
      // 都找不到时，返回默认值
      return 'CNY'
    }

    // 获取区域对应的币种符号
    const getRegionCurrencySymbol = (region) => {
      // 先从 regionOptions 查找
      if (regionOptions.length > 0) {
        const option = regionOptions.find(r => r.value === region)
        if (option) {
          return option.currencySymbol
        }
      }
      
      // 如果 regionOptions 中没有，尝试从商品的 regionConfigs 中获取
      if (formData.regionConfigs[region] && formData.regionConfigs[region].price) {
        // 如果商品配置中有 currencySymbol，使用它
        if (formData.regionConfigs[region].price.currencySymbol) {
          return formData.regionConfigs[region].price.currencySymbol
        }
      }
      
      // 都找不到时，返回默认值
      return '¥'
    }

    // 获取区域显示标签
    const getRegionLabel = (region) => {
      // 先从 regionOptions 查找
      if (regionOptions.length > 0) {
        const option = regionOptions.find(r => r.value === region)
        if (option) {
          return option.label
        }
      }
      
      // 如果找不到，直接返回 region code（已禁用或删除的区域）
      return region
    }

    // 计算指定区域的售价
    const calculateSellingPrice = (region) => {
      const config = formData.regionConfigs[region]
      if (!config || !config.price.originalPrice) return 0
      
      const originalPrice = parseFloat(config.price.originalPrice)
      const discountRate = parseFloat(config.price.discountRate) || 0
      const validDiscountRate = Math.max(0, Math.min(90, discountRate))
      
      return (originalPrice * (1 - validDiscountRate / 100)).toFixed(2)
    }

    // 计算指定区域的会员价格
    const calculateMemberPrice = (region, vipLevel) => {
      const config = formData.regionConfigs[region]
      if (!config) {
        return null
      }
      
      const sellingPrice = parseFloat(calculateSellingPrice(region))
      if (isNaN(sellingPrice) || sellingPrice === 0) {
        return null
      }
      
      // 获取会员折扣率（单位：%）
      const memberDiscountValue = config.price.memberDiscount[vipLevel]
      // 如果会员折扣为空、null、undefined或空字符串，不显示会员价格
      if (memberDiscountValue === null || memberDiscountValue === undefined || memberDiscountValue === '' || memberDiscountValue === 0) {
        return null
      }
      
      const memberDiscount = parseFloat(memberDiscountValue)
      if (isNaN(memberDiscount)) {
        return null
      }
      
      const validMemberDiscount = Math.max(0, Math.min(90, memberDiscount))
      
      // 正确计算：会员价格 = 售价 - (售价 × 会员折扣率)
      const memberPrice = sellingPrice - (sellingPrice * validMemberDiscount / 100)
      
      return memberPrice.toFixed(2)
    }

    // 添加数字格式化函数
    const formatToTwoDecimals = (value) => {
      if (value === null || value === undefined || value === '') return null
      const num = parseFloat(value)
      return isNaN(num) ? null : num.toFixed(2)
    }

    // 添加数字输入验证函数
    const validateTwoDecimals = (rule, value, callback) => {
      if (value === null || value === undefined || value === '') {
        callback()
        return
      }
      
      const num = parseFloat(value)
      if (isNaN(num)) {
        callback(new Error('请输入有效的数字'))
        return
      }
      
      // 检查小数位数
      const strValue = value.toString()
      if (strValue.includes('.')) {
        const decimalPart = strValue.split('.')[1]
        if (decimalPart.length > 2) {
          callback(new Error('最多只能输入两位小数'))
          return
        }
      }
      
      callback()
    }

    // 添加原价验证函数（必须大于0）
    const validateOriginalPrice = (rule, value, callback) => {
      if (value === null || value === undefined || value === '') {
        callback(new Error('请输入商品原价'))
        return
      }
      
      const num = parseFloat(value)
      if (isNaN(num)) {
        callback(new Error('请输入有效的数字'))
        return
      }
      
      // 原价必须大于0
      if (num <= 0) {
        callback(new Error('商品原价必须大于零'))
        return
      }
      
      // 检查小数位数
      const strValue = value.toString()
      if (strValue.includes('.')) {
        const decimalPart = strValue.split('.')[1]
        if (decimalPart.length > 2) {
          callback(new Error('最多只能输入两位小数'))
          return
        }
      }
      
      callback()
    }

    // 表单验证规则
    const formRules = {
      title: [
        { required: true, message: '请输入商品名称', trigger: 'blur' }
      ],
      status: [
        { required: true, message: '请选择商品状态', trigger: 'change' }
      ],
      // 添加分类验证规则
      categoryId: [
        { required: true, message: '请选择一级分类', trigger: 'change' }
      ],
      subcategoryId: [
        { required: true, message: '请选择二级分类', trigger: 'change' }
      ],
      itemId: [
        { required: true, message: '请选择三级分类', trigger: 'change' }
      ],
      // 添加主图验证规则
      mainImage: [
        { 
          validator: (rule, value, callback) => {
            if (!value || value.trim() === '') {
              callback(new Error('请上传商品主图'))
            } else {
              callback()
            }
          }, 
          trigger: 'change' 
        }
      ],
      // 添加发货区域验证规则
      shippingRegions: [
        {
          type: 'array',
          required: true,
          message: '请至少选择一个发货区域',
          trigger: 'change',
          validator: (rule, value, callback) => {
            if (!value || value.length === 0) {
              callback(new Error('请至少选择一个发货区域'))
            } else {
              callback()
            }
          }
        }
      ],
      // 商品属性验证规则
      'length': [
        { validator: validateTwoDecimals, trigger: 'blur' }
      ],
      'width': [
        { validator: validateTwoDecimals, trigger: 'blur' }
      ],
      'height': [
        { validator: validateTwoDecimals, trigger: 'blur' }
      ],
      'weight': [
        { validator: validateTwoDecimals, trigger: 'blur' }
      ],
      // 包装信息验证规则
      'packageLength': [
        { validator: validateTwoDecimals, trigger: 'blur' }
      ],
      'packageWidth': [
        { validator: validateTwoDecimals, trigger: 'blur' }
      ],
      'packageHeight': [
        { validator: validateTwoDecimals, trigger: 'blur' }
      ],
      'packageWeight': [
        { validator: validateTwoDecimals, trigger: 'blur' }
      ],
      // 库存信息验证规则
      'stock.availableStock': [
        { validator: validateNonNegativeInteger, trigger: 'blur' }
      ],
      'alertStockLine': [
        { validator: validateNonNegativeInteger, trigger: 'blur' }
      ]
    }

    // 为会员折扣动态添加验证规则
    const addMemberDiscountValidationRules = () => {
      // 为每个会员等级添加验证规则
      for (let i = 0; i <= 5; i++) {
        formRules[`price.memberDiscount.${i}`] = [
          { validator: validateOneDecimal, trigger: 'blur' }
        ];
      }
    };

    // 添加一位小数验证函数（用于会员折扣，可以大于等于0）
    const validateOneDecimal = (rule, value, callback) => {
      if (value === null || value === undefined || value === '') {
        callback();
        return;
      }
      
      const num = parseFloat(value);
      if (isNaN(num)) {
        callback(new Error('请输入有效的数字'));
        return;
      }
      
      // 折扣可以大于等于0
      if (num < 0) {
        callback(new Error('折扣率不能为负数'));
        return;
      }
      
      // 检查小数位数
      const strValue = value.toString();
      if (strValue.includes('.')) {
        const decimalPart = strValue.split('.')[1];
        if (decimalPart.length > 1) {
          callback(new Error('最多只能输入一位小数'));
          return;
        }
      }
      
      // 检查范围是否在0-90之间
      if (num > 90) {
        callback(new Error('折扣率不能超过90'));
        return;
      }
      
      callback();
    };

    // 添加正整数（包括零）验证函数
    const validateNonNegativeInteger = (rule, value, callback) => {
      if (value === null || value === undefined || value === '') {
        callback()
        return
      }
      
      const num = parseFloat(value)
      if (isNaN(num)) {
        callback(new Error('请输入有效的数字'))
        return
      }
      
      // 检查是否为非负整数
      if (num < 0 || !Number.isInteger(num)) {
        callback(new Error('请输入非负整数'))
        return
      }
      
      callback()
    }

    // 所有与价格和库存相关的watch已移除，因为它们现在在regionConfigs中管理

    // 加载分类数据
    const loadCategories = async () => {
      try {
        const response = await fetch(`/supplier${props.supplierLoginPath}/product/categories`, {
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
      }
    }

    // 处理一级分类变化
    const handleCategoryChange = async (categoryId) => {
      formData.subcategoryId = ''
      formData.itemId = ''
      subcategories.value = []
      items.value = []

      if (!categoryId) return

      await loadSubcategoriesForCategory(categoryId)
    }

    // 处理二级分类变化
    const handleSubcategoryChange = async (subcategoryId) => {
      formData.itemId = ''
      items.value = []

      if (!subcategoryId) return

      await loadItemsForSubcategory(subcategoryId)
    }

    // 为指定分类加载子分类（不重置表单数据）
    const loadSubcategoriesForCategory = async (categoryId) => {
      try {
        const response = await fetch(`/supplier${props.supplierLoginPath}/product/subcategories/${categoryId}`, {
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
  
      }
    }

    // 为指定子分类加载商品项（不重置表单数据）
    const loadItemsForSubcategory = async (subcategoryId) => {
      try {
        const response = await fetch(`/supplier${props.supplierLoginPath}/product/items/${subcategoryId}`, {
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

      }
    }

    // 删除旧的主图相关代码
    // const mainImages = ref([{ url: '' }]);

    // 重置表单数据
    const resetFormData = () => {
      // 清空所有表单字段
      Object.assign(formData, {
        id: null,
        sku: '',
        spu: '',
        title: '',
        titleEn: '',
        mainImage: '',
        thumbnailImage: '',
        detailImages: [],
        categoryId: '',
        subcategoryId: '',
        itemId: '',
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
        isLimited: false,
        supportDropship: true,
        supportWholesale: false,
        supportCircleBuy: false,
        supportSelfPickup: false,
        shippingRegions: [],
        richContent: '',
        status: 'draft',
        regionConfigs: {}
      })
      
      // 清空分类数据
      subcategories.value = []
      items.value = []
      
      // 重置激活的区域
      activeRegion.value = ''
      
      // 重置表单验证状态
      if (formRef.value) {
        formRef.value.clearValidate()
      }
    }

    // 加载商品详情数据
    const loadProductDetail = async () => {
      if (!props.productId) {
        ElMessage.error('商品ID缺失')
        return
      }

      // 先重置表单数据，清空之前商品的信息
      resetFormData()
      
      // 立即设置loading状态
      loading.value = true
      console.log('[商品编辑] 开始加载，loading =', loading.value)
      
      try {
        const response = await fetch(`/supplier${props.supplierLoginPath}/product/detail/${props.productId}`, {
          method: 'GET',
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          }
        })

        const result = await response.json()

        if (result.success) {
          const product = result.data
          
          console.log('[商品编辑] 后端返回的商品数据:', product)
          console.log('[商品编辑] mainImage:', product.mainImage)
          console.log('[商品编辑] thumbnailImage:', product.thumbnailImage)
          console.log('[商品编辑] detailImages:', product.detailImages)

          // 先加载分类数据
          await loadCategories()

          // 填充表单数据
          Object.assign(formData, {
            id: product.id,
            sku: product.sku,
            spu: product.spu,
            title: product.title,
            titleEn: product.titleEn || '',
            mainImage: product.mainImageUrl || product.mainImage || '',
            thumbnailImage: product.thumbnailImage || '',
            detailImages: Array.isArray(product.detailImages) 
              ? product.detailImages.map(img => ({
                  key: img.key || '',
                  previewUrl: img.url || '',
                  canBeMain: img.canBeMain || false
                }))
              : [],
            categoryId: product.categoryId || '',
            subcategoryId: product.subcategoryId || '',
            itemId: product.itemId || '',
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
            isLimited: product.isLimited || false,
            supportDropship: product.supportDropship,
            supportWholesale: product.supportWholesale,
            supportCircleBuy: product.supportCircleBuy,
            supportSelfPickup: product.supportSelfPickup,
            shippingRegions: product.shippingRegions || [],
            richContent: product.richContent || '',
            status: product.status
          })

          // 填充库存信息
          if (product.stock) {
            Object.assign(formData.stock, product.stock)
          }

          // 填充多区域配置（后端返回的regionConfigs已经转换为百分比格式）
          if (product.regionConfigs && typeof product.regionConfigs === 'object') {
            // 不要直接赋值，而是逐个区域填充，保持响应性
            Object.keys(product.regionConfigs).forEach(regionCode => {
              const backendConfig = product.regionConfigs[regionCode]
              
              // 先创建默认配置，确保所有字段都存在
              if (!formData.regionConfigs[regionCode]) {
                formData.regionConfigs[regionCode] = createRegionConfig(regionCode)
              }
              
              const config = formData.regionConfigs[regionCode]
              
              // 填充价格数据
              if (backendConfig.price) {
                config.price.currency = backendConfig.price.currency || config.price.currency
                config.price.businessType = backendConfig.price.businessType || config.price.businessType
                config.price.originalPrice = backendConfig.price.originalPrice || null
                config.price.discountRate = backendConfig.price.discountRate || 0
                // 会员折扣
                if (backendConfig.price.memberDiscount) {
                  Object.assign(config.price.memberDiscount, backendConfig.price.memberDiscount)
                }
                config.price.minWholesaleQuantity = backendConfig.price.minWholesaleQuantity || null
              }
              
              // 填充满减规则
              if (backendConfig.discountRule) {
                config.discountRule.enabled = backendConfig.discountRule.enabled || false
                config.discountRule.minAmount = backendConfig.discountRule.minAmount || null
                config.discountRule.discountAmount = backendConfig.discountRule.discountAmount || null
              }
              
              // 填充运费数据
              if (backendConfig.shipping) {
                // 转换旧的物流方式值为新的常量格式
                let shippingMethod = backendConfig.shipping.shippingMethod || config.shipping.shippingMethod
                // 将旧值转换为新值
                if (shippingMethod === 'Standard Shipping' || shippingMethod === 'standard') {
                  shippingMethod = 'STANDARD_SHIPPING'
                } else if (shippingMethod === 'Self-Pick up' || shippingMethod === 'self-pickup' || shippingMethod === 'Self Pick up') {
                  shippingMethod = 'SELF_PICKUP'
                }
                config.shipping.shippingMethod = shippingMethod
                config.shipping.shippingPrice = backendConfig.shipping.shippingPrice || 0
                config.shipping.additionalPrice = backendConfig.shipping.additionalPrice || 0
                config.shipping.currency = backendConfig.shipping.currency || config.shipping.currency
                config.shipping.deliveryTime = backendConfig.shipping.deliveryTime || config.shipping.deliveryTime
                config.shipping.carriers = backendConfig.shipping.carriers || []
                config.shipping.shippingAddress = backendConfig.shipping.shippingAddress || ''
                config.shipping.returnAddress = backendConfig.shipping.returnAddress || ''
              }
              
              // 填充库存数据
              if (backendConfig.stock) {
                config.stock.availableStock = backendConfig.stock.availableStock || 0
                config.stock.alertStockLine = backendConfig.stock.alertStockLine || 10
                config.stock.warehouseCode = backendConfig.stock.warehouseCode || ''
                config.stock.warehouseName = backendConfig.stock.warehouseName || ''
                config.stock.warehouseAddress = backendConfig.stock.warehouseAddress || ''
              }
            })
          }
          
          console.log('[商品编辑] 填充后的 formData.regionConfigs:', formData.regionConfigs)
          
          // 将商品已配置的区域合并到发货区域选项中
          // 这样即使某些区域在数据库中已被禁用或删除，也能正常编辑
          if (formData.shippingRegions && formData.shippingRegions.length > 0) {
            formData.shippingRegions.forEach(regionCode => {
              // 检查这个区域是否已经在 shippingRegionOptions 中
              const exists = shippingRegionOptions.value.some(opt => opt.value === regionCode)
              if (!exists) {
                // 如果不存在，从 regionConfigs 中提取信息并添加
                const config = formData.regionConfigs[regionCode]
                if (config) {
                  // 从后端数据中获取 currencySymbol，如果没有则使用默认值
                  const currencySymbol = config.price.currencySymbol || '¥'
                  
                  shippingRegionOptions.value.push({
                    value: regionCode,
                    label: regionCode, // 使用 code 作为 label，因为已经被禁用/删除
                    labelEn: regionCode,
                    currency: config.price.currency || 'CNY',
                    currencySymbol: currencySymbol
                  })
                  
                  // 同时检查并添加到 regionOptions，避免重复
                  const existsInRegionOptions = regionOptions.some(opt => opt.value === regionCode)
                  if (!existsInRegionOptions) {
                    regionOptions.push({
                      value: regionCode,
                      label: regionCode,
                      labelEn: regionCode,
                      currency: config.price.currency || 'CNY',
                      currencySymbol: currencySymbol
                    })
                  }
                }
              }
            })
          }
          
          // 设置默认激活的Tab
          if (formData.shippingRegions.length > 0) {
            activeRegion.value = formData.shippingRegions[0]
          }

          // 删除旧的主图数据处理代码
          // 不再需要处理 mainImages 数组
          
          // 立即隐藏loading，让表单先显示出来
          loading.value = false
          console.log('[商品编辑] 文字数据加载完成，立即显示表单，loading =', loading.value)

          // 如果有一级分类，加载二级分类（异步，不阻塞显示）
          if (formData.categoryId) {
            loadSubcategoriesForCategory(formData.categoryId)
          }

          // 如果有二级分类，加载三级分类（异步，不阻塞显示）
          if (formData.subcategoryId) {
            loadItemsForSubcategory(formData.subcategoryId)
          }
        } else {
          ElMessage.error(result.message || '加载商品详情失败')
          loading.value = false
        }
      } catch (error) {
        console.error('加载商品详情失败:', error)
        ElMessage.error('网络错误，请检查网络连接或稍后重试')
        loading.value = false
      }
    };

    // 提交表单 - 更新商品
    const handleSubmit = async () => {
      if (!formRef.value) return

      await formRef.value.validate(async (valid) => {
        if (!valid) {
          ElMessage.error('请完善表单信息')
          return
        }

        try {
          submitting.value = true;

          // 验证主图必须上传
          if (!formData.mainImage || formData.mainImage.trim() === '') {
            ElMessage.error('请上传商品主图')
            submitting.value = false
            return
          }

          // 验证必须选择至少一个发货区域
          if (!formData.shippingRegions || formData.shippingRegions.length === 0) {
            ElMessage.error('请至少选择一个发货区域')
            submitting.value = false
            return
          }

          // 验证每个区域都配置了价格
          for (const region of formData.shippingRegions) {
            const config = formData.regionConfigs[region]
            if (!config || !config.price.originalPrice) {
              ElMessage.error(`请配置${getRegionLabel(region)}的价格信息`)
              submitting.value = false
              return
            }
          }
          
          // 验证每个区域都配置了发货地址和退货地址
          for (const region of formData.shippingRegions) {
            const config = formData.regionConfigs[region]
            if (!config || !config.shipping.shippingAddress || config.shipping.shippingAddress.trim() === '') {
              ElMessage.error(`请配置${getRegionLabel(region)}的发货地址`)
              submitting.value = false
              return
            }
            if (!config || !config.shipping.returnAddress || config.shipping.returnAddress.trim() === '') {
              ElMessage.error(`请配置${getRegionLabel(region)}的退货地址`)
              submitting.value = false
              return
            }
          }
          
          // 验证满减配置：如果开启满减，必须填写满减条件和减免金额
          for (const region of formData.shippingRegions) {
            const config = formData.regionConfigs[region]
            if (config && config.discountRule.enabled) {
              if (!config.discountRule.minAmount || config.discountRule.minAmount <= 0) {
                ElMessage.error(`请配置${getRegionLabel(region)}的满减条件金额`)
                submitting.value = false
                return
              }
              if (!config.discountRule.discountAmount || config.discountRule.discountAmount <= 0) {
                ElMessage.error(`请配置${getRegionLabel(region)}的减免金额`)
                submitting.value = false
                return
              }
            }
          }

          // 构造提交数据，过滤掉detailImages中的previewUrl字段
          const submitData = {
            ...formData,
            // 只提交key和canBeMain，不提交previewUrl
            detailImages: formData.detailImages.map(img => ({
              key: img.key,
              canBeMain: img.canBeMain
            }))
          }

          // 转换 regionConfigs → prices/discountRules/shippings
          const prices = {}
          const discountRules = {}
          const shippings = {}

          formData.shippingRegions.forEach(region => {
            const config = formData.regionConfigs[region]
            if (!config) return

            // 计算售价：售价 = 原价 × (1 - 折扣率/100)
            const originalPrice = parseFloat(config.price.originalPrice) || 0
            const discountRate = parseFloat(config.price.discountRate) || 0
            const sellingPrice = originalPrice * (1 - discountRate / 100)

            // 价格数据（百分比转小数）
            prices[region] = {
              currency: config.price.currency,
              businessType: config.price.businessType,
              originalPrice: config.price.originalPrice,
              sellingPrice: sellingPrice.toFixed(2),  // 添加售价字段
              discountRate: (config.price.discountRate || 0) / 100,  // 10 → 0.10
              memberDiscount: {
                '0': (config.price.memberDiscount['0'] || 0) / 100,
                '1': (config.price.memberDiscount['1'] || 0) / 100,
                '2': (config.price.memberDiscount['2'] || 0) / 100,
                '3': (config.price.memberDiscount['3'] || 0) / 100,
                '4': (config.price.memberDiscount['4'] || 0) / 100,
                '5': (config.price.memberDiscount['5'] || 0) / 100
              },
              minWholesaleQuantity: config.price.minWholesaleQuantity
            }

            // 满减规则（仅当启用时）
            if (config.discountRule.enabled && config.discountRule.minAmount) {
              discountRules[region] = {
                minAmount: config.discountRule.minAmount,
                discountAmount: config.discountRule.discountAmount
              }
            }

            // 运费数据（包括地址和库存信息）
            shippings[region] = {
              shippingMethod: config.shipping.shippingMethod,
              shippingPrice: config.shipping.shippingPrice,
              additionalPrice: config.shipping.additionalPrice || 0,
              currency: config.shipping.currency,
              deliveryTime: config.shipping.deliveryTime,
              carriers: config.shipping.carriers,
              shippingAddress: config.shipping.shippingAddress || null,
              returnAddress: config.shipping.returnAddress || null,
              // 库存信息（新增）
              availableStock: config.stock.availableStock || 0,
              alertStockLine: config.stock.alertStockLine || 10,
              warehouseCode: config.stock.warehouseCode || '',
              warehouseName: config.stock.warehouseName || '',
              warehouseAddress: config.stock.warehouseAddress || ''
            }
          })

          // 添加转换后的数据
          submitData.prices = prices
          submitData.discountRules = discountRules
          submitData.shippings = shippings

          // 删除旧的regionConfigs字段（后端不需要）
          delete submitData.regionConfigs

          // 处理主图：如果主图包含http或https，提取其中的key
          if (submitData.mainImage && (submitData.mainImage.startsWith('http://') || submitData.mainImage.startsWith('https://'))) {
            try {
              const url = new URL(submitData.mainImage);
              submitData.mainImage = url.pathname.substring(1); // 去掉开头的斜杠
              // 如果URL中有查询参数，也需要去掉
              const queryIndex = submitData.mainImage.indexOf('?');
              if (queryIndex > 0) {
                submitData.mainImage = submitData.mainImage.substring(0, queryIndex);
              }
            } catch (e) {
              console.error('解析主图URL失败:', e);
            }
          }

          // 处理缩略图：如果缩略图包含http或https，提取其中的key
          if (submitData.thumbnailImage && (submitData.thumbnailImage.startsWith('http://') || submitData.thumbnailImage.startsWith('https://'))) {
            try {
              const url = new URL(submitData.thumbnailImage);
              submitData.thumbnailImage = url.pathname.substring(1); // 去掉开头的斜杠
              // 如果URL中有查询参数，也需要去掉
              const queryIndex = submitData.thumbnailImage.indexOf('?');
              if (queryIndex > 0) {
                submitData.thumbnailImage = submitData.thumbnailImage.substring(0, queryIndex);
              }
            } catch (e) {
              console.error('解析缩略图URL失败:', e);
            }
          }

          // 处理详情图：如果详情图key包含http或https，提取其中的key
          if (Array.isArray(submitData.detailImages)) {
            submitData.detailImages = submitData.detailImages.map(img => {
              if (img.key && (img.key.startsWith('http://') || img.key.startsWith('https://'))) {
                try {
                  const url = new URL(img.key);
                  img.key = url.pathname.substring(1); // 去掉开头的斜杠
                  // 如果URL中有查询参数，也需要去掉
                  const queryIndex = img.key.indexOf('?');
                  if (queryIndex > 0) {
                    img.key = img.key.substring(0, queryIndex);
                  }
                } catch (e) {
                  console.error('解析详情图URL失败:', e);
                }
              }
              return img;
            });
          }

          const response = await fetch(`/supplier${props.supplierLoginPath}/product/update/${formData.id}`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify(submitData)
          })

          const result = await response.json()

          if (result.success) {
            ElMessage.success('商品更新成功')
            
            // 先关闭当前编辑商品标签页
            window.dispatchEvent(new CustomEvent('close-current-tab'))
            // 然后触发导航事件返回商品列表
            setTimeout(() => {
              window.dispatchEvent(new CustomEvent('navigate-to', {
                detail: { key: 'product-list' }
              }))
            }, 100)
          } else {
            ElMessage.error(result.message || '更新失败')
          }
        } catch (error) {
          console.error('更新失败:', error)
          ElMessage.error('网络错误，请稍后重试')
        } finally {
          submitting.value = false
        }
      })
    }

    // 取消编辑
    const handleCancel = () => {
      ElMessageBox.confirm('确定要取消编辑吗？未保存的数据将丢失。', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '继续编辑',
        type: 'warning'
      }).then(() => {
        // 先关闭当前编辑商品标签页
        window.dispatchEvent(new CustomEvent('close-current-tab'))
        // 然后触发导航事件返回商品列表
        setTimeout(() => {
          window.dispatchEvent(new CustomEvent('navigate-to', {
            detail: { key: 'product-list' }
          }))
        }, 100)
      })
    }

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
        const response = await fetch(`/supplier${props.supplierLoginPath}/product/vip-levels`, {
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
        const response = await fetch(`/supplier${props.supplierLoginPath}/product/logistics-companies`, {
          method: 'GET',
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          }
        })

        const result = await response.json()

        if (result.success) {
          logisticsCompanies.value = result.data || []
        }
      } catch (error) {
        console.error('加载物流公司数据失败:', error)
      }
    }

    // 加载商品标签数据
    const loadProductTags = async () => {
      try {
        const response = await fetch(`/supplier${props.supplierLoginPath}/product/tags`, {
          method: 'GET',
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          }
        })

        const result = await response.json()

        if (result.success) {
          productTags.value = result.data || []
        }
      } catch (error) {
        console.error('加载商品标签数据失败:', error)
      }
    }
    
    // 加载发货区域选项
    const loadShippingRegions = async () => {
      try {
        const response = await fetch(`/supplier${props.supplierLoginPath}/product/shipping-regions`, {
          method: 'GET',
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          }
        })

        const result = await response.json()

        if (result.success) {
          shippingRegionOptions.value = result.data || []
          // 同时更新 regionOptions，供其他方法使用
          regionOptions = result.data || []
        } else {
          // 如果后端返回错误（例如数据库中没有发货区域配置）
          ElMessage.error(result.message || '加载发货区域失败')
          shippingRegionOptions.value = []
          regionOptions = []
        }
      } catch (error) {
        console.error('加载发货区域数据失败:', error)
        ElMessage.error('加载发货区域失败，请刷新页面重试')
        shippingRegionOptions.value = []
        regionOptions = []
      }
    }

    // 加载供应商地址（根据类型和区域过滤）
    const loadSupplierAddresses = async (type, region) => {
      try {
        addressDialogType.value = type;
        currentRegionForAddress.value = region; // 保存当前区域
        addressDialogVisible.value = true;
        
        // 调用新接口，根据类型和区域过滤
        const params = new URLSearchParams({
          type: type,
          region: region
        });
        
        const response = await fetch(`/supplier${props.supplierLoginPath}/address/options?${params}`, {
          method: 'GET',
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          }
        });

        const result = await response.json();

        if (result.success) {
          // 将返回的地址选项格式转换为表格需要的格式
          supplierAddresses.value = result.data.map(addr => ({
            id: addr.value,
            address: addr.label,
            type: addr.type,
            typeText: addr.type === 'shipping' ? '发货地址' : '退货地址',
            region: addr.region
          }));
          
          if (supplierAddresses.value.length === 0) {
            ElMessage.warning(`暂无${type === 'shipping' ? '发货' : '退货'}地址，请先在地址管理中添加`);
          }
        } else {
          ElMessage.error(result.message || '加载地址数据失败');
        }
      } catch (error) {
        console.error('加载地址数据失败:', error);
        ElMessage.error('网络错误，请稍后重试');
      }
    };

    // 处理地址选择
    const handleAddressSelect = (row) => {
      // 添加检查确保row对象存在且有address属性
      if (!row || !row.address) {
        ElMessage.error('选择的地址数据不完整');
        return;
      }
      
      const region = currentRegionForAddress.value;
      if (!region || !formData.regionConfigs[region]) {
        ElMessage.error('请先选择发货区域');
        return;
      }
      
      // 为指定区域设置地址
      if (addressDialogType.value === 'shipping') {
        formData.regionConfigs[region].shipping.shippingAddress = row.address;
      } else {
        formData.regionConfigs[region].shipping.returnAddress = row.address;
      }
      addressDialogVisible.value = false;
    };

    // 处理地址对话框关闭
    const handleAddressDialogClose = () => {
      supplierAddresses.value = [];
      addressDialogType.value = 'shipping';
    };

    // 初始化数据加载
    const initData = async () => {
      // 先加载发货区域选项，然后再加载商品详情
      // 这样商品详情中的区域信息才能正确合并
      await loadShippingRegions(); // 加载发货区域
      loadVipLevels(); // 加载会员等级信息
      loadLogisticsCompanies(); // 加载物流公司信息
      loadProductTags(); // 加载商品标签
      await loadProductDetail(); // 最后加载商品详情
    };

    // 暂时方法给父组件 (通过 setup 的 return 暴露)
    // defineExpose 只能在 <script setup> 中使用

    // 组件挂载时
    onMounted(() => {
      if (props.autoLoad) {
        initData()
      }
      addMemberDiscountValidationRules();
    })

    return {
      loading,
      submitting,
      formRef,
      newDetailImageKey,
      newDetailUploadKey,
      categories,
      subcategories,
      items,
      logisticsCompanies, // 添加物流公司数据
      productTags, // 添加商品标签数据
      shippingRegionOptions, // 添加发货区域选项
      supplierAddresses, // 添加供应商地址数据
      addressDialogVisible, // 添加地址对话框可见性
      addressDialogType, // 添加地址对话框类型
      selectedAddress, // 添加选中的地址
      activeRegion, // 添加激活的区域标签
      formData,
      formRules,
      handleMainImageUpload,
      updateDetailImageKey,
      addNewDetailImage,
      loadProductDetail,
      handleSubmit,
      handleCancel,
      initData,
      // 添加 vipLevels 到返回的对象中
      vipLevels,
      // 添加分类联动方法
      handleCategoryChange,
      handleSubcategoryChange,
      loadSubcategoriesForCategory,
      loadItemsForSubcategory,
      // 添加地址相关方法
      loadSupplierAddresses,
      handleAddressSelect,
      handleAddressDialogClose,
      // 添加区域相关工具方法
      getRegionCurrency,
      getRegionCurrencySymbol,
      getRegionLabel,
      calculateSellingPrice,
      calculateMemberPrice
    }
  }
}

</script>

<style scoped>
.product-edit {
  padding: 20px;
}

.box-card {
  max-width: 1200px;
  margin: 0 auto;
  position: relative; /* 为 v-loading 提供定位上下文 */
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  font-size: 16px;
}

.form-item-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
}

:deep(.el-divider__text) {
  font-weight: bold;
  color: #303133;
}

.image-upload-list {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.image-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.image-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.image-info .el-input {
  width: 178px;
}

.image-info .el-checkbox {
  margin-top: 5px;
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

/* 必填项星号样式 */
:deep(.el-form-item.is-required .el-form-item__label:before) {
  content: '*';
  color: #f56c6c;
  margin-right: 4px;
}

/* 自定义必填标签样式 */
.required-label::before {
  content: '*';
  color: #f56c6c;
  margin-right: 4px;
}
</style>
