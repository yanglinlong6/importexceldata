# coding=gbk
import pymysql

if __name__ == '__main__':
    conn = pymysql.connect(host='192.168.0.39',
                           port=3307,
                           user='root',
                           password='123456',
                           database='lj_shop',
                           charset='utf8',
                           autocommit='True')
    cursor = conn.cursor()

    oldTigerConn = pymysql.connect(host='192.168.5.25',
                                   port=3307,
                                   user='user_yangll',
                                   password='vGxw9jWg',
                                   database='glsx_open_platform',
                                   charset='utf8',
                                   autocommit='True')
    oldTigerCursor = oldTigerConn.cursor()

    sql = '''
    TRUNCATE TABLE t_platform_device_yll_0919;
    '''
    cursor.execute(sql)
    print('清理临时操作记录数据库')

    sql0 = '''
    select device_type from t_settle_order_202201to08 group by device_type;
    '''
    cursor.execute(sql0)
    deviceTypeList = cursor.fetchall()
    print('查出所有的设备类型===根据不同的类型持续递增===')

    num = 0

    # 先计算出货(settle_count >= 0)
    for deviceType in deviceTypeList:
        sql00 = '''
        SELECT settle_date ,customer_id ,settle_count ,device_type ,specific_version  FROM t_settle_order_202201to08 where device_type = %s and settle_count >= 0;   
        '''
        cursor.execute(sql00, deviceType[0])
        openPlatformSettleList = cursor.fetchall()
        print('查出==', deviceType[0], '==类型下所有的数据集合')

        sql01 = '''
                SELECT MAX(`device_sn`) FROM `t_platform_device` WHERE `create_time`>='2021-01-01 00:00:00' and `device_type` = %s;
                '''
        oldTigerCursor.execute(sql01, deviceType[0])
        maxDeviceSn = oldTigerCursor.fetchall()
        print('获取==最大的设备号==', maxDeviceSn[0][0])
        maxFragDeviceSn = int(maxDeviceSn[0][0])

        # 遍历每一条结算数量,获取结算时间
        for openPlatformSettle in openPlatformSettleList:
            # 遍历结算数量
            for index in range(openPlatformSettle[2]):
                # 设备号递增 1
                maxFragDeviceSn = maxFragDeviceSn + 1
                print('递增的设备号==', maxFragDeviceSn)
                sql02 = '''
                      INSERT INTO t_platform_device_yll_0919
                      (device_sn, device_type, version, customer_id, user_id, activat_time, status, create_time, update_time, create_by, update_by, remark)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                '''
                cursor.execute(sql02, [str(maxFragDeviceSn), openPlatformSettle[3], openPlatformSettle[4],
                                       openPlatformSettle[1], None, None, 1, openPlatformSettle[0], None, 0, 0, None])
                num = num + 1

                # 提交事务
                conn.commit()

    print('插入数据成功==', num)
    # 提交事务
    conn.commit()
    # 关闭光标对象
    cursor.close()

    # 关闭数据库连接
    conn.close()
