import requests
import re


class SystemCookie:
    __returncookie = ''

    def __init__(self, base_url, base_ser,username,passwd):
        self.base_url = base_url
        self.base_service = base_ser
        self.username = username
        self.passwd = passwd

    def login_param(self):
        url = 'http://app.chinatowercom.cn/bridge/GenerateToken?url={0}'.format(self.base_url)
        header = {'Host': 'sso.chinatowercom.cn',
                  'Connection': 'keep-alive',
                  # 'Upgrade-Insecure-Requests': 1,
                  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                  'Accept-Encoding': 'gzip, deflate, sdch',
                  'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'}

        bridge_res = requests.get(url, headers=header)

        lt_value = re.findall('name="lt" value="(.*?)" /', bridge_res.content, re.S)[0]
        execution_value = re.findall('name="execution" value="(.*?)" /', bridge_res.content, re.S)[0]
        bridge_cookie = str(bridge_res.headers['Set-Cookie']).split(';')[0]

        SystemCookie.login_location(self, lt_value, execution_value, bridge_cookie)

    def login_location(self, lt_value, execution_value, bridge_cookie):
        b_c = bridge_cookie.split('=')[1]

        url = 'http://sso.chinatowercom.cn/cas/login;jsessionid={0}?service={1}'.format(b_c, self.base_service)

        datas = {'username': self.username,
                 'lt': lt_value,
                 'password': self.passwd,
                 'execution': execution_value,
                 '_eventId': 'submit'}

        headers = {'Host': 'sso.chinatowercom.cn',
                   'Connection': 'keep-alive',
                   # 'Content-Length': 111,
                   'Cache-Control': 'max-age=0',
                   'Origin': 'http://sso.chinatowercom.cn',
                   # 'Upgrade-Insecure-Requests': 1,
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
                   'Cookie': bridge_cookie}

        req_location = requests.post(url, headers=headers, data=datas, allow_redirects=False)

        SystemCookie.bridge_token(self, req_location.headers['location'])

    def bridge_token(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

        req_token = requests.get(url, headers=headers, allow_redirects=False)

        SystemCookie.pms_token(self, req_token.headers['location'], req_token.cookies)

    def pms_token(self, url, cookies):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

        req_tokken = requests.get(url, headers=headers, cookies=cookies, allow_redirects=False)

        SystemCookie.go_pms(self, req_tokken.headers['location'])

    def go_pms(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
            #    'Cookie': 'userstyle="lightgray/report"'
        }

        req_tokken = requests.get(url, headers=headers, allow_redirects=False)

        pms_cookies = req_tokken.cookies

        SystemCookie.__returncookie = pms_cookies

    def getAttr(self):
        return SystemCookie.__returncookie


def getpmscookie(username,passwd):
    base_url = 'http%3a%2f%2f123.126.34.222%3a16666%2fuflow%2fproblemPortal.jsp'
    base_service = 'http%3A%2F%2Fapp.chinatowercom.cn%2Fbridge%2FGenerateToken%3Furl%3Dhttp%253a%252f%252f123.126.34.222%253a16666%252fuflow%252fproblemPortal.jsp'


    pmslogin = SystemCookie(base_url, base_service,username,passwd)
    pmslogin.login_param()

    return pmslogin.getAttr()

if __name__ == '__main__':
    print getpmscookie('huqiao', 'valencia429')
