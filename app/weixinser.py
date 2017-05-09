# -*- coding:utf-8 -*-
import sys
import werobot
import getproblemPortal
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf-8')



robot = werobot.WeRoBot(token='ngerllTower')


@robot.handler
def echo(message):
    #db = MySQLdb.connect(host='220.249.117.234', user='root', passwd='!q2w3e4r', db='wxauto', port=13306,
    #                     charset='utf8')
    #cursor = db.cursor()

    #if message.content == 'sp':
    #    pass
    #else:
    try:
            #sql = "select * from userinfo where user_id = '%s' " % message.content
            #cursor.execute(sql)
            #resinfo = cursor.fetchone()

            #userid = resinfo[0]
            #passwd = resinfo[1]

        res = getproblemPortal.getprolist('huqiao', 'valencia429')
        return res

    except:
        return '错误,请重试!'



# robot.config['HOST'] = '127.0.0.1'
# robot.config['PORT'] = 5000
# robot.config['SESSION_STORAGE'] = False

# if __name__ == '__main__':
#     robot.run()



