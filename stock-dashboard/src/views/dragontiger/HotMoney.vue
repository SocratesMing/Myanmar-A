<template>
  <div>
    <div class="page-title">知名游资动向</div>
    <div class="page-subtitle">2026-04-28 游资席位追踪</div>

    <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:16px">
      <div v-for="h in hotmoney" :key="h.name" class="card">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px">
          <div style="width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,#722ed1,#1890ff);display:flex;align-items:center;justify-content:center;color:#fff;font-size:14px;font-weight:600">{{ h.name[0] }}</div>
          <div>
            <div style="font-size:15px;font-weight:600">{{ h.name }}</div>
            <div style="font-size:12px;color:#8c8c8c">{{ h.seat }}</div>
          </div>
        </div>
        <div style="font-size:13px;margin-bottom:8px">
          <span style="color:#8c8c8c">买入：</span>
          <span v-for="s in h.buys" :key="s.name" style="margin-right:8px">
            {{ s.name }} <span class="rise">{{ s.amount }}</span>
          </span>
        </div>
        <div style="font-size:13px">
          <span style="color:#8c8c8c">卖出：</span>
          <span v-for="s in h.sells" :key="s.name" style="margin-right:8px">
            {{ s.name }} <span class="fall">{{ s.amount }}</span>
          </span>
        </div>
        <div style="margin-top:8px;font-size:12px;color:#8c8c8c">操作风格：{{ h.style }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
const hotmoney = [
  {name:'炒股养家',seat:'华鑫证券上海分公司',buys:[{name:'中芯国际',amount:'5,234万'},{name:'科大讯飞',amount:'3,456万'}],sells:[{name:'万科A',amount:'2,345万'}],style:'短线打板，偏好科技股'},
  {name:'章盟主',seat:'国泰君安上海江苏路',buys:[{name:'宁德时代',amount:'8,567万'},{name:'比亚迪',amount:'6,789万'}],sells:[{name:'隆基绿能',amount:'4,567万'}],style:'大资金运作，偏好新能源'},
  {name:'赵老哥',seat:'银河证券绍兴路',buys:[{name:'贵州茅台',amount:'4,321万'}],sells:[{name:'平安银行',amount:'3,456万'},{name:'中信证券',amount:'2,345万'}],style:'波段操作，偏好消费蓝筹'},
  {name:'作手新一',seat:'中信证券上海分公司',buys:[{name:'北方华创',amount:'3,567万'},{name:'立讯精密',amount:'2,890万'}],sells:[{name:'海通证券',amount:'1,234万'}],style:'短线快进快出，偏好半导体'},
  {name:'小鳄鱼',seat:'华泰证券深圳益田路',buys:[{name:'恒瑞医药',amount:'2,456万'},{name:'迈瑞医疗',amount:'1,987万'}],sells:[{name:'药明康德',amount:'1,567万'}],style:'中线布局，偏好医药'},
  {name:'方新侠',seat:'招商证券深圳蛇口',buys:[{name:'科大讯飞',amount:'6,543万'}],sells:[{name:'格力电器',amount:'2,345万'}],style:'龙头战法，偏好AI概念'},
]
</script>
