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
    # print('清空所有数据')

    # sql01 = "SELECT DISTINCT LEFT(settle_date,7), customer_type FROM d_settle_doc_1517 WHERE LEFT(settle_date,4) = '2017' ORDER BY LEFT(settle_date,7);"
    sql01 = "SELECT DISTINCT LEFT(settle_date,7), customer_type FROM d_settle_doc_1517 ORDER BY LEFT(settle_date,7);"
    # sql01 = "SELECT DISTINCT LEFT(settle_date,7), customer_type FROM d_settle_doc_1517  WHERE customer_type not in ('零星','零售','其他') ORDER BY LEFT(settle_date,7);"
    cursor.execute(sql01)
    settleDocTypeList = cursor.fetchall()
    # print('1111')
    # print(settleDocTypeList.__len__())

    num = 0
    for settleDocType in settleDocTypeList:
        sql02 = "SELECT sn,vin,doc_code FROM d_device_activate_1517 WHERE LEFT(activeDate,7) >= '2014-12' AND LEFT(activeDate,7) <= %s AND customer_type = %s AND sn not in (select distinct sn from d_settle_doc_big_customer_copy1517) order by activeDate desc;"
        cursor.execute(sql02, [settleDocType[0], settleDocType[1]])
        deviceActivateList = cursor.fetchall()
        print(settleDocType[0], settleDocType[1])
        # print('2222')
        # print(deviceActivateList.__len__())
        # print(bigCustomerData)

        sql03 = "SELECT * FROM d_settle_doc_1517 WHERE LEFT(settle_date,7) = %s AND customer_type = %s;"
        cursor.execute(sql03, [settleDocType[0], settleDocType[1]])
        settleDocList = cursor.fetchall()
        # print('3333')
        # print(settleDocList.__len__())
        # print(activateDetailData)

        # sql06 = "SELECT sn,vin,doc_code FROM d_device_activate_1517 WHERE LEFT(activeDate,7) < %s AND customer_type = '零售' AND sn not in (select distinct sn from d_settle_doc_big_customer_copy1517);"
        sql06 = "SELECT sn,vin,doc_code FROM d_device_activate_1517 WHERE LEFT(activeDate,7) >= %s AND LEFT(activeDate,7) <= '2017-12' AND customer_type = '其他' AND sn not in (select distinct sn from d_settle_doc_big_customer_copy1517);"
        cursor.execute(sql06, [settleDocType[0]])
        retailActivateList = cursor.fetchall()
        # print('6666')
        # print(retailActivateList.__len__())
        # print(retailDocList)

        # sql09 = "SELECT sn,vin,doc_code FROM d_device_activate_1517 WHERE LEFT(activeDate,7) >= %s AND LEFT(activeDate,7) <= '2017-11' AND customer_type = '其他'  AND sn not in (select distinct sn from d_settle_doc_big_customer_copy1517);"
        # cursor.execute(sql09, [settleDocType[0]])
        # lingxingActivateList = cursor.fetchall()
        # print('9999')
        # print(lingxingActivateList.__len__())
        # print(retailDocList)

        indexNum = 0
        retailNum = 0
        lingxingNum = 0
        serviceNum12 = 0
        serviceNum24 = 0
        serviceNum36 = 0
        serviceNum36to24 = 0
        serviceNum36to24to12 = 0
        serviceNum24to12 = 0

        # 先分配硬件的价格
        sql04 = "INSERT INTO d_settle_doc_big_customer_copy1517 (`sn`, `standno`, `device_price`, `doc_code`, `settle_date`, `settle_month`, `customer_type`, `customer_name`, `settle_count`, `device_period`, `del_flag`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

        # 再分配服务的价格
        sql05 = "UPDATE d_settle_doc_big_customer_copy1517 SET `service_period` = %s, `service_price` = %s , `del_flag` = '3' WHERE `sn` = %s ;"

        sql07 = "SELECT sn FROM d_settle_doc_big_customer_copy1517 WHERE customer_type = %s AND device_period = %s AND LEFT(settle_date,7) = %s AND del_flag = '1';"

        sql08 = "SELECT sn FROM d_settle_doc_big_customer_copy1517 WHERE customer_type = %s AND (device_period = %s OR device_period = %s) AND LEFT(settle_date,7) = %s AND del_flag = '1';"

        sql09 = "SELECT sn FROM d_settle_doc_big_customer_copy1517 WHERE customer_type = %s AND (device_period = %s OR device_period = %s OR device_period = %s) AND LEFT(settle_date,7) = %s AND del_flag = '1';"

        for settleDoc in settleDocList:
            print(settleDoc[4], settleDoc[5], settleDoc[6], settleDoc[10], settleDoc[11], settleDoc[12])
            # 先分配硬件的价格
            if settleDoc[1] != '零售' and settleDoc[1] != '零星' and settleDoc[1] != '其他':
                # 12期
                for settleNum in range(settleDoc[4]):
                    if len(deviceActivateList) > indexNum:
                        cursor.execute(sql04, [deviceActivateList[indexNum][0], deviceActivateList[indexNum][1],
                                               settleDoc[7], deviceActivateList[indexNum][2], settleDoc[3],
                                               str(settleDoc[3])[:7].replace('-', ''), settleDoc[1], settleDoc[2], '1',
                                               '12',
                                               '1'])
                        indexNum = indexNum + 1
                    else:
                        print(settleDocType[0], settleDocType[1], '缺少的数', '12', settleDoc[4] - settleNum)
                        break
                # 24期
                for settleNum in range(settleDoc[5]):
                    if len(deviceActivateList) > indexNum:
                        cursor.execute(sql04, [deviceActivateList[indexNum][0], deviceActivateList[indexNum][1],
                                               settleDoc[8], deviceActivateList[indexNum][2], settleDoc[3],
                                               str(settleDoc[3])[:7].replace('-', ''), settleDoc[1], settleDoc[2], '1',
                                               '24', '1'])
                        indexNum = indexNum + 1
                    else:
                        print(settleDocType[0], settleDocType[1], '缺少的数', '24', settleDoc[5] - indexNum)
                        break
                # 36期
                for settleNum in range(settleDoc[6]):
                    if len(deviceActivateList) > indexNum:
                        cursor.execute(sql04, [deviceActivateList[indexNum][0], deviceActivateList[indexNum][1],
                                               settleDoc[9], deviceActivateList[indexNum][2], settleDoc[3],
                                               str(settleDoc[3])[:7].replace('-', ''), settleDoc[1], settleDoc[2], '1',
                                               '36', '1'])
                        indexNum = indexNum + 1
                    else:
                        print(settleDocType[0], settleDocType[1], '缺少的数', '36', settleDoc[6] - indexNum)
                        break
            else:
                # 先分配硬件的价格
                # 12期
                for settleNum in range(settleDoc[4]):
                    if len(retailActivateList) > retailNum:
                        cursor.execute(sql04, [retailActivateList[retailNum][0], retailActivateList[retailNum][1],
                                               settleDoc[7], retailActivateList[retailNum][2], settleDoc[3],
                                               str(settleDoc[3])[:7].replace('-', ''), settleDoc[1], settleDoc[2], '1',
                                               '12', '1'])
                        retailNum = retailNum + 1
                    else:
                        print(settleDocType[0], settleDocType[1], '缺少的数', '12', settleDoc[4] - settleNum)
                        break
                # 24期
                for settleNum in range(settleDoc[5]):
                    if len(retailActivateList) > retailNum:
                        cursor.execute(sql04, [retailActivateList[retailNum][0], retailActivateList[retailNum][1],
                                               settleDoc[8], retailActivateList[retailNum][2], settleDoc[3],
                                               str(settleDoc[3])[:7].replace('-', ''), settleDoc[1], settleDoc[2], '1',
                                               '24', '1'])
                        retailNum = retailNum + 1
                    else:
                        print(settleDocType[0], settleDocType[1], '缺少的数', '24', settleDoc[5] - settleNum)
                        break

                # 36期
                for settleNum in range(settleDoc[6]):
                    if len(retailActivateList) > retailNum:
                        cursor.execute(sql04, [retailActivateList[retailNum][0], retailActivateList[retailNum][1],
                                               settleDoc[9], retailActivateList[retailNum][2], settleDoc[3],
                                               str(settleDoc[3])[:7].replace('-', ''), settleDoc[1], settleDoc[2], '1',
                                               '36', '1'])
                        retailNum = retailNum + 1
                    else:
                        print(settleDocType[0], settleDocType[1], '缺少的数', '36', settleDoc[6] - settleNum)
                        break

            # 提交事务
            conn.commit()

            # 再分配服务的价格
            sql0000 = "DELETE FROM d_settle_doc_big_customer_copy1517 where id = 1; "
            cursor.execute(sql0000)

            # 36期
            cursor.execute(sql07, [settleDocType[1], '36', settleDocType[0]])
            snCopyList = cursor.fetchall()
            print('service 36期')
            print(snCopyList.__len__())
            cursor.execute(sql07, [settleDocType[1], '24', settleDocType[0]])
            snCopyList36to24 = cursor.fetchall()
            cursor.execute(sql07, [settleDocType[1], '12', settleDocType[0]])
            snCopyList36to24to12 = cursor.fetchall()
            for settleNum in range(settleDoc[12]):
                if len(snCopyList) > serviceNum36:
                    cursor.execute(sql05, ['36', settleDoc[15], snCopyList[serviceNum36][0]])
                    serviceNum36 = serviceNum36 + 1
                else:
                    print('service 36期 找不够就去24里面找')
                    print(snCopyList36to24.__len__())
                    if len(snCopyList36to24) > serviceNum36to24:
                        cursor.execute(sql05, ['36', settleDoc[15], snCopyList36to24[serviceNum36to24][0]])
                        serviceNum36to24 = serviceNum36to24 + 1
                    else:
                        print('service 36期 找不够就去24期里面找 24期里面找不到就到12期里面找')
                        print(snCopyList36to24to12.__len__())
                        if len(snCopyList36to24to12) > serviceNum36to24to12:
                            cursor.execute(sql05, ['36', settleDoc[15], snCopyList36to24to12[serviceNum36to24to12][0]])
                            serviceNum36to24to12 = serviceNum36to24to12 + 1
                        else:
                            print(settleDocType[0], settleDocType[1], '缺少的数', '36', settleDoc[12] - settleNum)
                            break

            # 提交事务
            conn.commit()

            # 24期
            cursor.execute(sql08, [settleDocType[1], '24', '36', settleDocType[0]])
            snCopyList24 = cursor.fetchall()
            print('service 24期')
            print(snCopyList24.__len__())
            cursor.execute(sql07, [settleDocType[1], '12', settleDocType[0]])
            snCopyList24to12 = cursor.fetchall()
            for settleNum in range(settleDoc[11]):
                if len(snCopyList24) > serviceNum24:
                    cursor.execute(sql05, ['24', settleDoc[14], snCopyList24[serviceNum24][0]])
                    serviceNum24 = serviceNum24 + 1
                else:
                    print('service 24期  24期里面找不到就到12期里面找')
                    print(snCopyList24to12.__len__())
                    if len(snCopyList24to12) > serviceNum24to12:
                        cursor.execute(sql05, ['36', settleDoc[15], snCopyList24to12[serviceNum24to12][0]])
                        serviceNum24to12 = serviceNum24to12 + 1
                    else:
                        print(settleDocType[0], settleDocType[1], '缺少的数', '24', settleDoc[11] - settleNum)
                        break

            # 提交事务
            conn.commit()

            # 12期
            cursor.execute(sql09, [settleDocType[1], '12', '24', '36', settleDocType[0]])
            snCopyList12 = cursor.fetchall()
            print('service 12期')
            print(snCopyList12.__len__())
            for settleNum in range(settleDoc[10]):
                if len(snCopyList12) > serviceNum12:
                    cursor.execute(sql05, ['12', settleDoc[13], snCopyList12[serviceNum12][0]])
                    serviceNum12 = serviceNum12 + 1
                else:
                    print(settleDocType[0], settleDocType[1], '缺少的数', '12', settleDoc[10] - settleNum)
                    break

            # 提交事务
            conn.commit()

        # 提交事务
        conn.commit()

    # print(num)
    # 提交事务
    conn.commit()
    # 关闭光标对象
    cursor.close()

    # 关闭数据库连接
    conn.close()
