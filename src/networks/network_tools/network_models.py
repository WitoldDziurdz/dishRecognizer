from keras import layers
from keras import models
import network_tools.utils

from keras import optimizers
from keras.optimizers import SGD
from keras.regularizers import l2
import network_tools.base_models as bm
import network_tools.settings as settings

def get_conv_network():
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
    model.add(layers.Dense(101, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer=optimizers.RMSprop(lr=0.001), metrics=['acc'])
    return model

# 95 dla food/nonfood
def get_conv_network2():
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)))
    model.add(layers.BatchNormalization(axis=-1))
    model.add(layers.MaxPooling2D(pool_size=(3, 3)))
    model.add(layers.Dropout(0.25))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.BatchNormalization(axis=-1))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.BatchNormalization(axis=-1))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(layers.Dropout(0.25))
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.BatchNormalization(axis=-1))
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.BatchNormalization(axis=-1))
    model.add(layers.Dropout(0.25))
    model.add(layers.Flatten())
    model.add(layers.Dense(512, activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(1, activation='sigmoid'))
    
    model.compile(loss='binary_crossentropy', optimizer=optimizers.RMSprop(lr=1e-4), metrics=['acc'])
    
    return model

# mysle, ze dojdzie do 98 dla food/non-food
def get_conv_VGG16():
    #conv_base = VGG16(weights='imagenet',
    #                  include_top=False,
    #                  input_shape=(150, 150, 3))
    
    conv_base = bm.get_VGG16(include_weights=True, do_include_top=False)

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
    model.add(layers.Dense(1024, activation='relu'))
    model.add(layers.Dropout(rate=0.3))
    model.add(layers.Dense(1024, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy',
                  optimizer=optimizers.RMSprop(lr=1e-5),
                  metrics=['acc'])
    return model

# mysle, ze dojdzie do 99 dla food/nonfood
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

def get_conv_food101_VGG16():
    conv_base = bm.get_InceptionResNetV2(include_weights=True, do_include_top=False)

    conv_base.summary()

    #conv_base.trainable = True
    conv_base.trainable = False
    set_trainable = False
    for layer in conv_base.layers:
        if layer.name == 'block4_conv1':
            set_trainable = True
        if set_trainable:
            layer.trainable = True
        else:
            layer.trainable = False

    #for layer in conv_base.layers:
    #    layer.set_trainable = False
      
    #conv_base.summary()

    model = models.Sequential()
    model.add(conv_base)
    model.add(layers.Flatten())
    model.add(layers.Dense(4096, activation='relu'))
    model.add(layers.Dropout(rate=0.2))
    model.add(layers.Dense(4096, activation='relu'))
    model.add(layers.Dense(101, activation='softmax'))
    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    
    model.summary()
    
    model.compile(loss='categorical_crossentropy',
                  optimizer=optimizers.RMSprop(lr=1e-5),
                  metrics=['acc'])
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

# scores 66
def get_empty_VGG16():
    conv_base = bm.get_InceptionV3(include_weights=True, do_include_top=False)
        
    model = models.Sequential()
    model.add(conv_base)
    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(1, activation='softmax'))
    
    model.compile(loss='binary_crossentropy',
                  optimizer=optimizers.RMSprop(lr=1e-5),
                  metrics=['acc'])
    return model

def get_conv_food11_VGG16():
    #conv_base = VGG16(weights='imagenet',
    #                 include_top=False,
    #                 input_shape=(150, 150, 3))

    conv_base = bm.get_VGG16(include_weights=True, do_include_top=False)

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
    model.add(layers.Dropout(rate=0.3))
    model.add(layers.Dense(1024, activation='relu'))
    model.add(layers.Dense(11, activation='softmax'))
    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    adagrad = optimizers.Adagrad(lr=0.00001, epsilon=None, decay=0.0)
    model.compile(loss='categorical_crossentropy',
                  optimizer=optimizers.RMSprop(lr=1e-5),
                  metrics=['acc'])
    return model

if __name__ == "__main__":
    get_conv_food101_VGG16().summary()