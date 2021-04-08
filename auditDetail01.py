from datetime import datetime, timedelta

import pymysql

if __name__ == '__main__':
    conn = pymysql.connect(host='192.168.1.39',
                           port=3306,
                           user='os_user',
                           password='os#123',
                           database='glsx_audit',
                           charset='utf8')
    cursor = conn.cursor()
    # sql01 = "select * from d_settle_doc_big_customer_copy;"
    # cursor.execute(sql01)
    # bigCustomerData = cursor.fetchall()
    # print('1111')
    # print(bigCustomerData.__len__())
    # print(bigCustomerData)
    #
    strField = {}
    # num = 0
    num01 = 0
    # # sql03 = "INSERT INTO `glsx_audit`.`d_eshield_device_details`(`sn`, `device_type`, `active_time`, `device_period`, `settle_merchant`, `settle_order`, `settle_time`, `device_price`, `type`, `classid`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    # sql03 = "INSERT INTO `glsx_audit`.`d_eshield_device_details_yangll`(`sn`, `device_type`, `device_period`, `settle_merchant`, `settle_order`, `settle_time`, `device_price`, `type`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
    #
    # # sql04 = "INSERT INTO `glsx_audit`.`d_eshield_service_details`(`sn`, `starttime`, `endtime`, `period`, `price`, `customer`, `type`) VALUES (%s, %s, %s, %s, %s, %s, %s);"
    # sql04 = "INSERT INTO `glsx_audit`.`d_eshield_service_details_yangll`(`sn`, `period`, `price`, `customer`, `type`) VALUES (%s, %s, %s, %s, %s);"
    #
    # for customerData in bigCustomerData:
    #     if customerData is None:
    #         pass
    #     elif int(customerData[4]) > 0:
    #         print(num)
    #         strField[1] = str(customerData[1])
    #         strField[2] = '8'
    #         # strField[3] = str(detailData[7])
    #         strField[4] = str(customerData[14])
    #         strField[5] = str(customerData[12])
    #         strField[6] = str(customerData[6])
    #         strField[7] = str(customerData[9])
    #         strField[8] = str(customerData[4])
    #         strField[9] = '1'
    #         # strField[10] = str(detailData[3])
    #         print(sql03)
    #         cursor.execute(sql03,
    #                        [strField[1], strField[2], strField[4], strField[5], strField[6],
    #                         strField[7],
    #                         strField[8], strField[9]])
    #         if int(customerData[5]) > 0:
    #             strField[11] = str(customerData[1])
    #             # strField[12] = str(detailData[7])
    #             # startTime = datetime.strptime(str(detailData[7]), "%Y-%m-%d %H:%M:%S")
    #             # endTime = startTime + timedelta(days=30 * customerData[3])
    #             # strField[13] = str(endTime)
    #             strField[14] = str(customerData[3])
    #             strField[15] = str(customerData[5])
    #             strField[16] = str(customerData[12])
    #             strField[17] = '1'
    #
    #             print(sql04)
    #             cursor.execute(sql04,
    #                            [strField[11], strField[14], strField[15], strField[16],
    #                             strField[17]])
    #         num = num + 1

    sql02 = "select * from d_device_activate_detail;"
    cursor.execute(sql02)
    activateDetailData = cursor.fetchall()
    print('2222')
    print(activateDetailData.__len__())
    # print(activateDetailData)

    sql05 = "UPDATE `glsx_audit`.`d_eshield_device_details_yangll` SET `active_time` = %s, `classid` = %s WHERE `sn` = %s;"
    # sql06 = "UPDATE `glsx_audit`.`d_eshield_service_details_yangll` SET `starttime` = %s, `endtime` = %s WHERE `sn` = %s;"
    sql06 = "UPDATE `glsx_audit`.`d_eshield_service_details_yangll` SET `starttime` = %s WHERE `sn` = %s;"
    for detailData in activateDetailData:
        print(num01)
        strField[18] = str(detailData[7])
        strField[19] = str(detailData[3])
        strField[20] = detailData[1]
        print(sql05)
        cursor.execute(sql05, [strField[18], strField[19], strField[20]])

        strField[21] = str(detailData[7])
        # strField[22] = '1'
        strField[23] = detailData[1]
        print(sql06)
        cursor.execute(sql06, [strField[21], strField[23]])
        num01 = num01 + 1
    # sqltest = "INSERT INTO `d_eshield_service_details`(`sn`, `starttime`, `endtime`, `period`, `price`, `customer`, `type`) VALUES ('123123', null ,null, '12', '12', null , '1');"
    # cursor.execute(sqltest)
    # 提交事务
    conn.commit()
    # 关闭光标对象
    cursor.close()

    # 关闭数据库连接
    conn.close()
