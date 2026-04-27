from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import warnings
import time
from collections import Counter
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape

warnings.filterwarnings('ignore')

app = FastAPI(title="Stock Analysis Dashboard")

# 获取项目根目录（quant 包的父目录）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=select_autoescape(['html', 'xml']),
    cache_size=0  # 禁用缓存以避免 dict 类型问题
)

def templates(name: str, context: dict):
    from starlette.templating import _TemplateResponse
    template = jinja_env.get_template(name)
    request = context.get("request")
    return _TemplateResponse(template, {"request": request, **context})


def get_sectors_with_3day_gains():
    """
    分析近三天涨幅大于3%的板块，挑选5只
    """
    try:
        sector_df = ak.stock_board_industry_name_em()
        
        if sector_df is None or sector_df.empty:
            return []
        
        gain_col = None
        for col in ['3日涨幅', '三日涨幅', '3日涨跌幅', '三日涨跌幅']:
            if col in sector_df.columns:
                gain_col = col
                break
        
        if gain_col:
            sector_df[gain_col] = pd.to_numeric(sector_df[gain_col], errors='coerce')
            filtered = sector_df[sector_df[gain_col] > 3].copy()
            filtered = filtered.sort_values(gain_col, ascending=False)
            
            if not filtered.empty:
                top_5 = filtered.head(5)
                result = []
                for _, row in top_5.iterrows():
                    result.append({
                        '板块名称': row.get('板块名称', 'N/A'),
                        '3日涨幅(%)': round(row.get(gain_col, 0), 2),
                        '最新价': row.get('最新价', 'N/A'),
                        '涨跌幅(%)': row.get('涨跌幅', 'N/A'),
                        '成交额': row.get('成交额', 'N/A')
                    })
                return result
        
        return []
    except Exception:
        return []


def get_stocks_from_sectors(sectors):
    """
    从板块中选出沪深主板和创业板股票，近5日涨幅大于5%的股票
    """
    try:
        selected_stocks = []
        
        for sector in sectors:
            sector_name = sector.get('板块名称', '')
            if not sector_name:
                continue
            
            try:
                stocks_df = ak.stock_board_industry_cons_em(symbol=sector_name)
                
                if stocks_df is None or stocks_df.empty:
                    continue
                
                gain_col = None
                for col in ['5日涨幅', '五日涨幅', '5日涨跌幅', '五日涨跌幅']:
                    if col in stocks_df.columns:
                        gain_col = col
                        break
                
                if not gain_col:
                    continue
                
                for _, stock in stocks_df.iterrows():
                    stock_code = str(stock.get('代码', ''))
                    
                    if not (stock_code.startswith('60') or 
                            stock_code.startswith('00') or 
                            stock_code.startswith('30')):
                        continue
                    
                    if stock_code.startswith('60'):
                        board_type = '沪市主板'
                    elif stock_code.startswith('00'):
                        board_type = '深市主板'
                    else:
                        board_type = '创业板'
                    
                    try:
                        gain_5d = float(stock.get(gain_col, 0))
                        if gain_5d > 5:
                            selected_stocks.append({
                                '代码': stock_code,
                                '名称': stock.get('名称', 'N/A'),
                                '所属板块': sector_name,
                                '板块类型': board_type,
                                '5日涨幅(%)': round(gain_5d, 2),
                                '最新价': stock.get('最新价', 'N/A'),
                                '涨跌幅(%)': stock.get('涨跌幅', 'N/A')
                            })
                    except (ValueError, TypeError):
                        pass
                
                time.sleep(0.5)
                
            except Exception:
                continue
        
        selected_stocks.sort(key=lambda x: x['5日涨幅(%)'], reverse=True)
        return selected_stocks
            
    except Exception:
        return []


