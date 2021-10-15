# coding=gbk
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
    sql0 = '''
    DELETE FROM yll_copy_log_0508;
    '''
    cursor.execute(sql0)
    print('清理日志记录数据库')

    sql00 = '''
    SELECT DISTINCT DATE_FORMAT(`settle_time`, '%Y-%m') FROM d_eshield_device_details_new_wangnb_yll0401 
    WHERE `settle_time`<'2020-07-01 00:00:00' AND `active_time` IS NULL ORDER BY DATE_FORMAT(`settle_time`, '%Y-%m');
    '''
    cursor.execute(sql00)
    dateTimeList = cursor.fetchall()
    # duplicateList = []
    for dateTime in dateTimeList:
        sql01 = '''
                    SELECT `id`, `sn` FROM d_eshield_device_details_new_wangnb_yll0401 WHERE `settle_time`<'2020-07-01 00:00:00' AND `active_time` IS NULL
                    AND DATE_FORMAT(`settle_time`,'%%Y-%%m')= %s;
                        '''
        cursor.execute(sql01, [dateTime[0]])
        deviceDetailList = cursor.fetchall()
        print(deviceDetailList.__len__())

        sql02 = '''
                   SELECT DISTINCT a.`sn`, a.`activeDate` FROM `d_device_activate_detail` a
                   WHERE DATE_FORMAT(a.`activeDate`,'%%Y-%%m') > %s 
                   AND a.`sn` NOT IN (SELECT bb.`sn` FROM `d_settle_doc_big_customer_yll0401` bb)
                   AND a.`sn` NOT IN (SELECT bb.`sn` FROM `d_settle_doc_big_customer_copy1517` bb)
                   AND a.`sn` NOT IN (SELECT cc.`sn` FROM `d_eshield_device_details_new_wangnb_yll0401` cc)
                   AND a.`sn` NOT IN (SELECT ff.`new_sn` FROM `yll_copy_log_0508` ff);
                        '''
        cursor.execute(sql02, [dateTime[0]])
        activateSnList = cursor.fetchall()
        print(activateSnList.__len__())

        # if shwuSnList and bigCustomerSnList and len(bigCustomerSnList) > len(shwuSnList):
        if activateSnList and deviceDetailList:
            for indexNum, deviceDetai in enumerate(deviceDetailList):
                # print('indexNum数值', indexNum)
                if indexNum < len(activateSnList):
                    sql03 = "INSERT INTO yll_copy_log_0508(`detail_id`, `source_sn`, `new_sn`, `active_time`) VALUES(%s, %s, %s, %s);"
                    cursor.execute(sql03, [deviceDetailList[indexNum][0], deviceDetailList[indexNum][1],
                                           activateSnList[indexNum][0], activateSnList[indexNum][1]])
                    # 提交事务
                    conn.commit()
                else:
                    print(dateTime[0], '缺失的数', len(deviceDetailList) - indexNum)

    # 提交事务
    conn.commit()
    # 关闭光标对象
    cursor.close()

    # 关闭数据库连接
    conn.close()
