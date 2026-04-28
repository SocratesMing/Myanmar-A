<template>
  <div>
    <div class="page-title">技术分析 — 贵州茅台（模拟）</div>
    <div class="page-subtitle">600519 | 近60个交易日K线</div>

    <div class="card">
      <div style="display:flex;gap:8px;margin-bottom:12px">
        <button v-for="t in ['K线','成交量','MACD','KDJ']" :key="t" @click="activeTab=t"
          :style="{padding:'4px 12px',border:'1px solid #d9d9d9',borderRadius:'4px',background:activeTab===t?'#1890ff':'#fff',color:activeTab===t?'#fff':'#333',cursor:'pointer',fontSize:'13px'}">{{ t }}</button>
      </div>
      <div ref="klineChart" style="width:100%;height:500px"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'

const klineChart = ref(null)
const activeTab = ref('K线')
let chart = null

function genKlineData(n) {
  const data = [], volumes = [], ma5 = [], ma10 = [], ma20 = [], ma60 = []
  let base = 1650
  for (let i = 0; i < n; i++) {
    const open = base + (Math.random() - 0.48) * 20
    const close = open + (Math.random() - 0.45) * 30
    const high = Math.max(open, close) + Math.random() * 15
    const low = Math.min(open, close) - Math.random() * 15
    base = close
    data.push([+open.toFixed(2), +close.toFixed(2), +low.toFixed(2), +high.toFixed(2)])
    volumes.push(+(Math.random() * 5 + 1).toFixed(1))
  }
  const closes = data.map(d => d[1])
  for (let i = 0; i < n; i++) {
    ma5.push(i >= 4 ? +(closes.slice(i-4,i+1).reduce((a,b)=>a+b,0)/5).toFixed(2) : null)
    ma10.push(i >= 9 ? +(closes.slice(i-9,i+1).reduce((a,b)=>a+b,0)/10).toFixed(2) : null)
    ma20.push(i >= 19 ? +(closes.slice(i-19,i+1).reduce((a,b)=>a+b,0)/20).toFixed(2) : null)
    ma60.push(i >= 59 ? +(closes.slice(i-59,i+1).reduce((a,b)=>a+b,0)/60).toFixed(2) : null)
  }
  return { data, volumes, ma5, ma10, ma20, ma60 }
}

const kdata = genKlineData(60)
const dates = Array.from({length:60},(_,i)=>{const d=new Date(2026,1,i+1);return `${d.getMonth()+1}/${d.getDate()}`})

function renderChart() {
  if (!chart) return
  const series = [
    { name:'K线', type:'candlestick', data: kdata.data, xAxisIndex:0, yAxisIndex:0 },
    { name:'MA5', type:'line', data:kdata.ma5, smooth:true, lineStyle:{width:1}, symbol:'none', xAxisIndex:0, yAxisIndex:0 },
    { name:'MA10', type:'line', data:kdata.ma10, smooth:true, lineStyle:{width:1}, symbol:'none', xAxisIndex:0, yAxisIndex:0 },
    { name:'MA20', type:'line', data:kdata.ma20, smooth:true, lineStyle:{width:1}, symbol:'none', xAxisIndex:0, yAxisIndex:0 },
  ]
  if (activeTab.value === '成交量') {
    series.push({ name:'成交量', type:'bar', data:kdata.volumes, xAxisIndex:0, yAxisIndex:1 })
  }
  chart.setOption({
    tooltip:{trigger:'axis',axisPointer:{type:'cross'}},
    legend:{data:['K线','MA5','MA10','MA20'],top:0},
    grid:[{top:40,left:60,right:20,bottom:activeTab.value==='成交量'?80:30}],
    xAxis:[{type:'category',data:dates}],
    yAxis:[
      {type:'value',scale:true,splitLine:{lineStyle:{type:'dashed'}}},
      {type:'value',scale:true,show:activeTab.value==='成交量',splitLine:{show:false}},
    ],
    series
  }, true)
}

onMounted(() => {
  chart = echarts.init(klineChart.value)
  renderChart()
  window.addEventListener('resize',()=>chart?.resize())
})

watch(activeTab, renderChart)
onUnmounted(()=>chart?.dispose())
</script>
