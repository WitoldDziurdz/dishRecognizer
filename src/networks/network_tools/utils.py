import matplotlib.pyplot as plt
import os


class Util:

    @staticmethod
    def visualization_loss_and_accuracy(history, model_path):
        acc = history.history['acc']
        val_acc = history.history['val_acc']
        loss = history.history['loss']
        val_loss = history.history['val_loss']
        epochs = range(1, len(acc) + 1)
        accuracy_figure = plt.figure()
        plt.plot(epochs, acc, 'bo', label='Training acc')
        plt.plot(epochs, val_acc, 'b', label='Validation acc')
        plt.title('Training and validation accuracy')
        plt.legend()
        accuracy_figure.savefig(model_path + 'accuracy.png')
        loss_figure = plt.figure()
        plt.plot(epochs, loss, 'bo', label='Training loss')
        plt.plot(epochs, val_loss, 'b', label='Validation loss')
        plt.title('Training and validation loss')
        plt.legend()
        loss_figure.savefig(model_path + 'loss.png')
        #plt.show()
        pass

    @staticmethod
    def save_model(model, path_name, test_acc):
        model_json = model.to_json()
        file_name = path_name + "_" + str(test_acc);
        with open(file_name + ".json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        model.save_weights(file_name + ".h5")
        print("Saved model to disk")
        pass

    @staticmethod
    def create_dir(path):
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            print("directory already exists")