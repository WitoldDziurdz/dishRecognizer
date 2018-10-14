from src.networks.network_tools import utils
from src.networks.network_tools import network_models as m

def main():
    # direcotires
    #base_dir = 'C:\data'
    base_dir = 'C:\\data\\11food'
    data = utils.DataGenerator(base_dir)
    #data.set_food_nonfood_data()
    data.set_11_food_categorical()
    # model definition
    #model = m.get_conv_network()
    #model = m.get_conv_VGG16()
    model = m.get_conv_food11_VGG16()

    #training
    history = model.fit_generator(
         data.train_generator,
         steps_per_epoch=200,
         epochs=60,
         validation_data=data.validation_generator,
         validation_steps=10, workers=16)

    # evaluation
    test_loss, test_acc = model.evaluate_generator(data.test_generator, steps=50)
    print('test acc:', test_acc)

    # loss and accuracy visualization
    utils.visualization_loss_and_accuracy(history=history)


if __name__ == "__main__":
    main()