<template>
  <div class="product-add">
    <!-- 审核状态和激活状态警告 -->
    <el-alert
      v-if="!canAddProduct"
      title="无法添加商品"
      type="error"
      :closable="false"
      show-icon
      style="margin-bottom: 20px;"
    >
      <template #default>
        <div style="line-height: 1.8;">
          <p style="margin: 0 0 8px 0; font-size: 14px; font-weight: bold;">
            您当前无法添加商品，原因如下：
          </p>
          <p v-if="!isActive" style="margin: 5px 0; font-size: 14px; color: #f56c6c;">
            ❌ 账号状态：<strong>未激活</strong>
          </p>
          <p v-else style="margin: 5px 0; font-size: 14px; color: #67c23a;">
            ✅ 账号状态：<strong>已激活</strong>
          </p>
          <p v-if="!isAuditApproved" style="margin: 5px 0; font-size: 14px; color: #f56c6c;">
            ❌ 审核状态：<strong>{{ auditStatusText }}</strong>
          </p>
          <p v-else style="margin: 5px 0; font-size: 14px; color: #67c23a;">
            ✅ 审核状态：<strong>已通过</strong>
          </p>
          <p style="margin: 10px 0 0 0; padding: 8px; background-color: #fef0f0; border-left: 3px solid #f56c6c; font-size: 13px; color: #606266;">
            <strong style="color: #f56c6c;">💡 提示：</strong>
            只有同时满足<strong>账号状态为"已激活"</strong>且<strong>审核状态为"已通过"</strong>才能添加商品。
            <span v-if="!isActive">请联系管理员激活您的账号。</span>
            <span v-if="!isAuditApproved">{{ isActive ? '请先完善您的供应商资料，等待管理员审核通过后再添加商品。' : '' }}</span>
          </p>
        </div>
      </template>
    </el-alert>
    
    <el-card class="box-card" :class="{ 'disabled-card': !canAddProduct }">
      <template #header>
        <div class="card-header">
          <span>添加商品</span>
        </div>
      </template>
      
      <el-form :model="formData" :rules="formRules" ref="formRef" label-width="120px" :disabled="!canAddProduct">
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
        <div class="form-item-tip" style="margin-bottom: 20px; color: #E6A23C;">
          💡 您需要为每个发货区域单独配置价格、折扣、会员折扣、满减和运费信息
        </div>
        
        <!-- 区域切换标签 -->
        <el-tabs v-model="activeRegion" type="border-card" v-if="formData.shippingRegions.length > 0">
          <el-tab-pane 
            v-for="region in formData.shippingRegions" 
            :key="region" 
            :label="getRegionLabel(region)" 
            :name="region"
          >
            <!-- 单个区域的完整配置 -->
            <div class="region-config-panel">
              <!-- 价格配置 -->
              <h4 style="margin-bottom: 15px; color: #409EFF;">💰 价格配置</h4>
              
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="币种">
                    <el-input :value="getRegionCurrency(region)" disabled />
                    <div class="form-item-tip">本网站的结算货币是{{ getRegionCurrency(region) }}，货币符号为{{ getRegionCurrencySymbol(region) }}</div>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="业务类型">
                    <el-select v-model="formData.regionConfigs[region].price.businessType" placeholder="请选择业务类型">
                      <el-option label="一件代发" value="dropship" />
                      <el-option label="批发" value="wholesale" />
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="原价" required>
                    <el-input 
                      v-model.number="formData.regionConfigs[region].price.originalPrice" 
                      type="number" 
                      step="0.01"
                      placeholder="请输入原价" 
                      @input="(val) => formData.regionConfigs[region].price.originalPrice = parseFloat(parseFloat(val).toFixed(2))"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="商品折扣率(%)">
                    <el-input 
                      v-model.number="formData.regionConfigs[region].price.discountRate" 
                      type="number" 
                      placeholder="0-90" 
                      min="0" 
                      max="90"
                    >
                      <template #append>%</template>
                    </el-input>
                    <div class="form-item-tip">折扣范围：0-90%</div>
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="售价">
                    <el-input 
                      :value="calculateSellingPrice(region)" 
                      disabled
                    />
                    <div class="form-item-tip">根据原价和折扣自动计算</div>
                  </el-form-item>
                </el-col>
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
              
              <!-- 会员折扣设置 -->
              <h4 style="margin: 20px 0 15px; color: #409EFF;">👥 会员折扣配置</h4>
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
                      <div class="member-price" v-if="calculateMemberPrice(region, level.value) !== null">
                        实际售价：{{ getRegionCurrencySymbol(region) }}{{ calculateMemberPrice(region, level.value) }}
                      </div>
                    </el-form-item>
                  </el-col>
                </el-row>
              </div>
              <div class="form-item-tip">会员折扣范围：0-90%，基于售价计算</div>
              
              <!-- 满减活动设置 -->
              <h4 style="margin: 20px 0 15px; color: #409EFF;">🎁 满减活动配置</h4>
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
              
              <!-- 运费设置 -->
              <h4 style="margin: 20px 0 15px; color: #409EFF;">🚚 运费配置</h4>
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
                <el-col :span="12">
                  <el-form-item label="承运商">
                    <el-select 
                      v-model="formData.regionConfigs[region].shipping.carriers" 
                      multiple 
                      placeholder="请选择承运商" 
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
                </el-col>
              </el-row>

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
          v-else 
          title="请先选择发货区域" 
          type="warning" 
          :closable="false" 
          show-icon
          style="margin-bottom: 20px;"
        >
          <template #default>
            请在上方"发货区域"选项中选择至少一个区域，然后为每个区域配置价格、折扣、满减和运费信息。
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
          <el-radio-group v-model="formData.status">
            <el-radio label="draft">保存为草稿</el-radio>
            <el-radio label="approved">发布</el-radio>
          </el-radio-group>
          <div class="form-item-tip">草稿状态可以继续编辑，发布后商品将直接上架</div>
        </el-form-item>
        
        <!-- 提交按钮 -->
        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">提交</el-button>
          <el-button @click="handleReset">重置</el-button>
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
  ElDialog,
  ElTable,
  ElTableColumn,
  ElTag,
  ElTabs,
  ElTabPane,
  ElAlert
} from 'element-plus'
import FileUpload from './FileUpload.vue'
import RichTextEditor from './RichTextEditor.vue'

