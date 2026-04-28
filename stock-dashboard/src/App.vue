<template>
  <div class="app-container">
    <Sidebar
      :activeMenu="activeMenu"
      :activeSubMenu="activeSubMenu"
      :expandedMenus="expandedMenus"
      @select="handleSelect"
      @toggle="handleToggle"
    />
    <div class="main-content">
      <div class="content-wrapper">
        <transition name="fade" mode="out-in">
          <component :is="currentComponent" :key="activeSubMenu" />
        </transition>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, shallowRef } from 'vue'
import Sidebar from './components/Sidebar.vue'

import MarketIndex from './views/market/MarketIndex.vue'
import RiseFallDist from './views/market/RiseFallDist.vue'
import HotSectors from './views/sector/HotSectors.vue'
import IndustryRotation from './views/sector/IndustryRotation.vue'
import StockFilter from './views/stock/StockFilter.vue'
import StockCompare from './views/stock/StockCompare.vue'
import TechChart from './views/stock/TechChart.vue'
import NorthMoney from './views/money/NorthMoney.vue'
import MainForce from './views/money/MainForce.vue'
import MarginTrading from './views/money/MarginTrading.vue'
import CoreFinance from './views/finance/CoreFinance.vue'
import Valuation from './views/finance/Valuation.vue'
import EarningsForecast from './views/finance/EarningsForecast.vue'
import MarketSentiment from './views/sentiment/MarketSentiment.vue'
import FearGreed from './views/sentiment/FearGreed.vue'
import NewsSentiment from './views/sentiment/NewsSentiment.vue'
import StrategyBacktest from './views/quant/StrategyBacktest.vue'
import AIPredict from './views/quant/AIPredict.vue'
import FactorAnalysis from './views/quant/FactorAnalysis.vue'
import InstSeats from './views/dragontiger/InstSeats.vue'
import HotMoney from './views/dragontiger/HotMoney.vue'
import BlockTrade from './views/dragontiger/BlockTrade.vue'

const componentMap = {
  'market-index': MarketIndex,
  'rise-fall-dist': RiseFallDist,
  'hot-sectors': HotSectors,
  'industry-rotation': IndustryRotation,
  'stock-filter': StockFilter,
  'stock-compare': StockCompare,
  'tech-chart': TechChart,
  'north-money': NorthMoney,
  'main-force': MainForce,
  'margin-trading': MarginTrading,
  'core-finance': CoreFinance,
  'valuation': Valuation,
  'earnings-forecast': EarningsForecast,
  'market-sentiment': MarketSentiment,
  'fear-greed': FearGreed,
  'news-sentiment': NewsSentiment,
  'strategy-backtest': StrategyBacktest,
  'ai-predict': AIPredict,
  'factor-analysis': FactorAnalysis,
  'inst-seats': InstSeats,
  'hot-money': HotMoney,
  'block-trade': BlockTrade,
}

const activeMenu = ref('sector')
const activeSubMenu = ref('hot-sectors')
const expandedMenus = ref(['sector'])

const currentComponent = computed(() => componentMap[activeSubMenu.value] || HotSectors)

function handleSelect(menu, subMenu) {
  activeMenu.value = menu
  activeSubMenu.value = subMenu
}

function handleToggle(menu) {
  const idx = expandedMenus.value.indexOf(menu)
  if (idx >= 0) {
    expandedMenus.value.splice(idx, 1)
  } else {
    expandedMenus.value.push(menu)
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #app {
  height: 100%;
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

.app-container {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.main-content {
  flex: 1;
  background: #f0f2f5;
  overflow-y: auto;
  overflow-x: hidden;
}

.content-wrapper {
  padding: 20px;
  min-height: 100%;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  padding: 20px;
  margin-bottom: 16px;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a2e;
  margin-bottom: 4px;
}

.page-subtitle {
  font-size: 13px;
  color: #8c8c8c;
  margin-bottom: 20px;
}

.stat-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.stat-card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  padding: 20px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.12);
}

.stat-card .label {
  font-size: 13px;
  color: #8c8c8c;
  margin-bottom: 8px;
}

.stat-card .value {
  font-size: 24px;
  font-weight: 700;
  color: #1a1a2e;
}

.stat-card .change {
  font-size: 13px;
  margin-top: 4px;
}

.rise { color: #e83951; }
.fall { color: #22c55e; }
.flat { color: #8c8c8c; }

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  background: #fafafa;
  padding: 12px 16px;
  text-align: left;
  font-weight: 600;
  font-size: 13px;
  color: #595959;
  border-bottom: 1px solid #f0f0f0;
}

td {
  padding: 12px 16px;
  font-size: 13px;
  color: #262626;
  border-bottom: 1px solid #f0f0f0;
}

tr:nth-child(even) td {
  background: #fafafa;
}

tr:hover td {
  background: #e6f7ff;
}

.chart-container {
  width: 100%;
  height: 400px;
}

.chart-container-sm {
  width: 100%;
  height: 300px;
}
</style>
