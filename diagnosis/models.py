from django.db import models


class Disease(models.Model):
    """
    Knowledge base model storing livestock diseases,
    applicable animal species, symptom weight maps, and recommended actions.
    """
    RISK_LEVEL_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]

    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    # List of animals, e.g. ["cow", "buffalo", "sheep", "goat"]
    animal_types = models.JSONField(
        default=list,
        help_text="List of animal types prone to this disease (lowercase)."
    )
    # Dictionary of symptoms with weights, e.g. {"fever": 1, "skin nodules": 3}
    symptoms = models.JSONField(
        default=dict,
        help_text="Mapping of symptom names (lowercase) to importance weights (e.g. 1-3)."
    )
    risk_level = models.CharField(
        max_length=20,
        choices=RISK_LEVEL_CHOICES,
        default='MEDIUM'
    )
    recommended_action = models.TextField(
        help_text="Immediate farmer guidance and veterinary consultation instructions."
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Disease Knowledge Record'
        verbose_name_plural = 'Disease Knowledge Base'

    def __str__(self):
        return f"{self.name} ({self.risk_level})"


class Diagnosis(models.Model):
    """
    Audit log of screening queries performed by farmers/users.
    """
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    animal_type = models.CharField(max_length=50)
    age = models.FloatField(null=True, blank=True, help_text="Age in years (optional)")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    selected_symptoms = models.JSONField(
        default=list,
        help_text="List of symptoms reported by the user."
    )
    other_symptoms = models.TextField(
        blank=True,
        null=True,
        help_text="Additional observations entered by the user."
    )
    predicted_disease = models.CharField(
        max_length=200,
        help_text="Most likely preliminary condition identified by the screening engine."
    )
    confidence = models.FloatField(
        help_text="Confidence percentage (0-100%)."
    )
    risk_level = models.CharField(
        max_length=20,
        help_text="Screening risk classification (LOW, MEDIUM, HIGH, CRITICAL)."
    )
    matched_symptoms = models.JSONField(
        default=list,
        blank=True,
        help_text="Symptoms from user selection that matched the predicted disease."
    )
    recommendation = models.TextField(
        help_text="Guidance provided to the user."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Diagnosis Record'
        verbose_name_plural = 'Diagnosis Records'

    def __str__(self):
        return f"{self.animal_type.title()} - {self.predicted_disease} ({self.confidence:.0f}%) - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
