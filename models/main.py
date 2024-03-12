from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf

app = FastAPI()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/predict")
def predict(data: dict):
    model = tf.saved_model.load('models/model.pb')
    return model.predict(data)

@app.get("/")
def root():
    return {"greeting": "Hello"}
