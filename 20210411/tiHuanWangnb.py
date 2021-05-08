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
    print('������־��¼���ݿ�')

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
                    WHERE a.`settle_merchant` IN ('�Ϻ�������Ϣ�Ƽ����޹�˾','�ϲ��غ�̩���������������ι�˾','����������ͨ����ó�����޹�˾','��������ͨ���������������޹�˾','������ͨ�������۷������޹�˾','��ɽ�аĶ���ӿƼ����޹�˾','��³ľ����ΰ���������������޹�˾','��³ľ���ʤ���������������޹�˾','�Ž�����ͨ���������������޹�˾','�Ž�����ͨ�����������޹�˾','�Ž�����ͨ����ó�����޹�˾','���Ϻ��������������޹�˾','���������������۷������޹�˾','�����ٿ��������۷������޹�˾','���Ϸ����ӽ���ó���޹�˾��GPS)','�����л�ͨ����ͨ�Ź������޹�˾','����','���','���������Ǽ���Ϣ�����ɷ����޹�˾','�������ֿ��������������޹�˾','�ϲ��ֳ��������������޹�˾','�ϲ�ΰ���������۷������޹�˾','�����������������۷������޹�˾','���Ż��Ͷ����ѯ���޹�˾','�Ϸ��»�������Ϣ��ѯ���޹�˾','�Ϸ����ܵ�װ�������޹�˾','��������ͨ�����������۷������޹�˾','��������ͨ�������۷������޹�˾','����������������۷������޹�˾','�����в�����е�豸�ɷ����޹�˾','�Ĵ���»������������޹�˾','�������輯�����޹�˾','�������人�������������޹�˾','�˴���ͨ�������۷������޹�˾','ɽ�����������豸�������޹�˾','�㶫�ѻ���ҵͶ�����޹�˾','�㶫�����������޷������޹�˾','�㶫������Ƽ����޹�˾','����һﻻ�е�������޹�˾','�����濨������Ʒ��չ���޹�˾','���ݵ������ع����޹�˾','����������˶��ó���޹�˾','�������м����������������ι�˾','�ȷ���˳֮���������۷������޹�˾�������ֹ�˾','�ź���','�Ż�','�ɶ�׿��������Ʒ���޹�˾','���ݳɹ�������װ�������޹�˾','����ͨ�ݽ������޹�˾','������ͨ�������۷������޹�˾','������ͨ�������۷������޹�˾','��������ͨ��������ó�����޹�˾','��������ͨ���������������޹�˾','��������ͨ�������۷������޹�˾','��ʤ��','��ʤ��','���ݹ��ν�����װ�������޹�˾','�人�г~����ȫ�ӽ�����������Ʒ����','�����������̻�е���޹�˾','��������ͨ���۷������޹�˾','������ͨ���������������޹�˾','������ͨ�����������۷������޹�˾','������ͨ���������۷������޹�˾','������ͨ�����������۷������޹�˾','������ͨ���������������޹�˾','������ͨ�º������������޹�˾','�ӱ�����������Ʒ���޹�˾','���ϰ�ά���������۷������޹�˾�˳Ƿֹ�˾','Ȫ�ݺ�Դ������е�������޹�˾','�����л����������۷������޹�˾����ֹ�˾','�����п��ڿƼ����޹�˾','��������Ͷ�ʹ������޹�˾','����·��������ó���޹�˾','��ά������Ƽ������ݣ����޹�˾','�����ʢԴ��ó���޹�˾','ʯ��ׯ���ĺ�ͨ����ó���޹�˾','ʯ��ׯ���¡�����豸���޹�˾','�����������Ͷ�ʹ������޹�˾','���ݿ����������������޹�˾','Ƽ�������������۷������޹�˾','Ƽ����ͨ���������������޹�˾','Ƽ����ͨ�������۷������޹�˾','�������ͽ�����е���޹�˾','���ݳ���ʢ��������Ϣ��ѯ���޹�˾','������������װ�ξ�Ӫ��','����ͬ���������۷������޹�˾','����ͬ�۷����������۷������޹�˾','������ͨ���������������޹�˾','������ͨ����ó�����޹�˾','������ͨ�������۷������޹�˾','������','֣��������������Ʒ���޹�˾','�����λ�����ó���޹�˾','�����������ų������������޹�˾','�����㲩��ͨ������Ʒ�������޹�˾','����/���̿ͻ�','�����','�ൺ�׽�ͨ�����������޹�˾','�ຣ��̩�������������޹�˾','�ɵ��������񣨶�ݸ�����޹�˾��ɽ�ֹ�˾','��ɽ�����е�Ƽ����޹�˾','������˳֮���������۷������޹�˾')
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
                # print('indexNum��ֵ', indexNum)
                if indexNum < len(activateSnList):
                    sql03 = "INSERT INTO yll_copy_log_0411(`detail_id`, `source_sn`, `new_sn`, `active_time`) VALUES(%s, %s, %s, %s);"
                    cursor.execute(sql03, [deviceDetailList[indexNum][0], deviceDetailList[indexNum][1],
                                           activateSnList[indexNum][0], activateSnList[indexNum][1]])
                    # �ύ����
                    conn.commit()
                else:
                    print(dateTime[0], 'ȱʧ����', len(deviceDetailList) - indexNum)

    # �ύ����
    conn.commit()
    # �رչ�����
    cursor.close()

    # �ر����ݿ�����
    conn.close()
