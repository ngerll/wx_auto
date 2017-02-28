# -*- coding:utf-8 -*-
import sys
import requests

reload(sys)
sys.setdefaultencoding('utf-8')


def te():
    headers = {'Authorization': 'zdio4dzwyth4gxdx0vn27ftxutz6lqhhgbh8tyti'}
    res = requests.get('https://openapi.daocloud.io/v1/apps', headers=headers).json()

    for rapp in  res['app']:
        if rapp['name'] == 'wx_auto':
            if rapp['state'] == 'stopped':
                appid = rapp['id']

                surl = 'https://openapi.daocloud.io/v1/apps/%s/actions/start' % appid

                sapp = requests.post(surl,headers=headers).json()

                return '启动命令生效'
            else:
                return '已启动'

if __name__ == '__main__':
    print te()