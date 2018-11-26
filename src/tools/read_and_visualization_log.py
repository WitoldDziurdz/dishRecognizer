import matplotlib.pyplot as plt
import csv

def visualization_loss_and_accuracy(history):
    acc = history['acc']
    val_acc = history['val_acc']
    loss = history['loss']
    val_loss = history['val_loss']
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


def csv_dict_reader(file_obj):
    reader = csv.DictReader(file_obj, delimiter=';')
    history = {}
    history['acc'] = []
    history['val_acc'] = []
    history['loss'] = []
    history['val_loss'] = []
    for line in reader:
        history['acc'].append(float(line['acc']))
        history['val_acc'].append(float(line['val_acc']))
        history['loss'].append(float(line['loss']))
        history['val_loss'].append(float(line['val_loss']))
    return history


def main(path_name):
    with open(path_name) as f_obj:
        dict = csv_dict_reader(f_obj)
    visualization_loss_and_accuracy(dict)


if __name__ == "__main__":
    path_name = "C:\\xception_witek\\log.csv"
    main(path_name)