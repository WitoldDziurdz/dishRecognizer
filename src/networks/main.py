from network_tools import utils as u
from keras.callbacks import CSVLogger, ModelCheckpoint
from network_tools.data import DataGenerator
from network_tools.networks import NetworkVGG16
from network_tools.architecture import Architecture
import network_tools.settings as settings

def main():
    # directories
    #base_dir = 'C:\data'
    base_dir = 'C:\\data\\101food'
    #base_dir = 'data'
    network_name = 'tmp_name'
    model_path = 'models/' + network_name + '/'
    # path_log = "C:\\praca_inzynierska\\dishRecognizer\\src\\models\\food101\\log.csv"
    path_log = model_path + "log.csv"
    # path_name = "C:\\praca_inzynierska\\dishRecognizer\\src\\models\\food101\\network_food11"
    path_name = "."

    u.create_dir(model_path)

    # data generate
    data = DataGenerator(base_dir, settings.input_x, settings.input_y)
    model = NetworkVGG16(settings.input_x, settings.input_y).create_model()
    Architecture(model).log(model_path)

    csv_logger = CSVLogger(path_log, append=True, separator=';')
    checkpointer = ModelCheckpoint(filepath=model_path + network_name + '.hdf5', verbose=1, save_best_only=True)

    history = model.fit_generator(
         data.train_generator,
         steps_per_epoch=3000,
         epochs=50,
         callbacks=[csv_logger, checkpointer],
         validation_data=data.validation_generator,
         validation_steps=250, workers=16)

    test_loss, test_acc = model.evaluate_generator(data.test_generator, steps=600)
    print('test acc:', test_acc)

    # save model, please check file name
    u.save_model(model, path_name, test_acc)

    # loss and accuracy visualization
    u.visualization_loss_and_accuracy(history=history)


if __name__ == "__main__":
    main()