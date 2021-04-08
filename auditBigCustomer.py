from datetime import datetime, timedelta

import pymysql

if __name__ == '__main__':
    conn = pymysql.connect(host='192.168.1.39',
                           port=3306,
                           user='os_user',
                           password='os#123',
                           database='glsx_audit',
                           charset='utf8',
                           autocommit='True')
    cursor = conn.cursor()

    # sql01 = "SELECT DISTINCT LEFT(settle_date,7), customer_type FROM d_settle_doc_big_customer_copy ORDER BY LEFT(settle_date,7);"
    sql01 = "SELECT DISTINCT LEFT(settle_date,7), customer_type FROM d_settle_doc_big_new ORDER BY LEFT(settle_date,7);"
    cursor.execute(sql01)
    settleDataTypeList = cursor.fetchall()
    print('1111')
    print(settleDataTypeList.__len__())

    num = 0
    for settleDataType in settleDataTypeList:
        sql02 = "SELECT id FROM d_settle_doc_big_customer_copy WHERE LEFT(settle_date,7) = %s AND customer_type = %s;"
        cursor.execute(sql02, [settleDataType[0], settleDataType[1]])
        bigCustomerDataList = cursor.fetchall()
        print(settleDataType[0], settleDataType[1])
        print('2222')
        print(bigCustomerDataList.__len__())
        # print(bigCustomerData)

        sql03 = "SELECT period, settle_count, device_price, service_price, settle_date, LEFT(settle_date,7), service_period ,customer_type FROM d_settle_doc_big_new WHERE LEFT(settle_date,7) = %s AND customer_type = %s;"
        cursor.execute(sql03, [settleDataType[0], settleDataType[1]])
        bigNewDataList = cursor.fetchall()
        print('3333')
        print(bigNewDataList.__len__())
        # print(activateDetailData)
        indexNum = 0
        snNum = 0
        adjustNum = 0
        sql04 = "UPDATE `glsx_audit`.`d_settle_doc_big_customer_copy` SET `device_price` = %s, `service_price` = %s, `device_period` = %s, `service_period` = %s, `settle_count` = %s, `del_flag` = 3 WHERE `id` = %s;"
        sql07 = "SELECT sn,vin,doc_code,customer_type,customer_name from  d_device_activate_detail WHERE customer_type = %s AND LEFT(activeDate,7) >= '2017-12' AND LEFT(activeDate,7) <= %s AND sn not in (select distinct sn from d_settle_doc_big_customer_copy);"
        cursor.execute(sql07, [settleDataType[1], settleDataType[0]])
        activateDetailList = cursor.fetchall()
        print('7777')
        print(activateDetailList.__len__())
        sql08 = "SELECT sn,vin,doc_code,customer_type,customer_name from  d_device_activate_detail WHERE customer_name ='调剂用' AND LEFT(activeDate,7) >= '2017-12' AND LEFT(activeDate,7) <= %s AND sn not in (select distinct sn from d_settle_doc_big_customer_copy);"
        cursor.execute(sql08, [settleDataType[0]])
        adjustDetailList = cursor.fetchall()
        print('8888')
        print(adjustDetailList.__len__())
        sql05 = "INSERT INTO `glsx_audit`.`d_settle_doc_big_customer_copy`(`sn`, `standno`, `service_period`, `device_price`, `service_price`, `doc_code`, `settle_date`, `settle_month`, `customer_type`, `customer_name`, `settle_count`, `device_period`, `del_flag`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

        for bigNewData in bigNewDataList:
            if bigNewData[1] == 1:
                print("settle_count 设备数量===1")
                if len(bigCustomerDataList) > indexNum:
                    cursor.execute(sql04,
                                   [bigNewData[2], bigNewData[3], bigNewData[0], bigNewData[6], '1',
                                    bigCustomerDataList[indexNum][0]])
                    # 从大客户索引中获取数据的索引下标+1
                    indexNum = indexNum + 1
                else:
                    if len(activateDetailList) > snNum:
                        # 从d_device_activate_detail 表中获取激活时间小于settle_date 的设备号数据插入
                        cursor.execute(sql05,
                                       [activateDetailList[snNum][0], activateDetailList[snNum][1], bigNewData[6],
                                        bigNewData[2],
                                        bigNewData[3], activateDetailList[snNum][2], bigNewData[4],
                                        bigNewData[5].replace('-', ''), bigNewData[7],
                                        activateDetailList[snNum][4], '1', bigNewData[0],
                                        '3'])
                        # 从设备索引中获取数据的索引下标+1
                        snNum = snNum + 1
                    else:
                        # 从d_device_activate_detail 表中获取激活时间小于settle_date 的设备号数据插入
                        cursor.execute(sql05,
                                       [adjustDetailList[adjustNum][0], adjustDetailList[adjustNum][1], bigNewData[6],
                                        bigNewData[2],
                                        bigNewData[3], adjustDetailList[adjustNum][2], bigNewData[4],
                                        bigNewData[5].replace('-', ''), bigNewData[7],
                                        adjustDetailList[adjustNum][4], '1', bigNewData[0],
                                        '3'])
                        # 从设备索引中获取数据的索引下标+1
                        adjustNum = adjustNum + 1

                num = num + 1
                # 提交事务
                conn.commit()
            elif bigNewData[1] == 2:
                print("settle_count 设备数量===2")
                if len(bigCustomerDataList) > indexNum:
                    cursor.execute(sql04,
                                   [bigNewData[2], bigNewData[3], bigNewData[0], bigNewData[6], '1',
                                    bigCustomerDataList[indexNum][0]])
                    # 从大客户索引中获取数据的索引下标+1
                    indexNum = indexNum + 1
                else:
                    if len(activateDetailList) > snNum:
                        # 从d_device_activate_detail 表中获取激活时间小于settle_date 的设备号数据插入
                        cursor.execute(sql05,
                                       [activateDetailList[snNum][0], activateDetailList[snNum][1], bigNewData[6],
                                        bigNewData[2],
                                        bigNewData[3], activateDetailList[snNum][2], bigNewData[4],
                                        bigNewData[5].replace('-', ''), bigNewData[7],
                                        activateDetailList[snNum][4], '1', bigNewData[0],
                                        '3'])
                        # 从设备索引中获取数据的索引下标+1
                        snNum = snNum + 1
                    else:
                        # 从d_device_activate_detail 表中获取激活时间小于settle_date 的设备号数据插入
                        cursor.execute(sql05,
                                       [adjustDetailList[adjustNum][0], adjustDetailList[adjustNum][1], bigNewData[6],
                                        bigNewData[2],
                                        bigNewData[3], adjustDetailList[adjustNum][2], bigNewData[4],
                                        bigNewData[5].replace('-', ''), bigNewData[7],
                                        adjustDetailList[adjustNum][4], '1', bigNewData[0],
                                        '3'])
                        # 从设备索引中获取数据的索引下标+1
                        adjustNum = adjustNum + 1
                # 提交事务
                conn.commit()

                if len(bigCustomerDataList) > indexNum:
                    cursor.execute(sql04,
                                   [bigNewData[2], bigNewData[3], bigNewData[0], bigNewData[6], '1',
                                    bigCustomerDataList[indexNum][0]])
                    # 从大客户索引中获取数据的索引下标+1
                    indexNum = indexNum + 1
                else:
                    if len(activateDetailList) > snNum:
                        # 从d_device_activate_detail 表中获取激活时间小于settle_date 的设备号数据插入
                        cursor.execute(sql05,
                                       [activateDetailList[snNum][0], activateDetailList[snNum][1], bigNewData[6],
                                        bigNewData[2],
                                        bigNewData[3], activateDetailList[snNum][2], bigNewData[4],
                                        bigNewData[5].replace('-', ''), bigNewData[7],
                                        activateDetailList[snNum][4], '1', bigNewData[0],
                                        '3'])
                        # 从设备索引中获取数据的索引下标+1
                        snNum = snNum + 1
                    else:
                        # 从d_device_activate_detail 表中获取激活时间小于settle_date 的设备号数据插入
                        cursor.execute(sql05,
                                       [adjustDetailList[adjustNum][0], adjustDetailList[adjustNum][1], bigNewData[6],
                                        bigNewData[2],
                                        bigNewData[3], adjustDetailList[adjustNum][2], bigNewData[4],
                                        bigNewData[5].replace('-', ''), bigNewData[7],
                                        adjustDetailList[adjustNum][4], '1', bigNewData[0],
                                        '3'])
                        # 从设备索引中获取数据的索引下标+1
                        adjustNum = adjustNum + 1

                num = num + 2
                # 提交事务
                conn.commit()

            elif bigNewData[1] == 3:
                print("settle_count 设备数量===3")
                if len(bigCustomerDataList) > indexNum:
                    cursor.execute(sql04,
                                   [bigNewData[2], bigNewData[3], bigNewData[0], bigNewData[6], '1',
                                    bigCustomerDataList[indexNum][0]])
                    # 从大客户索引中获取数据的索引下标+1
                    indexNum = indexNum + 1
                else:
                    if len(activateDetailList) > snNum:
                        # 从d_device_activate_detail 表中获取激活时间小于settle_date 的设备号数据插入
                        cursor.execute(sql05,
                                       [activateDetailList[snNum][0], activateDetailList[snNum][1], bigNewData[6],
                                        bigNewData[2],
                                        bigNewData[3], activateDetailList[snNum][2], bigNewData[4],
                                        bigNewData[5].replace('-', ''), bigNewData[7],
                                        activateDetailList[snNum][4], '1', bigNewData[0],
                                        '3'])
                        # 从设备索引中获取数据的索引下标+1
                        snNum = snNum + 1
                    else:
                        # 从d_device_activate_detail 表中获取激活时间小于settle_date 的设备号数据插入
                        cursor.execute(sql05,
                                       [adjustDetailList[adjustNum][0], adjustDetailList[adjustNum][1], bigNewData[6],
                                        bigNewData[2],
                                        bigNewData[3], adjustDetailList[adjustNum][2], bigNewData[4],
                                        bigNewData[5].replace('-', ''), bigNewData[7],
                                        adjustDetailList[adjustNum][4], '1', bigNewData[0],
                                        '3'])
                        # 从设备索引中获取数据的索引下标+1
                        adjustNum = adjustNum + 1
                # 提交事务
                conn.commit()

                if len(bigCustomerDataList) > indexNum:
                    cursor.execute(sql04,
                                   [bigNewData[2], bigNewData[3], bigNewData[0], bigNewData[6], '1',
                                    bigCustomerDataList[indexNum][0]])
                    # 从大客户索引中获取数据的索引下标+1
                    indexNum = indexNum + 1
                else:
                    if len(activateDetailList) > snNum:
                        # 从d_device_activate_detail 表中获取激活时间小于settle_date 的设备号数据插入
                        cursor.execute(sql05,
                                       [activateDetailList[snNum][0], activateDetailList[snNum][1], bigNewData[6],
                                        bigNewData[2],
                                        bigNewData[3], activateDetailList[snNum][2], bigNewData[4],
                                        bigNewData[5].replace('-', ''), bigNewData[7],
                                        activateDetailList[snNum][4], '1', bigNewData[0],
                                        '3'])
                        # 从设备索引中获取数据的索引下标+1
                        snNum = snNum + 1
                    else:
                        # 从d_device_activate_detail 表中获取激活时间小于settle_date 的设备号数据插入
                        cursor.execute(sql05,
                                       [adjustDetailList[adjustNum][0], adjustDetailList[adjustNum][1], bigNewData[6],
                                        bigNewData[2],
                                        bigNewData[3], adjustDetailList[adjustNum][2], bigNewData[4],
                                        bigNewData[5].replace('-', ''), bigNewData[7],
                                        adjustDetailList[adjustNum][4], '1', bigNewData[0],
                                        '3'])
                        # 从设备索引中获取数据的索引下标+1
                        adjustNum = adjustNum + 1
                # 提交事务
                conn.commit()

                if len(bigCustomerDataList) > indexNum:
                    cursor.execute(sql04,
                                   [bigNewData[2], bigNewData[3], bigNewData[0], bigNewData[6], '1',
                                    bigCustomerDataList[indexNum][0]])
                    # 从大客户索引中获取数据的索引下标+1
                    indexNum = indexNum + 1
                else:
                    if len(activateDetailList) > snNum:
                        # 从d_device_activate_detail 表中获取激活时间小于settle_date 的设备号数据插入
                        cursor.execute(sql05,
                                       [activateDetailList[snNum][0], activateDetailList[snNum][1], bigNewData[6],
                                        bigNewData[2],
                                        bigNewData[3], activateDetailList[snNum][2], bigNewData[4],
                                        bigNewData[5].replace('-', ''), bigNewData[7],
                                        activateDetailList[snNum][4], '1', bigNewData[0],
                                        '3'])
                        # 从设备索引中获取数据的索引下标+1
                        snNum = snNum + 1
                    else:
                        # 从d_device_activate_detail 表中获取激活时间小于settle_date 的设备号数据插入
                        cursor.execute(sql05,
                                       [adjustDetailList[adjustNum][0], adjustDetailList[adjustNum][1], bigNewData[6],
                                        bigNewData[2],
                                        bigNewData[3], adjustDetailList[adjustNum][2], bigNewData[4],
                                        bigNewData[5].replace('-', ''), bigNewData[7],
                                        adjustDetailList[adjustNum][4], '1', bigNewData[0],
                                        '3'])
                        # 从设备索引中获取数据的索引下标+1
                        adjustNum = adjustNum + 1

                num = num + 3
                # 提交事务
                conn.commit()

    sql06 = "UPDATE `glsx_audit`.`d_settle_doc_big_customer_copy` SET `service_period` = 0 ,`device_price` = 0, `service_price` = 0, `device_period` = 0, `settle_count` = 0 ,`del_flag` = 4 WHERE del_flag <> 3;"
    cursor.execute(sql06)

    print(num)
    # 提交事务
    conn.commit()
    # 关闭光标对象
    cursor.close()

    # 关闭数据库连接
    conn.close()
