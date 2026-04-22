import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import warnings
import time
from collections import Counter

warnings.filterwarnings('ignore')


def get_dragon_tiger_3days():
    """
    获取近3天龙虎榜都出现的股票，且5日涨幅大于5%的主板和创业板股票
    """
    print("=" * 60)
    print("近3天龙虎榜连续上榜股票分析")
    print("=" * 60)
    
    try:
        # 获取今天和3天前的日期
        today = datetime.now()
        
        all_dragon_tiger = {}
        
        # 遍历近3天的每一天
        for i in range(3):
            date = today - timedelta(days=i)
            date_str = date.strftime('%Y%m%d')
            
            print(f"\n正在获取 {date_str} 的龙虎榜数据...")
            
            try:
                dragon_tiger_df = ak.stock_lhb_detail_em(start_date=date_str, end_date=date_str)
                
                if dragon_tiger_df is not None and not dragon_tiger_df.empty:
                    all_dragon_tiger[date_str] = dragon_tiger_df
                    print(f"  获取到 {len(dragon_tiger_df)} 只股票")
                else:
                    print(f"  {date_str} 没有龙虎榜数据")
                
                time.sleep(0.5)
                
            except Exception as e:
                print(f"  获取 {date_str} 数据失败: {e}")
                continue
        
        if not all_dragon_tiger:
            print("近3天没有获取到龙虎榜数据")
            return None
        
        # 统计每只股票上榜次数
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
        
        # 筛选3天都上榜的股票
        continuous_stocks = [code for code, count in stock_counter.items() if count >= 3]
        
        print(f"\n近3天连续上榜的股票: {len(continuous_stocks)} 只")
        
        if not continuous_stocks:
            print("没有连续3天上榜的股票")
            return None
        
        # 筛选主板和创业板股票，并获取5日涨幅
        qualified_stocks = []
        
        for stock_code in continuous_stocks:
            # 筛选主板和创业板
            if not (stock_code.startswith('60') or 
                    stock_code.startswith('00') or 
                    stock_code.startswith('30')):
                continue
            
            # 判断板块类型
            if stock_code.startswith('60'):
                board_type = '沪市主板'
            elif stock_code.startswith('00'):
                board_type = '深市主板'
            elif stock_code.startswith('30'):
                board_type = '创业板'
            else:
                continue
            
            # 获取个股5日涨幅
            try:
                print(f"\n正在获取 {stock_code} 的5日涨幅数据...")
                
                # 获取个股历史数据
                hist_df = ak.stock_zh_a_hist(
                    symbol=stock_code,
                    period='daily',
                    start_date=(today - timedelta(days=10)).strftime('%Y%m%d'),
                    end_date=today.strftime('%Y%m%d'),
                    adjust='qfq'
                )
                
                if hist_df is not None and not hist_df.empty and len(hist_df) >= 5:
                    # 计算5日涨幅
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
                            print(f"  符合条件! 5日涨幅: {gain_5d:.2f}%")
                        else:
                            print(f"  5日涨幅: {gain_5d:.2f}% (不符合>5%条件)")
                    else:
                        print(f"  无法计算5日涨幅")
                else:
                    print(f"  历史数据不足")
                
                time.sleep(0.3)
                
            except Exception as e:
                print(f"  获取 {stock_code} 历史数据失败: {e}")
                continue
        
        if qualified_stocks:
            result_df = pd.DataFrame(qualified_stocks)
            result_df = result_df.sort_values('5日涨幅(%)', ascending=False)
            
            print(f"\n" + "=" * 60)
            print(f"符合条件的股票共 {len(result_df)} 只:")
            print(f"  - 近3天连续上榜")
            print(f"  - 主板或创业板")
            print(f"  - 5日涨幅 > 5%")
            print("=" * 60)
            
            print(f"\n{'代码':<10} {'名称':<15} {'板块':<10} {'5日涨幅(%)':<12} {'最新价':<10} {'上榜日期'}")
            print("-" * 80)
            
            for _, row in result_df.iterrows():
                print(f"{row['代码']:<10} {row['名称']:<15} {row['板块类型']:<10} {row['5日涨幅(%)']:<12} {row['最新价']:<10} {row['上榜日期']}")
            
            return result_df
        else:
            print("\n没有找到符合条件的股票")
            return None
            
    except Exception as e:
        print(f"分析失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """
    主函数：执行龙虎榜分析
    """
    print("龙虎榜连续上榜股票分析脚本启动")
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # 获取近3天连续上榜且5日涨幅>5%的主板/创业板股票
    result = get_dragon_tiger_3days()
    
    print("\n" + "=" * 60)
    print("分析完成")
    print("=" * 60)


if __name__ == '__main__':
    main()
