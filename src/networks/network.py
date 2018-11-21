from keras import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense, Dropout
import keras


from keras.preprocessing.image import ImageDataGenerator

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

opt = keras.optimizers.rmsprop(lr=0.0001, decay=1e-6)

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)

training_set = train_datagen.flow_from_directory('data/training',
                                                 target_size=(32,32),
                                                 batch_size=128,
                                                 class_mode='categorical')

test_set = test_datagen.flow_from_directory('data/evaluation',
                                             target_size=(32,32),
                                             batch_size=128,
                                             class_mode='categorical')

history = model.fit_generator(training_set,
                     steps_per_epoch=100,
                     epochs=10,
                     validation_data=test_set,
                     validation_steps=100)

# accuracy and loss visualistion
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