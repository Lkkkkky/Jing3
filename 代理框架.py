'''
=========================================================    
       @File     : 代理框架.py
       @IDE      : PyCharm
       @Author   : Jing3
       @Date     : 2025/1/8 18:04
       @Desc     : 
=========================================================   
'''
import requests
import json
import time
def get_proxy():
    r = requests.get(
        "http://route.xiongmaodaili.com/xiongmao-web/apiPlus/vgl?secret=b6840f11b6ca4cb1bf1e6e022eea51f9&orderNo=VGL20260113153705yL8IUrkJ&count=1&isTxt=0&proxyType=1&validTime=0&removal=0&cityIds=&returnAccount=2",
        verify=False, allow_redirects=False)
    r.encoding = 'utf8'

    resp_dict = json.loads(r.text)
    resp_dict_list = resp_dict.get('obj')
    print(resp_dict_list)
    return resp_dict_list


proxy_dict = get_proxy()
for ip_dict in proxy_dict:
    ip = ip_dict.get('ip')
    port = ip_dict.get('port')
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), end=' ')
    print(f'取到ip为{ip}:{port}')
    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": ip,
        "port": port,
        # 代理认证的用户名
        "user": ip_dict.get('account'),
        # 代理认证的密码
        "pass": ip_dict.get('password'),
    }
    ip = proxyMeta
proxy = {"http": ip, "https": ip}