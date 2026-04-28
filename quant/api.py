from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import warnings
import time
import numpy as np

warnings.filterwarnings('ignore')

api_app = FastAPI(title="智研股票系统 API")

api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def safe_float(val, default=0):
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


@api_app.get("/api/market/index")
async def market_index():
    try:
        spot_df = ak.stock_zh_index_spot_em()
        indices = ['上证指数', '深证成指', '创业板指', '科创50']
        result = []
        for idx_name in indices:
            row = spot_df[spot_df['名称'] == idx_name]
            if not row.empty:
                r = row.iloc[0]
                result.append({
                    'name': idx_name,
                    'value': safe_float(r.get('最新价', 0)),
                    'change': safe_float(r.get('涨跌额', 0)),
                    'pct': safe_float(r.get('涨跌幅', 0)),
                })
            else:
                result.append({'name': idx_name, 'value': 0, 'change': 0, 'pct': 0})
        return {'status': 'success', 'data': result}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@api_app.get("/api/market/rise-fall")
async def rise_fall_dist():
    try:
        spot_df = ak.stock_zh_a_spot_em()
        if spot_df is None or spot_df.empty:
            return {'status': 'error', 'message': 'No data'}
        spot_df['涨跌幅'] = pd.to_numeric(spot_df['涨跌幅'], errors='coerce').fillna(0)
        up_count = len(spot_df[spot_df['涨跌幅'] > 0])
        down_count = len(spot_df[spot_df['涨跌幅'] < 0])
        flat_count = len(spot_df[spot_df['涨跌幅'] == 0])
        bins = [
            {'label': '跌停', 'min': -100, 'max': -9.5},
            {'label': '-7%~', 'min': -9.5, 'max': -7},
            {'label': '-5%~', 'min': -7, 'max': -5},
            {'label': '-3%~', 'min': -5, 'max': -3},
            {'label': '-1%~', 'min': -3, 'max': -1},
            {'label': '0', 'min': -1, 'max': 1},
            {'label': '1%~', 'min': 1, 'max': 3},
            {'label': '3%~', 'min': 3, 'max': 5},
            {'label': '5%~', 'min': 5, 'max': 7},
            {'label': '7%~', 'min': 7, 'max': 9.5},
            {'label': '涨停', 'min': 9.5, 'max': 100},
        ]
        dist = []
        for b in bins:
            count = len(spot_df[(spot_df['涨跌幅'] >= b['min']) & (spot_df['涨跌幅'] < b['max'])])
            dist.append({'label': b['label'], 'count': count})
        return {'status': 'success', 'data': {'up': up_count, 'down': down_count, 'flat': flat_count, 'dist': dist}}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@api_app.get("/api/sector/hot")
async def hot_sectors():
    try:
        sector_df = ak.stock_board_industry_name_em()
        if sector_df is None or sector_df.empty:
            return {'status': 'error', 'message': 'No data'}
        gain_col = None
        for col in ['涨跌幅', '3日涨幅', '三日涨幅']:
            if col in sector_df.columns:
                gain_col = col
                break
        if gain_col:
            sector_df[gain_col] = pd.to_numeric(sector_df[gain_col], errors='coerce')
            sector_df = sector_df.sort_values(gain_col, ascending=False)
        result = []
        for _, row in sector_df.head(12).iterrows():
            result.append({
                'name': row.get('板块名称', 'N/A'),
                'pct': safe_float(row.get(gain_col, 0)),
                'leadStock': row.get('领涨股票', 'N/A'),
                'leadPct': safe_float(row.get('领涨涨幅', 0)),
                'flow': safe_float(row.get('主力净流入', 0)) / 1e8 if safe_float(row.get('主力净流入', 0)) != 0 else 0,
            })
        return {'status': 'success', 'data': result}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@api_app.get("/api/sector/rotation")
async def industry_rotation():
    try:
        sector_df = ak.stock_board_industry_name_em()
        if sector_df is None or sector_df.empty:
            return {'status': 'error', 'message': 'No data'}
        pct_col = '涨跌幅'
        if pct_col in sector_df.columns:
            sector_df[pct_col] = pd.to_numeric(sector_df[pct_col], errors='coerce')
        result = []
        for _, row in sector_df.iterrows():
            result.append({
                'name': row.get('板块名称', 'N/A'),
                'pct': safe_float(row.get(pct_col, 0)),
            })
        return {'status': 'success', 'data': result}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@api_app.get("/api/stock/filter")
