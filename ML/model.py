import tensorflow as tf
from tensorflow import keras
import numpy as np
import cv2
import os
CLASSES    = ["straight", "textured"]
IMG_SIZE   = 224
MODEL_PATH = os.path.join(os.path.dirname(__file__),"models","hair_mobilenetv3.keras")


model = keras.models.load_model(MODEL_PATH)

def detect_hair_texture(image) -> dict:
   
    img = cv2.imread(image)
    if img is None:
        return {"error": "Could not read image"}

    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))   
    img = img / 255.0                             
    img = np.expand_dims(img, axis=0)             # add batch dim: (224,224,3) → (1,224,224,3)

    # Run prediction
    preds = model.predict(img, verbose=0)   
    probs = preds[0]                       

    idx        = int(np.argmax(probs))     
    hair_type  = CLASSES[idx]
    confidence = round(float(probs[idx]), 2)

    return {
        "hair_texture": hair_type,
        "confidence":   confidence,
        
    }