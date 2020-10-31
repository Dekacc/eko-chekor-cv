from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.resnet import preprocess_input
from tensorflow.keras.applications.resnet import ResNet152
from tensorflow.keras.models import Model, load_model


def evaluate_waste(image):
    # The image should be loaded with resolution (224, 224) using the load_img function from tensorflow.keras.preprocessing.image
    # Example: image = load_img(image_path, target_size=(224, 224))

    # Preprocess the image
    image = img_to_array(image)  # Convert the image pixels to a numpy array
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))  # reshape data for the model
    image = preprocess_input(image)  # prepare the image for the ResNet50 model

    # Load ResNet152
    model = ResNet152()                                                     # Load the model
    model = Model(inputs=model.inputs, outputs=model.layers[-2].output)     # Remove the output layer
    image_features = model.predict(image)                                   # Get image features for the image

    # Load the waste model
    model = load_model('ResNet152_64hidden_63accuracy.h5')

    # Return a prediction
    return model.predict(image_features)


if __name__ == "__main__":
    # Example usage
    image = load_img('images/img_0_0.jpg', target_size=(224, 224))
    print(evaluate_waste(image))