export default {
  name: 'ProductAdd',
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
    autoLoad: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    const loading = ref(false)
    const submitting = ref(false)
    const formRef = ref(null)
    const newDetailImageKey = ref('') // 用于新增详情图的临时key
    const newDetailUploadKey = ref(0) // 用于强制刷新新的详情图上传组件
    
    // 审核状态和激活状态相关
    const supplierAuditStatus = ref('resubmit') // 默认状态
    const isActive = ref(false) // 激活状态
    const isAuditApproved = computed(() => supplierAuditStatus.value === 'approved')
    const canAddProduct = computed(() => isActive.value && isAuditApproved.value)
    
    // 获取审核状态文本
    const auditStatusText = computed(() => {
      const statusMap = {
        'pending': '待审核',
        'approved': '已通过',
        'rejected': '已拒绝',
        'resubmit': '待重新提交'
      }
      return statusMap[supplierAuditStatus.value] || supplierAuditStatus.value
    })

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

    // 当前激活的区域标签
    const activeRegion = ref('')

    // 表单数据
    const formData = reactive({
      sku: null,  // 改为 null，让后端自动生成
      spu: null,  // 改为 null，让后端自动生成
      title: '',
      titleEn: '',
      mainImage: '',  // 主图key
      thumbnailImage: '',  // 缩略图key
      detailImages: [],  // 详情图数组 [{key: '', canBeMain: false}]
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
      // 多区域配置：每个区域独立的价格、折扣、会员折扣、满减、运费和库存
      regionConfigs: {}
    })

    // 删除主图相关的旧代码
    // const mainImages = ref([{ url: '' }]);
    
    // 处理主图上传成功
    const handleMainImageUpload = (response) => {
      console.log('[ProductAdd] 主图上传成功:', response)
      if (response && response.success) {
        formData.mainImage = response.mainImageKey
        formData.thumbnailImage = response.thumbnailKey
        // 不需要显示提示，由父组件统一显示
      } else {
        // 特别处理非正方形图片的情况
        if (response && response.message && response.message.includes('正方形')) {
          ElMessage.error('主图必须是正方形图片，请重新选择!')
        } else {
          ElMessage.error(response.message || '主图上传失败')
        }
      }
    }
    
    // 更新详情图key
    const updateDetailImageKey = (index, newKey) => {
      console.log(`[ProductAdd] 更新详情图[${index}] key:`, newKey);
      if (formData.detailImages[index]) {
        formData.detailImages[index].key = newKey;
      }
    }
    
    // 添加新详情图 - 直接从上传响应中获取数据，避免重复调用签名URL接口
    const addNewDetailImage = (response) => {
      console.log('[ProductAdd] addNewDetailImage called with response:', response);
      
      // 检查上传是否成功
      if (!response || !response.success) {
        console.error('[ProductAdd] 详情图上传失败:', response)
        return
      }
      
      // 检查数组长度限制
      if (formData.detailImages.length >= 10) {
        ElMessage.warning('最多只能上传10张详情图')
        return
      }
      
      // 保存key、previewUrl和canBeMain
      // key和canBeMain用于提交到后端
      // previewUrl仅用于前端显示
      const newImage = {
        key: response.key,  // 后端返回的文件key，用于提交到后端
        previewUrl: response.previewUrl || response.url || '',  // 用于前端显示
        canBeMain: false  // 默认不作为主图
      }
      
      // 添加到详情图数组
      formData.detailImages.push(newImage)
      
      // 清空临时变量，准备下一次上传
      newDetailImageKey.value = ''
      
      // 强制刷新上传组件，确保可以继续上传
      newDetailUploadKey.value++
    }

    // 监听原价和折扣率变化，自动计算售价（移除旧逻辑，现在每个区域独立计算）
    // watch(() => [formData.price.originalPrice, formData.price.discountRate], () => { ... })
    
    // 监听发货区域变化，为新增区域初始化配置
    watch(() => formData.shippingRegions, (newRegions, oldRegions) => {
      console.log('[ProductAdd] 发货区域变化:', newRegions)
      
      // 为新增的区域初始化配置
      newRegions.forEach(region => {
        if (!formData.regionConfigs[region]) {
          formData.regionConfigs[region] = createRegionConfig(region)
        }
      })
      
      // 删除不再需要的区域配置
      Object.keys(formData.regionConfigs).forEach(region => {
        if (!newRegions.includes(region)) {
          delete formData.regionConfigs[region]
        }
      })
      
      // 如果当前激活的区域被移除，切换到第一个区域
      if (!newRegions.includes(activeRegion.value) && newRegions.length > 0) {
        activeRegion.value = newRegions[0]
      } else if (newRegions.length === 0) {
        activeRegion.value = ''
      }
    }, { deep: true })
    
    // 为指定区域创建默认配置
    const createRegionConfig = (region) => {
      const currency = getRegionCurrency(region)
      return {
        price: {
          currency: currency,
          businessType: 'dropship',
          originalPrice: null,
          sellingPrice: null,
          discountRate: 0,
          memberDiscount: {
            '0': 0,
            '1': 0,
            '2': 0,
            '3': 0,
            '4': 0,
            '5': 0
          },
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
        }
      } catch (error) {
        console.error('获取区域选项失败:', error)
      }
    }

    // 获取区域对应的币种
    const getRegionCurrency = (region) => {
      if (regionOptions.length === 0) {
        throw new Error('发货区域配置未加载，请刷新页面重试')
      }
      const option = regionOptions.find(r => r.value === region)
      if (!option) {
        throw new Error(`未找到区域 ${region} 的配置信息`)
      }
      return option.currency
    }
    
    // 获取区域对应的币种符号
    const getRegionCurrencySymbol = (region) => {
      if (regionOptions.length === 0) {
        throw new Error('发货区域配置未加载，请刷新页面重试')
      }
      const option = regionOptions.find(r => r.value === region)
      if (!option) {
        throw new Error(`未找到区域 ${region} 的配置信息`)
      }
      return option.currencySymbol
    }
    
    // 获取区域标签显示名称编辑商品的时候。
    const getRegionLabel = (region) => {
      if (regionOptions.length === 0) {
        throw new Error('发货区域配置未加载，请刷新页面重试')
      }
      const option = regionOptions.find(r => r.value === region)
      if (!option) {
        throw new Error(`未找到区域 ${region} 的配置信息`)
      }
      return `${option.label} (${option.currency})`
    }
    
    // 计算指定区域的售价
    const calculateSellingPrice = (region) => {
      const config = formData.regionConfigs[region]
      if (!config || !config.price.originalPrice) {
        return '0.00'
      }
      
      const originalPrice = parseFloat(config.price.originalPrice)
      const discountRate = parseFloat(config.price.discountRate) || 0
      const validDiscountRate = Math.max(0, Math.min(90, discountRate))
      const sellingPrice = originalPrice * (1 - validDiscountRate / 100)
      
      return sellingPrice.toFixed(2)
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
      // 添加数字字段验证规则
      'price.originalPrice': [
        { validator: validateOriginalPrice, trigger: 'blur' }
      ],
      'price.sellingPrice': [
        { validator: validateTwoDecimals, trigger: 'blur' }
      ],
      'shipping.shippingPrice': [
        { validator: validateTwoDecimals, trigger: 'blur' }
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
      ],
      // 价格信息验证规则
      'price.minWholesaleQuantity': [
        { validator: validateNonNegativeInteger, trigger: 'blur' }
      ],
      // 折扣率验证规则（可以大于等于0）
      'price.discountRate': [
        { validator: validateOneDecimal, trigger: 'blur' }
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

    // 监听表单数据变化，自动格式化数字字段
    watch(() => formData.length, (newVal) => {
      if (newVal !== null && newVal !== undefined && newVal !== '') {
        const num = parseFloat(newVal)
        if (!isNaN(num)) {
          formData.length = num // 不再自动格式化为两位小数
        }
      }
    })

    watch(() => formData.width, (newVal) => {
      if (newVal !== null && newVal !== undefined && newVal !== '') {
        const num = parseFloat(newVal)
        if (!isNaN(num)) {
          formData.width = num // 不再自动格式化为两位小数
        }
      }
    })

    watch(() => formData.height, (newVal) => {
      if (newVal !== null && newVal !== undefined && newVal !== '') {
        const num = parseFloat(newVal)
        if (!isNaN(num)) {
          formData.height = num // 不再自动格式化为两位小数
        }
      }
    })

    watch(() => formData.weight, (newVal) => {
      if (newVal !== null && newVal !== undefined && newVal !== '') {
        const num = parseFloat(newVal)
        if (!isNaN(num)) {
          formData.weight = num // 不再自动格式化为两位小数
        }
      }
    })

    watch(() => formData.packageLength, (newVal) => {
      if (newVal !== null && newVal !== undefined && newVal !== '') {
        const num = parseFloat(newVal)
        if (!isNaN(num)) {
          formData.packageLength = num // 不再自动格式化为两位小数
        }
      }
    })

    watch(() => formData.packageWidth, (newVal) => {
      if (newVal !== null && newVal !== undefined && newVal !== '') {
        const num = parseFloat(newVal)
        if (!isNaN(num)) {
          formData.packageWidth = num // 不再自动格式化为两位小数
        }
      }
    })

    watch(() => formData.packageHeight, (newVal) => {
      if (newVal !== null && newVal !== undefined && newVal !== '') {
        const num = parseFloat(newVal)
        if (!isNaN(num)) {
          formData.packageHeight = num // 不再自动格式化为两位小数
        }
      }
    })

    watch(() => formData.packageWeight, (newVal) => {
      if (newVal !== null && newVal !== undefined && newVal !== '') {
        const num = parseFloat(newVal)
        if (!isNaN(num)) {
          formData.packageWeight = num // 不再自动格式化为两位小数
        }
      }
    })

    // 所有与价格相关的watch已移除，因为价格现在在regionConfigs中管理
    // 库存现在也在regionConfigs中管理，不再需要全局watch

    // 删除旧的主图相关方法
    // const updateMainImageUrl = ...
    // const addNewMainImage = ...

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
        console.error('加载子分类数据失败:', error)
      }
    }

    // 处理二级分类变化
    const handleSubcategoryChange = async (subcategoryId) => {
      formData.itemId = ''
      items.value = []

      if (!subcategoryId) return

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
        console.error('加载商品项数据失败:', error)
      }
    }

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
          // 同时加载到组件级别，供区域配置使用
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

    // 提交表单
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

          // 转换数据格式：regionConfigs → prices/discountRules/shippings
          const prices = {}
          const discountRules = {}
          const shippings = {}
          
          formData.shippingRegions.forEach(region => {
            const config = formData.regionConfigs[region]
            
            // 计算售价：售价 = 原价 × (1 - 折扣率/100)
            const originalPrice = parseFloat(config.price.originalPrice) || 0
            const discountRate = parseFloat(config.price.discountRate) || 0
            const sellingPrice = originalPrice * (1 - discountRate / 100)
            
            // 价格数据（将百分比转换为小数）
            prices[region] = {
              currency: config.price.currency,
              businessType: config.price.businessType,
              originalPrice: config.price.originalPrice,
              sellingPrice: sellingPrice.toFixed(2),  // 添加售价字段
              discountRate: config.price.discountRate / 100,  // 转换为小数
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
            
            // 满减规则数据（仅当启用时才添加）
            if (config.discountRule.enabled && config.discountRule.minAmount && config.discountRule.discountAmount) {
              discountRules[region] = {
                minAmount: config.discountRule.minAmount,
                discountAmount: config.discountRule.discountAmount
              }
            }
            
            // 运费数据（包括地址和库存信息）
            shippings[region] = {
              shippingMethod: config.shipping.shippingMethod,
              shippingPrice: config.shipping.shippingPrice || 0,
              additionalPrice: config.shipping.additionalPrice || 0,
              currency: config.shipping.currency,
              deliveryTime: config.shipping.deliveryTime,
              carriers: config.shipping.carriers || [],
              shippingAddress: config.shipping.shippingAddress || null,  // 发货地址
              returnAddress: config.shipping.returnAddress || null,      // 退货地址
              // 库存信息（新增）
              availableStock: config.stock.availableStock || 0,           // 可售库存
              alertStockLine: config.stock.alertStockLine || 10,          // 库存预警线
              warehouseCode: config.stock.warehouseCode || '',            // 仓库代码
              warehouseName: config.stock.warehouseName || '',            // 仓库名称
              warehouseAddress: config.stock.warehouseAddress || ''       // 仓库地址
            }
          })

          // 构造提交数据
          const submitData = {
            sku: formData.sku,
            spu: formData.spu,
            title: formData.title,
            titleEn: formData.titleEn,
            mainImage: formData.mainImage,
            thumbnailImage: formData.thumbnailImage,
            detailImages: formData.detailImages.map(img => ({
              key: img.key,
              canBeMain: img.canBeMain
            })),
            categoryId: formData.categoryId,
            subcategoryId: formData.subcategoryId,
            itemId: formData.itemId,
            brand: formData.brand,
            length: formData.length,
            width: formData.width,
            height: formData.height,
            weight: formData.weight,
            packageLength: formData.packageLength,
            packageWidth: formData.packageWidth,
            packageHeight: formData.packageHeight,
            packageWeight: formData.packageWeight,
            tags: formData.tags,
            isLimited: formData.isLimited,
            supportDropship: formData.supportDropship,
            supportWholesale: formData.supportWholesale,
            supportCircleBuy: formData.supportCircleBuy,
            supportSelfPickup: formData.supportSelfPickup,
            shippingRegions: formData.shippingRegions,
            richContent: formData.richContent,
            status: formData.status,
            // 多区域配置数据（价格、满减、运费和库存均包含在shippings中）
            prices: prices,
            discountRules: discountRules,
            shippings: shippings
          }

          const response = await fetch(`/supplier${props.supplierLoginPath}/product/create`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify(submitData)
          })

          const result = await response.json()

          if (result.success) {
            ElMessage.success(formData.status === 'draft' ? '商品保存成功' : '商品已提交审核')
            
            // 询问是否返回列表
            ElMessageBox.confirm('操作成功，是否返回商品列表？', '提示', {
              confirmButtonText: '返回列表',
              cancelButtonText: '继续添加',
              type: 'success'
            }).then(() => {
              // 先关闭当前添加商品标签页
              window.dispatchEvent(new CustomEvent('close-current-tab'))
              // 然后触发导航事件返回商品列表
              setTimeout(() => {
                window.dispatchEvent(new CustomEvent('navigate-to', {
                  detail: { key: 'product-list' }
                }))
              }, 100)
            }).catch(() => {
              // 继续添加，重置表单
              handleReset()
            })
          } else {
            ElMessage.error(result.message || '提交失败')
          }
        } catch (error) {
          console.error('提交失败:', error)
          ElMessage.error('网络错误，请稍后重试')
        } finally {
          submitting.value = false
        }
      })
    }

    // 重置表单
    const handleReset = () => {
      resetFormData()
    };

    // 取消添加
    const handleCancel = () => {
      ElMessageBox.confirm('确定要取消添加商品吗？未保存的数据将丢失。', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '继续编辑',
        type: 'warning'
      }).then(() => {
        // 先关闭当前添加商品标签页
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

    // 加载供应商地址（根据类型和区域过滤）
    const currentRegionForAddress = ref('') // 当前选择地址的区域
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

    // 重置表单数据，清空之前的老数据
    const resetFormData = () => {
      // 重置为默认值
      Object.assign(formData, {
        sku: null,
        spu: null,
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
      
      // 重置分类相关数据
      subcategories.value = []
      items.value = []
      
      // 重置区域相关数据
      activeRegion.value = ''
      
      // 重置详情图上传组件
      newDetailImageKey.value = ''
      newDetailUploadKey.value++
      
      // 清空表单验证
      if (formRef.value) {
        formRef.value.clearValidate()
      }
    }
    
    // 初始化数据加载
    const initData = async () => {
      // 先重置表单数据，清空之前商品的信息
      resetFormData()
      
      // 加载供应商审核状态
      await loadSupplierProfile()
      
      loadRegionOptions(); // 加载区域选项
      loadCategories();
      loadVipLevels(); // 加载会员等级信息
      loadLogisticsCompanies(); // 加载物流公司信息
      loadProductTags(); // 加载商品标签
      loadShippingRegions(); // 加载发货区域
    };
    
    // 加载供应商信息（获取审核状态）
    const loadSupplierProfile = async () => {
      try {
        const response = await fetch(`/supplier${props.supplierLoginPath}/profile/data`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
          }
        })
        
        const result = await response.json()
        
        if (result.success && result.data) {
          supplierAuditStatus.value = result.data.auditStatus || 'resubmit'
          // 正确处理布尔值，避免 false 被转换为 false
          isActive.value = result.data.isActive === true || result.data.isActive === 1
          
          console.log('[ProductAdd] 供应商状态:', {
            auditStatus: supplierAuditStatus.value,
            isActive: isActive.value,
            rawIsActive: result.data.isActive
          })
        }
      } catch (error) {
        console.error('加载供应商信息失败:', error)
      }
    }

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
      supplierAuditStatus,
      isActive,
      isAuditApproved,
      canAddProduct,
      auditStatusText,
      categories,
      subcategories,
      items,
      logisticsCompanies,
      productTags,
      shippingRegionOptions,
      supplierAddresses,
      addressDialogVisible,
      addressDialogType,
      selectedAddress,
      currentRegionForAddress,
      activeRegion,
      formData,
      formRules,
      handleMainImageUpload,
      updateDetailImageKey,
      addNewDetailImage,
      loadCategories,
      handleCategoryChange,
      handleSubcategoryChange,
      handleSubmit,
      handleReset,
      handleCancel,
      initData,
      resetFormData,
      vipLevels,
      loadSupplierAddresses,
      handleAddressSelect,
      handleAddressDialogClose,
      // 区域相关方法
      getRegionCurrency,
      getRegionCurrencySymbol,
      getRegionLabel,
      calculateSellingPrice,
      calculateMemberPrice,
      createRegionConfig
    }
  }
}

</script>

<style scoped>
.product-add {
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

/* 禁用状态的卡片样式 */
.disabled-card {
  opacity: 0.7;
  pointer-events: none;
  user-select: none;
}

.disabled-card :deep(.el-form-item__content) {
  cursor: not-allowed;
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

/* 多区域配置面板样式 */
.region-config-panel {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.region-config-panel h4 {
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 2px solid #e4e7ed;
}
</style>