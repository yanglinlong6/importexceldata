import pymysql

conn = pymysql.connect(host='192.168.5.22',
                       port=3307,
                       user='user_yangll',
                       password='vGxw9jWg',
                       database='gps',
                       charset='utf8')
cursor = conn.cursor()

if __name__ == '__main__':
    sql = '''
        select classid from d_class where  className = %s;
        '''
    cursor.execute(sql, '东莞茂鑫（广东）F广东高静（包活干）')
    classidData = cursor.fetchall()
    print('classidData', classidData)

