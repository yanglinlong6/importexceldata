import pymysql

import requests

if __name__ == '__main__':
    conn = pymysql.connect(host='192.168.3.222',
                           port=3307,
                           user='root',
                           password='Msd^*$@online',
                           database='newgps',
                           charset='utf8',
                           autocommit='True')

    cursor = conn.cursor()
    sql01 = "select distinct sn from d_track_info;"
    cursor.execute(sql01)
    snList = cursor.fetchall()
    for sn in snList:
        # r = requests.get('http://localhost:9999/ots/vehicle/validateAJDeviceLocation?sn=' + sn[0])
        r = requests.get('http://localhost:9999/ots/vehicle/queryInvoicingData?sn=' + sn[0])
        print(sn[0], r.text)
