from keras import layers
from keras import models
from keras import optimizers
from keras.applications import VGG16, Xception


class Network:
    def __init__(self, setting, data):
        self.__input_x = setting.input_x
        self.__input_y = setting.input_y
        self.__input_z = setting.input_z
        self.__n_classes = setting.n_classes
        self.__input_shape = (self.__input_x, self.__input_y, self.__input_z)
        self.__model = models.Sequential()
        self.__data = data

    def fit(self, epochs, callbacks):
        history = self.__model.fit_generator(
            self.__data.train_data(),
            steps_per_epoch=700 * self.__n_classes // self.__data.batch_size(),
            epochs=epochs,
            callbacks=callbacks,
            validation_data=self.__data.validate_data(),
            validation_steps=150 * self.__n_classes // self.__data.batch_size(), workers=16)
        return history

    def evaluate(self, steps):
        return self.__model.evaluate_generator(self.__data.test_data(), steps)


class NetworkVGG16(Network):
    def __init__(self, setting, data):
        Network.__init__(self, setting, data)
        self.__weights = 'imagenet'
        self.__include_top = False
        self.__conv_base = VGG16(weights=self.__weights, include_top=self.__include_top, input_shape=self.__input_shape)
        self.__loss = 'categorical_crossentropy'
        self.__optimizer = optimizers.RMSprop(lr=1e-5)
        self.__metrics = ['acc']
        self.__model = models.Sequential()

    def create_model(self):
        self.__conv_base.trainable = True
        set_trainable = False
        for layer in self.__conv_base.layers:
            if layer.name == 'block4_conv1':
                set_trainable = True
            if set_trainable:
                layer.trainable = True
            else:
                layer.trainable = False
        self.__model.add(self.__conv_base)
        self.__model.add(layers.Flatten())
        self.__model.add(layers.Dense(4096, activation='relu'))
        self.__model.add(layers.Dense(self.__n_classes, activation='softmax'))
        self.__model.compile(loss=self.__loss, optimizer=self.__optimizer, metrics=self.__metrics)
        return self.__model


class NetworkXception(Network):
    def __init__(self, setting, data):
        Network.__init__(self, setting, data)
        self.__weights = 'imagenet'
        self.__include_top = False
        self.__conv_base = Xception(weights=self.__weights, include_top=self.__include_top, input_shape=self.__input_shape)
        self.__loss = 'categorical_crossentropy'
        self.__optimizer = optimizers.SGD(lr=.01, momentum=.9)
        self.__metrics = ['acc']
        self.__model = models.Sequential()

    def create_model(self):
        self.__conv_base.trainable = True
        self.__model.add(self.__conv_base)
        self.__model.add(layers.GlobalAveragePooling2D())
        self.__model.add(layers.Dense(1024, activation='relu'))
        self.__model.add(layers.Dense(self.__n_classes, activation='softmax'))
        self.__model.compile(loss=self.__loss, optimizer=self.__optimizer, metrics=self.__metrics)
        return self.__model


class NetworkVGGFromScratch(Network):
    def __init__(self, setting, data):
        Network.__init__(self, setting, data)
        self.__weights = None
        self.__include_top = False
        self.__conv_base = VGG16(weights=self.__weights, include_top=self.__include_top, input_shape=self.__input_shape)
        self.__loss = 'categorical_crossentropy'
        self.__optimizer = optimizers.SGD(lr=.01, momentum=.9)
        self.__metrics = ['acc']
        self.__model = models.Sequential()

    def create_model(self):
        self.__conv_base.trainable = True
        self.__model.add(self.__conv_base)
        self.__model.add(layers.GlobalAveragePooling2D())
        self.__model.add(layers.Dense(self.__n_classes, activation='softmax'))
        self.__model.compile(loss=self.__loss, optimizer=self.__optimizer, metrics=self.__metrics)
        return self.__model