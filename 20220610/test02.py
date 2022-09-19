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

    sql01 = "select sn ,count(1) as num from t_alarm_track_rec where del_flag = 0 and alarm_type in (1, 99) group by sn;"
    neshieldCursor.execute(sql01)
    neShieldTrackRecList = neshieldCursor.fetchall()
    print('neShieldTrackRecList===', neShieldTrackRecList)
    print(neShieldTrackRecList.__len__())
    snList = []
    for neShieldTrackRec in neShieldTrackRecList:
        print(neShieldTrackRec)
        sql02 = "select count(1) as num from d_track_alarm_rec where delflag = 0 and sn = %s and alarmType in (1, 99);"
        oldTigerCursor.execute(sql02, [neShieldTrackRec[0]])
        oldTigerTrackRec = oldTigerCursor.fetchall()
        if (oldTigerTrackRec[0][0] != neShieldTrackRec[1]):
            print(oldTigerTrackRec)
            snList.append(neShieldTrackRec[0])

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
