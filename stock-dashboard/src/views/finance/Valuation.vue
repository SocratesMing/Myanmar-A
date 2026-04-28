<template>
  <div>
    <div class="page-title">估值分析</div>
    <div class="page-subtitle">宁德时代 (300750) 估值指标与行业对比</div>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px">
      <div class="card">
        <div style="font-size:15px;font-weight:600;margin-bottom:16px">当前估值</div>
        <div v-for="v in valuations" :key="v.label" style="display:flex;align-items:center;margin-bottom:12px">
          <span style="width:60px;font-size:13px;color:#8c8c8c">{{ v.label }}</span>
          <span style="width:60px;font-size:15px;font-weight:600">{{ v.value }}</span>
          <div style="flex:1;margin:0 12px;height:8px;background:#f0f0f0;border-radius:4px;position:relative">
            <div :style="{width:v.pct+'%',background:'#1890ff',height:'100%',borderRadius:'4px'}"></div>
          </div>
          <span style="font-size:12px;color:#8c8c8c">{{ v.pct }}%分位</span>
        </div>
      </div>
      <div class="card">
        <div style="font-size:15px;font-weight:600;margin-bottom:16px">行业平均对比</div>
        <div v-for="v in valuations" :key="v.label" style="display:flex;align-items:center;margin-bottom:12px">
          <span style="width:60px;font-size:13px;color:#8c8c8c">{{ v.label }}</span>
          <span style="width:60px;font-size:14px">{{ v.industry }}</span>
          <span :class="v.value>v.industry?'rise':'fall'" style="font-size:12px;margin-left:8px">
            {{ v.value > v.industry ? '↑高于' : '↓低于' }}行业
          </span>
        </div>
      </div>
    </div>

    <div class="card">
      <div style="font-size:15px;font-weight:600;margin-bottom:12px">PE Band（近5年）</div>
      <div ref="peBandChart" class="chart-container"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const peBandChart = ref(null)
let chart = null

const valuations = [
  {label:'PE',value:45.2,industry:32.5,pct:78},
  {label:'PB',value:8.9,industry:5.6,pct:72},
  {label:'PS',value:3.8,industry:2.4,pct:65},
  {label:'PCF',value:28.6,industry:18.3,pct:58},
]

onMounted(()=>{
  chart=echarts.init(peBandChart.value)
  const dates=Array.from({length:60},(_,i)=>{const y=2021+Math.floor(i/12);return `${y}-${String(i%12+1).padStart(2,'0')}`})
  let v=180
  const price=dates.map(()=>{v+=(Math.random()-0.45)*15;return +v.toFixed(2)})
  const band95=price.map(p=>p*1.35)
  const band75=price.map(p=>p*1.2)
  const band50=price.map(p=>p*1.05)
  const band25=price.map(p=>p*0.9)
  const band5=price.map(p=>p*0.75)
  chart.setOption({
    tooltip:{trigger:'axis'},legend:{data:['股价','95%分位','75%分位','50%分位','25%分位','5%分位'],top:0},
    grid:{top:40,left:60,right:20,bottom:30},
    xAxis:{type:'category',data:dates,axisLabel:{fontSize:10,rotate:30}},
    yAxis:{type:'value',scale:true},
    series:[
      {name:'股价',type:'line',data:price,smooth:true,lineStyle:{width:2,color:'#1890ff'}},
      {name:'95%分位',type:'line',data:band95,smooth:true,lineStyle:{width:1,type:'dashed',color:'#e83951'},symbol:'none'},
      {name:'75%分位',type:'line',data:band75,smooth:true,lineStyle:{width:1,type:'dashed',color:'#faad14'},symbol:'none'},
      {name:'50%分位',type:'line',data:band50,smooth:true,lineStyle:{width:1,type:'dashed',color:'#8c8c8c'},symbol:'none'},
      {name:'25%分位',type:'line',data:band25,smooth:true,lineStyle:{width:1,type:'dashed',color:'#52c41a'},symbol:'none'},
      {name:'5%分位',type:'line',data:band5,smooth:true,lineStyle:{width:1,type:'dashed',color:'#22c55e'},symbol:'none'},
    ]
  })
  window.addEventListener('resize',()=>chart?.resize())
})
onUnmounted(()=>chart?.dispose())
</script>
