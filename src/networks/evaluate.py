from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator

model = load_model('model.hdf5')

test_datagen = ImageDataGenerator(rescale=1. / 255)


test_generator = test_datagen.flow_from_directory(
            'data121/evaluation',
            target_size=(256, 256),
            batch_size=32,
            class_mode='categorical')

label_map = test_generator.class_indices
print(label_map)
scores = model.evaluate_generator(test_generator)


print("Loss = ", scores[0])
print("Accuracy = ", scores[1])
print(model.metrics_names)
