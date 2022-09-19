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

    sql01 = "select sn ,count(1) as num from t_alarm_second_data where del_flag = 0 and vd_id is not null and vd_id != 0 group by sn;"
    neshieldCursor.execute(sql01)
    neShieldSecondList = neshieldCursor.fetchall()
    print('neShieldSecondList===', neShieldSecondList)
    print(neShieldSecondList.__len__())
    snList = []
    for neShieldSecond in neShieldSecondList:
        print(neShieldSecond)
        sql02 = "select count(1) as num from d_alarm_second_data where del_flag = 1 and sn = %s ;"
        oldTigerCursor.execute(sql02, [neShieldSecond[0]])
        oldTigerSecond = oldTigerCursor.fetchall()
        if (oldTigerSecond[0][0] != neShieldSecond[1]):
            print(oldTigerSecond)
            snList.append(neShieldSecond[0])

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
