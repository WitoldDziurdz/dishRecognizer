from keras import layers
from keras import models
from keras import optimizers
from keras.applications import VGG16
from keras.applications import NASNetLarge
from keras.optimizers import SGD

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
    model.add(layers.Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer=optimizers.RMSprop(lr=1e-4), metrics=['acc'])
    return model

def get_conv_VGG16():
    conv_base = VGG16(weights='imagenet',
                      include_top=False,
                      input_shape=(150, 150, 3))

    conv_base.trainable = True
    set_trainable = False
    for layer in conv_base.layers:
        if layer.name == 'block5_conv1':
            set_trainable = True
        if set_trainable:
            layer.trainable = True
        else:
            layer.trainable = False

    model = models.Sequential()
    model.add(conv_base)
    model.add(layers.Flatten())
    model.add(layers.Dense(256, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy',
                  optimizer=optimizers.RMSprop(lr=1e-5),
                  metrics=['acc'])
    return model

def get_conv_food101_VGG16():
    conv_base = VGG16(weights='imagenet',
                      include_top=False,
                      input_shape=(150, 150, 3))

    conv_base.summary()

    #conv_base.trainable = True
    conv_base.trainable = False
    #set_trainable = False
    #for layer in conv_base.layers:
    #    if layer.name == 'block4_conv1':
    #        set_trainable = True
    #    if set_trainable:
    #        layer.trainable = True
    #    else:
    #        layer.trainable = False

    for layer in conv_base.layers:
        layer.set_trainable = False
      
    conv_base.summary()

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

def get_conv_food101_NASNet():
    
    conv_base = NASNetLarge(weights='imagenet',
                            include_top=False,
                            input_shape=(150, 150, 3))

    model = models.Sequential()
    model.add(conv_base)
    model.add(layers.Flatten())
    model.add(layers.Dense(4096, activation='relu'))
    model.add(layers.Dropout(rate=0.2))
    model.add(layers.Dense(101, activation='softmax'))
    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy',
                  optimizer=sgd,
                  metrics=['acc'])
    return model

def get_empty_VGG16():
    conv_base = VGG16(weights='imagenet',
                      include_top=False,
                      input_shape=(150, 150, 3))
    
    for layer in conv_base.layers:
        layer.trainable = True
        
    model = models.Sequential()
    model.add(conv_base)
    model.add(layers.Flatten())
    model.add(layers.Dense(4096, activation='relu'))
    model.add(layers.Dense(101, activation='softmax'))
    
    model.compile(loss='categorical_crossentropy',
                  optimizer=optimizers.RMSprop(lr=1e-5),
                  metrics=['acc'])
    return model
    


def get_conv_food11_VGG16():
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