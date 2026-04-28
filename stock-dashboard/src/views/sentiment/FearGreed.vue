<template>
  <div>
    <div class="page-title">恐惧与贪婪指数</div>
    <div class="page-subtitle">市场情绪综合指标</div>

    <div class="card" style="text-align:center;margin-bottom:16px;padding:40px">
      <div class="gauge-wrapper">
        <div class="gauge-dial">
          <div class="gauge-track"></div>
          <div class="gauge-needle" style="--angle:117deg"></div>
          <div class="gauge-center"></div>
        </div>
        <div style="font-size:48px;font-weight:700;color:#e83951;margin-top:16px">65</div>
        <div style="font-size:16px;color:#e83951;font-weight:600;margin-top:4px">贪婪</div>
      </div>
      <div style="margin-top:20px;font-size:14px;color:#8c8c8c;max-width:400px;margin-left:auto;margin-right:auto">
        市场偏贪婪，需注意回调风险。当前指数高于70%的历史交易日，建议谨慎追高。
      </div>
    </div>

    <div class="card">
      <div style="font-size:15px;font-weight:600;margin-bottom:12px">近30日恐惧贪婪指数</div>
      <div ref="lineChart" class="chart-container"></div>
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
  const dates=Array.from({length:30},(_,i)=>`03-${String(29+i>31?29+i-31:29+i).padStart(2,'0')}`)
  const data=[42,45,48,52,55,53,50,48,52,56,58,55,52,50,53,56,58,62,60,58,55,58,62,65,63,60,58,62,65,65]
  chart.setOption({
    tooltip:{trigger:'axis'},grid:{top:20,left:50,right:20,bottom:30},
    xAxis:{type:'category',data:dates,axisLabel:{fontSize:10,rotate:30}},
    yAxis:{type:'value',min:0,max:100,name:'指数',splitLine:{lineStyle:{type:'dashed'}}},
    visualMap:{show:false,dimension:0,pieces:[{lt:25,color:'#22c55e'},{gte:25,lt:45,color:'#4ade80'},{gte:45,lt:55,color:'#faad14'},{gte:55,lt:75,color:'#f87171'},{gte:75,color:'#e83951'}]},
    series:[{type:'line',data,smooth:true,lineStyle:{width:2},markLine:{data:[{yAxis:25,name:'极度恐惧',lineStyle:{color:'#22c55e'}},{yAxis:75,name:'极度贪婪',lineStyle:{color:'#e83951'}}]}}]
  })
  window.addEventListener('resize',()=>chart?.resize())
})
onUnmounted(()=>chart?.dispose())
</script>

<style scoped>
.gauge-wrapper { display:inline-block }
.gauge-dial { position:relative; width:240px; height:130px; margin:0 auto }
.gauge-track { width:240px; height:240px; border-radius:50%; background:conic-gradient(from 180deg, #22c55e 0deg, #4ade80 36deg, #faad14 72deg, #f87171 108deg, #e83951 144deg, #b91c1c 180deg); clip-path:polygon(0 0, 100% 0, 100% 55%, 0 55%) }
.gauge-needle { position:absolute; bottom:10px; left:50%; width:3px; height:90px; background:#333; transform-origin:bottom center; transform:rotate(var(--angle)); border-radius:2px; margin-left:-1.5px }
.gauge-center { position:absolute; bottom:5px; left:50%; width:16px; height:16px; background:#333; border-radius:50%; transform:translateX(-50%) }
</style>
