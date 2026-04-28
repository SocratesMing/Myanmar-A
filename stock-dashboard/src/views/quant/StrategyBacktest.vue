<template>
  <div>
    <div class="page-title">策略回测</div>
    <div class="page-subtitle">模拟量化策略历史表现</div>

    <div class="card" style="margin-bottom:16px">
      <div style="display:flex;gap:16px;flex-wrap:wrap;align-items:flex-end">
        <div><label style="font-size:12px;color:#8c8c8c">策略类型</label><select v-model="strategy" style="display:block;margin-top:4px;padding:4px 8px;border:1px solid #d9d9d9;border-radius:4px">
          <option value="dual_ma">双均线</option><option value="macd">MACD金叉</option><option value="momentum">动量策略</option>
        </select></div>
        <div><label style="font-size:12px;color:#8c8c8c">标的</label><select v-model="target" style="display:block;margin-top:4px;padding:4px 8px;border:1px solid #d9d9d9;border-radius:4px">
          <option value="hs300">沪深300</option><option value="stock">个股</option>
        </select></div>
        <div><label style="font-size:12px;color:#8c8c8c">回测区间</label><div style="display:flex;gap:4px;margin-top:4px">
          <input value="2025-01-01" style="padding:4px 8px;border:1px solid #d9d9d9;border-radius:4px;width:110px" readonly />
          <span>至</span>
          <input value="2026-04-28" style="padding:4px 8px;border:1px solid #d9d9d9;border-radius:4px;width:110px" readonly />
        </div></div>
        <button @click="runBacktest" style="padding:6px 20px;background:#1890ff;color:#fff;border:none;border-radius:4px;cursor:pointer;font-size:14px">运行回测</button>
      </div>
    </div>

    <template v-if="resultVisible">
      <div class="stat-cards">
        <div class="stat-card"><div class="label">年化收益</div><div class="value rise">+18.5%</div></div>
        <div class="stat-card"><div class="label">最大回撤</div><div class="value fall">-12.3%</div></div>
        <div class="stat-card"><div class="label">夏普比率</div><div class="value">1.45</div></div>
        <div class="stat-card"><div class="label">胜率</div><div class="value">62.5%</div></div>
        <div class="stat-card"><div class="label">超额收益</div><div class="value rise">+8.7%</div></div>
      </div>

      <div class="card" style="margin-bottom:16px">
        <div style="font-size:15px;font-weight:600;margin-bottom:12px">累计收益率曲线</div>
        <div ref="curveChart" class="chart-container"></div>
      </div>

      <div class="card">
        <div style="font-size:15px;font-weight:600;margin-bottom:12px">交易明细</div>
        <table>
          <thead><tr><th>日期</th><th>方向</th><th>价格</th><th>股数</th><th>盈亏比例</th></tr></thead>
          <tbody>
            <tr v-for="t in trades" :key="t.date+t.dir">
              <td>{{ t.date }}</td>
              <td :class="t.dir==='买入'?'rise':'fall'">{{ t.dir }}</td>
              <td>{{ t.price }}</td><td>{{ t.qty }}</td>
              <td :class="t.pnl>=0?'rise':'fall'">{{ t.pnl>=0?'+':'' }}{{ t.pnl }}%</td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const strategy = ref('dual_ma')
const target = ref('hs300')
const resultVisible = ref(false)
const curveChart = ref(null)
let chart = null

const trades = [
  {date:'2025-02-15',dir:'买入',price:'3,856.23',qty:'100',pnl:0},
  {date:'2025-03-08',dir:'卖出',price:'3,923.45',qty:'100',pnl:1.74},
  {date:'2025-04-12',dir:'买入',price:'3,789.12',qty:'150',pnl:0},
  {date:'2025-05-20',dir:'卖出',price:'3,945.67',qty:'150',pnl:4.13},
  {date:'2025-07-03',dir:'买入',price:'3,654.89',qty:'200',pnl:0},
  {date:'2025-08-15',dir:'卖出',price:'3,812.34',qty:'200',pnl:4.31},
  {date:'2025-10-10',dir:'买入',price:'3,567.45',qty:'200',pnl:0},
  {date:'2025-11-22',dir:'卖出',price:'3,789.56',qty:'200',pnl:6.23},
  {date:'2026-01-08',dir:'买入',price:'3,678.90',qty:'250',pnl:0},
  {date:'2026-03-15',dir:'卖出',price:'3,923.45',qty:'250',pnl:6.65},
]

function runBacktest() {
  resultVisible.value = true
  nextTick(() => {
    if (!chart && curveChart.value) chart = echarts.init(curveChart.value)
    if (!chart) return
    const dates = Array.from({length:250},(_,i)=>{const d=new Date(2025,0,i+1);return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`})
    let v1=1,v2=1
    const strategy_data=dates.map(()=>{v1*=(1+(Math.random()-0.45)*0.015);return +(v1*100).toFixed(2)})
    const benchmark_data=dates.map(()=>{v2*=(1+(Math.random()-0.47)*0.01);return +(v2*100).toFixed(2)})
    chart.setOption({
      tooltip:{trigger:'axis'},legend:{data:['策略收益','基准收益(沪深300)'],top:0},
      grid:{top:40,left:60,right:20,bottom:30},
      xAxis:{type:'category',data:dates,axisLabel:{fontSize:9,rotate:30}},
      yAxis:{type:'value',name:'累计收益率(%)',splitLine:{lineStyle:{type:'dashed'}}},
      series:[
        {name:'策略收益',type:'line',data:strategy_data,smooth:true,lineStyle:{width:2,color:'#e83951'}},
        {name:'基准收益(沪深300)',type:'line',data:benchmark_data,smooth:true,lineStyle:{width:2,color:'#1890ff'}},
      ]
    })
    window.addEventListener('resize',()=>chart?.resize())
  })
}

onUnmounted(()=>chart?.dispose())
</script>
