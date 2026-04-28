<template>
  <div>
    <div class="page-title">个股涨跌分布</div>
    <div class="page-subtitle">2026-04-28 实时数据</div>

    <div class="stat-cards">
      <div class="stat-card"><div class="label">上涨家数</div><div class="value rise">2,856</div></div>
      <div class="stat-card"><div class="label">下跌家数</div><div class="value fall">1,923</div></div>
      <div class="stat-card"><div class="label">平盘家数</div><div class="value flat">345</div></div>
    </div>

    <div class="card">
      <div style="font-size:15px;font-weight:600;margin-bottom:12px">涨跌区间分布</div>
      <div ref="barChart" class="chart-container"></div>
    </div>

    <div class="card">
      <div style="font-size:15px;font-weight:600;margin-bottom:12px">涨跌占比</div>
      <div ref="pieChart" class="chart-container-sm"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const barChart = ref(null)
const pieChart = ref(null)
let bar = null, pie = null

const bins = [
  { label: '跌停', count: 45, color: '#16a34a' },
  { label: '-7%~', count: 78, color: '#22c55e' },
  { label: '-5%~', count: 156, color: '#4ade80' },
  { label: '-3%~', count: 312, color: '#86efac' },
  { label: '-1%~', count: 534, color: '#bbf7d0' },
  { label: '0', count: 345, color: '#d4d4d8' },
  { label: '1%~', count: 612, color: '#fecaca' },
  { label: '3%~', count: 487, color: '#f87171' },
  { label: '5%~', count: 298, color: '#ef4444' },
  { label: '7%~', count: 134, color: '#dc2626' },
  { label: '涨停', count: 89, color: '#b91c1c' },
]

onMounted(() => {
  bar = echarts.init(barChart.value)
  bar.setOption({
    tooltip: { trigger: 'axis' },
    grid: { top: 20, left: 50, right: 20, bottom: 40 },
    xAxis: { type: 'category', data: bins.map(b => b.label), axisLabel: { fontSize: 11 } },
    yAxis: { type: 'value', name: '家数', splitLine: { lineStyle: { type: 'dashed' } } },
    series: [{
      type: 'bar',
      data: bins.map(b => ({ value: b.count, itemStyle: { color: b.color } })),
      barWidth: '60%',
      label: { show: true, position: 'top', fontSize: 11 }
    }]
  })

  pie = echarts.init(pieChart.value)
  pie.setOption({
    tooltip: { trigger: 'item' },
    legend: { top: 0 },
    series: [{
      type: 'pie', radius: ['40%', '70%'], center: ['50%', '55%'],
      data: [
        { value: 2856, name: '上涨', itemStyle: { color: '#e83951' } },
        { value: 1923, name: '下跌', itemStyle: { color: '#22c55e' } },
        { value: 345, name: '平盘', itemStyle: { color: '#8c8c8c' } },
      ],
      label: { formatter: '{b}: {c} ({d}%)' }
    }]
  })

  window.addEventListener('resize', () => { bar?.resize(); pie?.resize() })
})

onUnmounted(() => { bar?.dispose(); pie?.dispose() })
</script>
