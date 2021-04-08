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
    sql01 = "SELECT distinct LEFT(active_date,7) ,DATE_FORMAT(DATE_SUB(active_date ,INTERVAL 1 MONTH),'%Y-%m ') ,DATE_FORMAT(DATE_SUB(active_date ,INTERVAL 2 MONTH),'%Y-%m ') FROM d_bigcopy_change WHERE new_sn is NULL ORDER BY LEFT(active_date,7);"
    cursor.execute(sql01)
    activeDateList = cursor.fetchall()
    num = 0
    customerNameList = ['潽金融资租赁有限公司', '阳光保险', '中远海运租赁有限公司', '凯捷融资租赁有限公司', '上海宝信实嘉汽车销售有限公司天津武清分公司', '上海易鑫融资租赁有限公司',
                        '建元资本（中国）融资租赁有限公司']
    nameToTypeDict = {'潽金融资租赁有限公司': '潽金融资租赁有限公司', '阳光保险': '阳光保险', '中远海运租赁有限公司': '中远海运租赁有限公司',
                      '凯捷融资租赁有限公司': '凯捷融资租赁有限公司', '上海宝信实嘉汽车销售有限公司天津武清分公司': '广汇汽车', '上海易鑫融资租赁有限公司': '易鑫集团',
                      '建元资本（中国）融资租赁有限公司': '建元资本（中国）融资租赁有限公司'}
    fo = open("F:\PythonWorkSpaces\importexceldata\log.text", "w")
    snQuChongList = "SELECT "
    snQuChongList = []
    for activeDate in activeDateList:
        for customerName in customerNameList:
            print(activeDate[0], customerName)
            # sql02 = "SELECT sn ,activeDate FROM d_device_activate_detail WHERE (LEFT(activeDate,7) = %s OR LEFT(activeDate,7) = %s) and customer_name = '上海宝信实嘉汽车销售有限公司天津武清分公司' and sn not in (SELECT sn FROM d_settle_doc_big_customer_copy);"
            # sql02 = "SELECT sn ,activeDate FROM d_device_activate_detail WHERE (LEFT(activeDate,7) = %s OR LEFT(activeDate,7) = %s OR LEFT(activeDate,7) = %s) and customer_name = %s and sn not in (SELECT sn FROM d_settle_doc_big_customer_copy);"
            sql02 = "SELECT sn ,activeDate FROM d_device_activate_detail_yangll group by sn order by activeDate;"
            # cursor.execute(sql02, [activeDate[0], activeDate[0]])
            # cursor.execute(sql02, [activeDate[0], activeDate[1], activeDate[2], customerName])
            # cursor.execute(sql02, [activeDate[0]])
            cursor.execute(sql02)
            snAndActiveDateList = cursor.fetchall()
            print(snAndActiveDateList.__len__())

            sql03 = "SELECT id FROM d_bigcopy_change WHERE LEFT(active_date,7) = %s and customer_type = %s and new_sn is NULL;"
            cursor.execute(sql03, [activeDate[0], str(nameToTypeDict[customerName])])
            tiHuIdList = cursor.fetchall()
            print(tiHuIdList.__len__())

            indexNum = 0
            indexNumTwo = 0

            sql04 = "UPDATE `d_bigcopy_change` SET `new_sn` = %s, `new_active_date` = %s ,`active_flag` = 2 WHERE `id` = %s;"

            for tiHuId in tiHuIdList:
                flagOne = True
                flagTwo = True
                flag = True
                if indexNum < len(snAndActiveDateList):
                    while flagOne:
                        if indexNum < len(snAndActiveDateList):
                            if snAndActiveDateList[indexNum][0] not in snQuChongList:
                                snQuChongList.append(snAndActiveDateList[indexNum][0])
                                cursor.execute(sql04,
                                               [snAndActiveDateList[indexNum][0], snAndActiveDateList[indexNum][1],
                                                tiHuId])
                                indexNum = indexNum + 1
                                print('弥补缺失成功')
                                flagOne = False
                            else:
                                print('sn重复')
                                indexNum = indexNum + 1
                        else:
                            flagOne = False
                            print(activeDate[0], customerName, "缺少的数1", len(tiHuIdList) - len(snAndActiveDateList))
                else:
                    print(activeDate[0], customerName, "缺少的数2", len(tiHuIdList) - len(snAndActiveDateList))

                num = num + 1
    print(num)
    # 提交事务
    conn.commit()
    # 关闭光标对象
    cursor.close()

    # 关闭数据库连接
    conn.close()
