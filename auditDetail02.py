import random
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
    sql01 = "SELECT DISTINCT sn FROM d_track_info_import WHERE isActive = 0;"
    cursor.execute(sql01)
    snDataList = cursor.fetchall()
    print('1111')
    print(snDataList.__len__())
    print(snDataList)
    strField = {}

    num = 0

    sql02 = "INSERT INTO `d_eshield_device_details_new`(`sn`, `delivery_time`) VALUES (%s, %s);"
    for snData in snDataList:
        print(num)
        print(snData[0])
        strField[1] = str(snData[0])
        if num <= 3690:
            strField[2] = str("2020-09-" + str(random.randint(1, 30)) + " " + str(random.randint(0, 23)) + ":" + str(
                random.randint(0, 59)) + ":" + str(random.randint(0, 59)))
            print(sql02)
            print(strField[2])
            cursor.execute(sql02, [strField[1], strField[2]])
            num = num + 1
        elif 3690 < num <= 8650:
            strField[2] = str("2020-10-" + str(random.randint(1, 30)) + " " + str(random.randint(0, 23)) + ":" + str(
                random.randint(0, 59)) + ":" + str(random.randint(0, 59)))
            print(sql02)
            print(strField[2])
            cursor.execute(sql02, [strField[1], strField[2]])
            num = num + 1
        elif 8650 < num <= 14400:
            strField[2] = str("2020-11-" + str(random.randint(1, 30)) + " " + str(random.randint(0, 23)) + ":" + str(
                random.randint(0, 59)) + ":" + str(random.randint(0, 59)))
            print(sql02)
            print(strField[2])
            cursor.execute(sql02, [strField[1], strField[2]])
            num = num + 1
        elif 8650 < num <= 21564:
            strField[2] = str("2020-12-" + str(random.randint(1, 30)) + " " + str(random.randint(0, 23)) + ":" + str(
                random.randint(0, 59)) + ":" + str(random.randint(0, 59)))
            print(sql02)
            print(strField[2])
            cursor.execute(sql02, [strField[1], strField[2]])
            num = num + 1
        else:
            pass

    # 提交事务
    conn.commit()
    # 关闭光标对象
    cursor.close()

    # 关闭数据库连接
    conn.close()
