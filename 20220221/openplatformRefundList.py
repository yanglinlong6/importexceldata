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

    sql0 = '''
    select device_type from openplatform_settle_list group by device_type;
    '''
    cursor.execute(sql0)
    deviceTypeList = cursor.fetchall()
    print('������е��豸����===���ݲ�ͬ�����ͳ�������===')

    num = 0

    # �ټ����˻�(settle_count < 0)
    for deviceType in deviceTypeList:
        sql00 = '''
        SELECT settle_date ,customer_id ,settle_count ,device_type ,specific_version FROM openplatform_settle_list where device_type = %s and settle_count < 0 order by settle_date;   
        '''
        print("ִ�е�SQL==", sql00)
        cursor.execute(sql00, deviceType[0])
        openPlatformSettleList = cursor.fetchall()
        print('���==', deviceType[0], '==���������е����ݼ��ϴ�С==', len(openPlatformSettleList))

        # ����ÿһ����������, ��ȡ����ʱ��
        for openPlatformSettle in openPlatformSettleList:
            sql01 = '''
                select device_sn from t_platform_device_yll_0221 where device_type = %s and create_time < %s and version = %s and status = 1  and customer_id = %s order by create_time desc ;
                '''
            print("ִ�е�SQL==", sql01)
            print('��ѯ�˻��豸�Ĳ���===', deviceType[0], openPlatformSettle[0], openPlatformSettle[4], openPlatformSettle[1])
            cursor.execute(sql01, [deviceType[0], openPlatformSettle[0], openPlatformSettle[4], openPlatformSettle[1]])
            deviceSnList = cursor.fetchall()
            print('������п����˻�������==', len(deviceSnList), 'Ӧ���˻�������', abs(openPlatformSettle[2]))

            # ������������
            for index in range(abs(openPlatformSettle[2])):
                sql02 = '''
                          update t_platform_device_yll_0221 set status = 0 where device_sn = %s ;
                    '''
                print("ִ�е�SQL==", sql02)
                cursor.execute(sql02, deviceSnList[index][0])
                print(deviceType[0], '������,�˻���sn===', deviceSnList[index][0])
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
