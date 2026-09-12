from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

from .models import Diagnosis, Disease
from .forms import HealthScreeningForm
from .services import analyze_symptoms, ALL_SYMPTOMS
from .serializers import (
    DiagnosisInputSerializer,
    DiagnosisDetailSerializer,
    DiseaseSerializer,
)


# =====================================================================
# Web Views (HTML Templates)
# =====================================================================

def home_view(request):
    """
    Farmer-friendly homepage to enter animal information and observe symptoms.
    """
    if request.method == 'POST':
        form = HealthScreeningForm(request.POST)
        if form.is_valid():
            animal_type = form.cleaned_data['animal_type']
            age = form.cleaned_data.get('age')
            gender = form.cleaned_data['gender']
            symptoms = form.cleaned_data.get('symptoms', [])
            other_symptoms = form.cleaned_data.get('other_symptoms', '')

            # Execute rule-based screening analysis
            analysis = analyze_symptoms(
                animal_type=animal_type,
                selected_symptoms=symptoms,
                other_symptoms=other_symptoms
            )

            # Persist diagnosis record for audit and history
            diagnosis = Diagnosis.objects.create(
                animal_type=animal_type,
                age=age,
                gender=gender,
                selected_symptoms=symptoms,
                other_symptoms=other_symptoms,
                predicted_disease=analysis['predicted_disease'],
                confidence=analysis['confidence'],
                risk_level=analysis['risk_level'],
                matched_symptoms=analysis['matched_symptoms'],
                recommendation=analysis['recommendation'],
            )

            return redirect('result', pk=diagnosis.pk)
        else:
            messages.error(
                request,
                "Please correct the errors below and select at least one observed symptom."
            )
    else:
        form = HealthScreeningForm()

    return render(request, 'diagnosis/home.html', {
        'form': form,
        'all_symptoms': ALL_SYMPTOMS,
    })


def result_view(request, pk):
    """
    Displays the health screening result, risk level, confidence score,
    matched symptoms, and safety warnings.
    """
    diagnosis = get_object_or_404(Diagnosis, pk=pk)

    # Contextual color mappings
    risk_colors = {
        'LOW': {'badge': 'bg-success', 'border': 'border-success', 'text': 'text-success'},
        'MEDIUM': {'badge': 'bg-warning text-dark', 'border': 'border-warning', 'text': 'text-warning'},
        'HIGH': {'badge': 'bg-danger', 'border': 'border-danger', 'text': 'text-danger'},
        'CRITICAL': {'badge': 'bg-dark text-white', 'border': 'border-danger', 'text': 'text-danger'},
    }

    color_scheme = risk_colors.get(diagnosis.risk_level, risk_colors['MEDIUM'])

    return render(request, 'diagnosis/result.html', {
        'diagnosis': diagnosis,
        'color_scheme': color_scheme,
    })


def history_view(request):
    """
    Shows audit table of previous livestock screenings.
    """
    screenings = Diagnosis.objects.all()
    return render(request, 'diagnosis/history.html', {
        'screenings': screenings,
    })


def detail_view(request, pk):
    """
    Alias or direct view for past screening details.
    """
    return result_view(request, pk)


def about_view(request):
    """
    Explains the PashuRakshak screening philosophy, workflow, and prototype status.
    """
    total_diseases = Disease.objects.count()
    return render(request, 'diagnosis/about.html', {
        'total_diseases': total_diseases,
    })


# =====================================================================
# REST API Views
# =====================================================================

class DiagnoseAPIView(APIView):
    """
    POST /api/diagnose/
    Submit animal symptoms and receive preliminary screening prediction.
    """
    def post(self, request, *args, **kwargs):
        serializer = DiagnosisInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        animal_type = data['animal_type']
        age = data.get('age')
        gender = data.get('gender', 'Female')
        symptoms = data['symptoms']
        other_symptoms = data.get('other_symptoms', '')

        analysis = analyze_symptoms(
            animal_type=animal_type,
            selected_symptoms=symptoms,
            other_symptoms=other_symptoms
        )

        diagnosis = Diagnosis.objects.create(
            animal_type=animal_type,
            age=age,
            gender=gender,
            selected_symptoms=symptoms,
            other_symptoms=other_symptoms,
            predicted_disease=analysis['predicted_disease'],
            confidence=analysis['confidence'],
            risk_level=analysis['risk_level'],
            matched_symptoms=analysis['matched_symptoms'],
            recommendation=analysis['recommendation'],
        )

        return Response({
            "id": diagnosis.id,
            "animal_type": diagnosis.animal_type,
            "predicted_disease": diagnosis.predicted_disease,
            "confidence": diagnosis.confidence,
            "risk_level": diagnosis.risk_level,
            "matched_symptoms": diagnosis.matched_symptoms,
            "recommendation": diagnosis.recommendation,
            "warning": "This result is an AI/prototype preliminary screening and is NOT a confirmed diagnosis. Consult a qualified veterinarian before treatment.",
            "created_at": diagnosis.created_at,
        }, status=status.HTTP_201_CREATED)


class DiagnosisListAPIView(generics.ListAPIView):
    """
    GET /api/diagnoses/
    List all recorded screenings.
    """
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisDetailSerializer


class DiagnosisDetailAPIView(generics.RetrieveAPIView):
    """
    GET /api/diagnoses/<id>/
    Retrieve a specific diagnosis record by ID.
    """
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisDetailSerializer
    lookup_field = 'pk'


class DiseaseListAPIView(generics.ListAPIView):
    """
    GET /api/diseases/
    Optional helper endpoint to inspect the prototype disease knowledge base.
    """
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
