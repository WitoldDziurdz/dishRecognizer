import tensorflow as tf
import sys

if len(sys.argv) != 4:
    print("Usage:")
    print("arg1: path to model,")
    print("arg2: export model name,")
    print("arg3: version of exported model")
    exit(0)

model_path = sys.argv[1]
name = sys.argv[2]
version = sys.argv[3]

tf.keras.backend.set_learning_phase(0)
model = tf.keras.models.load_model(model_path)
export_path = './' + name + '/' + version

print('Exporting model to:', export_path)

with tf.keras.backend.get_session() as sess:
    tf.saved_model.simple_save(
        sess,
        export_path,
        inputs={'input_image': model.input},
        outputs={t.name: t for t in model.outputs})
