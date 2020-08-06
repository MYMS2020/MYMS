import time
import requests
import schedule
import threading
import random
import json

url = 'http://swxg.haust.edu.cn/xgh5/openData'

State = 0

header = {'Content-Type': 'application/x-www-form-urlencoded',
          'Connection': 'keep-alive',
          'Origin': 'http://swxg.haust.edu.cn',
          'X-Requested-With': 'XMLHttpRequest',
          'Accept-Encoding':'gzip, deflate',
          'Accept-Language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
          'Referer':'http://swxg.haust.edu.cn/xgh5/stu/bpa/yq_info.html?eCiO8e6SvujIOfdQGvwKfg==',
          'User-Agent': 'Mozilla/5.0 (Linux; Android 10; PCT-AL10 Build/HUAWEIPCT-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36 SuperApp',
          'userToken':'eyJhbGciOiJSUzUxMiJ9.eyJzdWIiOiIxNzE0MDQwMTAyMjUiLCJST0xFUyI6IlJPTEVfQURNSU4sYWRtaW5pc3RyYXRvcix1c2VyIiwiY3JlYXRlZCI6MTU4MDcwOTM1NDI3NiwiZXhwIjoxNTk3OTg4MjQ4fQ.aPAVMtH7naU-UwP16u7IjNybgmbtqE7HM2ZC-aL3dFuRuYvOLR3AFrtv9B7WPdVuiP-5EW-PVgyDR803gG8fhD3S0naTbNaw_7zwcwWGWuvKP3Y6nZVyEXDcodRDrFpB7_CW8aYvMgonc53RQ3uJ287xg5_m4En2C3bwY-gdHnI'
} 

UserAgents = [
    "Mozilla/5.0 (Linux; Android 10; PCT-AL10 Build/HUAWEIPCT-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36 SuperApp",
    "Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.1; PAR-AL00 Build/HUAWEIPAR-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044304 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/WIFI Language/zh_CN Process/tools",
    "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043807 Mobile Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 7.1.1; OD103 Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/4G Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 6.0.1; SM919 Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 5.1.1; vivo X6S A Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 5.1; HUAWEI TAG-AL00 Build/HUAWEITAG-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043622 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/4G Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043807 Mobile Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/4G Language/zh_CN MicroMessenger/6.6.1.1220(0x26060135) NetType/4G Language/zh_CN miniProgram"
]

sjHead = ["139","138","137","136","135","134","159","158","157","150","151","152","188","187","182","183","184","178","130","131","132","156","155","186","185","176","133","153","189","180","181","177"]

xhs = ["171404010225",
      "171404010211",  
      "171404010148", #赵建业
      "171404010117", #冀浩峰
      "171404010235", #张家溢
      "171404010311", #韩子豪
      "171404010107"  #代强强
]
O_O = {"cmd":"yqsbFormSave",
      "xh":"",
      "sbsj":"",
      "nl":"20",
      "lxfs":"",
      "jzdq":"411402",
      "jzdq_xxdz":"略",
      "tw":"36.5",
      "sflx":"0",
      "jcbr":"0",
      "zyzz":"1,",
      "fbrq":"",
      "zyzzms":"",
      "bz":"",
      "bz1":"",
      "wcjtgj":"",
      "wcjtgjxq":"",
      "wcdq":"",
      "wcdqxxdz":"",
      "lkdate":"",
      "fhdate":"",
      "zszt":"",
      "ylzd1":"",
      "qrblxqdz":"",
      "qrbltjdz":"",
      "jcdq":"",
      "jcxxdz":"",
      "jcsj":"",
      "qzsj":"",
      "zlyy":"",
      "zysj":""
}

I_I = {"cmd":"checkXsYqsbQx",
      "xh":""
}

timestamp = int(round((time.time() * 1000)))
times = time.strftime("%Y-%m-%d")

data = {
#    "timeStamp":timestamp,
    "command":"XGXT",
    "param":str(O_O)
}

checkdata = {
#    "timeStamp":timestamp,
    "command":"XGXT",
    "param":str(I_I)
}

BPA = 1

content = times+"：今日已完成报平安！！！"

def job():
    global BPA
    State = -1
    for xh in xhs:
        O_O["xh"] = xh
        O_O["tw"] = str(round(random.uniform(36,37),1))
        I_I["xh"] = xh
        data["param"] = str(O_O)
        checkdata["param"] = str(I_I)
        O_O["lxfs"] = "".join(random.sample(sjHead,1)) + str(random.randint(1,99999999))
        header["User-Agents"] = "".join(random.sample(UserAgents,1))
        print("  ",xh,":")

        r = requests.post(url=url,data=checkdata,headers=header)
        print("    ",r,r.text)
        text = json.loads(r.text)
        if (int(text["data"]) != -1):
            r = requests.post(url=url,data=data,headers=header)
            print("  ",O_O["xh"],":")
            print("    ",r,r.text)
            r = requests.post(url=url,data=checkdata,headers=header)
            print("    ",r,r.text)
            text = json.loads(r.text)
            if (int(text["data"]) != -1):
                State = text["data"]
                print("    未报平安，状态码：",State)
    if (State == -1):
        schedule.cancel_job(BPAN)
        BPA = 0
        print("报平安结果：",times,"全部通过！！！")
        print(content)
    time.sleep(1)

def BPAN():
    times = time.strftime("%Y-%m-%d")
    O_O["sbsj"] = times
    print(times,":")
    job_thread = threading.Thread(target=job)
    job_thread.start()

schedule.every().day.at("06:00").do(BPAN)
schedule.every().day.at("08:00").do(BPAN)
schedule.every().hour.do(BPAN)
schedule.every().minutes.do(BPAN)

if __name__ == '__main__':
    if BPA:
        BPAN()
        time.sleep(3)
    while BPA:
        schedule.run_pending()
        time.sleep(1)
