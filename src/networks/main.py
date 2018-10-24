from network_tools import utils
from network_tools import network_models as m
from keras.callbacks import CSVLogger, ModelCheckpoint

def main():
    # directories
    #base_dir = 'C:\data'
    #base_dir = 'C:\\data\\101food'
    base_dir = 'data'

    # data generate
    data = utils.DataGenerator(base_dir)
    #data.set_food_nonfood_data()
    data.set_101_food_categorical()

    # model definition
    #model = m.get_conv_network()
    #model = m.get_conv_VGG16()
    #model = m.get_conv_food11_VGG16()
    #model = m.get_empty_VGG16()
    #model = m.get_conv_food101_NASNet()
    model = m.get_conv_food101_VGG16()

    # log, one log for many network
    #path_log = "C:\\praca_inzynierska\\dishRecognizer\\src\\models\\food101\\log.csv"
    path_log = "log.csv"
    csv_logger = CSVLogger(path_log, append=True, separator=';')
    
    checkpointer = ModelCheckpoint(filepath='model_VGG16.{epoch:02d}-{val_loss:.2f}.hdf5', verbose=1, save_best_only=True)

    # training
    history = model.fit_generator(
         data.train_generator,
         steps_per_epoch=2000,
         epochs=20,
         callbacks=[csv_logger, checkpointer],
         validation_data=data.validation_generator,
         validation_steps=300, workers=16)

    # evaluation
    test_loss, test_acc = model.evaluate_generator(data.test_generator, steps=100)
    print('test acc:', test_acc)

    # save model, please check file name
    #path_name = "C:\\praca_inzynierska\\dishRecognizer\\src\\models\\food101\\network_food11"
    path_name = "..\models\food101\network_food101"
    utils.save_model(model, path_name, test_acc)

    # loss and accuracy visualization
    utils.visualization_loss_and_accuracy(history=history)


if __name__ == "__main__":
    main()