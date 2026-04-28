<template>
  <div>
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:20px">
      <div class="page-title">热门板块</div>
      <span style="background:#e6f7ff;color:#1890ff;padding:2px 10px;border-radius:4px;font-size:12px">今日</span>
    </div>

    <div class="sector-grid">
      <div v-for="s in sectors" :key="s.name" class="sector-card" @click="openModal(s)">
        <div class="sector-header">
          <span class="sector-name">{{ s.name }}</span>
          <span class="sector-pct" :class="s.pct >= 0 ? 'rise' : 'fall'">{{ s.pct >= 0 ? '+' : '' }}{{ s.pct.toFixed(2) }}%</span>
        </div>
        <div class="sector-lead">领涨: {{ s.leadStock }} <span class="rise">+{{ s.leadPct }}%</span></div>
        <div class="sector-money">资金净流入: <span :class="s.flow >= 0 ? 'rise' : 'fall'">{{ s.flow >= 0 ? '+' : '' }}{{ s.flow.toFixed(1) }}亿</span></div>
        <svg class="mini-trend" viewBox="0 0 100 30">
          <polyline :points="s.trend" fill="none" :stroke="s.pct >= 0 ? '#e83951' : '#22c55e'" stroke-width="1.5"/>
        </svg>
      </div>
    </div>

    <div v-if="modalVisible" class="modal-overlay" @click.self="modalVisible = false">
      <div class="modal-content">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
          <div style="font-size:18px;font-weight:600">{{ modalData?.name }} - 板块详情</div>
          <span style="cursor:pointer;font-size:20px" @click="modalVisible = false">&times;</span>
        </div>
        <table>
          <thead><tr><th>代码</th><th>名称</th><th>涨跌幅</th><th>资金流入</th></tr></thead>
          <tbody>
            <tr v-for="s in modalData?.top5" :key="s.code">
              <td>{{ s.code }}</td><td>{{ s.name }}</td>
              <td :class="s.pct >= 0 ? 'rise' : 'fall'">{{ s.pct >= 0 ? '+' : '' }}{{ s.pct }}%</td>
              <td :class="s.flow >= 0 ? 'rise' : 'fall'">{{ s.flow >= 0 ? '+' : '' }}{{ s.flow }}亿</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

function genTrend() {
  const pts = []
  let y = 15
  for (let i = 0; i < 10; i++) {
    y += (Math.random() - 0.45) * 5
    y = Math.max(3, Math.min(27, y))
    pts.push(`${i * 10},${30 - y}`)
  }
  return pts.join(' ')
}

const sectors = ref([
  { name: '半导体', pct: 3.82, leadStock: '中芯国际', leadPct: 6.21, flow: 28.5, trend: genTrend(), top5: [
    { code: '688981', name: '中芯国际', pct: 6.21, flow: 5.2 }, { code: '002371', name: '北方华创', pct: 5.18, flow: 3.8 },
    { code: '603501', name: '韦尔股份', pct: 4.56, flow: 2.1 }, { code: '688012', name: '中微公司', pct: 3.89, flow: 1.9 },
    { code: '300661', name: '圣邦股份', pct: 3.45, flow: 1.5 }
  ]},
  { name: '人工智能', pct: 2.95, leadStock: '科大讯飞', leadPct: 5.34, flow: 22.3, trend: genTrend(), top5: [
    { code: '002230', name: '科大讯飞', pct: 5.34, flow: 4.1 }, { code: '688787', name: '海天瑞声', pct: 4.89, flow: 2.3 },
    { code: '300454', name: '深信服', pct: 3.67, flow: 1.8 }, { code: '688208', name: '道通科技', pct: 3.21, flow: 1.5 },
    { code: '002415', name: '海康威视', pct: 2.98, flow: 1.2 }
  ]},
  { name: '新能源汽车', pct: 2.45, leadStock: '比亚迪', leadPct: 4.12, flow: 18.7, trend: genTrend(), top5: [
    { code: '002594', name: '比亚迪', pct: 4.12, flow: 6.3 }, { code: '300750', name: '宁德时代', pct: 3.56, flow: 4.2 },
    { code: '688599', name: '天合光能', pct: 2.89, flow: 1.7 }, { code: '002460', name: '赣锋锂业', pct: 2.34, flow: 1.1 },
    { code: '300014', name: '亿纬锂能', pct: 1.98, flow: 0.8 }
  ]},
  { name: '光伏', pct: -1.23, leadStock: '隆基绿能', leadPct: 1.56, flow: -12.4, trend: genTrend(), top5: [
    { code: '601012', name: '隆基绿能', pct: 1.56, flow: 1.2 }, { code: '688599', name: '天合光能', pct: -0.89, flow: -1.5 },
    { code: '002459', name: '晶澳科技', pct: -1.34, flow: -2.1 }, { code: '601865', name: '福莱特', pct: -2.01, flow: -1.8 },
    { code: '688223', name: '晶科能源', pct: -2.56, flow: -2.3 }
  ]},
  { name: '创新药', pct: 1.87, leadStock: '恒瑞医药', leadPct: 3.45, flow: 15.2, trend: genTrend(), top5: [
    { code: '600276', name: '恒瑞医药', pct: 3.45, flow: 3.8 }, { code: '300760', name: '迈瑞医疗', pct: 2.12, flow: 2.1 },
    { code: '688180', name: '君实生物', pct: 1.89, flow: 1.5 }, { code: '300347', name: '泰格医药', pct: 1.23, flow: 0.9 },
    { code: '002821', name: '凯莱英', pct: 0.78, flow: 0.5 }
  ]},
  { name: '消费电子', pct: 1.56, leadStock: '立讯精密', leadPct: 3.12, flow: 10.8, trend: genTrend(), top5: [
    { code: '002475', name: '立讯精密', pct: 3.12, flow: 2.5 }, { code: '002241', name: '歌尔股份', pct: 2.34, flow: 1.8 },
    { code: '600584', name: '长电科技', pct: 1.67, flow: 1.2 }, { code: '002371', name: '北方华创', pct: 1.23, flow: 0.9 },
    { code: '300433', name: '蓝思科技', pct: 0.89, flow: 0.6 }
  ]},
])

const modalVisible = ref(false)
const modalData = ref(null)

function openModal(sector) {
  modalData.value = sector
  modalVisible.value = true
}
</script>

<style scoped>
.sector-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
.sector-card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  padding: 16px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}
.sector-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(0,0,0,0.12);
}
.sector-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.sector-name { font-size: 15px; font-weight: 600; color: #1a1a2e; }
.sector-pct { font-size: 16px; font-weight: 700; }
.sector-lead { font-size: 12px; color: #8c8c8c; margin-bottom: 4px; }
.sector-money { font-size: 12px; color: #8c8c8c; margin-bottom: 8px; }
.mini-trend { width: 100%; height: 30px; }
.modal-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; z-index: 1000;
}
.modal-content {
  background: #fff; border-radius: 12px; padding: 24px; width: 600px; max-height: 80vh; overflow-y: auto;
}
</style>
