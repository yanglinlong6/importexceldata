from datetime import datetime, timedelta

import pymysql

if __name__ == '__main__':
    neshieldConn = pymysql.connect(host='192.168.5.24',
                                   port=3306,
                                   user='user_yangll',
                                   password='vGxw9jWg',
                                   database='neshield',
                                   charset='utf8')
    neshieldCursor = neshieldConn.cursor()

    oldTigerConn = pymysql.connect(host='192.168.5.22',
                                   port=3307,
                                   user='user_yangll',
                                   password='vGxw9jWg',
                                   database='gps',
                                   charset='utf8')
    oldTigerCursor = oldTigerConn.cursor()

    sql01 = "select sn ,count(1) as num from t_alarm_track_stujudge where del_flag = 2  group by sn;"
    neshieldCursor.execute(sql01)
    neShieldStujudgeList = neshieldCursor.fetchall()
    print('neShieldStujudgeList===', neShieldStujudgeList)
    print(neShieldStujudgeList.__len__())
    snList = []
    for neShieldStujudge in neShieldStujudgeList:
        print(neShieldStujudge)
        sql02 = "select count(1) as num from t_track_stujudge_alarm where delflag = 2 and sn = %s;"
        oldTigerCursor.execute(sql02, [neShieldStujudge[0]])
        oldTigerStujudge = oldTigerCursor.fetchall()
        if (oldTigerStujudge[0][0] != neShieldStujudge[1]):
            print(oldTigerStujudge)
            snList.append(neShieldStujudge[0])

    print('snList===', snList)
    # 提交事务
    neshieldConn.commit()
    oldTigerConn.commit()
    # 关闭光标对象
    neshieldCursor.close()
    oldTigerCursor.close()

    # 关闭数据库连接
    neshieldConn.close()
    oldTigerConn.close()
