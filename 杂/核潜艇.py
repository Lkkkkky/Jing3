'''
=========================================================    
       @File     : 核潜艇.py
       @IDE      : PyCharm
       @Author   : Jing3
       @Date     : 2025/6/23 22:17
       @Desc     : 
=========================================================   
'''
import requests
import json
import ddddocr
import time

def get_vertify():
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://www.hjbwg.com",
        "Pragma": "no-cache",
        "Referer": "https://www.hjbwg.com/hdyy",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0",
        "authToken": "da3b96ea-2808-412c-b93d-c3adb46b6b7c",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    cookies = {
        "authToken": "da3b96ea-2808-412c-b93d-c3adb46b6b7c"
    }
    url = "https://www.hjbwg.com/blueapi/api/user/ck/getImageValidateCode"
    data = {}
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, cookies=cookies, data=data).json()
    print(response['data']['code'])
    return response['data']['code']

def get_v_image():
    bs64=get_vertify()


    ocr=ddddocr.DdddOcr(det=False,show_ad=False)
    code=ocr.classification(bs64)
    print(code)
    return code

def qiangpiao():
    code=get_v_image()
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://www.hjbwg.com",
        "Pragma": "no-cache",
        "Referer": "https://www.hjbwg.com/hdyy",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0",
        "authToken": "da3b96ea-2808-412c-b93d-c3adb46b6b7c",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    cookies = {
        "authToken": "da3b96ea-2808-412c-b93d-c3adb46b6b7c"
    }
    url = "https://www.hjbwg.com/ticketapi/api/activityOrder/ck/addActivityOrder"
    data = {
        "activityOrder": {
            "activityId": 7543,
            "liaisonPhone": "17717337711",
            "liaisonUser": "李昊霖",
            "activityVisitDate": "2025-06-28",
            "activityVisitTime": "09:30-09:40"
        },
        "activityMemberList": [
            {
                "userName": "刘金",
                "userIdCard": "342201198511240836",
                "userPhone": "",
                "userCertificateType": "ID_CARD",
                "ticketType": "VISIT_TICKET"
            },{
                "userName": "李牛",
                "userIdCard": "342201198601230615",
                "userPhone": "",
                "userCertificateType": "ID_CARD",
                "ticketType": "VISIT_TICKET"
            },{
                "userName": "刘煜辰",
                "userIdCard": "341302201211240418",
                "userPhone": "",
                "userCertificateType": "ID_CARD",
                "ticketType": "VISIT_TICKET"
            },{
                "userName": "李昊霖 ",
                "userIdCard": "341302201708030619",
                "userPhone": "",
                "userCertificateType": "ID_CARD",
                "ticketType": "VISIT_TICKET"
            }
        ],
        "validateCode": code
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, cookies=cookies, data=data)
    if "该时间段活动预约剩余人数不足" not in response.text and "图形验证码错误，请点击刷新！"not in response.text:
        requests.get('https://api.day.app/YToREckaeQXotQJPrn7MWa/核潛艇拿下')
    print(response.text)
    print(response)
for i in range(10000):
    qiangpiao()
