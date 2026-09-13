"""
diagnosis/services.py

Modular business logic and disease screening service for PashuRakshak.
Contains symptom scoring, weighted matching, risk classification, and
veterinary guidance generation.

Designed so that the rule/weight-based scoring engine can seamlessly be
extended or swapped with an ML model or Bayesian classifier in future versions.
"""

from typing import List, Dict, Any, Tuple
from .models import Disease
from .ml_predictor import predict_disease_ml
from .utils import evaluate_risk_level



# List of symptoms that automatically trigger high/critical alerts
CRITICAL_SYMPTOMS = {
    "sudden death",
    "difficulty breathing",
    "bleeding",
    "bloody stool",
}

# Standard list of all supported symptoms for UI & validation
ALL_SYMPTOMS = [
    "Fever",
    "Loss of appetite",
    "Weakness",
    "Coughing",
    "Difficulty breathing",
    "Nasal discharge",
    "Eye discharge",
    "Diarrhea",
    "Vomiting",
    "Skin lesions",
    "Skin nodules",
    "Swelling",
    "Lameness",
    "Excessive salivation",
    "Mouth lesions",
    "Reduced milk production",
    "Weight loss",
    "Abdominal pain",
    "Dehydration",
    "Bloody stool",
    "Bleeding",
    "Sudden death",
]

def get_confidence_category(confidence: float) -> str:
    """Categorize confidence score into human-readable label."""
    if confidence >= 81.0:
        return "Very high confidence"
    elif confidence >= 61.0:
        return "High confidence"
    elif confidence >= 31.0:
        return "Moderate confidence"
    else:
        return "Low confidence"

def analyze_symptoms(animal_type: str, selected_symptoms: List[str], other_symptoms: str = "", age: int = None, temperature: float = None): # type: ignore
    """
    Predict using the bundled trained model and fall back safely if it cannot
    produce a prediction.
    """
    if not selected_symptoms and not other_symptoms.strip():
        return {
            "predicted_disease": "No symptoms provided",
            "confidence": 0.0,
            "confidence_label": "Low confidence",
            "risk_level": "LOW",
            "matched_symptoms": [],
            "recommendation": "Please record at least one observed symptom and consult a qualified veterinarian if the animal appears unwell.",
            "is_urgent": False,
            "disease_description": "",
        }

    try:
        disease_name, confidence = predict_disease_ml(
            animal=animal_type,
            symptoms=selected_symptoms,
            age=age,
            temperature=temperature
        )
    except Exception as e:
        fallback_risk = evaluate_risk_level(selected_symptoms=selected_symptoms)
        return {
            "predicted_disease": "Unable to predict (model error)",
            "confidence": 0.0,
            "confidence_label": "Error",
            "risk_level": fallback_risk,
            "matched_symptoms": selected_symptoms,
            "recommendation": f"Please consult a veterinarian. Technical note: {str(e)}",
            "is_urgent": False,
            "disease_description": "",
        }

    # Try to enrich with knowledge-base info if the disease exists
    matched_disease = Disease.objects.filter(name__icontains=disease_name).first()

    risk_level = "MEDIUM"
    recommendation = (
        matched_disease.recommended_action
        if matched_disease
        else "Please consult a qualified veterinarian for confirmation and treatment."
    )

    has_critical = any(
        str(symptom).strip().lower() in {
            "sudden death",
            "difficulty breathing",
            "bleeding",
            "bloody stool",
        }
        for symptom in selected_symptoms
    )
    risk_level = evaluate_risk_level(
        selected_symptoms=selected_symptoms,
        matched_disease=matched_disease,
        confidence=confidence,
        has_critical_symptom=has_critical,
    )
    if risk_level == "CRITICAL":
        recommendation = "URGENT: Contact a veterinarian immediately. " + recommendation

    return {
        "predicted_disease": disease_name,
        "confidence": confidence,
        "confidence_label": "High" if confidence >= 70 else "Medium" if confidence >= 40 else "Low",
        "risk_level": risk_level,
        "matched_symptoms": selected_symptoms,
        "recommendation": recommendation,
        "is_urgent": risk_level == "CRITICAL",
        "disease_description": matched_disease.description if matched_disease else "",
    }