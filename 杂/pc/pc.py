'''
=========================================================    
       @File     : pc.py
       @IDE      : PyCharm
       @Author   : Jing3
       @Date     : 2025/7/17 01:00
       @Desc     : 
=========================================================   
'''
import requests
import time
from datetime import datetime


headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Origin": "https://yo02pc.kg3jt1.com",
    "Pragma": "no-cache",
    "Referer": "https://yo02pc.kg3jt1.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "device": "1",
    "lang": "zh_cn",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "timezone": "GMT+8",
    "token": "b7f15b97f7704f15949867cada6242511752685049185"
}
url = "https://yo02api-cf.l414br.com/coron/trendGraph/chart/history"
params = {
    "ticketId": "2",
    "num": "1"
}

# 初始化开奖号码列表和连续计数器
lottery_results = []  # 存储开奖结果的列表
continuous_odd_even_count = 0
last_odd_even = None
continuous_size_count = 0
last_size = None
continuous_dragon_tiger_count = 0
last_dragon_tiger = None

def get_latest_lottery_data():
    """获取最新的开奖数据"""
    try:
        response = requests.get(url, headers=headers, params=params).json()
        if response.get('data'):
            return response['data'][0]  # 获取最新一期数据
        return None
    except Exception as e:
        print(f"请求失败: {e}")
        return None

def analyze_lottery_data(new_data):
    """分析开奖数据并计算连续期号"""
    global continuous_odd_even_count, last_odd_even, continuous_size_count, last_size, continuous_dragon_tiger_count, last_dragon_tiger, lottery_results
    
    # 检查是否是新的期号
    if lottery_results and lottery_results[-1]['issue'] == new_data['issue']:
        return  # 如果是相同期号，不处理
    
    # 添加到开奖列表
    lottery_results.append(new_data)
    
    code_list = new_data['code'].split(',')
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 新开奖数据:")
    print(f"期号: {new_data['issue']}, 开奖号码: {code_list}")
    
    # 计算开奖号码总和
    total_sum = sum(int(num) for num in code_list)
    current_odd_even = total_sum % 2  # 0为双，1为单
    current_size = 0 if total_sum <= 22 else 1  # 0为小，1为大
    
    # 计算龙虎（首位和末位数字对比）
    first_digit = int(code_list[0])
    last_digit = int(code_list[-1])
    current_dragon_tiger = 1 if first_digit > last_digit else 0  # 1为龙，0为虎
    
    odd_even_text = '单' if current_odd_even == 1 else '双'
    size_text = '小' if current_size == 0 else '大'
    dragon_tiger_text = '龙' if current_dragon_tiger == 1 else '虎'
    print(f"总和: {total_sum}, {odd_even_text}, {size_text}, {dragon_tiger_text}(首位{first_digit}vs末位{last_digit})")
    
    # 判断单双是否连续
    if last_odd_even is None:
        # 第一期，初始化
        continuous_odd_even_count = 1
    elif last_odd_even == current_odd_even:
        # 与上一期相同，连续计数+1
        continuous_odd_even_count += 1
    else:
        # 与上一期不同，重置计数
        continuous_odd_even_count = 1
    
    # 判断大小是否连续
    if last_size is None:
        # 第一期，初始化
        continuous_size_count = 1
    elif last_size == current_size:
        # 与上一期相同，连续计数+1
        continuous_size_count += 1
    else:
        # 与上一期不同，重置计数
        continuous_size_count = 1
    
    # 判断龙虎是否连续
    if last_dragon_tiger is None:
        # 第一期，初始化
        continuous_dragon_tiger_count = 1
    elif last_dragon_tiger == current_dragon_tiger:
        # 与上一期相同，连续计数+1
        continuous_dragon_tiger_count += 1
    else:
        # 与上一期不同，重置计数
        continuous_dragon_tiger_count = 1
    
    print(f"连续{odd_even_text}期数: {continuous_odd_even_count}, 连续{size_text}期数: {continuous_size_count}, 连续{dragon_tiger_text}期数: {continuous_dragon_tiger_count}")
    
    # 检查是否连续超过6期
    if continuous_odd_even_count > 6:
        print("⚠️ 警告: 22222 - 单双连续期数超过6期!")
        requests.get(f'https://api.day.app/YToREckaeQXotQJPrn7MWa/pc开始连续6期{odd_even_text}啦！！！！！')
    if continuous_size_count > 6:
        print("⚠️ 警告: 22222 - 大小连续期数超过6期!")
        requests.get(f'https://api.day.app/YToREckaeQXotQJPrn7MWa/pc开始连续6期{size_text}啦！！！！！')
    if continuous_dragon_tiger_count > 6:
        print("⚠️ 警告: 22222 - 龙虎连续期数超过6期!")
        requests.get(f'https://api.day.app/YToREckaeQXotQJPrn7MWa/pc开始连续6期{dragon_tiger_text}啦！！！！！')
    # 更新上一期状态
    last_odd_even = current_odd_even
    last_size = current_size
    last_dragon_tiger = current_dragon_tiger
    
    # 显示当前列表中的期号数量
    print(f"当前列表中共有 {len(lottery_results)} 期开奖数据")
    print("-" * 60)

def main():
    """主函数 - 每分钟请求一次接口"""
    print("开始监控彩票开奖数据...")
    print("每分钟请求一次接口，按 Ctrl+C 停止")
    
    # 首次获取数据
    initial_data = get_latest_lottery_data()
    if initial_data:
        analyze_lottery_data(initial_data)
    
    try:
        while True:
            time.sleep(5)  # 等待1分钟
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 正在请求最新开奖数据...")
            
            latest_data = get_latest_lottery_data()
            if latest_data:
                analyze_lottery_data(latest_data)
            else:
                print("未获取到数据")
                
    except KeyboardInterrupt:
        print("\n程序已停止")
        print(f"总共收集了 {len(lottery_results)} 期开奖数据")

if __name__ == "__main__":
    main()
