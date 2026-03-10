'''
=========================================================    
       @File     : 多线程.py
       @IDE      : PyCharm
       @Author   : Jing3
       @Date     : 2025/2/25 10:49
       @Desc     : 
=========================================================   
'''
import threading
import time
import requests
import execjs
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpblR5cGUiOiJsb2dpbiIsImxvZ2luSWQiOiJoNV91c2VyOjE1NzgwNDQ4NTk0OTQ2MjUyODAiLCJyblN0ciI6IkNRS3o0R1RrYXdObnFBclJ6MkxoWWY0S0FKQlJ1VWZTIn0.eq0UODwy3DqWHMQaP5Elw_utcMeVBAxzkwFJOnsd44Y",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Origin": "https://m.shengqingqy.cn",
    "Pragma": "no-cache",
    "Referer": "https://m.shengqingqy.cn/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Mobile Safari/537.36 Edg/133.0.0.0",
    "content-language": "zh-CN",
    "sec-ch-ua": "\"Not(A:Brand\";v=\"99\", \"Microsoft Edge\";v=\"133\", \"Chromium\";v=\"133\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\"",
    "token": "f23b3f3fff5c26e4a7a5591723fd6ff8"
}
# 定义需要监控的 ID 和价格
TARGETS = [
    {"id": "1893873287012458497", "price": 100},  # 小钻头
    {"id": "1893647694191648769", "price": 1000},  # 牛
    {"id": "1893914526362361858", "price": 1000},  # 大钻头
    {"id": "1893287210907533314", "price": 20},  # 腊梅
    {"id": "1894059474810425345", "price": 1000},  # 猫猫
    {"id": "1893647384007467009", "price": 500},  # 老鼠
]

def search_low_price(id, price):
    ret = execjs.compile(open('enc.js', 'r', encoding='utf-8').read()).call('getdata')
    # print(1)
    url = "https://api.shengqingqy.cn/market/app/market/list"
    data = {
        "pageNum": "1",
        "pageSize": "20",
        "type": "1",
        "key": "",
        "status": "",
        "sortType": "4",
        "productId": id,
        "sign_appid": "h5_23514861",
        "timestamp": str(int(time.time())),
        "nonce": ret[0],
        "sign": ret[1]
    }

    response = requests.get(url, headers=headers, data=data).json()
    try:
        logger.info(f"目前最低价为: {response['rows'][0]['id']} {response['rows'][0]['name']} ---- {response['rows'][0]['price']}")
        if int(response['rows'][0]['price'].replace('.0', '')) < price:
            make_order(response['rows'][0]['id'])
    except Exception as e:
        logger.info(f"暂无挂售: {e}")

def make_order(nft_id):
    ret = execjs.compile(open('enc.js', 'r', encoding='utf-8').read()).call('getdata')

    url = "https://api.shengqingqy.cn/order/app/order/preOrder"
    params = {
        "productId": nft_id,
        "count": "1",
        "type": "3",
        "firstBuyId": "",
        "ruleId": "",
        "randomCode": "",
        "sign_appid": "h5_23514861",
        "timestamp": str(int(time.time())),
        "nonce": ret[0],
        "sign": ret[1]
    }
    response = requests.get(url, headers=headers, params=params).json()
    if response['code'] == 200:
        requests.get('https://api.day.app/YToREckaeQXotQJPrn7MWa/青龙拿下啦！！！！！')

def monitor_target(target):
    while True:
        search_low_price(target["id"], target["price"])
        time.sleep(1)  # 每次检查后等待 32 秒

# 创建并启动线程
threads = []
for target in TARGETS:
    thread = threading.Thread(target=monitor_target, args=(target,))
    thread.start()
    threads.append(thread)

# 等待所有线程完成（理论上不会结束）
for thread in threads:
    thread.join()