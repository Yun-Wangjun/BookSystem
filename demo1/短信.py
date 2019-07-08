# 接口类型：互亿无线触发短信接口，支持发送验证码短信、订单通知短信等。
# 账户注册：请通过该地址开通账户http://sms.ihuyi.com/register.html
# 注意事项：
# （1）调试期间，请使用用系统默认的短信内容：您的验证码是：【变量】。请不要把验证码泄露给其他人。；
# （2）请使用APIID（查看APIID请登录用户中心->验证码短信->产品总览->APIID）及 APIkey来调用接口；
# （3）该代码仅供接入互亿无线短信接口参考使用，客户可根据实际需要自行编写；
#发送短信
#APIID：C11345804
#APIKEY：735d183ae02189f678c26800ac19b03a

# !/usr/local/bin/python
# -*- coding:utf-8 -*-
import http.client
import urllib

host = "106.ihuyi.com"
sms_send_uri = "/webservice/sms.php?method=Submit"

# 用户名是登录用户中心->验证码短信->产品总览->APIID
account = "C39724036"
# 密码 查看密码请登录用户中心->验证码短信->产品总览->APIKEY
password = "0a7e0b00b9f7b8f9933a4896e9527d12 "

def send_sms(text, mobile):
    params = urllib.parse.urlencode(
        {'account': account, 'password': password, 'content': text, 'mobile': mobile, 'format': 'json'})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection(host, port=80, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str


if __name__ == '__main__':
    #需要接受短信的目标手机号
    mobile = "17868876131"
    text = "您的验证码是：121254。请不要把验证码泄露给其他人。"
    ret = send_sms(text, mobile).decode('utf-8')
    import json
    ret = json.loads(ret)
    print(ret)
