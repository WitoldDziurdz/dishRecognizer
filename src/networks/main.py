from network_tools.utils import Util
from keras.callbacks import CSVLogger, ModelCheckpoint, LearningRateScheduler
from network_tools.data import DataGenerator
from network_tools.networks import NetworkVGG16, NetworkXception, NetworkVGGFromScratch
from network_tools.architecture import Architecture
from network_tools.settings import Setting

class Teacher:
    def __init__(self):
        self.base_dir = 'C:\\data\\101food'
        # self.base_dir = 'data121'
        self.network_name = 'tmp_name'
        self.model_path = 'models/' + self.network_name + '/'
        self.path_log = self.model_path + "log.csv"
        self.path_name = "."

    def schedule(self, epoch):
        if epoch < 5:
            return 0.01
        if epoch < 10:
            return 0.02
        else:
            return 0.004

    def get_callbacks(self):
        csv_logger = CSVLogger(self.path_log, append=True, separator=';')
        checkpointer = ModelCheckpoint(filepath=self.model_path + self.network_name + '.hdf5', verbose=1, save_best_only=True)
        lr_scheduler = LearningRateScheduler(self.schedule)
        return [lr_scheduler, csv_logger, checkpointer]

    def start(self):
        # create util
        util = Util()
        util.create_dir(self.model_path)

        # create settings
        setting = Setting()

        # data generate
        data = DataGenerator(self.base_dir, setting)

        # create network and get model
        network = NetworkXception(setting, data)
        model = network.create_model()

        # create util for model, logging
        architecture = Architecture(model, self.model_path)
        architecture.log()

        # create callbacks
        callbacks = self.get_callbacks()

        # train and validation
        history = network.fit(epochs=10, callbacks=callbacks)

        # test
        test_loss, test_acc = network.evaluate(steps=600)
        print('test acc:', test_acc)

        # save model, please check file name
        util.save_model(model, self.path_name, test_acc)

        # loss and accuracy visualization
        util.visualization_loss_and_accuracy(history=history)


if __name__ == "__main__":
    teacher = Teacher()
    teacher.start()