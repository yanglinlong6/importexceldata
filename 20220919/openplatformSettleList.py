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
    print('������ʱ������¼���ݿ�')

    sql0 = '''
    select device_type from t_settle_order_202201to08 group by device_type;
    '''
    cursor.execute(sql0)
    deviceTypeList = cursor.fetchall()
    print('������е��豸����===���ݲ�ͬ�����ͳ�������===')

    num = 0

    # �ȼ������(settle_count >= 0)
    for deviceType in deviceTypeList:
        sql00 = '''
        SELECT settle_date ,customer_id ,settle_count ,device_type ,specific_version  FROM t_settle_order_202201to08 where device_type = %s and settle_count >= 0;   
        '''
        cursor.execute(sql00, deviceType[0])
        openPlatformSettleList = cursor.fetchall()
        print('���==', deviceType[0], '==���������е����ݼ���')

        sql01 = '''
                SELECT MAX(`device_sn`) FROM `t_platform_device` WHERE `create_time`>='2021-01-01 00:00:00' and `device_type` = %s;
                '''
        oldTigerCursor.execute(sql01, deviceType[0])
        maxDeviceSn = oldTigerCursor.fetchall()
        print('��ȡ==�����豸��==', maxDeviceSn[0][0])
        maxFragDeviceSn = int(maxDeviceSn[0][0])

        # ����ÿһ����������,��ȡ����ʱ��
        for openPlatformSettle in openPlatformSettleList:
            # ������������
            for index in range(openPlatformSettle[2]):
                # �豸�ŵ��� 1
                maxFragDeviceSn = maxFragDeviceSn + 1
                print('�������豸��==', maxFragDeviceSn)
                sql02 = '''
                      INSERT INTO t_platform_device_yll_0919
                      (device_sn, device_type, version, customer_id, user_id, activat_time, status, create_time, update_time, create_by, update_by, remark)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                '''
                cursor.execute(sql02, [str(maxFragDeviceSn), openPlatformSettle[3], openPlatformSettle[4],
                                       openPlatformSettle[1], None, None, 1, openPlatformSettle[0], None, 0, 0, None])
                num = num + 1

                # �ύ����
                conn.commit()

    print('�������ݳɹ�==', num)
    # �ύ����
    conn.commit()
    # �رչ�����
    cursor.close()

    # �ر����ݿ�����
    conn.close()
