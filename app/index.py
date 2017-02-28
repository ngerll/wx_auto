# -*- coding:utf-8 -*-
import sys
import requests
from flask import Flask, render_template
from weixinser import robot
from werobot.contrib.flask import make_view

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

app.add_url_rule(rule='/weixinser/',
                 endpoint='werobot',
                 view_func=make_view(robot),
                 methods=['GET', 'POST'])


@app.route('/sp')
def sp():
    headers = {'Authorization': 'zdio4dzwyth4gxdx0vn27ftxutz6lqhhgbh8tyti'}
    res = requests.get('https://openapi.daocloud.io/v1/apps', headers=headers).json()

    for rapp in res['app']:
        if rapp['name'] == 'wx_auto':
            if rapp['state'] == 'stopped':
                appid = rapp['id']

                surl = 'https://openapi.daocloud.io/v1/apps/%s/actions/start' % appid

                sapp = requests.post(surl, headers=headers).json()

                return render_template('sp.html', resinfo='启动命令生效')

            else:
                return render_template('sp.html', resinfo='已启动')


#
# if __name__ == '__main__':
#     app.run(debug=True)
