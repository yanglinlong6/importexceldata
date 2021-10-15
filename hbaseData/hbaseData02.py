import happybase

# 连接
connection = happybase.Connection('127.0.0.1', 9090, autoconnect=False)
connection.open()

# connection.create_table('mytable', {'name' : dict(max_versions=5), 'course':dict()})
# 打印所有的表
print(connection.tables())
# table = connection.table('Score')
# row = table.row(b'95001')
# print(row[b'course:Math'])
#
# # 插入数据
# table.put(b'95002', {b'course:Math': b'65', b'course:English': b'77'})
