from network_tools import utils
from network_tools import network_models as m

from keras.callbacks import ModelCheckpoint

def main():
    # direcotires
    #base_dir = 'C:\data'
    base_dir = 'data'
    data = utils.DataGenerator(base_dir)
    data.set_11_food_categorical()
    # model definition
    #model = m.get_conv_network()
    #model = m.get_conv_VGG16()
    #model = m.get_conv_food101_VGG16()
    model = m.get_conv_food101_inception_v3()

    # Callback for saving model to file
    checkpointer = ModelCheckpoint(filepath='model4.{epoch:02d}-{val_loss:.2f}.hdf5', verbose=1, save_best_only=True)

    #training
    #data.set_food_nonfood_data()
    history = model.fit_generator(
         data.train_generator,
         steps_per_epoch=400,
         epochs=60,
         validation_data=data.validation_generator,
         validation_steps=10, workers=16,
         callbacks=[checkpointer])

    # evaluation
    test_loss, test_acc = model.evaluate_generator(data.test_generator, steps=50)
    print('test acc:', test_acc)

    # loss and accuracy visualization
    utils.visualization_loss_and_accuracy(history=history)


if __name__ == "__main__":
    main()