# 输入python，进入python环境
import tensorflow as tf

# 查看tensorflow版本
print(tf.__version__)
# 输出'2.0.0-alpha0'
# 测试GPU能否调用,先查看显卡使用情况
import os

os.system("nvidia-smi")


# 调用显卡
@tf.function
def f():
    pass


f()
# 这时会打印好多日志，我电脑上还有warning，感觉不影响
# 再次查询显卡
os.system("nvidia-smi")
