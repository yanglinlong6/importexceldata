from pyhdfs import HdfsClient

client = HdfsClient(hosts='26.26.26.1:50070')  # hdfs地址


def read(name):
    res = client.open('/user/wcinput/' + name)  # hdfs文件路径,根目录/
    for r in res:
        line = str(r)  # open后是二进制,str()转换为字符串并转码
        print(line)


def write():
    str = 'hello world'
    client.create('/hdfs/py.txt', str)  # 创建新文件并写入字符串


write()


def delete(name):
    client.delete('/user/wcinput/' + name)


def copyFromLocal():
    client.copy_from_local('D:/test01.txt', '/user/wcinput/yang')  # 本地文件绝对路径,HDFS目录必须不存在


# client.copy_to_local('/user/wcinput/11111.xls', 'D:/tmp/11111.xls')
# print(client.list_status('/user/wcinput/'))
print(client.get_content_summary('/user/wcinput/'))
# client.create('/hdfs')
if __name__ == '__main__':
    print('==========')
    # write()
    # read('py.txt')
    # delete('test')
    # copyFromLocal()