def get_dragon_tiger_3days():
    """
    获取近3天龙虎榜都出现的股票，且5日涨幅大于5%的主板和创业板股票
    """
    try:
        today = datetime.now()
        all_dragon_tiger = {}
        
        for i in range(3):
            date = today - timedelta(days=i)
            date_str = date.strftime('%Y%m%d')
            
            try:
                dragon_tiger_df = ak.stock_lhb_detail_em(start_date=date_str, end_date=date_str)
                
                if dragon_tiger_df is not None and not dragon_tiger_df.empty:
                    all_dragon_tiger[date_str] = dragon_tiger_df
                
                time.sleep(0.5)
                
            except Exception:
                continue
        
        if not all_dragon_tiger:
            return []
        
        stock_counter = Counter()
        stock_info = {}
        
        for date_str, df in all_dragon_tiger.items():
            for _, row in df.iterrows():
                stock_code = str(row.get('代码', ''))
                if stock_code:
                    stock_counter[stock_code] += 1
                    stock_info[stock_code] = {
                        '代码': stock_code,
                        '名称': row.get('名称', 'N/A'),
                        '上榜日期': []
                    }
                    stock_info[stock_code]['上榜日期'].append(date_str)
        
        continuous_stocks = [code for code, count in stock_counter.items() if count >= 3]
        
        if not continuous_stocks:
            return []
        
        qualified_stocks = []
        
        for stock_code in continuous_stocks:
            if not (stock_code.startswith('60') or 
                    stock_code.startswith('00') or 
                    stock_code.startswith('30')):
                continue
            
            if stock_code.startswith('60'):
                board_type = '沪市主板'
            elif stock_code.startswith('00'):
                board_type = '深市主板'
            elif stock_code.startswith('30'):
                board_type = '创业板'
            else:
                continue
            
            try:
                hist_df = ak.stock_zh_a_hist(
                    symbol=stock_code,
                    period='daily',
                    start_date=(today - timedelta(days=10)).strftime('%Y%m%d'),
                    end_date=today.strftime('%Y%m%d'),
                    adjust='qfq'
                )
                
                if hist_df is not None and not hist_df.empty and len(hist_df) >= 5:
                    latest_price = hist_df['收盘'].iloc[-1]
                    price_5_days_ago = hist_df['收盘'].iloc[-5]
                    
                    if price_5_days_ago > 0:
                        gain_5d = ((latest_price - price_5_days_ago) / price_5_days_ago) * 100
                        
                        if gain_5d > 5:
                            qualified_stocks.append({
                                '代码': stock_code,
                                '名称': stock_info[stock_code]['名称'],
                                '板块类型': board_type,
                                '5日涨幅(%)': round(gain_5d, 2),
                                '最新价': round(latest_price, 2),
                                '上榜次数': stock_counter[stock_code],
                                '上榜日期': ', '.join(stock_info[stock_code]['上榜日期'])
                            })
                
                time.sleep(0.3)
                
            except Exception:
                continue
        
        qualified_stocks.sort(key=lambda x: x['5日涨幅(%)'], reverse=True)
        return qualified_stocks
            
    except Exception:
        return []


