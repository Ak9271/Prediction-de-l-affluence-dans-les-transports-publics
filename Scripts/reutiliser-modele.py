import tensorflow as tf
import joblib

# Charger modèle + le scaler
model = tf.keras.models.load_model("mlp_affluence_final.keras")
scaler = joblib.load("scaler_mlp.pkl")

# pré-traiter  donnée nouvelle
X_new = scaler.transform(...)  #utilise scaler !!!!!!!!!!!!!!!!!

#Prédire
prediction = model.predict(X_new)