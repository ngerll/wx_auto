# -*- coding:utf-8 -*-
import json
import re
import sys

import requests
from bs4 import BeautifulSoup

import syslogin

reload(sys)
sys.setdefaultencoding('utf-8')


def getreq(url, datas, cookie):
    headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
               'Content-Type': 'application/x-www-form-urlencoded;charset="UTF-8"',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.8 Safari/537.36'}

    req = json.loads(requests.post(url, headers=headers, data=datas, cookies=cookie).content)

    return req


def getprolist(username, passwd):
    cookie = syslogin.getpmscookie(username, passwd)
    url = 'http://123.126.34.222:16666/uflow/listProcessOOP.do?method=getWaitingHandle'
    datas = {'pageNo': 1,
             'pageSize': 7,
             'sortname': 'WARN_ALARM',
             'sortorder': 'desc',
             'query': '',
             'queryKeyVal': '',
             'flowName': '全部'}
    req = getreq(url, datas, cookie)

    # exereqs = ''
    n = 0
    j = 0

    if len(req['rows']) > 0:
        for plist in req['rows']:
            PROCESS_ID = plist['PROCESS_ID']
            TASK_ID = plist['TASK_ID']

            exereq = getsystetype(PROCESS_ID, TASK_ID, cookie)

            # exereqs = exereqs + str(n) + ' -----' + exereq + '\n'
            if exereq == '"success"':
                n = n + 1
            else:
                j = j + 1

        exereqs = str(n) + '个问题工单已处理！' + str(j) + '个问题工单处理失败!'

        return exereqs

    else:
        return '暂无问题工单!'



def getsystetype(process_id, task_id, cookie):
    try:
        urlinsy = 'http://123.126.34.222:16666/uflow/process.do?method=prepareHandle&processId=%s&taskId=%s' % (
            process_id, task_id)  # 获取所属系统URL

        headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                   'Content-Type': 'application/x-www-form-urlencoded;charset="UTF-8"',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.8 Safari/537.36'}

        req = requests.get(urlinsy, headers=headers, cookies=cookie).content

        soup = BeautifulSoup(req, 'lxml').find_all('script')[2].string

        forminfo = str(re.findall('form = (.*?)var transitions', soup, re.S)[0]).strip()  # 表单抓取
        resinfolists = json.loads(forminfo[:-1])  # 表单抓取信息toJSON

        probaseinfo = resinfolists['sheetList'][0]  # 问题基本信息
        proviceaccpet = resinfolists['sheetList'][1]  # 受理信息
        attachment = resinfolists['sheetList'][4]  # 附件
        attachid = ''

        problemRequestDept = probaseinfo['rowList'][0]['fieldList'][1]['value']  # 问题提出部门
        problemRequest = probaseinfo['rowList'][0]['fieldList'][0]['displayValue']  # 问题提出人

        problemTitle = probaseinfo['rowList'][2]['fieldList'][1]['value']  # 问题标题
        problemId = probaseinfo['rowList'][2]['fieldList'][0]['value']  # 问题编号

        involveSystem = probaseinfo['rowList'][4]['fieldList'][0]['value']  # 涉及系统
        reqsubsy = probaseinfo['rowList'][4]['fieldList'][1]['value']  # 子系统

        attactinfos = attachment['rowList'][0]['fieldList'][0]  # 附件列表

        firstAcceptPeople = proviceaccpet['rowList'][0]['fieldList'][0]['value']  # 受理人
        firstAcceptDept = proviceaccpet['rowList'][0]['fieldList'][1]['value']  # 受理部门
        firstAcceptPhone = proviceaccpet['rowList'][1]['fieldList'][0]['value']  # 电话
        firstAcceptMail = proviceaccpet['rowList'][1]['fieldList'][1]['value']  # 邮箱
        firstEndTime = proviceaccpet['rowList'][2]['fieldList'][0]['value']  # 时间
        firstAcceptOpinion = ''

        if 'value' in attactinfos:

            attaclists = json.loads(attactinfos['value'])

            if len(attaclists) > 1:
                for i in attaclists:
                    attachid = str(attachid) + ',' + str(i['attachId'])

                attachid = attachid[1:]
                firstAcceptOpinion = '请协助处理，具体请详见附件，谢谢！'

            elif len(attaclists) == 1:
                for j in attaclists:
                    attachid = str(j['attachId'])

                firstAcceptOpinion = '请协助处理，具体请详见附件，谢谢！'

        else:
            attachid = ''
            firstAcceptOpinion = '请协助处理，谢谢！'

        urlbysubname = 'http://123.126.34.222:16666/uflow/questionSystem.do?method=queryBySubName'
        bysubdata = {'subName': reqsubsy,
                     'involveSystem': involveSystem,
                     'processId': process_id}

        reqbypeos = getreq(urlbysubname, bysubdata, cookie)[0]['id']  # 总部处理人

        # 提交post data
        formdatas = {
            'involveSystem': involveSystem,
            'subName': reqsubsy,
            'firstAcceptPeople': firstAcceptPeople,
            'firstAcceptDept': firstAcceptDept,
            'firstAcceptPhone': firstAcceptPhone,
            'firstAcceptMail': firstAcceptMail,
            'firstEndTime': firstEndTime,
            'questionType': '系统报错',
            'questionLevel': '紧急',
            'recurrence': '否',
            'effectDegree': '影响系统运行',
            'processMode': '升级总部',
            'firstAcceptOpinion': firstAcceptOpinion,
            'proviceCopyTo': '',
            'update': str(attachid),
            'questionRelation': '0',
            'precedence': '',
            'processMode2': '',
            'ResearchPerson2': reqbypeos
        }

        subprodatas = {'processId': process_id,
                       'taskId': task_id,
                       'formData': json.dumps(formdatas)}

        # return '问题：{0}，编号：{1}，提出单位：{2}，提出人：{3}。提交结果：{4}。'. \
        #      format(str(problemTitle), str(problemId), str(problemRequestDept), str(problemRequest),'success')

        urlsubmit = 'http://123.126.34.222:16666/uflow/process.do?method=handle'

        headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                   'Content-Type': 'application/x-www-form-urlencoded;charset="UTF-8"',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.8 Safari/537.36'}

        subres = requests.post(urlsubmit, subprodatas, headers=headers, cookies=cookie)

        # returninfo = '问题：{0}'. \
        #     format(str(problemTitle))
        #
        # return returninfo

        return subres.text
    except:
        return 500


if __name__ == '__main__':
    print getprolist('huqiao', 'valencia429')
