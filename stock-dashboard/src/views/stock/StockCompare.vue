<template>
  <div>
    <div class="page-title">个股对比</div>
    <div class="page-subtitle">对比分析两只股票的核心指标</div>

    <div class="card" style="margin-bottom:16px">
      <div style="display:flex;gap:16px;align-items:center">
        <div><label style="font-size:12px;color:#8c8c8c">股票A</label><input v-model="stockA" style="margin-left:6px;padding:4px 8px;border:1px solid #d9d9d9;border-radius:4px;width:140px" /></div>
        <div style="font-size:18px;color:#8c8c8c">VS</div>
        <div><label style="font-size:12px;color:#8c8c8c">股票B</label><input v-model="stockB" style="margin-left:6px;padding:4px 8px;border:1px solid #d9d9d9;border-radius:4px;width:140px" /></div>
      </div>
    </div>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px">
      <div class="stat-card" v-for="s in [dataA, dataB]" :key="s.name">
        <div style="font-size:16px;font-weight:600;margin-bottom:12px">{{ s.name }}</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
          <div><div class="label">股价</div><div class="value" style="font-size:18px">{{ s.price }}</div></div>
          <div><div class="label">涨跌幅</div><div :class="s.pct>=0?'rise':'fall'" style="font-size:18px;font-weight:700">{{ s.pct>=0?'+':'' }}{{ s.pct }}%</div></div>
          <div><div class="label">市值</div><div style="font-size:14px">{{ s.mv }}亿</div></div>
          <div><div class="label">PE</div><div style="font-size:14px">{{ s.pe }}</div></div>
          <div><div class="label">ROE</div><div style="font-size:14px">{{ s.roe }}%</div></div>
          <div><div class="label">营收增长</div><div :class="s.revGrowth>=0?'rise':'fall'" style="font-size:14px">{{ s.revGrowth>=0?'+':'' }}{{ s.revGrowth }}%</div></div>
        </div>
      </div>
    </div>

    <div class="card">
      <div style="font-size:15px;font-weight:600;margin-bottom:12px">股价走势对比</div>
      <div ref="compareChart" class="chart-container"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const stockA = ref('贵州茅台')
const stockB = ref('五粮液')
const compareChart = ref(null)
let chart = null

const dataA = { name:'贵州茅台', price:1688.00, pct:1.23, mv:21200, pe:32.5, roe:31.2, revGrowth:15.6 }
const dataB = { name:'五粮液', price:156.32, pct:-0.56, mv:6080, pe:24.8, roe:25.8, revGrowth:12.3 }

onMounted(() => {
  chart = echarts.init(compareChart.value)
  const dates = Array.from({length:30},(_,i)=>`04-${String(i+1).padStart(2,'0')}`)
  const gen = (base, vol) => { let v=base; return dates.map(()=>{v+=(Math.random()-0.48)*vol;return +v.toFixed(2)}) }
  chart.setOption({
    tooltip:{trigger:'axis'},
    legend:{data:['贵州茅台','五粮液'],top:0},
    grid:{top:40,left:60,right:60,bottom:30},
    xAxis:{type:'category',data:dates},
    yAxis:[
      {type:'value',name:'茅台',position:'left',scale:true},
      {type:'value',name:'五粮液',position:'right',scale:true}
    ],
    series:[
      {name:'贵州茅台',type:'line',data:gen(1670,15),smooth:true,yAxisIndex:0,lineStyle:{width:2}},
      {name:'五粮液',type:'line',data:gen(155,2),smooth:true,yAxisIndex:1,lineStyle:{width:2}},
    ]
  })
  window.addEventListener('resize',()=>chart?.resize())
})
onUnmounted(()=>chart?.dispose())
</script>
