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
    print('查出所有的设备类型===根据不同的类型持续递增===')

    num = 0

    for deviceType in deviceTypeList:
        sql00 = '''
        select max(id), count(1) num from t_platform_device where device_type = %s group by device_sn having num > 1;  
        '''
        cursor.execute(sql00, deviceType[0])
        openPlatformSettleList = cursor.fetchall()
        print('查出==', deviceType[0], '==类型下所有的数据集合大小==', len(openPlatformSettleList))

        sql01 = '''
        SELECT max(device_sn) FROM t_platform_device where device_type = %s;   
        '''
        cursor.execute(sql01, deviceType[0])
        maxDeviceSn = cursor.fetchall()
        print('获取==', deviceType[0], '==类型下最大的设备号==', maxDeviceSn[0][0])
        maxFragDeviceSn = int(maxDeviceSn[0][0])

        # 遍历每一条结算数量, 获取结算时间
        for openPlatformSettle in openPlatformSettleList:
            # 设备号递增 1
            maxFragDeviceSn = maxFragDeviceSn + 1

            # update t_platform_device set device_sn = %s where id = %s ;
            sql02 = '''
                          insert into t_device_manydevice(new_sn ,id) values (%s, %s);
                    '''
            print('id参数', openPlatformSettle[0])
            print('id参数', int(openPlatformSettle[0]))
            cursor.execute(sql02, [str(maxFragDeviceSn), int(openPlatformSettle[0])])
            print(deviceType[0], '类型下,退货的sn===', openPlatformSettle[0])
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
