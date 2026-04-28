<template>
  <div>
    <div class="page-title">融资融券数据</div>
    <div class="page-subtitle">2026-04-28</div>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px">
      <div class="stat-card"><div class="label">融资余额</div><div class="value">15,234.56 亿</div><div class="rise" style="font-size:13px;margin-top:4px">+23.45亿</div></div>
      <div class="stat-card"><div class="label">融券余额</div><div class="value">987.32 亿</div><div class="fall" style="font-size:13px;margin-top:4px">-5.67亿</div></div>
    </div>

    <div class="card" style="margin-bottom:16px">
      <div style="font-size:15px;font-weight:600;margin-bottom:12px">融资余额变化趋势（近20日）</div>
      <div ref="trendChart" class="chart-container-sm"></div>
    </div>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
      <div class="card">
        <div style="font-size:15px;font-weight:600;margin-bottom:12px" class="rise">融资净买入前10</div>
        <table><thead><tr><th>代码</th><th>名称</th><th>净买入(亿)</th></tr></thead>
        <tbody><tr v-for="s in marginBuy" :key="s.code"><td>{{s.code}}</td><td>{{s.name}}</td><td class="rise">+{{s.amount}}</td></tr></tbody></table>
      </div>
      <div class="card">
        <div style="font-size:15px;font-weight:600;margin-bottom:12px" class="fall">融券净卖出前10</div>
        <table><thead><tr><th>代码</th><th>名称</th><th>净卖出(亿)</th></tr></thead>
        <tbody><tr v-for="s in marginSell" :key="s.code"><td>{{s.code}}</td><td>{{s.name}}</td><td class="fall">{{s.amount}}</td></tr></tbody></table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const trendChart = ref(null)
let chart = null

const marginBuy = [
  {code:'600519',name:'贵州茅台',amount:'2.34'},{code:'300750',name:'宁德时代',amount:'1.89'},
  {code:'002594',name:'比亚迪',amount:'1.56'},{code:'601318',name:'中国平安',amount:'1.23'},
  {code:'600276',name:'恒瑞医药',amount:'0.98'},{code:'002475',name:'立讯精密',amount:'0.87'},
  {code:'300760',name:'迈瑞医疗',amount:'0.76'},{code:'688981',name:'中芯国际',amount:'0.65'},
  {code:'002230',name:'科大讯飞',amount:'0.54'},{code:'600036',name:'招商银行',amount:'0.43'},
]
const marginSell = [
  {code:'000001',name:'平安银行',amount:'-1.56'},{code:'600030',name:'中信证券',amount:'-1.23'},
  {code:'000002',name:'万科A',amount:'-0.98'},{code:'601166',name:'兴业银行',amount:'-0.87'},
  {code:'600837',name:'海通证券',amount:'-0.76'},{code:'601688',name:'华泰证券',amount:'-0.65'},
  {code:'600000',name:'浦发银行',amount:'-0.54'},{code:'601398',name:'工商银行',amount:'-0.43'},
  {code:'600016',name:'民生银行',amount:'-0.32'},{code:'601288',name:'农业银行',amount:'-0.21'},
]

onMounted(()=>{
  chart=echarts.init(trendChart.value)
  const dates=Array.from({length:20},(_,i)=>`04-${String(i+9).padStart(2,'0')}`)
  let v=15100
  const data=dates.map(()=>{v+=(Math.random()-0.45)*30;return +v.toFixed(2)})
  chart.setOption({
    tooltip:{trigger:'axis'},grid:{top:20,left:60,right:20,bottom:30},
    xAxis:{type:'category',data:dates},yAxis:{type:'value',name:'亿元',scale:true},
    series:[{type:'line',data,smooth:true,areaStyle:{color:'rgba(24,144,255,0.15)'},lineStyle:{color:'#1890ff'}}]
  })
  window.addEventListener('resize',()=>chart?.resize())
})
onUnmounted(()=>chart?.dispose())
</script>
