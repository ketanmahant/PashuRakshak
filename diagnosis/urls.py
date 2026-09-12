from django.urls import path
from . import views

urlpatterns = [
    # Web UI Routes
    path('', views.home_view, name='home'),
    path('result/<int:pk>/', views.result_view, name='result'),
    path('history/', views.history_view, name='history'),
    path('history/<int:pk>/', views.detail_view, name='detail'),
    path('about/', views.about_view, name='about'),

    # REST API Routes
    path('api/diagnose/', views.DiagnoseAPIView.as_view(), name='api_diagnose'),
    path('api/diagnoses/', views.DiagnosisListAPIView.as_view(), name='api_diagnosis_list'),
    path('api/diagnoses/<int:pk>/', views.DiagnosisDetailAPIView.as_view(), name='api_diagnosis_detail'),
    path('api/diseases/', views.DiseaseListAPIView.as_view(), name='api_disease_list'),
]
