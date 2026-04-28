<template>
  <div>
    <div class="page-title">个股筛选</div>
    <div class="page-subtitle">根据条件筛选A股标的</div>

    <div class="card" style="margin-bottom:16px">
      <div style="display:flex;gap:16px;flex-wrap:wrap;align-items:center">
        <div><label style="font-size:12px;color:#8c8c8c">行业</label><select v-model="filter.industry" style="margin-left:6px;padding:4px 8px;border:1px solid #d9d9d9;border-radius:4px">
          <option value="all">全部</option><option value="科技">科技</option><option value="消费">消费</option><option value="医药">医药</option><option value="制造">制造</option>
        </select></div>
        <div><label style="font-size:12px;color:#8c8c8c">涨跌</label>
          <label v-for="o in ['all','up','down']" :key="o" style="margin-left:8px;font-size:13px;cursor:pointer">
            <input type="radio" :value="o" v-model="filter.direction" /> {{ {all:'全部',up:'上涨',down:'下跌'}[o] }}
          </label>
        </div>
        <div><label style="font-size:12px;color:#8c8c8c">PE范围</label>
          <input v-model.number="filter.peMin" type="number" placeholder="最低" style="width:60px;margin-left:6px;padding:4px;border:1px solid #d9d9d9;border-radius:4px" />
          <span style="margin:0 4px">-</span>
          <input v-model.number="filter.peMax" type="number" placeholder="最高" style="width:60px;padding:4px;border:1px solid #d9d9d9;border-radius:4px" />
        </div>
      </div>
    </div>

    <div class="card">
      <table>
        <thead><tr><th>代码</th><th>名称</th><th>最新价</th><th>涨跌幅</th><th>成交量(万手)</th><th>市值(亿)</th><th>行业</th><th>PE(TTM)</th></tr></thead>
        <tbody>
          <tr v-for="s in pagedStocks" :key="s.code" @click="openDrawer(s)" style="cursor:pointer">
            <td>{{ s.code }}</td><td>{{ s.name }}</td>
            <td>{{ s.price }}</td>
            <td :class="s.pct >= 0 ? 'rise' : 'fall'">{{ s.pct >= 0 ? '+' : '' }}{{ s.pct }}%</td>
            <td>{{ s.vol }}</td><td>{{ s.mv }}</td><td>{{ s.ind }}</td><td>{{ s.pe }}</td>
          </tr>
        </tbody>
      </table>
      <div style="display:flex;justify-content:center;gap:8px;margin-top:16px">
        <button v-for="p in totalPages" :key="p" @click="page = p"
          :style="{padding:'4px 12px',border:'1px solid #d9d9d9',borderRadius:'4px',background:page===p?'#1890ff':'#fff',color:page===p?'#fff':'#333',cursor:'pointer'}">{{ p }}</button>
      </div>
    </div>

    <div v-if="drawerVisible" class="drawer-overlay" @click.self="drawerVisible = false">
      <div class="drawer">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
          <div style="font-size:16px;font-weight:600">{{ drawerData?.name }} ({{ drawerData?.code }})</div>
          <span style="cursor:pointer;font-size:18px" @click="drawerVisible = false">&times;</span>
        </div>
        <div style="font-size:13px;color:#8c8c8c;margin-bottom:12px">分时走势</div>
        <div style="background:#f5f5f5;border-radius:4px;height:120px;display:flex;align-items:center;justify-content:center;color:#bbb">分时图占位</div>
        <div style="margin-top:16px;font-size:13px;color:#8c8c8c;margin-bottom:8px">五档盘口</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:4px;font-size:12px">
          <div v-for="i in 5" :key="'s'+i" style="display:flex;justify-content:space-between;padding:2px 8px">
            <span class="fall">卖{{ 6-i }}</span><span>{{ (drawerData?.price - 0.01*i).toFixed(2) }}</span>
          </div>
          <div v-for="i in 5" :key="'b'+i" style="display:flex;justify-content:space-between;padding:2px 8px">
            <span class="rise">买{{ i }}</span><span>{{ (drawerData?.price + 0.01*i).toFixed(2) }}</span>
          </div>
        </div>
        <div style="margin-top:16px;font-size:13px;color:#8c8c8c;margin-bottom:8px">财务亮点</div>
        <div style="font-size:12px;color:#595959;line-height:1.8">
          ROE: {{ (15 + Math.random()*10).toFixed(1) }}% | 毛利率: {{ (30 + Math.random()*20).toFixed(1) }}% | 净利率: {{ (10 + Math.random()*10).toFixed(1) }}%
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const filter = ref({ industry: 'all', direction: 'all', peMin: null, peMax: null })
const page = ref(1)
const pageSize = 10

const allStocks = Array.from({ length: 15 }, (_, i) => ({
  code: ['600519','000858','300750','601318','000001','002594','600276','601012','002475','300760','688981','002230','600036','000651','603259'][i],
  name: ['贵州茅台','五粮液','宁德时代','中国平安','平安银行','比亚迪','恒瑞医药','隆基绿能','立讯精密','迈瑞医疗','中芯国际','科大讯飞','招商银行','格力电器','药明康德'][i],
  price: [1688.00, 156.32, 234.56, 48.23, 12.45, 278.90, 45.67, 23.45, 38.90, 289.34, 56.78, 52.34, 35.67, 42.18, 68.45][i],
  pct: [1.23, -0.56, 2.34, 0.89, -1.12, 3.45, 1.56, -2.34, 0.67, 1.89, 4.12, 2.78, 0.34, -0.89, -1.56][i],
  vol: [3.2, 8.5, 12.3, 15.6, 22.1, 6.7, 4.5, 9.8, 7.2, 2.1, 5.6, 8.9, 11.2, 6.3, 3.8][i],
  mv: [21200, 6080, 10200, 8800, 2420, 8100, 2920, 1780, 2780, 3500, 4500, 1220, 8960, 2530, 2020][i],
  ind: ['消费','消费','制造','金融','金融','制造','医药','制造','科技','医药','科技','科技','金融','消费','医药'][i],
  pe: [32.5, 24.8, 45.2, 8.9, 5.6, 38.7, 52.3, 18.9, 35.6, 48.2, 67.8, 89.3, 6.7, 12.3, 42.1][i],
}))

const filtered = computed(() => {
  return allStocks.filter(s => {
    if (filter.value.industry !== 'all' && s.ind !== filter.value.industry) return false
    if (filter.value.direction === 'up' && s.pct < 0) return false
    if (filter.value.direction === 'down' && s.pct >= 0) return false
    if (filter.value.peMin && s.pe < filter.value.peMin) return false
    if (filter.value.peMax && s.pe > filter.value.peMax) return false
    return true
  })
})

const totalPages = computed(() => Math.ceil(filtered.value.length / pageSize) || 1)
const pagedStocks = computed(() => filtered.value.slice((page.value - 1) * pageSize, page.value * pageSize))

const drawerVisible = ref(false)
const drawerData = ref(null)
function openDrawer(s) { drawerData.value = s; drawerVisible.value = true }
</script>

<style scoped>
.drawer-overlay { position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.3);z-index:1000;display:flex;justify-content:flex-end }
.drawer { background:#fff;width:380px;height:100vh;padding:24px;overflow-y:auto;box-shadow:-4px 0 12px rgba(0,0,0,0.1) }
</style>
