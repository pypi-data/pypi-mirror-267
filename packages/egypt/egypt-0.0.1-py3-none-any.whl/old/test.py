import tensorflow as tf

# 创建一个输入张量
input_tensor = tf.constant([[1, 2], [3, 4]])

# 使用 tf.pad 进行填充
padded_tensor = tf.pad(input_tensor, paddings=[[1, 1], [2, 2]])

# 打印结果
with tf.Session() as sess:
    print("原始张量:")
    print(sess.run(input_tensor))
    
    print("\n填充后的张量:")
    print(sess.run(padded_tensor))
