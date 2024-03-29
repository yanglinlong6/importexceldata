import pymysql
import xlrd

if __name__ == '__main__':
    data = xlrd.open_workbook('E:\\data\\all_second_car.xls')

    table = data.sheet_by_index(0)
    nrows = table.nrows
    conn = pymysql.connect(host='192.168.5.22',
                           port=3307,
                           user='user_yangll',
                           password='vGxw9jWg',
                           database='gps',
                           charset='utf8')
    cursor = conn.cursor()
    for i in range(nrows):
        # for i in range(5):
        # print(table.row_values(i))
        if i == 0:
            continue

        str = table.row_values(i)
        print(str[1])
        print(str[2])
        print(str[3])
        sql = """
            update `d_vehicle` set classId = {} where `standno` = {} and `name` = {};
            """.format()

        sql = """
            update `d_vehicle_workorder` set classId = {} where standno = {} and name = {} and sqbh = {};
            """.format()

        # sql = """
        #     INSERT INTO `d_class` (`longitude`, `latitude`, `name`) VALUES (%s, %s,%s);
        #     """
        # data01 = (str[1], str[2], str[3])
        # cursor.execute(sql % data)
        # sql = """
        # INSERT INTO `newgps`.`d_second_hand_car_dealer` (`longitude`, `latitude`, `name`) VALUES ("111.0436627", "21.47089445","华兄弟二手车行");
        # """
        cursor.execute(sql, [str[1], str[2], str[3]])
        # cursor.execute(sql, [str[1], str[2], str[3]])
        # cursor.execute(sql)

        data02 = cursor.fetchone()
        print("Database version : %s " % data02)

        # 提交事务
        conn.commit()
        fw = open("H:\PythonWorkSpaces\importexceldata\sql.txt", 'w')  # 将要输出保存的文件地址

        for line in open("H:\PythonWorkSpaces\importexceldata\sql.txt"):  # 读取的文件
            fw.write(sql)  # 将字符串写入文件中
            line.rstrip("\n")  # 为去除行尾换行符
            fw.write("\n")  # 换行

    # 提交事务
    conn.commit()
    # 关闭光标对象
    cursor.close()

    # 关闭数据库连接
    conn.close()
