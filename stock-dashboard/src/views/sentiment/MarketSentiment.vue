<template>
  <div>
    <div class="page-title">市场情绪仪表</div>
    <div class="page-subtitle">2026-04-28 实时情绪监控</div>

    <div class="stat-cards">
      <div class="stat-card">
        <div class="label">上涨/下跌家数</div>
        <div style="display:flex;align-items:center;gap:8px;margin-top:8px">
          <span class="rise" style="font-weight:700">2,856</span>
          <div style="flex:1;height:8px;background:#22c55e;border-radius:4px;position:relative;overflow:hidden">
            <div style="width:60%;height:100%;background:#e83951;border-radius:4px"></div>
          </div>
          <span class="fall" style="font-weight:700">1,923</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="label">涨停/跌停家数</div>
        <div style="margin-top:8px"><span class="rise" style="font-size:24px;font-weight:700">89</span> / <span class="fall" style="font-size:24px;font-weight:700">45</span></div>
      </div>
      <div class="stat-card">
        <div class="label">炸板率</div>
        <div style="font-size:24px;font-weight:700;color:#faad14;margin-top:8px">28%</div>
      </div>
    </div>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
      <div class="card">
        <div style="font-size:15px;font-weight:600;margin-bottom:12px">市场温度计</div>
        <div style="display:flex;justify-content:center">
          <div class="gauge">
            <div class="gauge-bg"></div>
            <div class="gauge-fill" style="--temp:62"></div>
            <div class="gauge-value">62°</div>
            <div class="gauge-label">偏热</div>
          </div>
        </div>
      </div>
      <div class="card">
        <div style="font-size:15px;font-weight:600;margin-bottom:12px">近10日情绪波动</div>
        <div ref="lineChart" class="chart-container-sm"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const lineChart = ref(null)
let chart = null

onMounted(()=>{
  chart=echarts.init(lineChart.value)
  const dates=Array.from({length:10},(_,i)=>`04-${String(19+i).padStart(2,'0')}`)
  chart.setOption({
    tooltip:{trigger:'axis'},grid:{top:20,left:40,right:20,bottom:30},
    xAxis:{type:'category',data:dates},yAxis:{type:'value',min:0,max:100,name:'温度'},
    series:[{type:'line',data:[45,52,48,55,62,58,65,60,58,62],smooth:true,areaStyle:{color:'rgba(232,57,81,0.1)'},lineStyle:{color:'#e83951'}}]
  })
  window.addEventListener('resize',()=>chart?.resize())
})
onUnmounted(()=>chart?.dispose())
</script>

<style scoped>
.gauge { position:relative; width:200px; height:120px; overflow:hidden; }
.gauge-bg { width:200px; height:200px; border-radius:50%; background:conic-gradient(from 180deg, #22c55e 0deg, #faad14 90deg, #e83951 180deg); clip-path:polygon(0 0, 100% 0, 100% 50%, 0 50%); }
.gauge-fill { position:absolute; bottom:0; left:0; width:200px; height:100px; background:#fff; border-radius:0 0 100px 100px; }
.gauge-value { position:absolute; top:55%; left:50%; transform:translate(-50%,-50%); font-size:36px; font-weight:700; color:#e83951; }
.gauge-label { position:absolute; top:75%; left:50%; transform:translate(-50%,-50%); font-size:14px; color:#8c8c8c; }
</style>
