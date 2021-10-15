from pyhive import hive

conn = hive.Connection(host='127.0.0.1', port=10000, username='yangll', database='test')
cursor = conn.cursor()
cursor.execute('select * from student limit 10')
for result in cursor.fetchall():
    print(result)
