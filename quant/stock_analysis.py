import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import warnings
import time

warnings.filterwarnings('ignore')


def analyze_sectors_with_3day_gains():
    """
    分析仅三天涨幅维度大于3%的板块，挑选5只
    """
    print("=" * 60)
    print("三天涨幅大于3%的板块分析")
    print("=" * 60)
    
    try:
        # 获取东方财富行业板块数据
        sector_df = ak.stock_board_industry_name_em()
        
        if sector_df is None or sector_df.empty:
            print("未获取到板块列表")
            return None
        
        print(f"共获取到 {len(sector_df)} 个板块")
        
        # 筛选3日涨幅大于3%的板块
        # 尝试不同的列名
        gain_col = None
        for col in ['3日涨幅', '三日涨幅', '3日涨跌幅', '三日涨跌幅', '3日涨幅%', '3日涨跌幅%']:
            if col in sector_df.columns:
                gain_col = col
                break
        
        if gain_col:
            # 转换为数值类型
            sector_df[gain_col] = pd.to_numeric(sector_df[gain_col], errors='coerce')
            
            # 筛选涨幅大于3%的板块
            filtered = sector_df[sector_df[gain_col] > 3].copy()
            filtered = filtered.sort_values(gain_col, ascending=False)
            
            if not filtered.empty:
                top_5 = filtered.head(5)
                
                print(f"\n共找到 {len(filtered)} 个板块3日涨幅大于3%")
                print(f"\n{'排名':<6} {'板块名称':<20} {'3日涨幅(%)':<12} {'收盘价':<10}")
                print("-" * 50)
                for idx, (_, row) in enumerate(top_5.iterrows(), 1):
                    print(f"{idx:<6} {row.get('板块名称', 'N/A'):<20} {str(row.get(gain_col, 'N/A')):<12} {str(row.get('最新价', 'N/A')):<10}")
                
                return top_5
            else:
                print("没有找到3日涨幅大于3%的板块")
                return None
        else:
            print(f"未找到3日涨幅列，可用列: {sector_df.columns.tolist()}")
            return None
            
    except Exception as e:
        print(f"获取板块数据失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def select_stocks_from_sectors(sector_df):
    """
    从前面板块中选出沪深主板和创业板股票，近5日涨幅大于5%的股票
    """
    print("\n" + "=" * 60)
    print("从板块中筛选符合条件的股票")
    print("=" * 60)
    
    if sector_df is None or sector_df.empty:
        print("没有板块数据，无法筛选股票")
        return None
    
    try:
        selected_stocks = []
        
        # 遍历每个板块
        for idx, (_, sector) in enumerate(sector_df.iterrows()):
            sector_name = sector.get('板块名称', '')
            if not sector_name:
                continue
            
            print(f"\n正在获取板块: {sector_name}")
            
            try:
                # 获取板块成分股
                stocks_df = ak.stock_board_industry_cons_em(symbol=sector_name)
                
                if stocks_df is None or stocks_df.empty:
                    continue
                
                # 筛选沪深主板和创业板股票
                # 沪市主板: 60开头
                # 深市主板: 00开头
                # 创业板: 30开头
                for _, stock in stocks_df.iterrows():
                    stock_code = str(stock.get('代码', ''))
                    
                    if (stock_code.startswith('60') or 
                        stock_code.startswith('00') or 
                        stock_code.startswith('30')):
                        
                        # 判断板块类型
                        if stock_code.startswith('60'):
                            board_type = '沪市主板'
                        elif stock_code.startswith('00'):
                            board_type = '深市主板'
                        elif stock_code.startswith('30'):
                            board_type = '创业板'
                        else:
                            continue
                        
                        # 获取近5日涨幅
                        gain_5d = None
                        gain_col = None
                        for col in ['5日涨幅', '五日涨幅', '5日涨跌幅', '五日涨跌幅', '5日涨幅%', '5日涨跌幅%']:
                            if col in stocks_df.columns:
                                gain_col = col
                                break
                        
                        if gain_col:
                            gain_5d = stock.get(gain_col)
                            if gain_5d is not None:
                                try:
                                    gain_5d = float(gain_5d)
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
            except Exception as e:
                print(f"  获取板块 {sector_name} 成分股失败: {e}")
                continue
            
            time.sleep(0.5)
        
        if selected_stocks:
            result_df = pd.DataFrame(selected_stocks)
            result_df = result_df.sort_values('5日涨幅(%)', ascending=False)
            
            print(f"\n共找到 {len(result_df)} 只符合条件的股票:")
            print(f"\n{'代码':<10} {'名称':<15} {'所属板块':<20} {'板块类型':<10} {'5日涨幅(%)':<10}")
            print("-" * 70)
            for _, row in result_df.iterrows():
                print(f"{row['代码']:<10} {row['名称']:<15} {row['所属板块']:<20} {row['板块类型']:<10} {row['5日涨幅(%)']:<10}")
            
            return result_df
        else:
            print("没有找到符合条件的股票")
            return None
            
    except Exception as e:
        print(f"筛选股票失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def get_tomorrow_earnings_stocks():
    """
    分析明天发布财报的股票，仅限主板和创业板
    """
    print("\n" + "=" * 60)
    print("明天发布财报的股票（主板和创业板）")
    print("=" * 60)
    
    try:
        # 计算明天的日期
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_str = tomorrow.strftime('%Y%m%d')
        
        print(f"查询日期: {tomorrow_str}")
        
        # 获取财报日历数据
        earnings_df = ak.stock_yjbb_em(date=tomorrow_str)
        
        if earnings_df is not None and not earnings_df.empty:
            print(f"数据列: {earnings_df.columns.tolist()}")
            print(f"共获取到 {len(earnings_df)} 只股票")
            
            # 筛选主板和创业板股票
            # 主板: 60开头(沪市), 00开头(深市主板)
            # 创业板: 30开头
            filtered_stocks = []
            
            for _, row in earnings_df.iterrows():
                stock_code = str(row.get('代码', ''))
                if (stock_code.startswith('60') or 
                    stock_code.startswith('00') or 
                    stock_code.startswith('30')):
                    
                    # 判断板块类型
                    if stock_code.startswith('60'):
                        board_type = '沪市主板'
                    elif stock_code.startswith('00'):
                        board_type = '深市主板'
                    elif stock_code.startswith('30'):
                        board_type = '创业板'
                    else:
                        continue
                    
                    filtered_stocks.append({
                        '代码': stock_code,
                        '名称': row.get('名称', 'N/A'),
                        '板块': board_type,
                        '预约披露日期': row.get('预约披露日期', tomorrow_str),
                        '每股收益': row.get('每股收益', 'N/A'),
                        '净利润': row.get('净利润', 'N/A')
                    })
            
            if filtered_stocks:
                result_df = pd.DataFrame(filtered_stocks)
                print(f"\n共找到 {len(result_df)} 只主板和创业板股票:")
                print(f"\n{'代码':<10} {'名称':<15} {'板块':<12} {'每股收益':<10}")
                print("-" * 50)
                
                for _, row in result_df.head(50).iterrows():
                    print(f"{row['代码']:<10} {row['名称']:<15} {row['板块']:<12} {str(row['每股收益']):<10}")
                
                return result_df
            else:
                print("明天没有主板和创业板的财报发布")
                return None
        else:
            print(f"未获取到 {tomorrow_str} 的财报数据")
            return None
            
    except Exception as e:
        print(f"获取财报数据失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def get_dragon_tiger_top_100():
    """
    获取当天龙虎榜前100的股票
    """
    print("\n" + "=" * 60)
    print("当天龙虎榜前100股票")
    print("=" * 60)
    
    try:
        # 获取今天的日期
        today = datetime.now().strftime('%Y%m%d')
        
        print(f"查询日期: {today}")
        
        # 获取龙虎榜数据
        dragon_tiger_df = ak.stock_lhb_detail_em(start_date=today, end_date=today)
        
        if dragon_tiger_df is not None and not dragon_tiger_df.empty:
            print(f"共获取到 {len(dragon_tiger_df)} 只上榜股票")
            
            # 使用龙虎榜买入额列
            buy_col = '龙虎榜买入额'
            
            if buy_col in dragon_tiger_df.columns:
                # 按买入金额排序，取前100
                dragon_tiger_df = dragon_tiger_df.sort_values(buy_col, ascending=False)
                top_100 = dragon_tiger_df.head(100)
                
                print(f"\n{'排名':<6} {'代码':<10} {'名称':<15} {'买入额(万)':<12} {'卖出额(万)':<12} {'净额(万)':<12}")
                print("-" * 70)
                
                for idx, (_, row) in enumerate(top_100.iterrows(), 1):
                    buy_amount = round(row.get('龙虎榜买入额', 0) / 10000, 2)
                    sell_amount = round(row.get('龙虎榜卖出额', 0) / 10000, 2)
                    net_amount = round(row.get('龙虎榜净买额', 0) / 10000, 2)
                    
                    print(f"{idx:<6} {row.get('代码', 'N/A'):<10} {row.get('名称', 'N/A'):<15} {buy_amount:<12} {sell_amount:<12} {net_amount:<12}")
                
                return top_100
            else:
                print(f"未找到买入金额列，可用列: {dragon_tiger_df.columns.tolist()}")
                return None
        else:
            print(f"今天({today})没有龙虎榜数据")
            return None
            
    except Exception as e:
        print(f"获取龙虎榜数据失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """
    主函数：执行所有分析任务
    """
    print("股票分析脚本启动")
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # 1. 分析近三天涨幅大于3%的板块，挑选5只
    top_sectors = analyze_sectors_with_3day_gains()
    
    # 2. 从前面板块中选出沪深主板和创业板股票，近5日涨幅大于5%的股票
    selected_stocks = select_stocks_from_sectors(top_sectors)
    
    # 3. 分析明天发布财报的股票（主板和创业板）
    tomorrow_earnings = get_tomorrow_earnings_stocks()
    
    # 4. 获取当天龙虎榜前100的股票
    dragon_tiger = get_dragon_tiger_top_100()
    
    print("\n" + "=" * 60)
    print("分析完成")
    print("=" * 60)


if __name__ == '__main__':
    main()
