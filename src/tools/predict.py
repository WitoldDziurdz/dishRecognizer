from keras.models import load_model
from keras.preprocessing import image
import numpy as np

model = load_model('Xception_299x299_1x4k.hdf5')



img = image.load_img("spa.jpg", target_size=(256, 256))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = np.divide(x, 255)

scores = model.predict(x)

print(np.argmax(scores))
