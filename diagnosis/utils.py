from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .models import Disease

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


def normalize_symptom_name(name: str) -> str:
    """Normalize symptom text before comparing it with risk rules."""
    return str(name).strip().lower()


def evaluate_risk_level(
    selected_symptoms: List[str],
    matched_disease: Optional["Disease"] = None,
    confidence: float = 0.0,
    has_critical_symptom: bool = False,
) -> str:
    """Return a risk level based on emergency signs, disease risk, and symptoms."""
    normalized_selected = {normalize_symptom_name(symptom) for symptom in selected_symptoms}

    if any(symptom in CRITICAL_SYMPTOMS for symptom in normalized_selected) or has_critical_symptom:
        return "CRITICAL"

    matched_symptom_count = 0
    if matched_disease:
        disease_symptoms = {
            normalize_symptom_name(symptom)
            for symptom in matched_disease.symptoms
        }
        matched_symptom_count = len(normalized_selected & disease_symptoms)

    if matched_disease and confidence >= 50.0 and matched_symptom_count >= 2:
        if matched_disease.risk_level == "CRITICAL":
            return "CRITICAL"
        if matched_disease.risk_level == "HIGH":
            return "HIGH"

    high_alert_count = sum(
        symptom in HIGH_ALERT_SYMPTOMS for symptom in normalized_selected
    )
    total_count = len(normalized_selected)

    if total_count >= 4 or high_alert_count >= 2:
        return "HIGH"
    if total_count >= 2 or high_alert_count >= 1:
        return "MEDIUM"
    return "LOW"