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

    sql0 = '''
    select device_type from t_platform_device group by device_type;
    '''
    cursor.execute(sql0)
    deviceTypeList = cursor.fetchall()
    print('������е��豸����===���ݲ�ͬ�����ͳ�������===')

    num = 0

    for deviceType in deviceTypeList:
        sql00 = '''
        select max(id), count(1) num from t_platform_device where device_type = %s group by device_sn having num > 1;  
        '''
        cursor.execute(sql00, deviceType[0])
        openPlatformSettleList = cursor.fetchall()
        print('���==', deviceType[0], '==���������е����ݼ��ϴ�С==', len(openPlatformSettleList))

        sql01 = '''
        SELECT max(device_sn) FROM t_platform_device where device_type = %s;   
        '''
        cursor.execute(sql01, deviceType[0])
        maxDeviceSn = cursor.fetchall()
        print('��ȡ==', deviceType[0], '==�����������豸��==', maxDeviceSn[0][0])
        maxFragDeviceSn = int(maxDeviceSn[0][0])

        # ����ÿһ����������, ��ȡ����ʱ��
        for openPlatformSettle in openPlatformSettleList:
            # �豸�ŵ��� 1
            maxFragDeviceSn = maxFragDeviceSn + 1

            # update t_platform_device set device_sn = %s where id = %s ;
            sql02 = '''
                          insert into t_device_manydevice(new_sn ,id) values (%s, %s);
                    '''
            print('id����', openPlatformSettle[0])
            print('id����', int(openPlatformSettle[0]))
            cursor.execute(sql02, [str(maxFragDeviceSn), int(openPlatformSettle[0])])
            print(deviceType[0], '������,�˻���sn===', openPlatformSettle[0])
            num = num + 1

            # �ύ����
            conn.commit()

    print('�޸����ݳɹ�==', num)
    # �ύ����
    conn.commit()
    # �رչ�����
    cursor.close()

    # �ر����ݿ�����
    conn.close()
