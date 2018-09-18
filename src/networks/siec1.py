import os, shutil
from keras import layers
from keras import models
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image 
from keras import optimizers

# direcotires
base_dir = 'C:\data'
train_dir = os.path.join(base_dir, 'training') 
validation_dir = os.path.join(base_dir, 'validation')
test_dir = os.path.join(base_dir, 'evaluation') 

train_food_dir = os.path.join(train_dir, 'food')
train_non_food_dir = os.path.join(train_dir, 'non_food')
validation_food_dir = os.path.join(validation_dir, 'food')
validation_non_food_dir = os.path.join(validation_dir, 'non_food')
test_food_dir = os.path.join(test_dir, 'food')
test_non_food_dir = os.path.join(test_dir, 'non_food')

# data generators from direcotry from keras
train_datagen = ImageDataGenerator(rescale = 1./255, 
                                   rotation_range=40, 
                                   width_shift_range=0.2,
                                   height_shift_range=0.2,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
        train_dir, 
        target_size=(150, 150), 
        batch_size=32,
        class_mode='binary')

validation_generator = test_datagen.flow_from_directory(
        validation_dir,
        target_size=(150, 150),
        batch_size=32,
        class_mode='binary')

test_generator = test_datagen.flow_from_directory(
 test_dir,
 target_size=(150, 150),
 batch_size=20,
 class_mode='binary')

# model definition
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer=optimizers.RMSprop(lr=1e-4), metrics=['acc'])

model = Sequential()

model.add(Convolution2D(32, 3, input_shape=(32, 32, 3), activation='relu'))
model.add(Convolution2D(32, 3, activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(rate=0.1))
model.add(Convolution2D(64, 3, activation='relu'))
model.add(Convolution2D(64, 3, activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(rate=0.2))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(rate=0.3))
model.add(Dense(10, activation='sigmoid'))

#training
history = model.fit_generator(
     train_generator,
     steps_per_epoch=100,
     epochs=60,
     validation_data=validation_generator,
     validation_steps=40, workers=16)

# evaluation
test_loss, test_acc = model.evaluate_generator(test_generator, steps=50)
print('test acc:', test_acc)

# loss and accuracy visualization
import matplotlib.pyplot as plt
acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(acc) + 1)
plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()
plt.figure()
plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()
plt.show()
