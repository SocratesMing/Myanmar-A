<template>
  <div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">
      <div>
        <div class="page-title">大盘指数</div>
        <div class="page-subtitle">2026-04-28 14:35:00</div>
      </div>
    </div>

    <div class="stat-cards">
      <div v-for="idx in indices" :key="idx.name" class="stat-card index-card">
        <div class="idx-name">{{ idx.name }}</div>
        <div class="idx-value" :class="idx.change >= 0 ? 'rise' : 'fall'">{{ idx.value.toFixed(2) }}</div>
        <div class="idx-change" :class="idx.change >= 0 ? 'rise' : 'fall'">
          {{ idx.change >= 0 ? '+' : '' }}{{ idx.change.toFixed(2) }}
          ({{ idx.change >= 0 ? '+' : '' }}{{ idx.pct.toFixed(2) }}%)
        </div>
        <svg class="mini-chart" viewBox="0 0 120 40">
          <polyline :points="idx.sparkline" fill="none" :stroke="idx.change >= 0 ? '#e83951' : '#22c55e'" stroke-width="1.5"/>
        </svg>
      </div>
    </div>

    <div class="card">
      <div style="font-size:15px;font-weight:600;margin-bottom:12px">近5日指数走势对比</div>
      <div ref="trendChart" class="chart-container"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const trendChart = ref(null)
let chart = null

function genSparkline(base, vol) {
  const pts = []
  let v = base
  for (let i = 0; i < 20; i++) {
    v += (Math.random() - 0.48) * vol
    pts.push(`${i * 6},${40 - ((v - base) / vol) * 15 + 20}`)
  }
  return pts.join(' ')
}

const indices = ref([
  { name: '上证指数', value: 3387.56, change: 18.32, pct: 0.54, sparkline: genSparkline(3370, 30) },
  { name: '深证成指', value: 10245.23, change: -32.15, pct: -0.31, sparkline: genSparkline(10280, 60) },
  { name: '创业板指', value: 2056.78, change: 12.45, pct: 0.61, sparkline: genSparkline(2044, 25) },
  { name: '科创50', value: 987.34, change: -5.67, pct: -0.57, sparkline: genSparkline(993, 15) },
])

onMounted(() => {
  chart = echarts.init(trendChart.value)
  const dates = ['04-22', '04-23', '04-24', '04-25', '04-28']
  const genSeries = (base, vol) => {
    const d = []
    let v = base
    for (let i = 0; i < 5; i++) {
      const day = []
      for (let j = 0; j < 4; j++) {
        v += (Math.random() - 0.48) * vol
        day.push(v)
      }
      d.push(...day)
    }
    return d
  }
  chart.setOption({
    tooltip: { trigger: 'axis' },
    legend: { data: ['上证指数', '深证成指', '创业板指', '科创50'], top: 0 },
    grid: { top: 40, left: 50, right: 20, bottom: 30 },
    xAxis: {
      type: 'category',
      data: Array.from({ length: 20 }, (_, i) => `${dates[Math.floor(i / 4)]} ${9 + Math.floor((i % 4) * 1)}:00`),
      axisLabel: { fontSize: 10, rotate: 30 }
    },
    yAxis: { type: 'value', scale: true, splitLine: { lineStyle: { type: 'dashed' } } },
    series: [
      { name: '上证指数', type: 'line', data: genSeries(3370, 8), smooth: true, lineStyle: { width: 2 } },
      { name: '深证成指', type: 'line', data: genSeries(10280, 20), smooth: true, lineStyle: { width: 2 }, yAxisIndex: 0 },
      { name: '创业板指', type: 'line', data: genSeries(2044, 6), smooth: true, lineStyle: { width: 2 } },
      { name: '科创50', type: 'line', data: genSeries(993, 4), smooth: true, lineStyle: { width: 2 } },
    ]
  })
  window.addEventListener('resize', () => chart?.resize())
})

onUnmounted(() => {
  chart?.dispose()
})
</script>

<style scoped>
.index-card { position: relative; overflow: hidden; }
.idx-name { font-size: 13px; color: #8c8c8c; margin-bottom: 6px; }
.idx-value { font-size: 26px; font-weight: 700; }
.idx-change { font-size: 13px; margin-top: 4px; }
.mini-chart { width: 100%; height: 40px; margin-top: 8px; }
</style>
