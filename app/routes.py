from typing import Optional
from evaluate_waste import evaluate_waste
from tensorflow.keras.preprocessing.image import load_img
import uvicorn
from tensorflow.keras.applications.resnet import ResNet152
from tensorflow.keras.models import Model, load_model

from fastapi import FastAPI, File, UploadFile, Body
from PIL import Image
import shutil

app = FastAPI()

folder_name = 'images/'


@app.get("/")
def home():
    return "home"


@app.post("/predict")
def predict_image(image: UploadFile = File(...)):
    # image = Image.open(image)
    # result = evaluate_waste(image)
    # # result = None
    # return {"image": result}
    file_name = image.filename
    with open(folder_name + file_name, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    img = load_img(folder_name + file_name, target_size=(224, 224))
    result = evaluate_waste(img, resnet_model, model)
    print(result)
    return "hi"


if __name__ == '__main__':
    # Load ResNet152
    resnet_model = ResNet152()  # Load the model
    resnet_model = Model(inputs=resnet_model.inputs, outputs=resnet_model.layers[-2].output)  # Remove the output layer

    #Load trained model
    model = load_model('ResNet152_64hidden_63accuracy.h5')

    uvicorn.run(app, host='0.0.0.0', port=5000, loop='none')
