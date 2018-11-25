import matplotlib.pyplot as plt
import os


class Util:

    def visualization_loss_and_accuracy(self, history):
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

    def save_model(self, model, path_name, test_acc):
        model_json = model.to_json()
        file_name = path_name + "_" + str(test_acc);
        with open(file_name + ".json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        model.save_weights(file_name + ".h5")
        print("Saved model to disk")
        pass

    def list_layers(self, model):
        layers_list = []
        base_model_names = ['densenet', 'densenet121', 'densenet169', 'densenet201', 'inception_resnet_v2', 'inception_v3',
                            'NASNet', 'resnet50', 'vgg16', 'vgg19', 'xception', ]
        for layer in model.layers:
            if any(layer.name in s for s in base_model_names):
                for l in layer.layers:
                    layers_list.append(l.name + ' - ' +  'trainable: ' + str(l.trainable))
            else:
                layers_list.append(layer.name + ' - ' + 'trainable: ' + str(layer.trainable))
        model.layers_list = layers_list

    def create_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        else:
            print("directory already exists")