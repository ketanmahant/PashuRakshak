from django.contrib import admin
from .models import Disease, Diagnosis


@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'risk_level', 'get_animal_types_display', 'get_symptom_count')
    list_filter = ('risk_level',)
    search_fields = ('name', 'description')
    ordering = ('name',)

    def get_animal_types_display(self, obj):
        if isinstance(obj.animal_types, list):
            return ", ".join(a.title() for a in obj.animal_types)
        return str(obj.animal_types)
    get_animal_types_display.short_description = "Susceptible Animals"

    def get_symptom_count(self, obj):
        if isinstance(obj.symptoms, dict):
            return len(obj.symptoms)
        return 0
    get_symptom_count.short_description = "Tracked Symptoms"


@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'animal_type',
        'predicted_disease',
        'confidence_display',
        'risk_level_badge',
    )
    list_filter = ('risk_level', 'animal_type', 'created_at')
    search_fields = ('animal_type', 'predicted_disease', 'selected_symptoms')
    readonly_fields = (
        'created_at',
        'predicted_disease',
        'confidence',
        'risk_level',
        'matched_symptoms',
        'recommendation',
    )
    ordering = ('-created_at',)

    def confidence_display(self, obj):
        return f"{obj.confidence:.1f}%"
    confidence_display.short_description = "Confidence"

    def risk_level_badge(self, obj):
        return obj.risk_level
    risk_level_badge.short_description = "Risk Level"
