'''
拉勾网模拟登陆
思路解析：
1.login页面的get 与 post 网址；
2.post数据中需要传递的数据：用户名和密码；其中密码采用了加密方式，在json文件中找到该密码的加密方式；
3.post请求中的headers需要携带'X-Anit-Forge-Token'和'X-Anit-Forge-Code'，这两个数据可以从请求页源文件中获取；
'''

import requests
import hashlib
import re

session = requests.session()

HEADERS = {
    "Referer": "https://passport.lagou.com/login/login.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
}


#通过相应的json文件获取相应的密码加密方式
def get_password(password):
    password=hashlib.md5(password.encode('utf-8')).hexdigest()
    password = 'veenike' + password + 'veenike'
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    return password

#获取'X-Anit-Forge-Token'和'X-Anit-Forge-Code'
def get_token():
    Forge_Token = ""
    Forge_Code = ""
    login_page = 'https://passport.lagou.com/login/login.html'
    data = session.get(login_page, headers=HEADERS)
    match_obj = re.match(r'.*X_Anti_Forge_Token = \'(.*?)\';.*X_Anti_Forge_Code = \'(\d+?)\'', data.text, re.DOTALL)
    if match_obj:
        Forge_Token = match_obj.group(1)
        Forge_Code = match_obj.group(2)
    return Forge_Token, Forge_Code

#构建headers，发送登陆信息
def login(username ,password):
    Forge_Token, Forge_Code = get_token()
    login_headers = HEADERS.copy()
    login_headers.update({'X-Requested-With': 'XMLHttpRequest', 'X-Anit-Forge-Token': Forge_Token, 'X-Anit-Forge-Code': Forge_Code})
    passwd = get_password(password)
    postdata = {
        "isValidate": "true",
        "password": passwd,
        "request_form_verifyCode":"",
        "submit":"",
        "username": username,
    }
    response = session.post('https://passport.lagou.com/login/login.json',data=postdata,headers = login_headers)
    print(response.text)

def get_cookie():
    return requests.utils.dict_from_cookiejar(session.cookies)


if __name__ == '__main__':
    username = '请输入用户名'
    password = '请输入密码'
    login(username,password)
    print(get_cookie())

