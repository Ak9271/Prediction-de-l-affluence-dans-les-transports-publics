# YBoost Data B2

## Projet
Prédiction de l'affluence dans les transports publics à l'aide d'un modèle de machine learning multi-couche (MLP) et d'une API FastAPI.

## Structure du projet

- `Api-devops/`
  - `Dockerfile` : construction du conteneur Docker pour l'API.
  - `main.py` : application FastAPI qui charge le modèle et expose un endpoint `/predict`.
  - `requirements.txt` : dépendances Python nécessaires pour l'API.
- `Datas Netoyes/`
  - `frequentation-gares.csv`
  - `H_75_latest-2025-2026.csv`
  - `trimestre1.csv`
  - `trimestre2.csv`
  - `trimestre3.csv`
  - `trimestre4.csv`
- `Resultats-Machine Learning/`
  - `Données normalisation/`
    - `Role données normalisation.txt`
    - `scaler_mlp.pkl` : scaler utilisé pour normaliser les données avant prédiction.
  - `Graphique Analyse/`
    - `mlp_1_learning_curves.png`
    - `mlp_2_pred_vs_reel.png`
    - `mlp_3_residus.png`
    - `mlp_4_cross_validation.png`
    - `Roles Graphiques.txt`
  - `Modèles Entrainés/`
    - `best_mlp.keras`
    - `mlp_affluence_final.keras` : modèle chargé par l'API.
    - `Roles des fichier.txt`
- `Scripts/`
  - `Machine_Learning.ipynb` : notebook d'analyse et d'entraînement.
  - `reutiliser-modele.py` : script de réutilisation du modèle entraîné.
- `Sujet-Yboost_B2 25-26.pdf` : document du sujet du projet.

## Description détaillée

Ce projet vise à prédire l'affluence dans les transports publics en utilisant des variables temporelles, météorologiques et de catégorisation d'arrêts.
L'API FastAPI prend en entrée des caractéristiques pré-calculées, normalise les données avec le scaler sauvegardé, puis renvoie une prédiction de l'affluence.

## Installation et utilisation

### En local avec Python

1. Installer Python 3.11+ ou compatible.
2. Ouvrir un terminal à la racine du projet.
3. Installer les dépendances :
   ```bash
   cd Api-devops
   python -m pip install -r requirements.txt
   ```
4. Lancer l'API :
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
5. Ouvrir dans le navigateur :
   - `http://localhost:8000`
   - `http://localhost:8000/docs` pour la documentation Swagger

### Avec Docker

1. Construire l'image :
   ```bash
   docker build --no-cache -f Api-devops/Dockerfile -t api-mlp .
   ```
2. Lancer le conteneur :
   ```bash
   docker run -p 8000:8000 api-mlp
   ```
3. Ouvrir l'API :
   - `http://localhost:8000`
   - `http://localhost:8000/docs`

### Dashboard Streamlit

Pour lancer le dashboard :
```bash
streamlit run app.py
```

Le dashboard s'ouvrira automatiquement dans le navigateur (généralement sur `http://localhost:8501`).

## Endpoint principal

- `GET /` : vérifie que l'API fonctionne.
- `POST /predict` : reçoit les entrées de prédiction et renvoie la valeur estimée.

### Exemple de requête JSON

```json
{
  "heure_sin": 0.5,
  "heure_cos": 0.8,
  "mois_sin": 0.2,
  "mois_cos": 0.9,
  "js_sin": 0.1,
  "js_cos": 0.3,
  "Temperature": 18,
  "Pluie_1h": 0,
  "il_pleut": 0,
  "pluie_intense": 0,
  "est_weekend": 1,
  "est_vacances": 0,
  "cat_jour_enc": 2,
  "arret_enc": 15
}
```

## Notes

- Le modèle utilisé par l'API est `Resultats-Machine Learning/Modèles Entrainés/mlp_affluence_final.keras`.
- Le scaler de normalisation est `Resultats-Machine Learning/Données normalisation/scaler_mlp.pkl`.
- Les fichiers CSV de `Datas Netoyes/` contiennent les données nettoyées utilisées pour l'analyse et l'entraînement.

# Prediction-de-l-affluence-dans-les-transports-publics
