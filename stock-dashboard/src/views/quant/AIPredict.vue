<template>
  <div>
    <div class="page-title">AI 股价预测</div>
    <div class="page-subtitle">基于LSTM模型的股价预测（模拟）</div>

    <div class="card" style="margin-bottom:16px">
      <div style="display:flex;gap:12px;align-items:flex-end">
        <div><label style="font-size:12px;color:#8c8c8c">输入个股</label><input v-model="stockName" style="display:block;margin-top:4px;padding:4px 8px;border:1px solid #d9d9d9;border-radius:4px;width:140px" /></div>
        <button @click="predict" style="padding:6px 20px;background:#1890ff;color:#fff;border:none;border-radius:4px;cursor:pointer">开始预测</button>
      </div>
    </div>

    <template v-if="predicted">
      <div class="stat-cards">
        <div class="stat-card"><div class="label">预测方向</div><div class="value rise">上涨 68%</div></div>
        <div class="stat-card"><div class="label">预测变动幅度</div><div class="value rise">+2.35%</div></div>
        <div class="stat-card"><div class="label">模型MAE</div><div class="value">3.42</div></div>
        <div class="stat-card"><div class="label">模型RMSE</div><div class="value">4.56</div></div>
      </div>

      <div class="card" style="margin-bottom:16px">
        <div style="font-size:15px;font-weight:600;margin-bottom:12px">股价预测走势</div>
        <div ref="predictChart" class="chart-container"></div>
      </div>

      <div class="card">
        <div style="font-size:13px;color:#8c8c8c;line-height:1.8">
          <p><strong>模型说明：</strong>本预测基于LSTM深度学习模型，使用近60个交易日的历史数据作为输入特征。</p>
          <p><strong>免责声明：</strong>以上预测结果仅为模型模拟输出，不构成任何投资建议。股市有风险，投资需谨慎。</p>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, nextTick, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const stockName = ref('贵州茅台')
const predicted = ref(false)
const predictChart = ref(null)
let chart = null

function predict() {
  predicted.value = true
  nextTick(() => {
    if (!chart && predictChart.value) chart = echarts.init(predictChart.value)
    if (!chart) return
    const histDates = Array.from({length:30},(_,i)=>`04-${String(i+1).padStart(2,'0')}`)
    const predDates = ['04-29','04-30','05-05','05-06','05-07']
    const allDates = [...histDates, ...predDates]
    let v = 1680
    const histData = histDates.map(() => { v += (Math.random()-0.48)*15; return +v.toFixed(2) })
    const lastVal = histData[histData.length-1]
    let pv = lastVal
    const predData = predDates.map(() => { pv += (Math.random()-0.4)*10; return +pv.toFixed(2) })
    const upperBand = predData.map(d => +(d + 15 + Math.random()*10).toFixed(2))
    const lowerBand = predData.map(d => +(d - 15 - Math.random()*10).toFixed(2))
    const fullHist = [...histData, ...Array(predDates.length).fill(null)]
    const fullPred = [...Array(histDates.length-1).fill(null), histData[histData.length-1], ...predData]
    const fullUpper = [...Array(histDates.length-1).fill(null), histData[histData.length-1]+15, ...upperBand]
    const fullLower = [...Array(histDates.length-1).fill(null), histData[histData.length-1]-15, ...lowerBand]
    chart.setOption({
      tooltip:{trigger:'axis'},legend:{data:['历史收盘价','预测值','置信上界','置信下界'],top:0},
      grid:{top:40,left:60,right:20,bottom:30},
      xAxis:{type:'category',data:allDates,axisLabel:{fontSize:10,rotate:30}},
      yAxis:{type:'value',scale:true,splitLine:{lineStyle:{type:'dashed'}}},
      series:[
        {name:'历史收盘价',type:'line',data:fullHist,smooth:true,lineStyle:{width:2,color:'#1890ff'}},
        {name:'预测值',type:'line',data:fullPred,smooth:true,lineStyle:{width:2,color:'#e83951',type:'dashed'}},
        {name:'置信上界',type:'line',data:fullUpper,smooth:true,lineStyle:{width:0},symbol:'none',areaStyle:{color:'transparent'}},
        {name:'置信下界',type:'line',data:fullLower,smooth:true,lineStyle:{width:0},symbol:'none',areaStyle:{color:'rgba(232,57,81,0.15)'}},
      ]
    })
    window.addEventListener('resize',()=>chart?.resize())
  })
}

onUnmounted(()=>chart?.dispose())
</script>
