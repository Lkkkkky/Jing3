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

token='e91662f2b1da4a528b14ee2454314b4e1752876741397'
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
    "token": token
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

# 投注策略选择 (1=策略一: 7连反压, 2=策略二: 5连反压)
BET_STRATEGY = 2

# 投注记录 - 存储投注信息用于验证结果
bet_records = []  # 格式: [{'plan_no': '期号', 'bet_type': '投注类型', 'bet_time': '投注时间'}]

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
    global continuous_odd_even_count, last_odd_even, continuous_size_count, last_size, continuous_dragon_tiger_count, last_dragon_tiger, lottery_results, bet_records
    
    # 检查是否是新的期号
    if lottery_results and lottery_results[-1]['issue'] == new_data['issue']:
        return  # 如果是相同期号，不处理
    
    # 检查投注结果
    current_issue = new_data['issue']
    for bet_record in bet_records:
        if bet_record['plan_no'] == current_issue:
            # 计算当前期开奖结果
            code_list = new_data['code'].split(',')
            total_sum = sum(int(num) for num in code_list)
            current_odd_even = total_sum % 2  # 0为双，1为单
            current_size = 0 if total_sum <= 22 else 1  # 0为小，1为大
            first_digit = int(code_list[0])
            last_digit = int(code_list[-1])
            current_dragon_tiger = 1 if first_digit > last_digit else 0  # 1为龙，0为虎
            
            # 判断投注是否中奖
            bet_type = bet_record['bet_type']
            is_win = False
            if bet_type == '单' and current_odd_even == 1:
                is_win = True
            elif bet_type == '双' and current_odd_even == 0:
                is_win = True
            elif bet_type == '大' and current_size == 1:
                is_win = True
            elif bet_type == '小' and current_size == 0:
                is_win = True
            elif bet_type == '龙' and current_dragon_tiger == 1:
                is_win = True
            elif bet_type == '虎' and current_dragon_tiger == 0:
                is_win = True
            
            if is_win:
                yue=get_user_balance()
                requests.get(
                    f'https://api.day.app/YToREckaeQXotQJPrn7MWa/中啦！投注{bet_type}成功！期号：{current_issue}当前余额{yue}')
                
            else:
                requests.get(f'https://api.day.app/YToREckaeQXotQJPrn7MWa/很遗憾没压中{bet_type}期号：{current_issue} ')
            
            # 移除已验证的投注记录
            bet_records.remove(bet_record)
            break
    
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
    
    # 根据策略执行投注逻辑
    if BET_STRATEGY == 1:
        # 策略一：7连反压
        if continuous_odd_even_count > 6:
            print("⚠️ 警告: 22222 - 单双连续期数超过6期!")
            # 7连单投注双，7连双投注单
            if continuous_odd_even_count == 7:
                next_plan = get_next_plan_no(new_data['issue'])
                if next_plan:
                    bet_target = '双' if current_odd_even == 1 else '单'
                    print(f"🚀 策略一触发: 7连{odd_even_text}，投注{bet_target}")
                    bet(bet_target, next_plan)
        
        if continuous_size_count > 6:
            print("⚠️ 警告: 22222 - 大小连续期数超过6期!")
            requests.get(f'https://api.day.app/YToREckaeQXotQJPrn7MWa/pc连续{continuous_size_count}期{size_text}啦！！！！！')
            # 7连大投注小，7连小投注大
            if continuous_size_count == 7:
                next_plan = get_next_plan_no(new_data['issue'])
                if next_plan:
                    bet_target = '小' if current_size == 1 else '大'
                    print(f"🚀 策略一触发: 7连{size_text}，投注{bet_target}")
                    bet(bet_target, next_plan)
        
        if continuous_dragon_tiger_count > 6:
            print("⚠️ 警告: 22222 - 龙虎连续期数超过6期!")
            # 7连龙投注虎，7连虎投注龙
            if continuous_dragon_tiger_count == 7:
                next_plan = get_next_plan_no(new_data['issue'])
                if next_plan:
                    bet_target = '虎' if current_dragon_tiger == 1 else '龙'
                    print(f"🚀 策略一触发: 7连{dragon_tiger_text}，投注{bet_target}")
                    bet(bet_target, next_plan)
    
    elif BET_STRATEGY == 2:
        # 策略二：5连反压
        if continuous_odd_even_count == 5:
            next_plan = get_next_plan_no(new_data['issue'])
            if next_plan:
                bet_target = '双' if current_odd_even == 1 else '单'
                print(f"🚀 策略二触发: 5连{odd_even_text}，投注{bet_target}")
                bet(bet_target, next_plan)
        
        if continuous_size_count == 5:
            next_plan = get_next_plan_no(new_data['issue'])
            if next_plan:
                bet_target = '小' if current_size == 1 else '大'
                print(f"🚀 策略二触发: 5连{size_text}，投注{bet_target}")
                bet(bet_target, next_plan)
        
        if continuous_dragon_tiger_count == 5:
            next_plan = get_next_plan_no(new_data['issue'])
            if next_plan:
                bet_target = '虎' if current_dragon_tiger == 1 else '龙'
                print(f"🚀 策略二触发: 5连{dragon_tiger_text}，投注{bet_target}")
                bet(bet_target, next_plan)
    
    # 通用警告（6期以上）
    if continuous_odd_even_count > 6:
        print("⚠️ 警告: 22222 - 单双连续期数超过6期!")
    if continuous_size_count > 6:
        print("⚠️ 警告: 22222 - 大小连续期数超过6期!")
        requests.get(f'https://api.day.app/YToREckaeQXotQJPrn7MWa/pc开始连续6期{size_text}啦！！！！！')
    if continuous_dragon_tiger_count > 6:
        print("⚠️ 警告: 22222 - 龙虎连续期数超过6期!")
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
    print(f"当前投注策略: {'策略一(7连反压)' if BET_STRATEGY == 1 else '策略二(5连反压)'}")
    print("-" * 60)
    
    # 首次获取数据
    initial_data = get_latest_lottery_data()
    if initial_data:
        analyze_lottery_data(initial_data)
    
    try:
        while True:
            time.sleep(10)  # 等待1分钟
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 正在请求最新开奖数据...")
            
            latest_data = get_latest_lottery_data()
            if latest_data:
                analyze_lottery_data(latest_data)
            else:
                print("未获取到数据")
                
    except KeyboardInterrupt:
        print("\n程序已停止")
        print(f"总共收集了 {len(lottery_results)} 期开奖数据")

