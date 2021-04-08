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
    sql00 = "DELETE FROM d_settle_doc_big_customer_copy1517; "
    cursor.execute(sql00)
    sql000 = "INSERT INTO `glsx_audit`.`d_settle_doc_big_customer_copy1517`(`id`, `sn`, `standno`, `service_period`, `device_price`, `service_price`, `doc_code`, `mater_code`, `mater_name`, `settle_date`, `settle_month`, `customer_type`, `customer_name`, `settle_count`, `device_period`, `del_flag`, `set_id`) VALUES (1, '12', NULL, 0, 0.000, 0.000, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, NULL, 1, NULL); "
    cursor.execute(sql000)
    print('清空所有数据')

    # sql01 = "SELECT DISTINCT LEFT(settle_date,7), customer_type FROM d_settle_doc_big_customer_copy ORDER BY LEFT(settle_date,7);"
    sql01 = "SELECT DISTINCT LEFT(settle_date,7), customer_type FROM d_settle_doc_1517  WHERE customer_type not in ('零星','零售','其他') ORDER BY LEFT(settle_date,7);"
    cursor.execute(sql01)
    settleDocTypeList = cursor.fetchall()
    print('1111')
    print(settleDocTypeList.__len__())

    num = 0
    for settleDocType in settleDocTypeList:
        sql02 = "SELECT sn,vin,doc_code FROM d_device_activate_1517 WHERE LEFT(activeDate,7) >= '2014-11' AND LEFT(activeDate,7) <= %s AND customer_type = %s AND sn not in (select distinct sn from d_settle_doc_big_customer_copy1517);"
        cursor.execute(sql02, [settleDocType[0], settleDocType[1]])
        deviceActivateList = cursor.fetchall()
        print(settleDocType[0], settleDocType[1])
        print('2222')
        print(deviceActivateList.__len__())
        # print(bigCustomerData)

        sql03 = "SELECT * FROM d_settle_doc_1517 WHERE LEFT(settle_date,7) = %s AND customer_type = %s;"
        cursor.execute(sql03, [settleDocType[0], settleDocType[1]])
        settleDocList = cursor.fetchall()
        print('3333')
        print(settleDocList.__len__())
        # print(activateDetailData)

        # sql06 = "SELECT sn,vin,doc_code FROM d_device_activate_1517 WHERE LEFT(activeDate,7) < %s AND customer_type = '零售' AND sn not in (select distinct sn from d_settle_doc_big_customer_copy1517);"
        sql06 = "SELECT sn,vin,doc_code FROM d_device_activate_1517 WHERE LEFT(activeDate,7) >= '2014-11' AND LEFT(activeDate,7) <= %s AND (customer_type = '其他' OR customer_type = '嘀加' OR customer_type = '先锋') AND sn not in (select distinct sn from d_settle_doc_big_customer_copy1517);"
        cursor.execute(sql06, [settleDocType[0]])
        retailActivateList = cursor.fetchall()
        print('6666')
        print(retailActivateList.__len__())
        # print(retailDocList)

        sql09 = "SELECT sn,vin,doc_code FROM d_device_activate_1517 WHERE LEFT(activeDate,7) >= '2014-10' AND LEFT(activeDate,7) <= %s AND (customer_type = '其他' OR customer_type = '嘀加' OR customer_type = '先锋') AND sn not in (select distinct sn from d_settle_doc_big_customer_copy1517);"
        cursor.execute(sql09, [settleDocType[0]])
        lingxingActivateList = cursor.fetchall()
        print('9999')
        print(retailActivateList.__len__())
        # print(retailDocList)

        indexNum = 0
        retailNum = 0
        lingxingNum = 0
        serviceNum12 = 0
        serviceNum24 = 0
        serviceNum36 = 0

        # 先分配硬件的价格
        sql04 = "INSERT INTO d_settle_doc_big_customer_copy1517 (`sn`, `standno`, `device_price`, `doc_code`, `settle_date`, `settle_month`, `customer_type`, `customer_name`, `settle_count`, `device_period`, `del_flag`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

        # 再分配服务的价格
        sql05 = "UPDATE d_settle_doc_big_customer_copy1517 SET `service_period` = %s, `service_price` = %s WHERE `sn` = %s AND del_flag = '3';"

        sql07 = "SELECT sn FROM d_settle_doc_big_customer_copy1517 WHERE customer_type = %s AND device_period = %s AND del_flag = '1';"

        sql08 = "SELECT sn FROM d_settle_doc_big_customer_copy1517 WHERE customer_type = %s AND (device_period = %s OR device_period = %s OR device_period = %s) AND del_flag = '1';"

        for settleDoc in settleDocList:
            print(settleDoc[4], settleDoc[5], settleDoc[6], settleDoc[10], settleDoc[11], settleDoc[12])
            # 先分配硬件的价格
            if settleDoc[1] != '零售' and settleDoc[1] != '零星':
                # 12期
                for settleNum in range(settleDoc[4]):
                    cursor.execute(sql04, [deviceActivateList[indexNum][0], deviceActivateList[indexNum][1],
                                           settleDoc[7], deviceActivateList[indexNum][2], settleDoc[3],
                                           str(settleDoc[3])[:7].replace('-', ''), settleDoc[1], settleDoc[2], '1',
                                           '12',
                                           '1'])
                    indexNum = indexNum + 1
                # 24期
                for settleNum in range(settleDoc[5]):
                    cursor.execute(sql04, [deviceActivateList[indexNum][0], deviceActivateList[indexNum][1],
                                           settleDoc[7], deviceActivateList[indexNum][2], settleDoc[3],
                                           str(settleDoc[3])[:7].replace('-', ''), settleDoc[1], settleDoc[2], '1',
                                           '24', '1'])
                    indexNum = indexNum + 1

                # 36期
                for settleNum in range(settleDoc[6]):
                    cursor.execute(sql04, [deviceActivateList[indexNum][0], deviceActivateList[indexNum][1],
                                           settleDoc[7], deviceActivateList[indexNum][2], settleDoc[3],
                                           str(settleDoc[3])[:7].replace('-', ''), settleDoc[1], settleDoc[2], '1',
                                           '36', '1'])
                    indexNum = indexNum + 1
            elif settleDoc[1] == '零星':
                # 先分配硬件的价格
                # 12期
                for settleNum in range(settleDoc[4]):
                    cursor.execute(sql04, [lingxingActivateList[lingxingNum][0], lingxingActivateList[lingxingNum][1],
                                           settleDoc[7], lingxingActivateList[lingxingNum][2], settleDoc[3],
                                           str(settleDoc[3])[:7].replace('-', ''), settleDoc[1], settleDoc[2], '1',
                                           '12', '1'])
                    lingxingNum = lingxingNum + 1
                # 24期
                for settleNum in range(settleDoc[5]):
                    cursor.execute(sql04, [lingxingActivateList[lingxingNum][0], lingxingActivateList[lingxingNum][1],
                                           settleDoc[7], lingxingActivateList[lingxingNum][2], settleDoc[3],
                                           str(settleDoc[3])[:7].replace('-', ''), settleDoc[1], settleDoc[2], '1',
                                           '24', '1'])
                    lingxingNum = lingxingNum + 1

                # 36期
                for settleNum in range(settleDoc[6]):
                    cursor.execute(sql04, [lingxingActivateList[lingxingNum][0], lingxingActivateList[lingxingNum][1],
                                           settleDoc[7], lingxingActivateList[lingxingNum][2], settleDoc[3],
                                           str(settleDoc[3])[:7].replace('-', ''), settleDoc[1], settleDoc[2], '1',
                                           '36', '1'])
                    lingxingNum = lingxingNum + 1
            else:
                # 先分配硬件的价格
                # 12期
                for settleNum in range(settleDoc[4]):
                    cursor.execute(sql04, [retailActivateList[retailNum][0], retailActivateList[retailNum][1],
                                           settleDoc[7], retailActivateList[retailNum][2], settleDoc[3],
                                           str(settleDoc[3])[:7].replace('-', ''), settleDoc[1], settleDoc[2], '1',
                                           '12', '1'])
                    retailNum = retailNum + 1
                # 24期
                for settleNum in range(settleDoc[5]):
                    cursor.execute(sql04, [retailActivateList[retailNum][0], retailActivateList[retailNum][1],
                                           settleDoc[7], retailActivateList[retailNum][2], settleDoc[3],
                                           str(settleDoc[3])[:7].replace('-', ''), settleDoc[1], settleDoc[2], '1',
                                           '24', '1'])
                    retailNum = retailNum + 1

                # 36期
                for settleNum in range(settleDoc[6]):
                    cursor.execute(sql04, [retailActivateList[retailNum][0], retailActivateList[retailNum][1],
                                           settleDoc[7], retailActivateList[retailNum][2], settleDoc[3],
                                           str(settleDoc[3])[:7].replace('-', ''), settleDoc[1], settleDoc[2], '1',
                                           '36', '1'])
                    retailNum = retailNum + 1

            # 提交事务
            conn.commit()

            # 再分配服务的价格
            # 36期
            cursor.execute(sql07, [settleDocType[1], '36'])
            snCopyList = cursor.fetchall()
            print('service 36期')
            print(snCopyList.__len__())
            for settleNum in range(settleDoc[12]):
                cursor.execute(sql05, ['36', settleDoc[15], snCopyList[serviceNum36][0]])
                serviceNum36 = serviceNum36 + 1

            # 24期
            cursor.execute(sql07, [settleDocType[1], '24'])
            snCopyList24 = cursor.fetchall()
            print('service 24期')
            print(snCopyList24.__len__())
            for settleNum in range(settleDoc[11]):
                cursor.execute(sql05, ['24', settleDoc[14], snCopyList24[serviceNum24][0]])
                serviceNum24 = serviceNum24 + 1

            # 提交事务
            conn.commit()

            # 12期
            cursor.execute(sql08, [settleDocType[1], '12', '24', '36'])
            snCopyList12 = cursor.fetchall()
            print('service 12期')
            print(snCopyList12.__len__())
            for settleNum in range(settleDoc[10]):
                cursor.execute(sql05, ['12', settleDoc[13], snCopyList12[serviceNum12][0]])
                serviceNum12 = serviceNum12 + 1

        # 提交事务
        conn.commit()

    # print(num)
    # 提交事务
    conn.commit()
    # 关闭光标对象
    cursor.close()

    # 关闭数据库连接
    conn.close()
