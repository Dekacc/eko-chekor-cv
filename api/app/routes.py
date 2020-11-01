from typing import Optional
from evaluate_waste import evaluate_waste, calculate_score
from tensorflow.keras.preprocessing.image import load_img
import uvicorn
from datetime import time, datetime
from tensorflow.keras.applications.xception import Xception
from tensorflow.keras.models import Model, load_model
import json
from fastapi import FastAPI, File, UploadFile, Body
from PIL import Image
import shutil
import urllib
import os
from pydantic import BaseModel

app = FastAPI()

folder_name = 'images/'


@app.get("/")
def home():
    return "home"

class Image(BaseModel):
    image_url: str


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
def predict_image(image: Image):
    image_name = download_image_from_url(image.image_url, folder_name)

    img = load_img(folder_name + image_name, target_size=(299, 299))
    result = evaluate_waste(img, feature_model, model)

    r = result[0]
    return {'result':calculate_score(r)}


if __name__ == '__main__':
    # Load ResNet152
    feature_model = Xception()  # Load the model
    feature_model = Model(inputs=feature_model.inputs,
                          outputs=feature_model.layers[-2].output)  # Remove the output layer

    # Load trained model
    model = load_model('Xception_100-100.h5')

    uvicorn.run(app, host='0.0.0.0', port=5000, loop='none')
