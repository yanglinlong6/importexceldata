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

    sql01 = "select sn, last_gps_time, last_bs_time from t_device_location order by last_gps_time desc limit 1000;"
    neshieldCursor.execute(sql01)
    neShieldLocationList = neshieldCursor.fetchall()
    print('neShieldLocationList===', neShieldLocationList)
    print(neShieldLocationList.__len__())
    snList = []
    for neShieldLocation in neShieldLocationList:
        print(neShieldLocation)
        sql02 = "select sn, lastRtTrack, lastGprsTime from d_device_login where sn = %s ;"
        oldTigerCursor.execute(sql02, [neShieldLocation[0]])
        oldTigerLogin = oldTigerCursor.fetchall()
        if (oldTigerLogin[0][1] != neShieldLocation[1]):
            print(oldTigerLogin)
            snList.append(neShieldLocation[0])
        elif (oldTigerLogin[0][2] != neShieldLocation[2]):
            print(oldTigerLogin)
            snList.append(neShieldLocation[0])

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
