<template>
  <div>
    <div class="page-title">大宗交易</div>
    <div class="page-subtitle">近期大宗交易记录</div>

    <div class="card" style="margin-bottom:16px">
      <table>
        <thead><tr><th>日期</th><th>股票</th><th>成交价</th><th>成交额(万)</th><th>溢价率</th></tr></thead>
        <tbody>
          <tr v-for="t in trades" :key="t.date+t.stock">
            <td>{{ t.date }}</td><td>{{ t.stock }}</td><td>{{ t.price }}</td><td>{{ t.amount }}</td>
            <td :class="t.premium>=0?'rise':'fall'">{{ t.premium>=0?'+':'' }}{{ t.premium }}%</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="card">
      <div style="font-size:15px;font-weight:600;margin-bottom:12px">溢价率分布</div>
      <div ref="pieChart" class="chart-container-sm"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const pieChart = ref(null)
let chart = null

const trades = [
  {date:'2026-04-28',stock:'贵州茅台',price:'1,680.00',amount:'33,600',premium:0.48},
  {date:'2026-04-28',stock:'宁德时代',price:'232.50',amount:'18,600',premium:-0.89},
  {date:'2026-04-25',stock:'比亚迪',price:'276.80',amount:'13,840',premium:0.75},
  {date:'2026-04-25',stock:'中国平安',price:'47.90',amount:'9,580',premium:-1.23},
  {date:'2026-04-24',stock:'招商银行',price:'35.40',amount:'17,700',premium:0.28},
  {date:'2026-04-24',stock:'五粮液',price:'155.60',amount:'7,780',premium:-0.45},
  {date:'2026-04-23',stock:'恒瑞医药',price:'45.30',amount:'4,530',premium:1.12},
  {date:'2026-04-23',stock:'隆基绿能',price:'23.10',amount:'11,550',premium:-2.34},
  {date:'2026-04-22',stock:'立讯精密',price:'38.50',amount:'7,700',premium:0.65},
  {date:'2026-04-22',stock:'万科A',price:'8.90',amount:'8,900',premium:-3.56},
]

onMounted(()=>{
  chart=echarts.init(pieChart.value)
  chart.setOption({
    tooltip:{trigger:'item'},
    series:[{
      type:'pie',radius:['40%','70%'],
      data:[
        {value:4,name:'溢价成交',itemStyle:{color:'#e83951'}},
        {value:5,name:'折价成交',itemStyle:{color:'#22c55e'}},
        {value:1,name:'平价成交',itemStyle:{color:'#8c8c8c'}},
      ],
      label:{formatter:'{b}: {c}笔 ({d}%)'}
    }]
  })
  window.addEventListener('resize',()=>chart?.resize())
})
onUnmounted(()=>chart?.dispose())
</script>
