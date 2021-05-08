import xlrd
import pymysql

if __name__ == '__main__':
    data = xlrd.open_workbook('E:\\data\\广州已安装GPS车辆.xlsx')

    table = data.sheet_by_index(0)
    nrows = table.nrows
    conn = pymysql.connect(host='192.168.3.222',
                           port=3307,
                           user='root',
                           password='Msd^*$@online',
                           database='newgps',
                           charset='utf8')
    cursor = conn.cursor()
    for i in range(nrows):
        # for i in range(5):
        # print(table.row_values(i))
        if i == 0:
            continue

        str = table.row_values(i)
        print(str[3])
        print(str[4])
        sql = """
            INSERT INTO `newgps`.`d_vehicle_type_standno`(`standno`, `vehicle_type_name`, `create_time`) VALUES (%s, %s, now());
            """
        # data01 = (str[1], str[2], str[3])
        # cursor.execute(sql % data)
        # sql = """
        # INSERT INTO `newgps`.`d_second_hand_car_dealer` (`longitude`, `latitude`, `name`) VALUES ("111.0436627", "21.47089445","华兄弟二手车行");
        # """
        cursor.execute(sql, [str[3], str[4]])
        # cursor.execute(sql, [str[1], str[2], str[3]])
        # cursor.execute(sql)

        data02 = cursor.fetchone()
        print("Database version : %s " % data02)

    # 提交事务
    conn.commit()
    # 关闭光标对象
    cursor.close()

    # 关闭数据库连接
    conn.close()
