from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib
from tensorflow.keras.models import load_model

app = FastAPI()

MODEL_PATH = "../Resultats-Machine Learning/Modèles Entrainés/mlp_affluence_final.keras"
SCALER_PATH = "../Resultats-Machine Learning/Données normalisation/scaler_mlp.pkl"
LE_CAT_PATH = "../Resultats-Machine Learning/Données normalisation/le_cat.pkl"
LE_ARRT_PATH = "../Resultats-Machine Learning/Données normalisation/le_arrt.pkl"

model = load_model(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
le_cat = joblib.load(LE_CAT_PATH)
le_arrt = joblib.load(LE_ARRT_PATH)

class PredictionInput(BaseModel):
    heure: int
    mois: int
    jour_semaine: int
    Temperature: float
    Pluie_1h: float
    est_vacances: int
    cat_jour: str
    arret: str

@app.get("/")
def root():
    return {"message": "API MLP op"}

@app.post("/predict")
def predict(data: PredictionInput):
    heure_sin = np.sin(2 * np.pi * data.heure / 24)
    heure_cos = np.cos(2 * np.pi * data.heure / 24)

    mois_sin = np.sin(2 * np.pi * data.mois / 12)
    mois_cos = np.cos(2 * np.pi * data.mois / 12)

    js_sin = np.sin(2 * np.pi * data.jour_semaine / 7)
    js_cos = np.cos(2 * np.pi * data.jour_semaine / 7)

    il_pleut = int(data.Pluie_1h > 0)
    pluie_intense = int(data.Pluie_1h > 2)
    est_weekend = int(data.jour_semaine in [5, 6])

    cat_jour_enc = le_cat.transform([data.cat_jour])[0]
    arret_enc = le_arrt.transform([data.arret])[0]

    values = np.array([[
        heure_sin,
        heure_cos,
        mois_sin,
        mois_cos,
        js_sin,
        js_cos,
        data.Temperature,
        data.Pluie_1h,
        il_pleut,
        pluie_intense,
        est_weekend,
        data.est_vacances,
        cat_jour_enc,
        arret_enc
    ]])

    values_scaled = scaler.transform(values)
    prediction = model.predict(values_scaled)

    return {"prediction": float(prediction[0][0])}