def get_today_market_analysis():
    """
    分析今天的行情：涨停板、跌停板、成交量最大等
    """
    try:
        result = {
            'limit_up': [],
            'limit_down': [],
            'volume_top': [],
            'turnover_top': [],
            'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        try:
            limit_up_df = ak.stock_zt_pool_em(date=datetime.now().strftime('%Y%m%d'))
            if limit_up_df is not None and not limit_up_df.empty:
                for _, row in limit_up_df.head(20).iterrows():
                    result['limit_up'].append({
                        '代码': row.get('代码', 'N/A'),
                        '名称': row.get('名称', 'N/A'),
                        '最新价': row.get('最新价', 'N/A'),
                        '涨跌幅(%)': row.get('涨跌幅', 'N/A'),
                        '封板时间': row.get('封板时间', 'N/A'),
                        '连板数': row.get('连板数', 'N/A')
                    })
            time.sleep(0.5)
        except Exception:
            pass
        
        try:
            limit_down_df = ak.stock_dt_pool_em(date=datetime.now().strftime('%Y%m%d'))
            if limit_down_df is not None and not limit_down_df.empty:
                for _, row in limit_down_df.head(20).iterrows():
                    result['limit_down'].append({
                        '代码': row.get('代码', 'N/A'),
                        '名称': row.get('名称', 'N/A'),
                        '最新价': row.get('最新价', 'N/A'),
                        '涨跌幅(%)': row.get('涨跌幅', 'N/A')
                    })
            time.sleep(0.5)
        except Exception:
            pass
        
        try:
            hist_df = ak.stock_zh_a_spot_em()
            if hist_df is not None and not hist_df.empty:
                hist_df['成交量'] = pd.to_numeric(hist_df.get('成交量', 0), errors='coerce')
                hist_df['成交额'] = pd.to_numeric(hist_df.get('成交额', 0), errors='coerce')
                hist_df['涨跌幅'] = pd.to_numeric(hist_df.get('涨跌幅', 0), errors='coerce')
                
                volume_top_df = hist_df.nlargest(20, '成交量')
                for _, row in volume_top_df.iterrows():
                    result['volume_top'].append({
                        '代码': row.get('代码', 'N/A'),
                        '名称': row.get('名称', 'N/A'),
                        '最新价': row.get('最新价', 'N/A'),
                        '涨跌幅(%)': row.get('涨跌幅', 'N/A'),
                        '成交量': row.get('成交量', 'N/A')
                    })
                
                turnover_top_df = hist_df.nlargest(20, '成交额')
                for _, row in turnover_top_df.iterrows():
                    result['turnover_top'].append({
                        '代码': row.get('代码', 'N/A'),
                        '名称': row.get('名称', 'N/A'),
                        '最新价': row.get('最新价', 'N/A'),
                        '涨跌幅(%)': row.get('涨跌幅', 'N/A'),
                        '成交额': row.get('成交额', 'N/A')
                    })
        except Exception:
            pass
        
        return result
            
    except Exception:
        return {
            'limit_up': [],
            'limit_down': [],
            'volume_top': [],
            'turnover_top': [],
            'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """首页"""
    return templates("index.html", {"request": request})


@app.get("/sectors", response_class=HTMLResponse)
async def sectors_page(request: Request):
    """板块分析页面"""
    sectors = get_sectors_with_3day_gains()
    return templates(
        "sectors.html",
        {"request": request, "sectors": sectors, "update_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    )


@app.get("/stocks", response_class=HTMLResponse)
async def stocks_page(request: Request):
    """股票筛选页面"""
    sectors = get_sectors_with_3day_gains()
    stocks = get_stocks_from_sectors(sectors)
    return templates(
        "stocks.html",
        {"request": request, "stocks": stocks, "sectors": sectors, "update_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    )


@app.get("/dragon-tiger", response_class=HTMLResponse)
async def dragon_tiger_page(request: Request):
    """龙虎榜分析页面"""
    stocks = get_dragon_tiger_3days()
    return templates(
        "dragon_tiger.html",
        {"request": request, "stocks": stocks, "update_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    )


@app.get("/today", response_class=HTMLResponse)
async def today_page(request: Request):
    """今天行情页面"""
    market_data = get_today_market_analysis()
    return templates(
        "today.html",
        {"request": request, "market_data": market_data, "update_time": market_data['update_time']}
    )


@app.get("/api/today")
async def today_api():
    """今天行情API接口"""
    market_data = get_today_market_analysis()
    return {
        "status": "success",
        "data": market_data,
        "update_time": market_data['update_time']
    }


@app.get("/api/dragon-tiger")
async def dragon_tiger_api():
    """龙虎榜API接口"""
    stocks = get_dragon_tiger_3days()
    return {
        "status": "success",
        "data": stocks,
        "update_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
