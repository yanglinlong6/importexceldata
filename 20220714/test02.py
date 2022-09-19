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

    # oldTigerConn = pymysql.connect(host='192.168.5.22',
    #                                port=3307,
    #                                user='user_yangll',
    #                                password='vGxw9jWg',
    #                                database='gps',
    #                                charset='utf8')
    # oldTigerCursor = oldTigerConn.cursor()

    sql01 = '''
            select tv.vin   as vin,
                   count(1) as num
            from t_vehicle tv
                     left join t_vehicle_device tvd on tvd.vehicle_id = tv.id
            where tv.del_flag = 0
              and tvd.bind_status = 1
              and tvd.del_flag = 0
            group by tv.id;
            '''

    neshieldCursor.execute(sql01)
    allVinList = neshieldCursor.fetchall()
    print('allVinList===', allVinList)
    print(allVinList.__len__())

    sql02 = '''
            select tv.vin        as vin,
                   count(tvd.sn) as num
            from t_vehicle tv
                     left join t_vehicle_device tvd on tvd.vehicle_id = tv.id
                     left join t_device_location tdl on tdl.sn = tvd.sn
            where tv.del_flag = 0
              and tvd.bind_status = 1
              and tvd.del_flag = 0
              and ((timestampdiff(SECOND, tdl.last_gps_time, now()) > 259200 and timestampdiff(SECOND, tdl.last_bs_time, now()) > 259200)
              or (tdl.last_gps_time is null and tdl.last_bs_time is null)
              or (tdl.last_gps_time is null and timestampdiff(SECOND, tdl.last_bs_time, now()) > 259200)
              or (timestampdiff(SECOND, tdl.last_gps_time, now()) > 259200 and tdl.last_bs_time is null)
              )
            group by tv.id
            '''

    neshieldCursor.execute(sql02)
    officeVinList = neshieldCursor.fetchall()
    print('officeVinList===', officeVinList)
    print(officeVinList.__len__())

    vinList = []
    for allVin in allVinList:
        print(allVin)
        for officeVin in officeVinList:
            if (allVin[0] == officeVin[0]):
                if (allVin[1] == officeVin[1]):
                    print(officeVin)
                    vinList.append(officeVin[0])

    print('vinList===', vinList)
    # 提交事务
    neshieldConn.commit()
    # oldTigerConn.commit()
    # 关闭光标对象
    neshieldCursor.close()
    # oldTigerCursor.close()

    # 关闭数据库连接
    neshieldConn.close()
    # oldTigerConn.close()
