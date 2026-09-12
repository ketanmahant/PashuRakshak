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


# List of symptoms that automatically trigger high/critical alerts
CRITICAL_SYMPTOMS = {
    "sudden death",
    "difficulty breathing",
    "bleeding",
    "bloody stool",
}

HIGH_ALERT_SYMPTOMS = {
    "high fever",
    "fever",
    "vomiting",
    "severe diarrhea",
    "diarrhea",
    "skin nodules",
    "mouth lesions",
    "swelling",
    "excessive salivation",
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


def normalize_symptom_name(name: str) -> str:
    """Normalize symptom string to lowercase stripped form."""
    return name.strip().lower()


def evaluate_risk_level(
    selected_symptoms: List[str],
    matched_disease: Disease = None,
    confidence: float = 0.0,
    has_critical_symptom: bool = False
) -> str:
    """
    Classify the overall risk level into LOW, MEDIUM, HIGH, or CRITICAL
    based on symptom severity, symptom count, and disease severity.
    """
    normalized_selected = {normalize_symptom_name(s) for s in selected_symptoms}

    # 1. Check for life-threatening / emergency symptoms
    if any(s in normalized_selected for s in CRITICAL_SYMPTOMS) or has_critical_symptom:
        return "CRITICAL"

    # 2. Check disease's own risk profile if confidence is strong
    if matched_disease and confidence >= 50.0:
        if matched_disease.risk_level == "CRITICAL":
            return "CRITICAL"
        if matched_disease.risk_level == "HIGH":
            return "HIGH"

    # 3. Check for high alert symptoms
    high_alert_count = sum(1 for s in normalized_selected if s in HIGH_ALERT_SYMPTOMS)
    total_count = len(normalized_selected)

    if total_count >= 4 or high_alert_count >= 2:
        return "HIGH"
    elif total_count >= 2 or high_alert_count >= 1:
        return "MEDIUM"
    else:
        return "LOW"


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


def analyze_symptoms(
    animal_type: str,
    selected_symptoms: List[str],
    other_symptoms: str = ""
) -> Dict[str, Any]:
    """
    Analyze observed symptoms against the Disease knowledge base.

    Scoring formula:
        score = (sum of weights of matched symptoms) / (total weights in disease profile)
        confidence = score * 100 (scaled and adjusted based on match proportion)

    Returns:
        dict containing:
            - predicted_disease (str)
            - confidence (float)
            - confidence_label (str)
            - risk_level (str)
            - matched_symptoms (list of str)
            - recommendation (str)
            - is_urgent (bool)
            - disease_description (str)
    """
    animal_type_norm = animal_type.strip().lower()
    user_symptoms_norm = {normalize_symptom_name(s) for s in selected_symptoms if s}

    if not user_symptoms_norm:
        return {
            "predicted_disease": "Inconclusive / No symptoms selected",
            "confidence": 0.0,
            "confidence_label": "No confidence",
            "risk_level": "LOW",
            "matched_symptoms": [],
            "recommendation": "Please select at least one symptom to perform a health screening.",
            "is_urgent": False,
            "disease_description": "",
        }

    # Fetch candidate diseases from database
    # Filter by animal_type if applicable, or include all if animal_types list is empty
    all_diseases = Disease.objects.all()
    candidate_diseases = []

    for d in all_diseases:
        applicable_animals = [a.strip().lower() for a in (d.animal_types or [])]
        if not applicable_animals or animal_type_norm in applicable_animals:
            candidate_diseases.append(d)

    # Fallback to all diseases if none specifically tagged for this animal
    if not candidate_diseases:
        candidate_diseases = list(all_diseases)

    best_disease = None
    best_score = 0.0
    best_matched_symptoms = []

    for disease in candidate_diseases:
        disease_symptoms: Dict[str, int] = disease.symptoms or {}
        if not disease_symptoms:
            continue

        total_weight = sum(disease_symptoms.values())
        if total_weight <= 0:
            total_weight = len(disease_symptoms)

        matched_weight = 0
        matched_list = []

        for sym_name, weight in disease_symptoms.items():
            norm_sym = normalize_symptom_name(sym_name)
            if norm_sym in user_symptoms_norm:
                matched_weight += weight
                # Preserve a title-cased display version
                matched_list.append(sym_name.title())

        if total_weight > 0 and matched_weight > 0:
            # Ratio of matched weighted symptoms to total disease symptoms
            raw_ratio = matched_weight / total_weight

            # Bonus factor for high fraction of user's symptoms explained by this disease
            user_coverage = len(matched_list) / max(len(user_symptoms_norm), 1)
            composite_score = (raw_ratio * 0.7) + (user_coverage * 0.3)

            if composite_score > best_score:
                best_score = composite_score
                best_disease = disease
                best_matched_symptoms = matched_list

    # Check for critical symptoms present in input
    has_critical_symptom = any(s in user_symptoms_norm for s in CRITICAL_SYMPTOMS)

    if best_disease is None or best_score <= 0.0:
        # No disease in database matched any symptom
        risk_level = "CRITICAL" if has_critical_symptom else evaluate_risk_level(list(user_symptoms_norm))
        recommendation = (
            "No specific disease in the knowledge base strongly matched the reported symptoms. "
            "However, if the animal is visibly uncomfortable, not eating, or exhibiting abnormal behavior, "
            "please consult a qualified local veterinarian immediately."
        )
        if has_critical_symptom:
            recommendation = "URGENT: Critical symptoms detected. Contact a qualified veterinarian immediately."

        return {
            "predicted_disease": "Unspecified / General Malaise",
            "confidence": 15.0 if user_symptoms_norm else 0.0,
            "confidence_label": "Low confidence",
            "risk_level": risk_level,
            "matched_symptoms": [],
            "recommendation": recommendation,
            "is_urgent": has_critical_symptom,
            "disease_description": "The symptoms reported do not strongly correspond to a single specific condition in the prototype knowledge base.",
        }

    # Convert best score to percentage (capped between 20% and 95% for MVP realism)
    # Raw ratio can range up to 1.0; let's map it smoothly
    calculated_confidence = min(round(best_score * 100, 1), 95.0)
    # Ensure minimum non-zero confidence when at least 1 symptom matched
    if calculated_confidence < 25.0 and best_matched_symptoms:
        calculated_confidence = 28.0

    risk_level = evaluate_risk_level(
        selected_symptoms=list(user_symptoms_norm),
        matched_disease=best_disease,
        confidence=calculated_confidence,
        has_critical_symptom=has_critical_symptom,
    )

    is_urgent = (risk_level == "CRITICAL")

    # Build actionable recommendations
    base_rec = best_disease.recommended_action
    if is_urgent:
        recommendation = f"URGENT: Contact a qualified veterinarian immediately. {base_rec}"
    else:
        recommendation = f"{base_rec} Isolate the animal if infectious symptoms are present and arrange for veterinary confirmation."

    return {
        "predicted_disease": best_disease.name,
        "confidence": calculated_confidence,
        "confidence_label": get_confidence_category(calculated_confidence),
        "risk_level": risk_level,
        "matched_symptoms": best_matched_symptoms,
        "recommendation": recommendation,
        "is_urgent": is_urgent,
        "disease_description": best_disease.description,
    }