def bet(bet_type, next_plan_no):
    """投注函数
    bet_type: 投注类型 ('大', '小', '单', '双', '龙', '虎')
    next_plan_no: 下一期期号
    """
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
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
        "token": token
    }

    # 投注参数映射：大----201010101----da    小----201010102----xiao   单----201010201----dan  双----201010202----shuang 龙----201010401----long 虎----201010501----hu
    bet_mapping = {
        '大': ('201010101', 'da'),
        '小': ('201010102', 'xiao'),
        '单': ('201010201', 'dan'),
        '双': ('201010202', 'shuang'),
        '龙': ('201010401', 'long'),
        '虎': ('201010501', 'hu')
    }
    
    if bet_type not in bet_mapping:
        print(f"错误：不支持的投注类型 {bet_type}")
        return
    
    play_id, bet_num = bet_mapping[bet_type]
    
    url = "https://yo02api-cf.l414br.com/coron/order/double/create"
    # URL编码的content值映射
    content_mapping = {
        '大': '%E5%A4%A7',
        '小': '%E5%B0%8F', 
        '单': '%E5%8D%95',
        '双': '%E5%8F%8C',
        '龙': '%E9%BE%99',
        '虎': '%E8%99%8E'
    }
    
    encoded_content = content_mapping.get(bet_type, bet_type)
    data = f"orderSource=2&bet%5B0%5D.playId={play_id}&bet%5B0%5D.betNum={bet_num}&bet%5B0%5D.betAmount=2&bet%5B0%5D.betCount=1&bet%5B0%5D.content={encoded_content}&ticketId=2&planNo={next_plan_no}"
    
    try:
        response = requests.post(url, headers=headers, data=data)
        print(f"🎯 自动投注: {bet_type} (期号: {next_plan_no})")
        print(f"投注结果: {response.text}")
        return response
    except Exception as e:
        print(f"投注失败: {e}")
        return None
def get_user_balance():
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "0",
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
        "token": token
    }
    url = "https://yo02api-cf.l414br.com/boracay/member/front/userInfo"
    response = requests.post(url, headers=headers).json()
    return response['data']['balance']
def get_next_plan_no(current_plan_no):
    """根据当前期号生成下一期期号"""
    try:
        # 解析期号格式：20250717-1272
        date_part, number_part = current_plan_no.split('-')
        next_number = int(number_part) + 1
        return f"{date_part}-{next_number:04d}"
    except Exception as e:
        print(f"期号解析失败: {e}")
        return None
if __name__ == "__main__":
    main()
