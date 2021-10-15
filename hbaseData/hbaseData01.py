from hbase import Hbase
from hbase.ttypes import *
from thrift.transport import TSocket

transport = TSocket.TSocket('localhost', 54464)
protocol = TBinaryProtocol.TBinaryProtocol(transport)

client = Hbase.Client(protocol)
transport.open()
print(client.getTableNames())
