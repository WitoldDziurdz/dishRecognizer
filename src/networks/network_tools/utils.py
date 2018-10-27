import matplotlib.pyplot as plt
import os
from keras.preprocessing.image import ImageDataGenerator

base_model_names = ['densenet', 'densenet121', 'densenet169', 'densenet201', 'inception_resnet_v2', 'inception_v3', 'NASNet', 'resnet50', 'vgg16', 'vgg19', 'xception',]

class DataGenerator:
    def __init__(self, base_dir, width, length):
        self.base_dir = base_dir
        self.width = width
        self.length = length
        #self.train_dir = os.path.join(base_dir, 'training')
        #self.validation_dir = os.path.join(base_dir, 'validation')
        #self.test_dir = os.path.join(base_dir, 'evaluation')
        self.train_dir = os.path.join(base_dir, 'train')
        self.validation_dir = os.path.join(base_dir, 'test')
        self.test_dir = os.path.join(base_dir, 'test')

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
            target_size=(self.width, self.length),
            batch_size=32,
            class_mode='binary')

        self.validation_generator = self.test_datagen.flow_from_directory(
            self.validation_dir,
            target_size=(self.width, self.length),
            batch_size=32,
            class_mode='binary')

        self.test_generator = self.test_datagen.flow_from_directory(
            self.test_dir,
            target_size=(self.width, self.length),
            batch_size=32,
            class_mode='binary')

    def set_101_food_categorical(self):
        self.train_generator = self.train_datagen.flow_from_directory(
            self.train_dir,
            target_size=(self.width, self.length),
            batch_size=32,
            class_mode='categorical')

        self.validation_generator = self.test_datagen.flow_from_directory(
            self.validation_dir,
            target_size=(self.width, self.length),
            batch_size=32,
            class_mode='categorical')

        self.test_generator = self.test_datagen.flow_from_directory(
            self.test_dir,
            target_size=(self.width, self.length),
            batch_size=32,
            class_mode='categorical')

    def set_11_food_categorical(self):
        self.train_generator = self.train_datagen.flow_from_directory(
            self.train_dir,
            target_size=(self.width, self.length),
            batch_size=32,
            class_mode='categorical')

        self.validation_generator = self.test_datagen.flow_from_directory(
            self.validation_dir,
            target_size=(self.width, self.length),
            batch_size=32,
            class_mode='categorical')

        self.test_generator = self.test_datagen.flow_from_directory(
            self.test_dir,
            target_size=(self.width, self.length),
            batch_size=32,
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

def list_layers(model):
    layers_list = []
    for layer in model.layers:
        if any(layer.name in s for s in base_model_names):
            for l in layer.layers:
                layers_list.append(l.name + ' - ' +  'trainable: ' + str(l.trainable))
        else:
            layers_list.append(layer.name + ' - ' + 'trainable: ' + str(layer.trainable))
    model.layers_list = layers_list
    
class Architecture:
    
    full_config_file_name = "full_config.txt"
    opt_config_file_name = "opt_config.txt"
    layers_config_file_name = "layers_config.txt"
    
    def __init__(self, model):
        self.full_config = model.get_config()
        self.layers_list = self.list_layers(model)
        self.opt_config = model.optimizer.get_config()
        
    def log(self, path):
        with open(path + self.layers_config_file_name, 'w') as f:
            for layer in self.layers_list:
                f.write("%s\n" % layer)
            
        f = open(path + self.full_config_file_name,"w")
        f.write( str(self.full_config) )
        f.close()
        
        f = open(path + self.opt_config_file_name,"w")
        f.write( str(self.opt_config) )
        f.close()
        
    def list_layers(self, model):
        layers_list = []
        for layer in model.layers:
            if any(layer.name in s for s in base_model_names):
                for l in layer.layers:
                    layers_list.append(l.name + ' - ' +  'trainable: ' + str(l.trainable))
            else:
                layers_list.append(layer.name + ' - ' + 'trainable: ' + str(layer.trainable))
        return layers_list
