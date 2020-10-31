from typing import Optional

import uvicorn
from fastapi import FastAPI, File, UploadFile, Body

app = FastAPI()

@app.post("/predict")
def read_item(image_url: str):
    return {"image": image_url}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5000, loop='none')