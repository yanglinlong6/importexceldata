from hdfs import *

client = Client('http://26.26.26.1:50075')  # 2.X版本port 使用50070  3.x版本port 使用9870
client.list('/')
