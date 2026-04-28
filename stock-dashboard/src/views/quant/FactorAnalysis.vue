<template>
  <div>
    <div class="page-title">因子监控</div>
    <div class="page-subtitle">常用量化因子近期表现</div>

    <div class="card" style="margin-bottom:16px">
      <div style="font-size:15px;font-weight:600;margin-bottom:12px">因子多空组合近1月收益率</div>
      <div ref="barChart" class="chart-container"></div>
    </div>

    <div class="card" style="margin-bottom:16px">
      <div style="font-size:15px;font-weight:600;margin-bottom:12px">IC值表格</div>
      <table>
        <thead><tr><th>因子</th><th>IC均值</th><th>IC标准差</th><th>ICIR</th><th>t值</th><th>胜率</th></tr></thead>
        <tbody>
          <tr v-for="f in factors" :key="f.name">
            <td>{{ f.name }}</td>
            <td :class="f.icMean>=0?'rise':'fall'">{{ f.icMean }}</td>
            <td>{{ f.icStd }}</td>
            <td>{{ f.icir }}</td>
            <td>{{ f.tval }}</td>
            <td>{{ f.winRate }}%</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="card">
      <div style="font-size:15px;font-weight:600;margin-bottom:12px">累计IC曲线</div>
      <div ref="icChart" class="chart-container-sm"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const barChart = ref(null)
const icChart = ref(null)
let bar = null, ic = null

const factors = [
  {name:'市值因子',icMean:0.032,icStd:0.108,icir:0.296,tval:2.15,winRate:58.3},
  {name:'动量因子',icMean:0.045,icStd:0.125,icir:0.360,tval:2.67,winRate:61.2},
  {name:'价值因子',icMean:0.028,icStd:0.098,icir:0.286,tval:1.98,winRate:55.6},
  {name:'波动率因子',icMean:-0.018,icStd:0.089,icir:-0.202,tval:-1.56,winRate:43.5},
  {name:'流动性因子',icMean:-0.025,icStd:0.102,icir:-0.245,tval:-1.89,winRate:41.2},
  {name:'质量因子',icMean:0.038,icStd:0.112,icir:0.339,tval:2.43,winRate:59.8},
  {name:'成长因子',icMean:0.041,icStd:0.118,icir:0.347,tval:2.52,winRate:60.5},
]

onMounted(()=>{
  bar=echarts.init(barChart.value)
  const sorted=[...factors].sort((a,b)=>b.icMean-a.icMean)
  bar.setOption({
    tooltip:{trigger:'axis',axisPointer:{type:'shadow'}},
    grid:{top:10,left:80,right:20,bottom:20},
    xAxis:{type:'value',name:'收益率(%)'},
    yAxis:{type:'category',data:sorted.map(f=>f.name)},
    series:[{type:'bar',data:sorted.map(f=>({value:+(f.icMean*100*30).toFixed(2),itemStyle:{color:f.icMean>=0?'#e83951':'#22c55e'}})),label:{show:true,position:'right',formatter:'{c}%'}}]
  })

  ic=echarts.init(icChart.value)
  const dates=Array.from({length:20},(_,i)=>`04-${String(i+9).padStart(2,'0')}`)
  const genCumIC=(base)=>{let v=0;return dates.map(()=>{v+=(Math.random()-0.45)*0.01;return +v.toFixed(4)})}
  ic.setOption({
    tooltip:{trigger:'axis'},legend:{data:factors.map(f=>f.name).slice(0,4),top:0},
    grid:{top:40,left:50,right:20,bottom:30},
    xAxis:{type:'category',data:dates},yAxis:{type:'value',name:'累计IC'},
    series:factors.slice(0,4).map(f=>({name:f.name,type:'line',data:genCumIC(f.icMean),smooth:true,lineStyle:{width:1.5},symbol:'none'}))
  })

  window.addEventListener('resize',()=>{bar?.resize();ic?.resize()})
})
onUnmounted(()=>{bar?.dispose();ic?.dispose()})
</script>
