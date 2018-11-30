from network_tools.utils import Util
from keras.callbacks import CSVLogger, ModelCheckpoint, LearningRateScheduler
from network_tools.data import DataGenerator
from network_tools.networks import NetworkVGG16, NetworkXception, NetworkVGGFromScratch
from network_tools.architecture import Architecture
from network_tools.settings import Setting

class Teacher:
    def __init__(self):
        # self.__base_dir = 'C:\\data\\101food'
        self.__base_dir = 'data121'
        self.__network_name = 'NetworkVGG16_witek'
        self.__model_path = 'models/' + self.__network_name + '/'
        self.__path_log = self.__model_path + "log.csv"
        self.__path_name = "."

    def __schedule(self, epoch):
        if epoch < 5:
            return 0.01
        if epoch < 10:
            return 0.02
        else:
            return 0.004

    def __schedule_fine_tune(self, epoch):
        if epoch < 5:
            return 0.0008
        if epoch < 10:
            return 0.00016
        else:
            return 0.000032

    def __get_callbacks(self):
        csv_logger = CSVLogger(self.__path_log, append=True, separator=';')
        checkpointer = ModelCheckpoint(filepath=self.__model_path + self.__network_name + '.hdf5', verbose=1, save_best_only=True)
        lr_scheduler = LearningRateScheduler(self.__schedule)
        return [lr_scheduler, csv_logger, checkpointer]

    def start(self):
        # create util
        Util.create_dir(self.__model_path)

        # create settings
        setting = Setting()

        # data generate
        data = DataGenerator(self.__base_dir, setting)

        # create network and get model
        network = NetworkVGG16(setting, data)
        model = network.create_model()

        # create util for model, logging
        architecture = Architecture(model, self.__model_path)
        architecture.log()

        # create callbacks
        callbacks = self.__get_callbacks()

        # train and validation
        history = network.fit(epochs=30, callbacks=callbacks)

        # test
        test_loss, test_acc = network.evaluate(steps=600)
        print('test acc:', test_acc)

        # save model, please check file name
        Util.save_model(model, self.__path_name, test_acc)

        # loss and accuracy visualization
        Util.visualization_loss_and_accuracy(history=history, model_path=self.__model_path)


if __name__ == "__main__":
    teacher = Teacher()
    teacher.start()