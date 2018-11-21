from keras import layers
from keras import models
from keras import optimizers
from keras.applications import VGG16


class Network:
    def __init__(self, input_x, input_y, n_classes):
        self.input_x = input_x
        self.input_y = input_y
        self.input_z = 3
        self.n_classes = n_classes
        self.input_shape = (self.input_x, self.input_y, self.input_z)


class NetworkVGG16(Network):
    def __init__(self, input_x, input_y, n_classes):
        Network.__init__(self, input_x, input_y, n_classes)
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