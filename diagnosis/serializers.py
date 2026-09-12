from rest_framework import serializers
from .models import Diagnosis, Disease
from .services import analyze_symptoms, ALL_SYMPTOMS


class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = '__all__'


class DiagnosisInputSerializer(serializers.Serializer):
    animal_type = serializers.CharField(max_length=50)
    age = serializers.FloatField(required=False, allow_null=True, min_value=0.0)
    gender = serializers.CharField(max_length=10, required=False, default='Female')
    symptoms = serializers.ListField(
        child=serializers.CharField(max_length=100),
        allow_empty=False,
        help_text="List of observed symptom names"
    )
    other_symptoms = serializers.CharField(
        required=False,
        allow_blank=True,
        default=""
    )

    def validate_animal_type(self, value):
        valid_animals = ['cow', 'buffalo', 'goat', 'sheep', 'pig', 'poultry']
        val_norm = value.strip().lower()
        if val_norm not in valid_animals:
            raise serializers.ValidationError(
                f"Invalid animal type '{value}'. Supported types are: {', '.join(valid_animals)}."
            )
        return val_norm

    def validate_symptoms(self, value):
        if not value:
            raise serializers.ValidationError("Please provide at least one symptom.")
        return value


class DiagnosisDetailSerializer(serializers.ModelSerializer):
    warning = serializers.SerializerMethodField()

    class Meta:
        model = Diagnosis
        fields = [
            'id',
            'animal_type',
            'age',
            'gender',
            'selected_symptoms',
            'other_symptoms',
            'predicted_disease',
            'confidence',
            'risk_level',
            'matched_symptoms',
            'recommendation',
            'warning',
            'created_at',
        ]

    def get_warning(self, obj):
        return (
            "This result is an AI/prototype-based preliminary screening and is NOT a confirmed diagnosis. "
            "Consult a qualified veterinarian before treatment or medication."
        )
