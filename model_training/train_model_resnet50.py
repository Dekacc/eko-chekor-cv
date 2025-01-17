import pandas as pd
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from utilities import split_dataset, one_hot_encode
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.resnet import preprocess_input
from tensorflow.keras.applications.resnet import ResNet152
from tensorflow.keras.models import Model
from tensorflow.keras import regularizers
from tensorflow.keras import callbacks
from os import path


INPUT_SIZE = (224, 224)
NUM_FEATURES = 2048


if __name__ == "__main__":
    # Load the dataset
    df = pd.read_csv('dataset.csv')
    df = df[df['img_name'].notna()]
    df = df.sample(frac=1, random_state=1)      # Shuffle the dataset
    images_list = []
    classes_list = []
    for index, row in df.iterrows():
        image_path = path.join('images', row['img_name'])

        image = load_img(image_path, target_size=INPUT_SIZE)                                        # Load the image
        image = img_to_array(image)                                      # Convert the image pixels to a numpy array
        image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))      # reshape data for the model
        image = preprocess_input(image)                                   # prepare the image for the ResNet50 model

        images_list.append(image)
        classes_list.append(one_hot_encode(row['trash_size']))

    images_array = np.concatenate(images_list)
    classes_array = np.array(classes_list)

    # Get image features with ResNet50
    model = ResNet152()                                                      # Load the model
    model = Model(inputs=model.inputs, outputs=model.layers[-2].output)     # Remove the output layer
    image_features = model.predict(images_array)

    # Split the dataset 80%/10%/10%
    train_x, val_x, test_x = split_dataset(image_features)
    train_y, val_y, test_y = split_dataset(classes_array)

    # GRIDSEARCH
    for hidden in [64]:
        for batch in [16]:
            for lr in [0.0001]:
                # Build a simple dense network
                inputs = keras.Input(shape=(NUM_FEATURES,))
                x = layers.Dense(hidden, activation="relu")(inputs)
                outputs = layers.Dense(4, activation='softmax')(x)

                model = keras.Model(inputs=inputs, outputs=outputs, name="simple_dense_model")

                # Train the network
                model.compile(
                    loss=keras.losses.CategoricalCrossentropy(from_logits=True),
                    optimizer=keras.optimizers.Adam(learning_rate=lr,),
                    metrics=["accuracy"],
                )

                history = model.fit(x=train_x,
                                    y=train_y,
                                    batch_size=batch,
                                    epochs=50,
                                    validation_data=(val_x, val_y),
                                    callbacks=[callbacks.EarlyStopping(monitor='val_accuracy',
                                                                       patience=10,
                                                                       restore_best_weights=True)])
                print(lr, hidden, batch, max(history.history['val_accuracy']))

                model.save('ResNet152_64hidden.h5')
                #
                # test_scores = model.evaluate(x_test, y_test, verbose=2)