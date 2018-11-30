from keras import layers
from keras import models
from keras import optimizers
from keras.applications import VGG16, Xception, InceptionV3, InceptionResNetV2


class Network:
    def __init__(self, setting, data):
        self.__input_x = setting.input_x
        self.__input_y = setting.input_y
        self.__input_z = setting.input_z
        self._n_classes = setting.n_classes
        self._input_shape = (self.__input_x, self.__input_y, self.__input_z)
        self._model = models.Sequential()
        self._data = data
        self._metrics = ['acc']

    def fit(self, epochs, callbacks):
        history = self._model.fit_generator(
            self._data.train_data(),
            steps_per_epoch=700 * self._n_classes // self._data.batch_size(),
            epochs=epochs,
            callbacks=callbacks,
            validation_data=self._data.validate_data(),
            validation_steps=150 * self._n_classes // self._data.batch_size(), workers=16)
        return history

    def evaluate(self, steps):
        return self._model.evaluate_generator(self._data.test_data(), steps)


class NetworkVGG16(Network):
    def __init__(self, setting, data):
        Network.__init__(self, setting, data)
        self.__weights = 'imagenet'
        self.__include_top = False
        self.__conv_base = VGG16(weights=self.__weights, include_top=self.__include_top, input_shape=self._input_shape)
        self.__loss = 'categorical_crossentropy'
        self.__optimizer = optimizers.RMSprop(lr=1e-5)

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
        self._model.add(self.__conv_base)
        self._model.add(layers.Flatten())
        self._model.add(layers.Dense(4096, activation='relu'))
        self._model.add(layers.Dense(self._n_classes, activation='softmax'))
        self._model.compile(loss=self.__loss, optimizer=self.__optimizer, metrics=self._metrics)
        return self._model


class NetworkXception(Network):
    def __init__(self, setting, data):
        Network.__init__(self, setting, data)
        self.__weights = 'imagenet'
        self.__include_top = False
        self.__conv_base = Xception(weights=self.__weights, include_top=self.__include_top, input_shape=self._input_shape)
        self.__loss = 'categorical_crossentropy'
        self.__optimizer = optimizers.Adagrad(lr=0.01, epsilon=None, decay=0.0)

    def create_model(self):
        self.__conv_base.trainable = True
        self._model.add(self.__conv_base)
        self._model.add(layers.GlobalAveragePooling2D())
        self._model.add(layers.Dense(self._n_classes, activation='softmax'))
        self._model.compile(loss=self.__loss, optimizer=self.__optimizer, metrics=self._metrics)
        return self._model


class NetworkVGGFromScratch(Network):
    def __init__(self, setting, data):
        Network.__init__(self, setting, data)
        self.__weights = None
        self.__include_top = False
        self.__conv_base = VGG16(weights=self.__weights, include_top=self.__include_top, input_shape=self._input_shape)
        self.__loss = 'categorical_crossentropy'
        self.__optimizer = optimizers.SGD(lr=.01, momentum=.9)

    def create_model(self):
        self.__conv_base.trainable = True
        self._model.add(self.__conv_base)
        self._model.add(layers.GlobalAveragePooling2D())
        self._model.add(layers.Dense(self._n_classes, activation='softmax'))
        self._model.compile(loss=self.__loss, optimizer=self.__optimizer, metrics=self._metrics)
        return self._model

class NetworkInceptionV3(Network):
    def __init__(self, setting, data):
        Network.__init__(self, setting, data)
        self.__weights = 'imagenet'
        self.__include_top = False
        self.__conv_base = InceptionV3(weights=self.__weights, include_top=self.__include_top, input_shape=self._input_shape)
        self.__loss = 'categorical_crossentropy'
        self.__optimizer = optimizers.SGD(lr=.01, momentum=.9)

    def create_model(self):
        self.__conv_base.trainable = True
        self._model.add(self.__conv_base)
        self._model.add(layers.GlobalAveragePooling2D())
        self._model.add(layers.Dense(self._n_classes, activation='softmax'))
        self._model.compile(loss=self.__loss, optimizer=self.__optimizer, metrics=self._metrics)
        return self._model

class NetworkInceptionResNetV2(Network):
    def __init__(self, setting, data):
        Network.__init__(self, setting, data)
        self.__weights = 'imagenet'
        self.__include_top = False
        self.__conv_base = InceptionResNetV2(weights=self.__weights, include_top=self.__include_top, input_shape=self._input_shape)
        self.__loss = 'categorical_crossentropy'
        self.__optimizer = optimizers.SGD(lr=.01, momentum=.9)

    def create_model(self):
        self.__conv_base.trainable = True
        self._model.add(self.__conv_base)
        self._model.add(layers.GlobalAveragePooling2D())
        self._model.add(layers.Dense(self._n_classes, activation='softmax'))
        self._model.compile(loss=self.__loss, optimizer=self.__optimizer, metrics=self._metrics)
        return self._model