from network_tools import utils as u
from keras.callbacks import CSVLogger, ModelCheckpoint, LearningRateScheduler
from network_tools.data import DataGenerator
from network_tools.networks import NetworkVGG16, NetworkXception, NetworkVGGFromScratch
from network_tools.architecture import Architecture
import network_tools.settings as settings

def schedule(epoch):
    if epoch < 5:
        return 0.01
    if epoch < 10:
        return 0.02
    else:
        return 0.004


def main():
    # directories
    #base_dir = 'C:\\data\\101food'
    base_dir = 'data121'
    network_name = 'tmp_name'
    model_path = 'models/' + network_name + '/'
    path_log = model_path + "log.csv"
    path_name = "."

    u.create_dir(model_path)

    # data generate
    data = DataGenerator(base_dir, settings.input_x, settings.input_y)
    model = NetworkXception(settings.input_x, settings.input_y, settings.n_classes).create_model()
    Architecture(model).log(model_path)

    csv_logger = CSVLogger(path_log, append=True, separator=';')
    checkpointer = ModelCheckpoint(filepath=model_path + network_name + '.hdf5', verbose=1, save_best_only=True)
    lr_scheduler = LearningRateScheduler(schedule)

    history = model.fit_generator(
         data.train_generator,
         steps_per_epoch=700*settings.n_classes // data.batch_size,
         epochs=10,
         callbacks=[lr_scheduler, csv_logger, checkpointer],
         validation_data=data.validation_generator,
         validation_steps=150*settings.n_classes // data.batch_size, workers=16)

    test_loss, test_acc = model.evaluate_generator(data.test_generator, steps=600)
    print('test acc:', test_acc)

    # save model, please check file name
    u.save_model(model, path_name, test_acc)

    # loss and accuracy visualization
    u.visualization_loss_and_accuracy(history=history)


if __name__ == "__main__":
    main()