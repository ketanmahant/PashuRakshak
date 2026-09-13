from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Disease, Diagnosis
from .services import analyze_symptoms
from .management.commands.seed_diseases import Command as SeedCommand


class SymptomPredictionServiceTests(TestCase):
    def setUp(self):
        # Seed the database before tests
        seed = SeedCommand()
        seed.handle()

    def test_lumpy_skin_disease_matching(self):
        """Test that the trained model returns a usable cattle prediction."""
        symptoms = ["fever", "skin nodules", "swelling", "loss of appetite"]
        result = analyze_symptoms(animal_type="cow", selected_symptoms=symptoms)

        self.assertTrue(result["predicted_disease"])
        self.assertGreaterEqual(result["confidence"], 0.0)
        self.assertIn(result["risk_level"], ["LOW", "MEDIUM", "HIGH", "CRITICAL"])
        self.assertIn("skin nodules", [s.lower() for s in result["matched_symptoms"]])

    def test_mastitis_matching(self):
        """Test that a dairy-cow screening returns a trained-model result."""
        symptoms = ["swelling", "reduced milk production", "fever"]
        result = analyze_symptoms(animal_type="cow", selected_symptoms=symptoms)

        self.assertTrue(result["predicted_disease"])
        self.assertGreaterEqual(result["confidence"], 0.0)
        self.assertIn("reduced milk production", [s.lower() for s in result["matched_symptoms"]])

    def test_risk_level_changes_with_symptom_severity(self):
        self.assertEqual(analyze_symptoms("cow", ["loss of appetite"])["risk_level"], "LOW")
        self.assertEqual(
            analyze_symptoms("cow", ["fever", "diarrhea", "vomiting", "skin nodules"])["risk_level"],
            "HIGH",
        )

    def test_anthrax_critical_emergency_risk(self):
        """Test emergency escalation for life-threatening Anthrax signs."""
        symptoms = ["sudden death", "bleeding", "bloody stool", "fever"]
        result = analyze_symptoms(animal_type="cow", selected_symptoms=symptoms)

        self.assertEqual(result["predicted_disease"], "Anthrax")
        self.assertEqual(result["risk_level"], "CRITICAL")
        self.assertTrue(result["is_urgent"])
        self.assertIn("URGENT", result["recommendation"])

    def test_empty_symptoms_fallback(self):
        """Test graceful handling when no symptoms are provided."""
        result = analyze_symptoms(animal_type="cow", selected_symptoms=[])
        self.assertEqual(result["confidence"], 0.0)
        self.assertEqual(result["risk_level"], "LOW")


class WebViewsTests(TestCase):
    def setUp(self):
        SeedCommand().handle()
        self.client = Client()

    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "PashuRakshak")
        self.assertContains(response, "Check Animal Health")

    def test_home_page_submission_redirects_to_result(self):
        payload = {
            'animal_type': 'cow',
            'age': '3.0',
            'gender': 'Female',
            'symptoms': ['Fever', 'Skin nodules', 'Swelling'],
            'other_symptoms': 'Slight lethargy noted this morning',
        }
        response = self.client.post(reverse('home'), data=payload)
        self.assertEqual(response.status_code, 302)

        # Follow redirect to result page
        redirect_url = response.url
        result_resp = self.client.get(redirect_url)
        self.assertEqual(result_resp.status_code, 200)
        self.assertContains(result_resp, "Preliminary")
        self.assertContains(result_resp, "Preliminary Health Assessment")

    def test_history_page_loads(self):
        # Create a sample diagnosis record
        Diagnosis.objects.create(
            animal_type="buffalo",
            age=4.0,
            gender="Female",
            selected_symptoms=["Fever", "Excessive salivation"],
            predicted_disease="Foot and Mouth Disease (FMD)",
            confidence=75.0,
            risk_level="HIGH",
            matched_symptoms=["Fever", "Excessive salivation"],
            recommendation="Quarantine the animal.",
        )
        response = self.client.get(reverse('history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Foot and Mouth Disease")
        self.assertContains(response, "Buffalo")

    def test_about_page_loads(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "What is PashuRakshak?")


class DiagnosisAPITests(APITestCase):
    def setUp(self):
        SeedCommand().handle()

    def test_api_diagnose_post_success(self):
        """Test POST /api/diagnose/ endpoint with valid payload."""
        url = reverse('api_diagnose')
        payload = {
            "animal_type": "cow",
            "age": 4,
            "gender": "Female",
            "symptoms": [
                "fever",
                "skin nodules",
                "swelling",
                "loss of appetite"
            ],
            "other_symptoms": "Nodules appeared on neck yesterday"
        }
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertTrue(data["predicted_disease"])
        self.assertIn("confidence", data)
        self.assertIn("risk_level", data)
        self.assertIn("matched_symptoms", data)
        self.assertIn("warning", data)

    def test_api_diagnose_invalid_animal(self):
        """Test validation error on unsupported animal."""
        url = reverse('api_diagnose')
        payload = {
            "animal_type": "elephant",
            "symptoms": ["fever"]
        }
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_diagnoses_list(self):
        """Test GET /api/diagnoses/ endpoint."""
        Diagnosis.objects.create(
            animal_type="goat",
            age=2.0,
            gender="Male",
            selected_symptoms=["Diarrhea", "Fever"],
            predicted_disease="Peste des Petits Ruminants (PPR)",
            confidence=68.0,
            risk_level="HIGH",
            matched_symptoms=["Diarrhea", "Fever"],
            recommendation="Isolate goat.",
        )
        url = reverse('api_diagnosis_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertGreaterEqual(len(data), 1)
