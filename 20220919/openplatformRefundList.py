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
    select device_type from t_settle_order_202201to08 group by device_type;
    '''
    cursor.execute(sql0)
    deviceTypeList = cursor.fetchall()
    print('查出所有的设备类型===根据不同的类型持续递增===')

    num = 0

    # 再计算退货(settle_count < 0)
    for deviceType in deviceTypeList:
        sql00 = '''
        SELECT settle_date ,customer_id ,settle_count ,device_type ,specific_version FROM t_settle_order_202201to08 where device_type = %s and settle_count < 0 order by settle_date;   
        '''
        print("执行的SQL==", sql00)
        cursor.execute(sql00, deviceType[0])
        openPlatformSettleList = cursor.fetchall()
        print('查出==', deviceType[0], '==类型下所有的数据集合大小==', len(openPlatformSettleList))

        # 遍历每一条结算数量, 获取结算时间
        for openPlatformSettle in openPlatformSettleList:
            sql01 = '''
                select device_sn from t_platform_device_yll_0919 where device_type = %s and create_time < %s and version = %s and status = 1  and customer_id = %s order by create_time desc ;
                '''
            print("执行的SQL==", sql01)
            print('查询退货设备的参数===', deviceType[0], openPlatformSettle[0], openPlatformSettle[4], openPlatformSettle[1])
            cursor.execute(sql01, [deviceType[0], openPlatformSettle[0], openPlatformSettle[4], openPlatformSettle[1]])
            deviceSnList = cursor.fetchall()
            print('查出所有可以退货的数据==', len(deviceSnList), '应该退货的数量', abs(openPlatformSettle[2]))

            # 遍历结算数量
            for index in range(abs(openPlatformSettle[2])):
                sql02 = '''
                          update t_platform_device_yll_0919 set status = 0 where device_sn = %s ;
                    '''
                print("执行的SQL==", sql02)
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
