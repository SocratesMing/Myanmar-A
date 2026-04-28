<template>
  <div>
    <div class="page-title">核心财务数据</div>
    <div class="page-subtitle">最新一期财报关键指标</div>

    <div class="card" style="margin-bottom:16px">
      <select v-model="selectedStock" style="padding:4px 8px;border:1px solid #d9d9d9;border-radius:4px">
        <option value="宁德时代">宁德时代</option><option value="贵州茅台">贵州茅台</option><option value="比亚迪">比亚迪</option>
      </select>
    </div>

    <div class="card" style="margin-bottom:16px">
      <div style="font-size:15px;font-weight:600;margin-bottom:16px">{{ selectedStock }} — 2026Q1 财报</div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px">
        <div v-for="f in financeData" :key="f.label" style="padding:12px;background:#fafafa;border-radius:6px">
          <div style="font-size:12px;color:#8c8c8c">{{ f.label }}</div>
          <div style="font-size:18px;font-weight:600;margin-top:4px">{{ f.value }}</div>
          <div :class="f.yoy>=0?'rise':'fall'" style="font-size:12px;margin-top:2px">同比 {{ f.yoy>=0?'+':'' }}{{ f.yoy }}%</div>
        </div>
      </div>
    </div>

    <div class="card">
      <div style="font-size:15px;font-weight:600;margin-bottom:12px">五维能力雷达图</div>
      <div ref="radarChart" class="chart-container-sm"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const selectedStock = ref('宁德时代')
const radarChart = ref(null)
let chart = null

const financeData = [
  {label:'营业收入',value:'1,245.6亿',yoy:18.5},{label:'净利润',value:'156.3亿',yoy:22.1},
  {label:'每股收益',value:'6.45元',yoy:15.3},{label:'毛利率',value:'28.7%',yoy:2.1},
  {label:'净利率',value:'12.5%',yoy:1.8},{label:'资产负债率',value:'55.3%',yoy:-3.2},
]

onMounted(()=>{
  chart=echarts.init(radarChart.value)
  chart.setOption({
    radar:{indicator:[
      {name:'盈利能力',max:100},{name:'成长能力',max:100},{name:'偿债能力',max:100},
      {name:'运营能力',max:100},{name:'现金流',max:100}
    ],radius:'65%'},
    series:[{type:'radar',data:[{value:[82,78,65,71,73],name:'宁德时代',areaStyle:{color:'rgba(24,144,255,0.2)'},lineStyle:{color:'#1890ff'}}]}]
  })
  window.addEventListener('resize',()=>chart?.resize())
})
onUnmounted(()=>chart?.dispose())
</script>
