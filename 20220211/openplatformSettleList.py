# coding=gbk
import pymysql

if __name__ == '__main__':
    conn = pymysql.connect(host='192.168.3.184',
                           port=3306,
                           user='os_user',
                           password='os#123',
                           database='cyb_os',
                           charset='utf8',
                           autocommit='True')
    cursor = conn.cursor()

    sql = '''
    TRUNCATE TABLE t_platform_device_yll_0211;
    '''
    cursor.execute(sql)
    print('������ʱ������¼���ݿ�')

    sql0 = '''
    select device_type from openplatform_settle_list where left(settle_date, 7) = '2021-12' group by device_type;
    '''
    cursor.execute(sql0)
    deviceTypeList = cursor.fetchall()
    print('������е��豸����===���ݲ�ͬ�����ͳ�������===')

    num = 0

    # �ȼ������(settle_count >= 0)
    for deviceType in deviceTypeList:
        sql00 = '''
        SELECT settle_date ,customer_id ,settle_count ,device_type ,specific_version  FROM openplatform_settle_list where left(settle_date, 7) = '2021-12' and device_type = %s and settle_count >= 0;   
        '''
        cursor.execute(sql00, deviceType[0])
        openPlatformSettleList = cursor.fetchall()
        print('���==', deviceType[0], '==���������е����ݼ���')

        sql01 = '''
        SELECT max(device_sn) FROM t_platform_device where device_type = %s;   
        '''
        cursor.execute(sql01, deviceType[0])
        maxDeviceSn = cursor.fetchall()
        print('��ȡ==', deviceType[0], '==�����������豸��==', maxDeviceSn[0][0])
        maxFragDeviceSn = int(maxDeviceSn[0][0])

        # ����ÿһ����������,��ȡ����ʱ��
        for openPlatformSettle in openPlatformSettleList:
            # ������������
            for index in range(openPlatformSettle[2]):
                # �豸�ŵ��� 1
                maxFragDeviceSn = maxFragDeviceSn + 1
                print('�������豸��==', maxFragDeviceSn)
                sql02 = '''
                      INSERT INTO t_platform_device_yll_0211
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
