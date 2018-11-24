import os
from keras.preprocessing.image import ImageDataGenerator

class DataGenerator:
    def __init__(self, base_dir, input_x, input_y):
        self.base_dir = base_dir
        self.input_x = input_x
        self.input_y = input_y
        self.train_dir = os.path.join(base_dir, 'training')
        self.validation_dir = os.path.join(base_dir, 'validation')
        self.test_dir = os.path.join(base_dir, 'evaluation')
        self.batch_size = 30
        self.class_mode = 'categorical'
        self.train_datagen = ImageDataGenerator(rescale=1. / 255,
                                           rotation_range=30,
                                           width_shift_range=0.2,
                                           height_shift_range=0.2,
                                           shear_range=0.2,
                                           zoom_range=0.2,
                                           horizontal_flip=True)

        self.test_datagen = ImageDataGenerator(rescale=1. / 255)

        self.train_generator = self.train_datagen.flow_from_directory(
            self.train_dir,
            target_size=(self.input_x, self.input_y),
            batch_size=self.batch_size,
            class_mode=self.class_mode)

        self.validation_generator = self.test_datagen.flow_from_directory(
            self.validation_dir,
            target_size=(self.input_x, self.input_y),
            batch_size=self.batch_size,
            class_mode=self.class_mode)

        self.test_generator = self.test_datagen.flow_from_directory(
            self.test_dir,
            target_size=(self.input_x, self.input_y),
            batch_size=self.batch_size,
            class_mode=self.class_mode)

    def train_data(self):
        return self.train_generator

    def validate_data(self):
        return self.validation_generator

    def test_data(self):
        return self.test_generator

    def batch_size(self):
        return self.batch_size


