<template>
  <div>
    <div class="page-title">机构盈利预测</div>
    <div class="page-subtitle">宁德时代 (300750) 机构预测汇总</div>

    <div class="card" style="margin-bottom:16px">
      <table>
        <thead><tr><th>机构</th><th>预测年度</th><th>预测营收(亿)</th><th>预测净利润(亿)</th><th>EPS</th><th>评级</th></tr></thead>
        <tbody>
          <tr v-for="f in forecasts" :key="f.inst+f.year">
            <td>{{ f.inst }}</td><td>{{ f.year }}</td><td>{{ f.rev }}</td><td>{{ f.profit }}</td><td>{{ f.eps }}</td>
            <td><span :style="{color:f.rating==='买入'?'#e83951':f.rating==='增持'?'#faad14':'#8c8c8c'}">{{ f.rating }}</span></td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="card">
      <div style="font-size:15px;font-weight:600;margin-bottom:12px">一致预期净利润增长率趋势</div>
      <div ref="barChart" class="chart-container-sm"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const barChart = ref(null)
let chart = null

const forecasts = [
  {inst:'中金公司',year:'2026E',rev:'5,678',profit:'567',eps:'23.45',rating:'买入'},
  {inst:'中信证券',year:'2026E',rev:'5,432',profit:'543',eps:'22.56',rating:'买入'},
  {inst:'国泰君安',year:'2026E',rev:'5,234',profit:'523',eps:'21.78',rating:'增持'},
  {inst:'华泰证券',year:'2026E',rev:'5,123',profit:'512',eps:'21.23',rating:'增持'},
  {inst:'招商证券',year:'2026E',rev:'5,012',profit:'501',eps:'20.89',rating:'买入'},
  {inst:'一致预期',year:'2026E',rev:'5,296',profit:'529',eps:'21.98',rating:'—'},
]

onMounted(()=>{
  chart=echarts.init(barChart.value)
  chart.setOption({
    tooltip:{trigger:'axis'},grid:{top:20,left:50,right:20,bottom:30},
    xAxis:{type:'category',data:['2024A','2025A','2026E']},
    yAxis:{type:'value',name:'增长率(%)',splitLine:{lineStyle:{type:'dashed'}}},
    series:[{type:'bar',data:[
      {value:25.3,itemStyle:{color:'#1890ff'}},
      {value:22.1,itemStyle:{color:'#1890ff'}},
      {value:28.7,itemStyle:{color:'#e83951'}}
    ],barWidth:'40%',label:{show:true,position:'top',formatter:'{c}%'}}]
  })
  window.addEventListener('resize',()=>chart?.resize())
})
onUnmounted(()=>chart?.dispose())
</script>
