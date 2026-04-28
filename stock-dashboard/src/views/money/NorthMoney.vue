<template>
  <div>
    <div class="page-title">北向资金流向</div>
    <div class="page-subtitle">2026-04-28 实时数据</div>

    <div style="display:flex;gap:16px;margin-bottom:16px">
      <div class="stat-card"><div class="label">当日净流入</div><div class="value rise">+42.3亿</div></div>
      <div class="stat-card"><div class="label">近5日净流入</div><div class="value rise">+128.7亿</div></div>
      <div class="stat-card"><div class="label">近20日净流入</div><div class="value fall">-56.2亿</div></div>
    </div>

    <div class="card" style="margin-bottom:16px">
      <div style="font-size:15px;font-weight:600;margin-bottom:12px">日内累计净流入曲线</div>
      <div ref="flowChart" class="chart-container"></div>
    </div>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
      <div class="card">
        <div style="font-size:15px;font-weight:600;margin-bottom:12px" class="rise">净买入前10</div>
        <table><thead><tr><th>代码</th><th>名称</th><th>净买入(亿)</th></tr></thead>
        <tbody><tr v-for="s in topBuy" :key="s.code"><td>{{s.code}}</td><td>{{s.name}}</td><td class="rise">+{{s.amount}}</td></tr></tbody></table>
      </div>
      <div class="card">
        <div style="font-size:15px;font-weight:600;margin-bottom:12px" class="fall">净卖出前10</div>
        <table><thead><tr><th>代码</th><th>名称</th><th>净卖出(亿)</th></tr></thead>
        <tbody><tr v-for="s in topSell" :key="s.code"><td>{{s.code}}</td><td>{{s.name}}</td><td class="fall">{{s.amount}}</td></tr></tbody></table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const flowChart = ref(null)
let chart = null

const topBuy = [
  {code:'600519',name:'贵州茅台',amount:'5.23'},{code:'300750',name:'宁德时代',amount:'4.12'},
  {code:'601318',name:'中国平安',amount:'3.56'},{code:'000858',name:'五粮液',amount:'2.89'},
  {code:'600036',name:'招商银行',amount:'2.34'},{code:'002594',name:'比亚迪',amount:'2.12'},
  {code:'600276',name:'恒瑞医药',amount:'1.89'},{code:'601012',name:'隆基绿能',amount:'1.56'},
  {code:'002475',name:'立讯精密',amount:'1.34'},{code:'300760',name:'迈瑞医疗',amount:'1.12'},
]
const topSell = [
  {code:'000001',name:'平安银行',amount:'-3.45'},{code:'601166',name:'兴业银行',amount:'-2.87'},
  {code:'600030',name:'中信证券',amount:'-2.34'},{code:'000002',name:'万科A',amount:'-2.12'},
  {code:'600837',name:'海通证券',amount:'-1.89'},{code:'601688',name:'华泰证券',amount:'-1.56'},
  {code:'600000',name:'浦发银行',amount:'-1.34'},{code:'601398',name:'工商银行',amount:'-1.12'},
  {code:'600016',name:'民生银行',amount:'-0.98'},{code:'601288',name:'农业银行',amount:'-0.87'},
]

onMounted(() => {
  chart = echarts.init(flowChart.value)
  const times = Array.from({length:240},(_,i)=>{const h=9+Math.floor((i+30)/60);const m=(i+30)%60;return `${h}:${String(m).padStart(2,'0')}`})
  let v = 0
  const data = times.map(()=>{v+=(Math.random()-0.42)*0.5;return +v.toFixed(2)})
  chart.setOption({
    tooltip:{trigger:'axis'},grid:{top:20,left:50,right:20,bottom:30},
    xAxis:{type:'category',data:times,axisLabel:{fontSize:10}},
    yAxis:{type:'value',name:'亿元',splitLine:{lineStyle:{type:'dashed'}}},
    series:[{type:'line',data,smooth:true,areaStyle:{color:new echarts.graphic.LinearGradient(0,0,0,1,[{offset:0,color:'rgba(232,57,81,0.3)'},{offset:1,color:'rgba(232,57,81,0.02)'}])},lineStyle:{color:'#e83951',width:2},itemStyle:{color:'#e83951'}}]
  })
  window.addEventListener('resize',()=>chart?.resize())
})
onUnmounted(()=>chart?.dispose())
</script>
