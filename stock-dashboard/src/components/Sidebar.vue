<template>
  <div class="sidebar">
    <div class="brand">
      <svg class="brand-icon" viewBox="0 0 24 24" fill="none" stroke="#1890ff" stroke-width="2">
        <polyline points="22,12 18,12 15,21 9,3 6,12 2,12"/>
      </svg>
      <span class="brand-text">智研股票系统</span>
    </div>

    <nav class="nav-menu">
      <div v-for="menu in menus" :key="menu.key" class="menu-group">
        <div
          class="menu-item"
          :class="{ active: activeMenu === menu.key }"
          @click="$emit('toggle', menu.key)"
        >
          <div class="menu-left">
            <svg class="menu-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" v-html="menu.iconPath"></svg>
            <span>{{ menu.label }}</span>
          </div>
          <svg class="arrow" :class="{ rotated: expandedMenus.includes(menu.key) }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="6,9 12,15 18,9"/>
          </svg>
        </div>
        <transition name="expand">
          <div v-if="expandedMenus.includes(menu.key)" class="sub-menu">
            <div
              v-for="sub in menu.children"
              :key="sub.key"
              class="sub-menu-item"
              :class="{ active: activeSubMenu === sub.key }"
              @click="$emit('select', menu.key, sub.key)"
            >
              <span>{{ sub.label }}</span>
            </div>
          </div>
        </transition>
      </div>
    </nav>

    <div class="user-area">
      <div class="avatar">投</div>
      <span class="user-name">投资者</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  activeMenu: String,
  activeSubMenu: String,
  expandedMenus: Array,
})

defineEmits(['select', 'toggle'])

const menus = [
  {
    key: 'market', label: '行情总览',
    iconPath: '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>',
    children: [
      { key: 'market-index', label: '大盘指数' },
      { key: 'rise-fall-dist', label: '涨跌分布' },
    ]
  },
  {
    key: 'sector', label: '板块分析',
    iconPath: '<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>',
    children: [
      { key: 'hot-sectors', label: '热门板块' },
      { key: 'industry-rotation', label: '行业轮动' },
    ]
  },
  {
    key: 'stock', label: '个股分析',
    iconPath: '<polyline points="23,6 13.5,15.5 8.5,10.5 1,18"/><polyline points="17,6 23,6 23,12"/>',
    children: [
      { key: 'stock-filter', label: '个股筛选' },
      { key: 'stock-compare', label: '个股对比' },
      { key: 'tech-chart', label: '技术图表' },
    ]
  },
  {
    key: 'money', label: '资金流向',
    iconPath: '<line x1="12" y1="1" x2="12" y2="23"/><path d="M17,5 H9.5a3.5,3.5 0 0,0 0,7h5a3.5,3.5 0 0,1 0,7H6"/>',
    children: [
      { key: 'north-money', label: '北向资金' },
      { key: 'main-force', label: '主力资金' },
      { key: 'margin-trading', label: '融资融券' },
    ]
  },
  {
    key: 'finance', label: '财务数据',
    iconPath: '<path d="M14,2 H6 a2,2 0 0,0 -2,2 v16 a2,2 0 0,0 2,2 h12 a2,2 0 0,0 2,-2 V8 z"/><polyline points="14,2 14,8 20,8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>',
    children: [
      { key: 'core-finance', label: '核心财报' },
      { key: 'valuation', label: '估值指标' },
      { key: 'earnings-forecast', label: '盈利预测' },
    ]
  },
  {
    key: 'sentiment', label: '情绪分析',
    iconPath: '<polyline points="22,12 18,12 15,21 9,3 6,12 2,12"/>',
    children: [
      { key: 'market-sentiment', label: '市场情绪' },
      { key: 'fear-greed', label: '恐惧贪婪指数' },
      { key: 'news-sentiment', label: '新闻舆情' },
    ]
  },
  {
    key: 'quant', label: '量化策略',
    iconPath: '<rect x="4" y="4" width="16" height="16" rx="2" ry="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/>',
    children: [
      { key: 'strategy-backtest', label: '策略回测' },
      { key: 'ai-predict', label: 'AI 股价预测' },
      { key: 'factor-analysis', label: '因子分析' },
    ]
  },
  {
    key: 'dragontiger', label: '龙虎榜',
    iconPath: '<line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/>',
    children: [
      { key: 'inst-seats', label: '机构席位' },
      { key: 'hot-money', label: '游资动态' },
      { key: 'block-trade', label: '大宗交易' },
    ]
  },
]
</script>

<style scoped>
.sidebar {
  width: 250px;
  min-width: 250px;
  height: 100vh;
  background: linear-gradient(180deg, #1b1e2b 0%, #131620 100%);
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  overflow-x: hidden;
}

.brand {
  display: flex;
  align-items: center;
  padding: 20px 20px 16px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}

.brand-icon {
  width: 24px;
  height: 24px;
  margin-right: 10px;
}

.brand-text {
  font-size: 18px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 1px;
}

.nav-menu {
  flex: 1;
  padding: 8px 0;
}

.menu-group {
  margin-bottom: 2px;
}

.menu-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 20px;
  cursor: pointer;
  color: rgba(255,255,255,0.65);
  transition: all 0.2s;
  font-size: 14px;
}

.menu-item:hover {
  color: rgba(255,255,255,0.9);
  background: rgba(255,255,255,0.04);
}

.menu-item.active {
  color: #fff;
}

.menu-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.menu-icon {
  width: 18px;
  height: 18px;
}

.arrow {
  width: 14px;
  height: 14px;
  transition: transform 0.25s ease;
}

.arrow.rotated {
  transform: rotate(180deg);
}

.sub-menu {
  overflow: hidden;
}

.sub-menu-item {
  padding: 9px 20px 9px 48px;
  cursor: pointer;
  color: rgba(255,255,255,0.45);
  font-size: 13px;
  transition: all 0.2s;
  position: relative;
}

.sub-menu-item:hover {
  color: rgba(255,255,255,0.8);
  background: rgba(255,255,255,0.04);
}

.sub-menu-item.active {
  color: #fff;
  background: rgba(24,144,255,0.12);
}

.sub-menu-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: #1890ff;
  border-radius: 0 2px 2px 0;
}

.expand-enter-active,
.expand-leave-active {
  transition: all 0.25s ease;
  max-height: 300px;
}

.expand-enter-from,
.expand-leave-to {
  max-height: 0;
  opacity: 0;
}

.user-area {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  border-top: 1px solid rgba(255,255,255,0.06);
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #1890ff, #722ed1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  margin-right: 10px;
}

.user-name {
  color: rgba(255,255,255,0.65);
  font-size: 13px;
}
</style>
