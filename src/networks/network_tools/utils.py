import matplotlib.pyplot as plt
import os
from keras.preprocessing.image import ImageDataGenerator
class DataGenerator:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.train_dir = os.path.join(base_dir, 'training')
        self.validation_dir = os.path.join(base_dir, 'validation')
        self.test_dir = os.path.join(base_dir, 'evaluation')

        self.train_datagen = ImageDataGenerator(rescale=1. / 255,
                                           rotation_range=30,
                                           width_shift_range=0.2,
                                           height_shift_range=0.2,
                                           shear_range=0.2,
                                           zoom_range=0.2,
                                           horizontal_flip=True)

        self.test_datagen = ImageDataGenerator(rescale=1. / 255)

    def set_food_nonfood_data(self):

        self.train_generator = self.train_datagen.flow_from_directory(
            self.train_dir,
            target_size=(150, 150),
            batch_size=32,
            class_mode='binary')

        self.validation_generator = self.test_datagen.flow_from_directory(
            self.validation_dir,
            target_size=(150, 150),
            batch_size=32,
            class_mode='binary')

        self.test_generator = self.test_datagen.flow_from_directory(
            self.test_dir,
            target_size=(150, 150),
            batch_size=20,
            class_mode='binary')

    def set_101_food_categorical(self):
        self.train_generator = self.train_datagen.flow_from_directory(
            self.train_dir,
            target_size=(150, 150),
            batch_size=72,
            class_mode='categorical')

        self.validation_generator = self.test_datagen.flow_from_directory(
            self.validation_dir,
            target_size=(150, 150),
            batch_size=72,
            class_mode='categorical')

        self.test_generator = self.test_datagen.flow_from_directory(
            self.test_dir,
            target_size=(150, 150),
            batch_size=72,
            class_mode='categorical')

    def set_11_food_categorical(self):
        self.train_generator = self.train_datagen.flow_from_directory(
            self.train_dir,
            target_size=(150, 150),
            batch_size=40,
            class_mode='categorical')

        self.validation_generator = self.test_datagen.flow_from_directory(
            self.validation_dir,
            target_size=(150, 150),
            batch_size=40,
            class_mode='categorical')

        self.test_generator = self.test_datagen.flow_from_directory(
            self.test_dir,
            target_size=(150, 150),
            batch_size=40,
            class_mode='categorical')


def visualization_loss_and_accuracy(history):
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
    pass

def save_model(model, path_name, test_acc):
    model_json = model.to_json()
    file_name = path_name + "_" + str(test_acc);
    with open(file_name + ".json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights(file_name + ".h5")
    print("Saved model to disk")
    pass