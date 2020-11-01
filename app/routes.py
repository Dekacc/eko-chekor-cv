from typing import Optional
from evaluate_waste import evaluate_waste, calculate_score
from tensorflow.keras.preprocessing.image import load_img
import uvicorn
from datetime import time, datetime
from tensorflow.keras.applications.resnet import ResNet152
from tensorflow.keras.models import Model, load_model
import json
from fastapi import FastAPI, File, UploadFile, Body
from PIL import Image
import shutil
import urllib
import os
app = FastAPI()

folder_name = 'images/'


@app.get("/")
def home():
    return "home"




def download_image_from_url(url, folder_name):
    try:
        img_name = datetime.now().timestamp()
        img_name = os.path.join("img_" + str(img_name) + ".jpg")
        urllib.request.urlretrieve(url, folder_name + img_name)
        print("can")
        return img_name
    except:
        print("cant")


@app.post("/predict")
def predict_image(image_url: str):
    # image = Image.open(image)
    # result = evaluate_waste(image)
    # # result = None
    # return {"image": result}
    image_name = download_image_from_url(image_url, folder_name)

    img = load_img(folder_name + image_name, target_size=(224, 224))
    result = evaluate_waste(img, resnet_model, model)

    r = result[0]
    return {'result':calculate_score(r)}


if __name__ == '__main__':
    # Load ResNet152
    resnet_model = ResNet152()  # Load the model
    resnet_model = Model(inputs=resnet_model.inputs, outputs=resnet_model.layers[-2].output)  # Remove the output layer

    #Load trained model
    model = load_model('ResNet152_64hidden_63accuracy.h5')

    uvicorn.run(app, host='0.0.0.0', port=5000, loop='none')
