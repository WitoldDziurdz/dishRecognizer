from keras import layers
from keras import models
import network_tools.utils

from keras import optimizers
from keras.optimizers import SGD
from keras.regularizers import l2
import network_tools.base_models as bm
import network_tools.settings as settings
from keras.applications import VGG16

def get_conv_IRS_V2():
    #conv_base = InceptionResNetV2(weights='imagenet',
    #                  include_top=False,
    #                  input_shape=(width, length, 3))
    
    conv_base = bm.get_InceptionResNetV2(include_weights=True, do_include_top=False)

    conv_base.trainable = False

    model = models.Sequential()
    model.add(conv_base)
    model.add(layers.Flatten())
    model.add(layers.Dense(4096, activation='relu'))
    model.add(layers.Dropout(rate=0.5))
    model.add(layers.Dense(4096, activation='relu'))
    model.add(layers.Dense(101, activation='softmax'))
    model.compile(loss='categorical_crossentropy',
                  optimizer=optimizers.RMSprop(lr=1e-4),
                  metrics=['acc'])
    network_tools.utils.list_layers(model)
    return model

def get_conv_InceptionV3():
    #conv_base = InceptionV3(weights='imagenet',
    #                 include_top=False,
    #                  input_shape=(150, 150, 3))


    conv_base = bm.get_InceptionV3(include_weights=True, do_include_top=False)

    model = models.Sequential()
    model.add(conv_base)
    model.add(layers.Flatten())
    model.add(layers.Dense(4096, activation='relu'))
    model.add(layers.Dropout(rate=0.2))
    model.add(layers.Dense(4096, activation='relu'))
    model.add(layers.Dense(101, activation='softmax'))
    
    
    model.summary()
    
    model.compile(loss='categorical_crossentropy',
                  optimizer=optimizers.RMSprop(lr=1e-5),
                  metrics=['acc'])
    return model

def get_conv_food101_NASNet():
    
    #conv_base = NASNetLarge(weights='imagenet',
    #                        include_top=False,
    #                        input_shape=(32, 32, 3))

    conv_base = bm.get_NASNetLarge(include_weights=True, do_include_top=True)

    model = models.Sequential()
    model.add(conv_base)
    model.add(layers.Flatten())
    model.add(layers.Dense(4096, activation='relu'))
    model.add(layers.Dense(101, activation='softmax'))
    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy',
                  optimizer=sgd,
                  metrics=['acc'])
    return model

def get_full_NASNetLarge():
    base_model = bm.get_NASNetLarge(include_weights=True, do_include_top=False)
    model = models.Sequential()
    model.add(base_model)
    model.add(layers.GlobalAveragePooling2D())
    model.add(layers.Dropout(rate=0.4))
    model.add(layers.Flatten())
    model.add(layers.Dense(settings.n_classes, init='glorot_uniform', W_regularizer=l2(.0005), activation='softmax'))
    opt = SGD(lr=.01, momentum=.9)
    model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
    
    return model

def get_full_inceptionv3():
    base_model = bm.get_InceptionV3(include_weights=True, do_include_top=False)
    model = models.Sequential()
    model.add(base_model)
    model.add(layers.GlobalAveragePooling2D())
    model.add(layers.Dropout(rate=0.4))
    model.add(layers.Flatten())
    model.add(layers.Dense(settings.n_classes, init='glorot_uniform', W_regularizer=l2(.0005), activation='softmax'))
    opt = SGD(lr=.01, momentum=.9)
    model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])

def get_conv_food101_VGG16():
    conv_base = VGG16(weights='imagenet',
                      include_top=False,
                      input_shape=(150, 150, 3))

    conv_base.trainable = True
    set_trainable = False
    for layer in conv_base.layers:
        if layer.name == 'block4_conv1':
            set_trainable = True
        if set_trainable:
            layer.trainable = True
        else:
            layer.trainable = False

    model = models.Sequential()
    model.add(conv_base)
    model.add(layers.Flatten())
    model.add(layers.Dense(4096, activation='relu'))
    model.add(layers.Dense(101, activation='softmax'))
    model.compile(loss='categorical_crossentropy',
                  optimizer=optimizers.RMSprop(lr=1e-5),
                  metrics=['acc'])
    return model


if __name__ == "__main__":
    get_conv_food101_VGG16().summary()