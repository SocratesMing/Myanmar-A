<template>
  <div>
    <div class="page-title">龙虎榜 — 机构席位</div>
    <div class="page-subtitle">2026-04-28 最新上榜数据</div>

    <div class="card" style="margin-bottom:16px">
      <table>
        <thead><tr><th>代码</th><th>名称</th><th>买入额(万)</th><th>卖出额(万)</th><th>净买额(万)</th><th>上榜原因</th></tr></thead>
        <tbody>
          <tr v-for="s in stocks" :key="s.code">
            <td>{{ s.code }}</td><td>{{ s.name }}</td>
            <td>{{ s.buy }}</td><td>{{ s.sell }}</td>
            <td :class="s.net>=0?'rise':'fall'">{{ s.net>=0?'+':'' }}{{ s.net }}</td>
            <td>{{ s.reason }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="card">
      <div style="font-size:15px;font-weight:600;margin-bottom:12px">机构净买入排名</div>
      <div ref="barChart" class="chart-container-sm"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const barChart = ref(null)
let chart = null

const stocks = [
  {code:'688981',name:'中芯国际',buy:'52,345',sell:'23,456',net:28889,reason:'涨幅偏离'},
  {code:'300750',name:'宁德时代',buy:'45,678',sell:'34,567',net:11111,reason:'换手率达20%'},
  {code:'002594',name:'比亚迪',buy:'38,901',sell:'28,345',net:10556,reason:'涨幅偏离'},
  {code:'002230',name:'科大讯飞',buy:'34,567',sell:'31,234',net:3333,reason:'连续涨停'},
  {code:'600276',name:'恒瑞医药',buy:'28,456',sell:'32,567',net:-4111,reason:'跌幅偏离'},
  {code:'601012',name:'隆基绿能',buy:'23,456',sell:'35,678',net:-12222,reason:'跌幅偏离'},
  {code:'300760',name:'迈瑞医疗',buy:'21,345',sell:'18,901',net:2444,reason:'换手率达20%'},
  {code:'002475',name:'立讯精密',buy:'19,876',sell:'25,432',net:-5556,reason:'跌幅偏离'},
]

onMounted(()=>{
  chart=echarts.init(barChart.value)
  const sorted=[...stocks].sort((a,b)=>b.net-a.net)
  chart.setOption({
    tooltip:{trigger:'axis',axisPointer:{type:'shadow'}},
    grid:{top:10,left:80,right:20,bottom:20},
    xAxis:{type:'value',name:'万元'},
    yAxis:{type:'category',data:sorted.map(s=>s.name)},
    series:[{type:'bar',data:sorted.map(s=>({value:s.net,itemStyle:{color:s.net>=0?'#e83951':'#22c55e'}})),label:{show:true,position:'right',formatter:p=>(p.value>=0?'+':'')+p.value}}]
  })
  window.addEventListener('resize',()=>chart?.resize())
})
onUnmounted(()=>chart?.dispose())
</script>
