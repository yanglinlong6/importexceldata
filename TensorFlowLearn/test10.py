import tensorflow as tf

tf.compat.v1.disable_eager_execution()

I_matrix = tf.eye(5)
print(I_matrix)