async def stock_filter(
    industry: str = Query('all'),
    direction: str = Query('all'),
    pe_min: float = Query(None),
    pe_max: float = Query(None),
    page: int = Query(1),
    page_size: int = Query(15),
):
    try:
        spot_df = ak.stock_zh_a_spot_em()
        if spot_df is None or spot_df.empty:
            return {'status': 'error', 'message': 'No data'}
        for col in ['涨跌幅', '成交量', '总市值']:
            if col in spot_df.columns:
                spot_df[col] = pd.to_numeric(spot_df[col], errors='coerce')
        if industry != 'all':
            industry_map = {'科技': ['电子', '计算机', '通信', '传媒'], '消费': ['食品饮料', '家用电器', '纺织服饰', '商贸零售'], '医药': ['医药生物'], '制造': ['电力设备', '汽车', '机械设备']}
            if industry in industry_map:
                pass
        if direction == 'up':
            spot_df = spot_df[spot_df['涨跌幅'] > 0]
        elif direction == 'down':
            spot_df = spot_df[spot_df['涨跌幅'] < 0]
        total = len(spot_df)
        start = (page - 1) * page_size
        paged = spot_df.iloc[start:start + page_size]
        result = []
        for _, row in paged.iterrows():
            result.append({
                'code': str(row.get('代码', '')),
                'name': row.get('名称', ''),
                'price': safe_float(row.get('最新价', 0)),
                'pct': safe_float(row.get('涨跌幅', 0)),
                'vol': round(safe_float(row.get('成交量', 0)) / 1e4, 2),
                'mv': round(safe_float(row.get('总市值', 0)) / 1e8, 2),
                'industry': row.get('所属行业', 'N/A'),
                'pe': round(safe_float(row.get('市盈率-动态', 0)), 2),
            })
        return {'status': 'success', 'data': {'stocks': result, 'total': total, 'page': page, 'page_size': page_size}}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@api_app.get("/api/stock/detail")
async def stock_detail(code: str = Query('600519')):
    try:
        hist_df = ak.stock_zh_a_hist(symbol=code, period='daily', start_date=(datetime.now() - timedelta(days=60)).strftime('%Y%m%d'), end_date=datetime.now().strftime('%Y%m%d'), adjust='qfq')
        kline = []
        if hist_df is not None and not hist_df.empty:
            for _, row in hist_df.iterrows():
                kline.append({
                    'date': str(row.get('日期', '')),
                    'open': safe_float(row.get('开盘', 0)),
                    'close': safe_float(row.get('收盘', 0)),
                    'high': safe_float(row.get('最高', 0)),
                    'low': safe_float(row.get('最低', 0)),
                    'volume': safe_float(row.get('成交量', 0)),
                })
        return {'status': 'success', 'data': {'kline': kline}}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@api_app.get("/api/money/north")
async def north_money():
    try:
        df = ak.stock_hsgt_north_net_flow_in_em(symbol="北向")
        if df is None or df.empty:
            return {'status': 'error', 'message': 'No data'}
        df = df.sort_values('日期', ascending=False)
        recent = df.head(20)
        flow_data = []
        for _, row in recent.iterrows():
            flow_data.append({
                'date': str(row.get('日期', '')),
                'net_flow': safe_float(row.get('当日净流入', 0)) / 1e8,
            })
        day_net = safe_float(df.iloc[0].get('当日净流入', 0)) / 1e8 if not df.empty else 0
        five_day = sum(safe_float(r.get('当日净流入', 0)) for _, r in df.head(5).iterrows()) / 1e8
        twenty_day = sum(safe_float(r.get('当日净流入', 0)) for _, r in df.head(20).iterrows()) / 1e8
        return {'status': 'success', 'data': {'day_net': round(day_net, 2), 'five_day': round(five_day, 2), 'twenty_day': round(twenty_day, 2), 'flow_data': flow_data}}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@api_app.get("/api/money/main-force")
