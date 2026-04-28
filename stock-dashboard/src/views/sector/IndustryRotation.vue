<template>
  <div>
    <div class="page-title">行业轮动热力图</div>
    <div class="page-subtitle">近5个交易日申万一级行业涨跌热力</div>

    <div style="display:flex;gap:16px">
      <div class="card" style="flex:1">
        <div ref="heatmap" class="chart-container"></div>
      </div>
      <div style="width:200px">
        <div class="stat-card">
          <div class="label">轮动速度</div>
          <div class="value" style="font-size:28px;color:#1890ff">0.76</div>
          <div style="font-size:13px;color:#faad14;margin-top:4px">较快</div>
        </div>
        <div class="stat-card" style="margin-top:12px">
          <div class="label">领涨行业</div>
          <div style="font-size:15px;font-weight:600;margin-top:4px" class="rise">半导体</div>
        </div>
        <div class="stat-card" style="margin-top:12px">
          <div class="label">领跌行业</div>
          <div style="font-size:15px;font-weight:600;margin-top:4px" class="fall">房地产</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const heatmap = ref(null)
let chart = null

const industries = ['电子','计算机','传媒','通信','电力设备','汽车','机械设备','国防军工','医药生物','食品饮料','家用电器','纺织服饰','轻工制造','商贸零售','社会服务','银行','非银金融','房地产','建筑材料','建筑装饰','钢铁','煤炭','石油石化','有色金属','基础化工','农林牧渔','公用事业','交通运输']
const dates = ['04-22','04-23','04-24','04-25','04-28']

onMounted(() => {
  chart = echarts.init(heatmap.value)
  const data = []
  industries.forEach((ind, i) => {
    dates.forEach((_, j) => {
      data.push([j, i, +(Math.random() * 8 - 3).toFixed(2)])
    })
  })
  chart.setOption({
    tooltip: { formatter: p => `${industries[p.data[1]]}<br/>${dates[p.data[0]]}: ${p.data[2]}%` },
    grid: { top: 10, left: 100, right: 40, bottom: 30 },
    xAxis: { type: 'category', data: dates, splitArea: { show: true } },
    yAxis: { type: 'category', data: industries, axisLabel: { fontSize: 10 } },
    visualMap: { min: -3, max: 5, calculable: true, orient: 'horizontal', left: 'center', bottom: -10, inRange: { color: ['#22c55e', '#f0f0f0', '#e83951'] }, show: false },
    series: [{ type: 'heatmap', data, label: { show: true, fontSize: 9, formatter: p => p.data[2] + '%' }, emphasis: { itemStyle: { shadowBlur: 10, shadowColor: 'rgba(0,0,0,0.3)' } } }]
  })
  window.addEventListener('resize', () => chart?.resize())
})

onUnmounted(() => chart?.dispose())
</script>
