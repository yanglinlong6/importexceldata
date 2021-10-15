import tensorflow as tf

tf.compat.v1.disable_eager_execution()

message = tf.constant('Welcome to the exciting world of Deep Neural Networks!')

with tf.compat.v1.Session() as sess:
    print(sess.run(message).decode())