async def main_force():
    try:
        sector_df = ak.stock_board_industry_name_em()
        if sector_df is None or sector_df.empty:
            return {'status': 'error', 'message': 'No data'}
        flow_col = None
        for col in ['主力净流入', '主力净流入-金额']:
            if col in sector_df.columns:
                flow_col = col
                break
        if flow_col:
            sector_df[flow_col] = pd.to_numeric(sector_df[flow_col], errors='coerce')
            sector_df = sector_df.sort_values(flow_col)
        sectors = []
        for _, row in sector_df.head(10).iterrows():
            sectors.append({'name': row.get('板块名称', ''), 'amount': round(safe_float(row.get(flow_col, 0)) / 1e8, 2)})
        for _, row in sector_df.tail(10).iterrows():
            sectors.append({'name': row.get('板块名称', ''), 'amount': round(safe_float(row.get(flow_col, 0)) / 1e8, 2)})
        return {'status': 'success', 'data': sectors}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@api_app.get("/api/money/margin")
async def margin_trading():
    try:
        df = ak.stock_margin_underlying_info_sz_sh(date=datetime.now().strftime('%Y%m%d'))
        if df is None or df.empty:
            return {'status': 'error', 'message': 'No data'}
        result = []
        for _, row in df.head(20).iterrows():
            result.append({
                'code': str(row.get('证券代码', '')),
                'name': row.get('证券简称', ''),
                'margin_buy': safe_float(row.get('融资买入额', 0)),
                'margin_balance': safe_float(row.get('融资余额', 0)),
            })
        return {'status': 'success', 'data': result}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@api_app.get("/api/finance/core")
async def core_finance(code: str = Query('300750')):
    try:
        df = ak.stock_financial_abstract_ths(symbol=code, indicator="按报告期")
        if df is None or df.empty:
            return {'status': 'error', 'message': 'No data'}
        latest = df.iloc[0] if not df.empty else {}
        result = {}
        for col in df.columns:
            result[col] = str(latest.get(col, 'N/A'))
        return {'status': 'success', 'data': result}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@api_app.get("/api/finance/valuation")
async def valuation(code: str = Query('300750')):
    try:
        spot_df = ak.stock_zh_a_spot_em()
        stock_row = spot_df[spot_df['代码'] == code]
        if stock_row.empty:
            return {'status': 'error', 'message': 'Stock not found'}
        r = stock_row.iloc[0]
        result = {
            'pe': safe_float(r.get('市盈率-动态', 0)),
            'pb': safe_float(r.get('市净率', 0)),
            'mv': safe_float(r.get('总市值', 0)),
            'circ_mv': safe_float(r.get('流通市值', 0)),
        }
        return {'status': 'success', 'data': result}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@api_app.get("/api/sentiment/market")
async def market_sentiment():
    try:
        spot_df = ak.stock_zh_a_spot_em()
        if spot_df is None or spot_df.empty:
            return {'status': 'error', 'message': 'No data'}
        spot_df['涨跌幅'] = pd.to_numeric(spot_df['涨跌幅'], errors='coerce').fillna(0)
        up = len(spot_df[spot_df['涨跌幅'] > 0])
        down = len(spot_df[spot_df['涨跌幅'] < 0])
        flat = len(spot_df[spot_df['涨跌幅'] == 0])
        limit_up = len(spot_df[spot_df['涨跌幅'] >= 9.5])
        limit_down = len(spot_df[spot_df['涨跌幅'] <= -9.5])
        return {'status': 'success', 'data': {'up': up, 'down': down, 'flat': flat, 'limit_up': limit_up, 'limit_down': limit_down}}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@api_app.get("/api/dragontiger/inst")
async def inst_seats():
    try:
        df = ak.stock_lhb_detail_em(start_date=datetime.now().strftime('%Y%m%d'), end_date=datetime.now().strftime('%Y%m%d'))
        if df is None or df.empty:
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
            df = ak.stock_lhb_detail_em(start_date=yesterday, end_date=yesterday)
        if df is None or df.empty:
            return {'status': 'error', 'message': 'No data'}
        result = []
        for _, row in df.head(20).iterrows():
            result.append({
                'code': str(row.get('代码', '')),
                'name': row.get('名称', ''),
                'buy': safe_float(row.get('买入额', 0)),
                'sell': safe_float(row.get('卖出额', 0)),
                'net': safe_float(row.get('净买额', 0)),
                'reason': row.get('上榜原因', ''),
            })
        return {'status': 'success', 'data': result}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@api_app.get("/api/dragontiger/hot-money")
