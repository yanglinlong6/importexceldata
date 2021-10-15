from pyhive import hive  # or import hive

conn = hive.Connection(host='127.0.0.1', port=10000, database='test')
cursor = conn.cursor()
# cursor.execute('SELECT * FROM my_awesome_data LIMIT 10')
# for i in range(** **):
sql = 'insert into table student values(1001, "zhangsan");'
cursor.execute(sql)

# 下面是官网代码：
from pyhive import presto  # or import hive

cursor = presto.connect('localhost', ).cursor()
cursor.execute('SELECT * FROM student LIMIT 10')
print(cursor.fetchone())
print(cursor.fetchall())
