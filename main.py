from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

app = FastAPI()
model = joblib.load('model.pkl')

class PredictRequest(BaseModel):
    country: str
    confirmed: int
    lat: float
    lon: float
    date: str

@app.post("/predict")
def predict(data: PredictRequest):
    # Парсим дату и признаки
    date = pd.to_datetime(data.date)
    features = np.array([
        [data.lat, data.lon, data.confirmed, date.dayofweek, date.month]
    ])
    pred = model.predict(features)[0]
    return {
        "country": data.country,
        "date": data.date,
        "predicted_new_cases": float(pred)
    }

