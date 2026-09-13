import os
import joblib
import numpy as np
import pandas as pd
from django.conf import settings

# Path to the saved models
MODEL_DIR = os.path.join(settings.BASE_DIR, 'diagnosis', 'ml_models')

# Load once at import time (efficient)
model = joblib.load(os.path.join(MODEL_DIR, 'livestock_disease_model.pkl'))
le_animal = joblib.load(os.path.join(MODEL_DIR, 'animal_encoder.pkl'))
le_disease = joblib.load(os.path.join(MODEL_DIR, 'disease_encoder.pkl'))
symptom_vocabulary = joblib.load(os.path.join(MODEL_DIR, 'symptom_vocabulary.pkl'))
training_defaults = joblib.load(os.path.join(MODEL_DIR, 'training_defaults.pkl'))

symptom_features = [f"symptom_{s.replace(' ', '_')}" for s in symptom_vocabulary]
feature_columns = ['Animal_encoded', 'Age', 'Temperature'] + symptom_features


def predict_disease_ml(animal: str, symptoms: list, age=None, temperature=None):
    """
    Returns: (disease_name, confidence_percent)
    """
    animal_name = str(animal).strip().lower()

    if animal_name not in le_animal.classes_:
        raise ValueError(f"Unknown animal '{animal}'. Available: {list(le_animal.classes_)}")

    # Normalize symptoms
    if isinstance(symptoms, str):
        symptoms = [s.strip() for s in symptoms.split(',') if s.strip()]
    normalized_symptoms = [str(s).strip().lower() for s in symptoms]

    # Map the farmer-facing symptom labels to the vocabulary used by the
    # trained model. Unsupported labels are ignored below.
    symptom_map = {
        "fever": "chills",
        "loss of appetite": "loss of appetite",
        "lameness": "lameness",
        "swelling": "swelling in muscle",
        "skin nodules": "painless lumps",
        "weakness": "depression",
        "coughing": "shortness of breath",
        "difficulty breathing": "shortness of breath",
        "abdominal pain": "swelling in abdomen",
        "dehydration": "fatigue",
        "skin lesions": "painless lumps",
    }
    mapped = []
    for s in normalized_symptoms:
        mapped.append(symptom_map.get(s, s))
    normalized_symptoms = mapped

    unknown = sorted(set(normalized_symptoms) - set(symptom_vocabulary))
    if unknown:
        # You can choose to ignore unknown symptoms or raise
        # For production, better to ignore unknowns than crash
        normalized_symptoms = [s for s in normalized_symptoms if s in symptom_vocabulary]

    if not normalized_symptoms:
        raise ValueError("No usable symptoms after mapping.")

    # Build feature vector
    input_values = {
        'Animal_encoded': le_animal.transform([animal_name])[0],
        'Age': training_defaults['age'] if age is None else float(age),
        'Temperature': training_defaults['temperature'] if temperature is None else float(temperature),
    }

    for feature in symptom_features:
        input_values[feature] = 0

    for symptom in normalized_symptoms:
        key = f"symptom_{symptom.replace(' ', '_')}"
        if key in input_values:
            input_values[key] = 1

    input_data = pd.DataFrame([input_values])[feature_columns]

    pred_encoded = model.predict(input_data)[0]
    disease_name = le_disease.inverse_transform([pred_encoded])[0]
    display_names = {
        "anthrax": "Anthrax",
        "blackleg": "Black Quarter (BQ)",
        "foot and mouth": "Foot and Mouth Disease (FMD)",
        "lumpy virus": "Lumpy Skin Disease",
        "pneumonia": "Pneumonia",
    }
    disease_name = display_names.get(str(disease_name).lower(), str(disease_name).title())
    probabilities = model.predict_proba(input_data)[0]
    confidence = round(float(np.max(probabilities)) * 100, 2)

    return disease_name, confidence