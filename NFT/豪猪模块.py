'''
=========================================================    
       @File     : 豪猪模块.py
       @IDE      : PyCharm
       @Author   : Jing3
       @Date     : 2025/3/19 02:00
       @Desc     : 
=========================================================   
'''
import requests
import time
from loguru import logger


def login():
    response=requests.get('https://api.haozhuma.com/sms/?api=login&user=db9d44ce09b33035e60f817d368429e124b49f64671f21ed&pass=876bacf58d02fd8080c8fb9a1cb6acb6d473ed0abc06dee8')
    token=response.json()['token']
    # logger.info(response.text)
    response=requests.get(f'https://api.haozhuma.com/sms/?api=getSummary&token={token}')
    logger.info('登录成功,余额为:'+response.json()['money'])
    return token
def get_number(token,item_id):
    response = requests.get(f'https://api.haozhuma.com/sms/?api=getPhone&token={token}&sid={item_id}&ascription=2')#只取实卡
    print(response.text)
    return response.json()['phone']

def get_yzm(token,item_id,phone):
    for i in range(60):  # 将循环次数限制为60次
        response = requests.get(f'https://api.haozhuma.com/sms/?api=getMessage&token={token}&sid={item_id}&phone={phone}')#只取实卡
        if(response.json()['code']=='0'):
            print(response.text)
            return response.json()['yzm']
        logger.info(f'正在获取验证码{phone}')
        time.sleep(1)
    # 如果60次尝试后仍未获取到验证码，则重新获取
    logger.info(f'获取验证码超时，重新获取{phone}')
    return get_yzm(token, item_id, phone)  # 递归调用自身重新获取
def cancelAllRecv(token):
    response = requests.get(f'https://api.haozhuma.cn/sms/?api=cancelAllRecv&token={token}')#释放所有号码
    print(response.text)


