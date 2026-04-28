<template>
  <div>
    <div class="page-title">实时舆情</div>
    <div class="page-subtitle">2026-04-28 新闻舆情监控</div>

    <div style="display:grid;grid-template-columns:200px 1fr;gap:16px">
      <div class="card">
        <div style="font-size:15px;font-weight:600;margin-bottom:12px">情感分布</div>
        <div ref="pieChart" style="width:100%;height:200px"></div>
      </div>
      <div class="card">
        <div style="font-size:15px;font-weight:600;margin-bottom:12px">舆情时间线</div>
        <div class="timeline">
          <div v-for="(n,i) in news" :key="i" class="news-item" @click="toggleExpand(i)">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px">
              <span class="dot" :class="n.sentiment==='利好'?'rise':n.sentiment==='利空'?'fall':'flat'">●</span>
              <span style="font-size:14px;font-weight:500">{{ n.title }}</span>
              <span class="sentiment-tag" :class="n.sentiment==='利好'?'tag-rise':n.sentiment==='利空'?'tag-fall':'tag-flat'">{{ n.sentiment }}</span>
            </div>
            <div style="font-size:12px;color:#8c8c8c">{{ n.time }}</div>
            <div v-if="expanded===i" style="font-size:13px;color:#595959;margin-top:8px;padding:8px;background:#fafafa;border-radius:4px">{{ n.summary }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const pieChart = ref(null)
const expanded = ref(-1)
let chart = null

const news = [
  {title:'国务院发布半导体产业扶持新政',time:'10:23',sentiment:'利好',summary:'国务院常务会议通过半导体产业新十条扶持政策，包括税收减免、研发补贴等多项利好措施，预计将带动半导体板块持续走强。'},
  {title:'央行下调MLF利率10个基点',time:'09:45',sentiment:'利好',summary:'中国人民银行下调中期借贷便利利率10个基点至2.4%，市场流动性预期改善，利好银行和地产板块。'},
  {title:'新能源汽车4月销量环比下降8%',time:'11:30',sentiment:'利空',summary:'中汽协数据显示4月新能源汽车销量环比下降8%，市场担忧补贴退坡影响持续，短期承压。'},
  {title:'宁德时代发布新一代麒麟电池',time:'13:15',sentiment:'利好',summary:'宁德时代正式发布第三代麒麟电池，能量密度提升20%，已获多家车企订单，预计Q3量产。'},
  {title:'美联储会议纪要偏鹰派',time:'08:30',sentiment:'利空',summary:'美联储4月会议纪要显示多数委员支持继续加息，美元走强，人民币承压，北向资金可能流出。'},
  {title:'光伏行业产能过剩预警',time:'14:20',sentiment:'利空',summary:'工信部发布光伏行业产能预警，当前产能利用率仅65%，建议企业理性扩产，行业整合加速。'},
  {title:'贵州茅台Q1营收超预期',time:'15:00',sentiment:'利好',summary:'贵州茅台一季度营收同比增长18.5%超市场预期，直销占比提升至45%，净利润增长22%。'},
  {title:'房地产调控政策微调',time:'12:00',sentiment:'中性',summary:'多地出台房地产调控微调政策，包括降低首付比例、放宽限购等，但整体基调仍为房住不炒。'},
]

function toggleExpand(i) { expanded.value = expanded.value === i ? -1 : i }

onMounted(()=>{
  chart=echarts.init(pieChart.value)
  chart.setOption({
    tooltip:{trigger:'item'},series:[{
      type:'pie',radius:['45%','75%'],center:['50%','50%'],
      data:[
        {value:45,name:'利好',itemStyle:{color:'#e83951'}},
        {value:25,name:'利空',itemStyle:{color:'#22c55e'}},
        {value:30,name:'中性',itemStyle:{color:'#8c8c8c'}},
      ],
      label:{formatter:'{b}\n{d}%',fontSize:11}
    }]
  })
  window.addEventListener('resize',()=>chart?.resize())
})
onUnmounted(()=>chart?.dispose())
</script>

<style scoped>
.timeline { max-height:500px; overflow-y:auto }
.news-item { padding:12px 0; border-bottom:1px solid #f0f0f0; cursor:pointer }
.news-item:hover { background:#fafafa }
.dot { font-size:10px }
.sentiment-tag { font-size:11px; padding:1px 6px; border-radius:3px }
.tag-rise { background:#fff1f0; color:#e83951 }
.tag-fall { background:#f0fff4; color:#22c55e }
.tag-flat { background:#f5f5f5; color:#8c8c8c }
</style>
