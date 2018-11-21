import argparse
import tensorflow as tf
from keras.preprocessing import image
import numpy as np

def load_graph(frozen_graph_filename):
    # We load the protobuf file from the disk and parse it to retrieve the
    # unserialized graph_def
    with tf.gfile.GFile(frozen_graph_filename, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())

    # Then, we import the graph_def into a new Graph and returns it
    with tf.Graph().as_default() as graph:
        # The name var will prefix every op/nodes in your graph
        # Since we load everything in a new graph, this is not needed
        tf.import_graph_def(graph_def, name="prefix")
    return graph

gf = tf.GraphDef()
gf.ParseFromString(open('tf_model.pb', 'rb').read())
graph = load_graph("tf_model.pb")
for op in graph.get_operations():
    print(op.name)
list = [n.name + '=>' +  n.op for n in gf.node if n.op in ( 'Softmax','Placeholder')]
print(list)

img = image.load_img("dataset/train/baklava/788.jpg", target_size=(256, 256))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = np.divide(x, 255)

# We launch a Session
with tf.Session(graph=graph) as sess:
    # Note: we don't nee to initialize/restore anything
    # There is no Variables in this graph, only hardcoded constants
    x_tensor = graph.get_tensor_by_name("prefix/xception_input:0")
    y = graph.get_tensor_by_name("prefix/dense_1/Softmax:0")
    feed_dict = {x_tensor: x}
    y_out = sess.run(y, feed_dict)
    # I taught a neural net to recognise when a sum of numbers is bigger than 45
    # it should return False in this case
    print(np.argmax(y_out))  # [[ False ]] Yay, it works!