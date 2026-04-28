<template>
  <div>
    <div class="page-title">主力资金流向</div>
    <div class="page-subtitle">板块及个股主力资金净流入排名</div>

    <div style="display:flex;gap:8px;margin-bottom:16px">
      <button v-for="t in ['板块','个股']" :key="t" @click="tab=t"
        :style="{padding:'4px 12px',border:'1px solid #d9d9d9',borderRadius:'4px',background:tab===t?'#1890ff':'#fff',color:tab===t?'#fff':'#333',cursor:'pointer'}">{{ t }}</button>
    </div>

    <div class="card">
      <div ref="barChart" class="chart-container"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'

const barChart = ref(null)
const tab = ref('板块')
let chart = null

const sectors = [
  {name:'半导体',amount:28.5,ratio:'12.3%'},{name:'人工智能',amount:22.3,ratio:'9.8%'},
  {name:'新能源汽车',amount:18.7,ratio:'8.1%'},{name:'创新药',amount:15.2,ratio:'6.5%'},
  {name:'消费电子',amount:10.8,ratio:'4.7%'},{name:'军工',amount:8.5,ratio:'3.9%'},
  {name:'白酒',amount:-5.2,ratio:'-2.3%'},{name:'房地产',amount:-12.4,ratio:'-5.6%'},
  {name:'银行',amount:-8.7,ratio:'-3.8%'},{name:'钢铁',amount:-6.3,ratio:'-2.9%'},
]
const stocks = [
  {name:'中芯国际',amount:5.2,ratio:'3.1%'},{name:'宁德时代',amount:4.8,ratio:'2.8%'},
  {name:'比亚迪',amount:4.2,ratio:'2.5%'},{name:'贵州茅台',amount:3.5,ratio:'1.9%'},
  {name:'科大讯飞',amount:3.1,ratio:'1.7%'},{name:'北方华创',amount:2.8,ratio:'1.5%'},
  {name:'万科A',amount:-3.4,ratio:'-1.8%'},{name:'平安银行',amount:-2.9,ratio:'-1.5%'},
  {name:'中信证券',amount:-2.3,ratio:'-1.2%'},{name:'海通证券',amount:-1.8,ratio:'-0.9%'},
]

function render() {
  if (!chart) return
  const d = tab.value === '板块' ? sectors : stocks
  const sorted = [...d].sort((a,b)=>a.amount-b.amount)
  chart.setOption({
    tooltip:{trigger:'axis',axisPointer:{type:'shadow'}},
    grid:{top:10,left:100,right:80,bottom:20},
    xAxis:{type:'value',name:'亿元'},
    yAxis:{type:'category',data:sorted.map(s=>s.name),axisLabel:{fontSize:12}},
    series:[{
      type:'bar',data:sorted.map(s=>({value:s.amount,itemStyle:{color:s.amount>=0?'#e83951':'#22c55e'}})),
      label:{show:true,position:'right',formatter:p=>`${p.value>=0?'+':''}${p.value}亿 (${sorted[p.dataIndex].ratio})`,fontSize:11}
    }]
  }, true)
}

onMounted(()=>{chart=echarts.init(barChart.value);render();window.addEventListener('resize',()=>chart?.resize())})
watch(tab, render)
onUnmounted(()=>chart?.dispose())
</script>
