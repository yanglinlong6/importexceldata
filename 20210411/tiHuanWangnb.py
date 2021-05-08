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
    DELETE FROM yll_copy_log_0411;
    '''
    cursor.execute(sql0)
    print('清理日志记录数据库')

    sql00 = '''
    SELECT DISTINCT DATE_FORMAT(`settle_time`, '%Y-%m') FROM d_eshield_device_details_new_wangnb 
    WHERE `settle_time`<'2019-01-01 00:00:00' ORDER BY DATE_FORMAT(`settle_time`, '%Y-%m');
    '''
    cursor.execute(sql00)
    dateTimeList = cursor.fetchall()
    # duplicateList = []
    for dateTime in dateTimeList:
        sql01 = '''
                    SELECT `id`, `sn` FROM `d_eshield_device_details_new_wangnb` a
                    WHERE a.`settle_merchant` IN ('上海欣渠信息科技有限公司','上蔡县宏泰物流运输有限责任公司','上饶市新运通汽车贸易有限公司','上饶新运通汽车技术服务有限公司','上饶运通汽车销售服务有限公司','中山市澳多电子科技有限公司','乌鲁木齐亿伟车尚汽车服务有限公司','乌鲁木齐百胜得行汽车服务有限公司','九江新运通汽车技术服务有限公司','九江新运通汽车服务有限公司','九江新运通汽车贸易有限公司','云南厚瑞汽车销售有限公司','云南玛派汽车销售服务有限公司','云南荣俊汽车销售服务有限公司','云南风行视界商贸有限公司（GPS)','保定市华通京保通信工程有限公司','其他','冯宏','北京九五智驾信息技术股份有限公司','北京深林开物市政工程有限公司','南昌乐车林汽车服务有限公司','南昌伟泽汽车销售服务有限公司','南阳市龙成汽车销售服务有限公司','厦门汇贷投资咨询有限公司','合肥新汇商务信息咨询有限公司','合肥皖能吊装工程有限公司','吉安新运通大有汽车销售服务有限公司','吉安新运通汽车销售服务有限公司','吉安汇成万方汽车销售服务有限公司','嘉兴市昌龙机械设备股份有限公司','四川厚德汇汽车服务有限公司','土力建设集团有限公司','好享车（武汉）汽车服务有限公司','宜春运通汽车销售服务有限公司','山东安起起重设备租赁有限公司','广东友汇商业投资有限公司','广东菜鸟汽车租赁服务有限公司','广东邦汇金服科技有限公司','广州一锘机械租赁有限公司','广州玩卡汽车用品发展有限公司','广州第三方控股有限公司','广西南宁麦硕商贸有限公司','广西汇尚佳汽车服务有限责任公司','廊坊市顺之风汽车销售服务有限公司安次区分公司','张海鑫','张辉','成都卓悦汽车用品有限公司','扬州成功建筑安装工程有限公司','扬州通惠建设有限公司','抚州运通汽车销售服务有限公司','新余运通汽车销售服务有限公司','景德镇运通华孚汽车贸易有限公司','景德镇运通汽车技术服务有限公司','景德镇运通汽车销售服务有限公司','李胜虎','杨胜飞','杭州广治建筑安装工程有限公司','武汉市硚口区全视界汽车电子用品商行','江苏瑞铁工程机械有限公司','江西新运通销售服务有限公司','江西运通众祥汽车服务有限公司','江西运通华孚汽车销售服务有限公司','江西运通大创汽车销售服务有限公司','江西运通汽车城西销售服务有限公司','江西运通汽车技术服务有限公司','江西运通致恒汽车服务有限公司','河北合利汽车用品有限公司','河南艾维欣汽车销售服务有限公司运城分公司','泉州宏源建筑机械租赁有限公司','深圳市华熙汽车销售服务有限公司福田分公司','深圳市酷众科技有限公司','湖北昌兴投资管理有限公司','湖北路琥揽星商贸有限公司','特维轮网络科技（杭州）有限公司','甘肃嘉盛源商贸有限公司','石家庄市四海通达商贸有限公司','石家庄金昌隆机电设备有限公司','福州市益佰年投资管理有限公司','苏州凯利莱融资租赁有限公司','萍乡美凯汽车销售服务有限公司','萍乡运通汽车技术服务有限公司','萍乡运通汽车销售服务有限公司','贵州庆晖建筑机械有限公司','贵州朝和盛世商务信息咨询有限公司','贵阳嘉鑫汽车装饰经营部','赣州同益汽车销售服务有限公司','赣州同驰丰田汽车销售服务有限公司','赣州运通众祥汽车服务有限公司','赣州运通汽车贸易有限公司','赣州运通汽车销售服务有限公司','邓锶韵','郑州新龙驰汽车饰品有限公司','重庆鑫华成商贸有限公司','长春市龙泽信诚汽车服务有限公司','陕西广博汇通汽车用品服务有限公司','零售/电商客户','雷玉杰','青岛易捷通汽车服务有限公司','青海嘉泰泓汽车服务有限公司','飞的汽车服务（东莞）有限公司佛山分公司','马鞍山奥天机械科技有限公司','黑龙江顺之风汽车销售服务有限公司')
                    AND a.`active_time` IS NULL AND DATE_FORMAT(a.`settle_time`,'%%Y-%%m')= %s;
                        '''
        cursor.execute(sql01, [dateTime[0]])
        deviceDetailList = cursor.fetchall()
        print(deviceDetailList.__len__())

        sql02 = '''
                   SELECT DISTINCT a.`sn`, a.`activeDate` FROM `d_device_activate_detail` a
                   WHERE DATE_FORMAT(a.`activeDate`,'%%Y-%%m') > %s 
                   AND a.`sn` NOT IN (SELECT bb.`sn` FROM `d_settle_doc_big_customer_yll0401` bb)
                   AND a.`sn` NOT IN (SELECT cc.`sn` FROM `d_eshield_device_details_new_wangnb` cc)
                   AND a.`sn` NOT IN (SELECT ff.`new_sn` FROM `yll_copy_log_0411` ff);
                        '''
        cursor.execute(sql02, [dateTime[0]])
        activateSnList = cursor.fetchall()
        print(activateSnList.__len__())

        # if shwuSnList and bigCustomerSnList and len(bigCustomerSnList) > len(shwuSnList):
        if activateSnList and deviceDetailList:
            for indexNum, deviceDetai in enumerate(deviceDetailList):
                # print('indexNum数值', indexNum)
                if indexNum < len(activateSnList):
                    sql03 = "INSERT INTO yll_copy_log_0411(`detail_id`, `source_sn`, `new_sn`, `active_time`) VALUES(%s, %s, %s, %s);"
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
