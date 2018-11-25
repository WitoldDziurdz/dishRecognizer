from keras import layers
from keras import models
from keras import optimizers
from keras.applications import VGG16, Xception


class Network:
    def __init__(self, setting, data):
        self.input_x = setting.input_x
        self.input_y = setting.input_y
        self.input_z = setting.input_z
        self.n_classes = setting.n_classes
        self.input_shape = (self.input_x, self.input_y, self.input_z)
        self.model = models.Sequential()
        self.data = data

    def fit(self, epochs, callbacks):
        history = self.model.fit_generator(
            self.data.train_generator,
            steps_per_epoch=5 * self.n_classes // self.data.batch_size,
            epochs=epochs,
            callbacks=callbacks,
            validation_data=self.data.validation_generator,
            validation_steps=5 * self.n_classes // self.data.batch_size, workers=16)
        return history

    def evaluate(self, steps):
        return self.model.evaluate_generator(self.data.test_generator, steps)


class NetworkVGG16(Network):
    def __init__(self, setting, data):
        Network.__init__(self, setting, data)
        self.weights = 'imagenet'
        self.include_top = False
        self.conv_base = VGG16(weights=self.weights, include_top=self.include_top, input_shape=self.input_shape)
        self.loss = 'categorical_crossentropy'
        self.optimizer = optimizers.RMSprop(lr=1e-5)
        self.metrics = ['acc']
        self.model = models.Sequential()

    def create_model(self):
        self.conv_base.trainable = True
        set_trainable = False
        for layer in self.conv_base.layers:
            if layer.name == 'block4_conv1':
                set_trainable = True
            if set_trainable:
                layer.trainable = True
            else:
                layer.trainable = False
        self.model.add(self.conv_base)
        self.model.add(layers.Flatten())
        self.model.add(layers.Dense(4096, activation='relu'))
        self.model.add(layers.Dense(self.n_classes, activation='softmax'))
        self.model.compile(loss=self.loss, optimizer=self.optimizer, metrics=self.metrics)
        return self.model


class NetworkXception(Network):
    def __init__(self, setting, data):
        Network.__init__(self, setting, data)
        self.weights = 'imagenet'
        self.include_top = False
        self.conv_base = Xception(weights=self.weights, include_top=self.include_top, input_shape=self.input_shape)
        self.loss = 'categorical_crossentropy'
        self.optimizer = optimizers.SGD(lr=.01, momentum=.9)
        self.metrics = ['acc']
        self.model = models.Sequential()

    def create_model(self):
        self.conv_base.trainable = True
        self.model.add(self.conv_base)
        self.model.add(layers.GlobalAveragePooling2D())
        self.model.add(layers.Dense(1024, activation='relu'))
        self.model.add(layers.Dense(self.n_classes, activation='softmax'))
        self.model.compile(loss=self.loss, optimizer=self.optimizer, metrics=self.metrics)
        return self.model


class NetworkVGGFromScratch(Network):
    def __init__(self, setting, data):
        Network.__init__(self, setting, data)
        self.weights = None
        self.include_top = False
        self.conv_base = VGG16(weights=self.weights, include_top=self.include_top, input_shape=self.input_shape)
        self.loss = 'categorical_crossentropy'
        self.optimizer = optimizers.SGD(lr=.01, momentum=.9)
        self.metrics = ['acc']
        self.model = models.Sequential()

    def create_model(self):
        self.conv_base.trainable = True
        self.model.add(self.conv_base)
        self.model.add(layers.GlobalAveragePooling2D())
        self.model.add(layers.Dense(self.n_classes, activation='softmax'))
        self.model.compile(loss=self.loss, optimizer=self.optimizer, metrics=self.metrics)
        return self.model