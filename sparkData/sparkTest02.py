from pyspark.sql import SparkSession

# 创建一个连接
spark = SparkSession.Builder().appName('sql_yang').master('local[*]').enableHiveSupport().getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

# spark.sql执行的就直接是DataFrame类型了
df1 = spark.sql("show tables")
spark.sql("set  hive.exec.dynamic.partition.mode = nonstrict")
spark.sql("set  hive.exec.dynamic.partition = true")
# df2 = spark.sql(
#     "create table tab_test(name string,age int,num1 double,num2 bigint,msg varchar(80)) partitioned by (p_age int,p_name string) row format delimited fields terminated by ',' stored as textfile location '/tab/test/tab_test'; ")

df2 = spark.sql("CREATE TABLE IF NOT EXISTS src_yang (key_yang INT, value_yang STRING)")

df3 = spark.sql("show tables")
df4 = spark.sql("show databases;")
# 打印列头及字段类型
print("\n\n\n")
print(df1)
print(df2)
print(df3)
print(df4)

# 打印查询得到的数据
print("\n\n\n\n\n")
df1.show()
df2.show()
df3.show()
df4.show()

# 关闭spark回话
spark.stop()