async def hot_money_seats():
    try:
        df = ak.stock_lhb_detail_em(start_date=datetime.now().strftime('%Y%m%d'), end_date=datetime.now().strftime('%Y%m%d'))
        if df is None or df.empty:
            return {'status': 'error', 'message': 'No data'}
        result = []
        for _, row in df.head(15).iterrows():
            result.append({
                'code': str(row.get('代码', '')),
                'name': row.get('名称', ''),
                'buy': safe_float(row.get('买入额', 0)),
                'sell': safe_float(row.get('卖出额', 0)),
                'reason': row.get('上榜原因', ''),
            })
        return {'status': 'success', 'data': result}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@api_app.get("/api/dragontiger/block-trade")
async def block_trade():
    try:
        df = ak.stock_dzjy_mrmx(start_date=(datetime.now() - timedelta(days=5)).strftime('%Y%m%d'), end_date=datetime.now().strftime('%Y%m%d'))
        if df is None or df.empty:
            return {'status': 'error', 'message': 'No data'}
        result = []
        for _, row in df.head(20).iterrows():
            result.append({
                'date': str(row.get('交易日期', '')),
                'stock': row.get('证券简称', ''),
                'price': safe_float(row.get('成交价', 0)),
                'amount': safe_float(row.get('成交额', 0)),
                'premium': safe_float(row.get('溢价率', 0)),
            })
        return {'status': 'success', 'data': result}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@api_app.get("/api/sector/detail")
async def sector_detail(name: str = Query('半导体')):
    try:
        stocks_df = ak.stock_board_industry_cons_em(symbol=name)
        if stocks_df is None or stocks_df.empty:
            return {'status': 'error', 'message': 'No data'}
        result = []
        for _, row in stocks_df.head(10).iterrows():
            result.append({
                'code': str(row.get('代码', '')),
                'name': row.get('名称', ''),
                'price': safe_float(row.get('最新价', 0)),
                'pct': safe_float(row.get('涨跌幅', 0)),
            })
        return {'status': 'success', 'data': result}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@api_app.get("/api/today")
async def today_api():
    try:
        result = {'limit_up': [], 'limit_down': [], 'volume_top': [], 'turnover_top': [], 'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        try:
            limit_up_df = ak.stock_zt_pool_em(date=datetime.now().strftime('%Y%m%d'))
            if limit_up_df is not None and not limit_up_df.empty:
                for _, row in limit_up_df.head(20).iterrows():
                    result['limit_up'].append({'code': str(row.get('代码', '')), 'name': row.get('名称', ''), 'price': safe_float(row.get('最新价', 0)), 'pct': safe_float(row.get('涨跌幅', 0)), 'time': str(row.get('封板时间', '')), 'boards': safe_float(row.get('连板数', 0))})
        except Exception:
            pass
        try:
            limit_down_df = ak.stock_dt_pool_em(date=datetime.now().strftime('%Y%m%d'))
            if limit_down_df is not None and not limit_down_df.empty:
                for _, row in limit_down_df.head(20).iterrows():
                    result['limit_down'].append({'code': str(row.get('代码', '')), 'name': row.get('名称', ''), 'price': safe_float(row.get('最新价', 0)), 'pct': safe_float(row.get('涨跌幅', 0))})
        except Exception:
            pass
        return {'status': 'success', 'data': result}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@api_app.get("/api/dragon-tiger")
async def dragon_tiger_api():
    try:
        df = ak.stock_lhb_detail_em(start_date=datetime.now().strftime('%Y%m%d'), end_date=datetime.now().strftime('%Y%m%d'))
        if df is None or df.empty:
            return {'status': 'success', 'data': []}
        result = []
        for _, row in df.head(20).iterrows():
            result.append({
                'code': str(row.get('代码', '')),
                'name': row.get('名称', ''),
                'buy': safe_float(row.get('买入额', 0)),
                'sell': safe_float(row.get('卖出额', 0)),
                'net': safe_float(row.get('净买额', 0)),
                'reason': row.get('上榜原因', ''),
            })
        return {'status': 'success', 'data': result}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
