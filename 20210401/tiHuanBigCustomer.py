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
    DELETE FROM yll_copy_log_0401;
    '''
    cursor.execute(sql0)
    print('清理日志记录数据库')

    sql00 = '''
    SELECT DISTINCT DATE_FORMAT(DATE_SUB(`settle_date`, INTERVAL 1 MONTH), '%Y%m'), customer_type FROM d_settle_doc_big_customer_yll0401 
    ORDER BY DATE_FORMAT(DATE_SUB(`settle_date`, INTERVAL 1 MONTH), '%Y%m');
    '''
    cursor.execute(sql00)
    dateTypeList = cursor.fetchall()
    customerTypeList = ['中远海运租赁有限公司', '凯捷融资租赁有限公司', '建元资本（中国）融资租赁有限公司', '易鑫集团', '潽金融资租赁有限公司', '阳光保险']
    duplicateList = []
    for dateType in dateTypeList:
        if dateType[1] in customerTypeList:
            print(customerTypeList, dateType[0], dateType[1])
            sql01 = '''
            select a.sn from d_settle_doc_big_customer_yll0401 a left join shwu_settle_detail b on a.sn = b.sn where b.sn is null 
            and a.customer_type = %s and DATE_FORMAT(DATE_SUB(a.settle_date, INTERVAL 1 MONTH),'%%Y%%m') = %s;
            '''
            cursor.execute(sql01, [dateType[1], dateType[0]])
            bigCustomerSnList = cursor.fetchall()
            print(bigCustomerSnList.__len__())

            sql02 = '''
            select b.sn from shwu_settle_detail b left join d_settle_doc_big_customer_yll0401 a on a.sn = b.sn where a.sn is null 
            and b.customer_name = %s and b.month_text = %s;
            '''
            cursor.execute(sql02, [dateType[1], dateType[0]])
            shwuSnList = cursor.fetchall()
            print(shwuSnList.__len__())

            # if shwuSnList and bigCustomerSnList and len(bigCustomerSnList) > len(shwuSnList):
            if shwuSnList and bigCustomerSnList:
                for indexNum, shwuSn in enumerate(shwuSnList):
                    if indexNum < len(bigCustomerSnList) and shwuSn not in duplicateList:
                        duplicateList.append(shwuSn)
                        sql03 = " UPDATE d_settle_doc_big_customer_yll0401 SET `sn` = %s  WHERE `sn` = %s;"
                        cursor.execute(sql03, [shwuSnList[indexNum], bigCustomerSnList[indexNum]])
                        # 提交事务
                        conn.commit()
                        sql04 = "INSERT INTO yll_copy_log_0401(source_sn, new_sn) VALUES( %s, %s);"
                        cursor.execute(sql04, [bigCustomerSnList[indexNum], shwuSnList[indexNum]])
                        # 提交事务
                        conn.commit()

    # 提交事务
    conn.commit()
    # 关闭光标对象
    cursor.close()

    # 关闭数据库连接
    conn.close()
