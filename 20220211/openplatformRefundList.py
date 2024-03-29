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
    print('查出所有的设备类型===根据不同的类型持续递增===')

    num = 0

    # 再计算退货(settle_count < 0)
    for deviceType in deviceTypeList:
        sql00 = '''
        SELECT settle_date ,customer_id ,settle_count ,device_type ,specific_version FROM openplatform_settle_list where device_type = %s and settle_count < 0 order by settle_date;   
        '''
        cursor.execute(sql00, deviceType[0])
        openPlatformSettleList = cursor.fetchall()
        print('查出==', deviceType[0], '==类型下所有的数据集合大小==', len(openPlatformSettleList))

        # 遍历每一条结算数量, 获取结算时间
        for openPlatformSettle in openPlatformSettleList:
            sql01 = '''
                select device_sn from t_platform_device_yll where device_type = %s and create_time < %s and version = %s and status = 1 order by create_time desc ;
                '''
            print('查询退货设备的参数===', deviceType[0], openPlatformSettle[0], openPlatformSettle[4])
            cursor.execute(sql01, [deviceType[0], openPlatformSettle[0], openPlatformSettle[4]])
            deviceSnList = cursor.fetchall()
            print('查出所有可以退货的数据==', len(deviceSnList), '应该退货的数量', abs(openPlatformSettle[2]))

            # 遍历结算数量
            for index in range(abs(openPlatformSettle[2])):
                sql02 = '''
                          update t_platform_device_yll set status = 0 where device_sn = %s ;
                    '''
                cursor.execute(sql02, deviceSnList[index][0])
                print(deviceType[0], '类型下,退货的sn===', deviceSnList[index][0])
                num = num + 1

                # 提交事务
                conn.commit()

    print('修改数据成功==', num)
    # 提交事务
    conn.commit()
    # 关闭光标对象
    cursor.close()

    # 关闭数据库连接
    conn.close()
