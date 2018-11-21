import tensorflow as tf
import numpy as np
import PIL
from keras.preprocessing import image
import os

def load_image( infilename ) :
    img = Image.open( infilename )
    img.load()
    data = np.asarray( img, dtype="int32" )
    return data

#im = load_image("dataset/train/apple_pie/134.jpg")
size = 256, 256
for file in os.listdir("dataset/train/baklava"):
    #img = np.array(PIL.Image.open(file).resize((256, 256))).astype(np.float32)
    img = image.load_img("dataset/train/baklava/" + file, target_size=(256, 256))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = np.divide(x, 255)

    # Load TFLite model and allocate tensors.
    interpreter = tf.contrib.lite.Interpreter(model_path="converted_model.tflite")
    interpreter.allocate_tensors()

    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Test model on random input data.
    input_shape = input_details[0]['shape']
    input_data = x
    interpreter.set_tensor(input_details[0]['index'], input_data)

    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    print(file, np.argmax(output_data))