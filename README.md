# 🐄 PashuRakshak (पशुरक्षक)
### Early Symptom-Based Livestock Health Screening Assistant

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/django-5.x-green.svg)](https://www.djangoproject.com/)
[![DRF Version](https://img.shields.io/badge/django--rest--framework-3.15%2B-red.svg)](https://www.django-rest-framework.org/)
[![Bootstrap](https://img.shields.io/badge/bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**PashuRakshak** is a beginner-friendly, early symptom-based livestock disease screening and advisory web platform and REST API. Built specifically for farmers, livestock caretakers, and rural para-vets, it provides timely preliminary health assessments for cattle, buffaloes, goats, and sheep to catch critical conditions early and reduce livestock mortality.

---

## 📑 Table of Contents
- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
- [Supported Diseases](#-supported-diseases)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation Steps](#installation-steps)
- [Running Automated Tests](#-running-automated-tests)
- [REST API Reference](#-rest-api-reference)
- [Veterinary & Safety Disclaimer](#-veterinary--safety-disclaimer)

---

## 🌟 Project Overview

Livestock health is the backbone of rural economies, but farmers often lack immediate access to certified veterinary professionals. Delayed identification of contagious outbreaks (like Foot & Mouth Disease or Lumpy Skin Disease) or fatal conditions (such as Anthrax) can devastate smallholder herds.

**PashuRakshak** bridges this gap by:
1. Translating observed field symptoms into potential health risk evaluations.
2. Escalating life-threatening emergencies with immediate alerts and isolation advisories.
3. Logging screening records so veterinarians can review animal history on arrival.

---

## ✨ Key Features

- **Multi-Species Support:** Screenings tailored for **Cows**, **Buffaloes**, **Goats**, and **Sheep**.
- **Interactive Symptom Picker:** Real-time search filter and visual symptom selection pills with selected item counter badges.
- **Rule-Based Screening Engine:** Transparent, weighted algorithm computing match confidence scores, core vs. secondary symptom overlap, and risk stratification (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`).
- **Emergency Flagging:** Automatic detection of high-fatality red flags (e.g. Anthrax, blackleg, sudden death signs, bloody discharge) that immediately trigger emergency warnings.
- **Comprehensive Screening Reports:** Detailed breakdowns showing:
  - Possible condition and confidence percentage bar.
  - Risk badge and matched symptoms checklist.
  - Actionable immediate care and biosecurity precautions.
- **Screening History Log:** Searchable audit trail of previous screenings with quick links to full reports.
- **RESTful API:** Ready for mobile apps, USSD gateways, and offline field-worker tools.

---

## 🩺 Supported Diseases

PashuRakshak's knowledge base includes common and high-impact conditions:

| Disease | Species Affected | Risk Level | Notable Indicators |
| :--- | :--- | :--- | :--- |
| **Foot and Mouth Disease (FMD)** | Cow, Buffalo, Goat, Sheep | High | Blisters on tongue/hooves, drooling, lameness |
| **Lumpy Skin Disease (LSD)** | Cow, Buffalo | High | Hard skin nodules, fever, enlarged lymph nodes |
| **Mastitis** | Cow, Buffalo, Goat, Sheep | Medium | Swollen/hard udder, abnormal milk, clots |
| **Anthrax** | Cow, Buffalo, Goat, Sheep | **CRITICAL** | Sudden fever, dark unclotted bleeding, acute fatality |
| **Blackleg (Black Quarter)** | Cow, Buffalo, Sheep | **CRITICAL** | Crepitant swelling in hip/shoulder, lameness, high fever |
| **Bovine Babesiosis (Tick Fever)** | Cow, Buffalo | High | Red/coffee-colored urine, anemia, ticks |
| **Peste des Petits Ruminants (PPR)** | Goat, Sheep | High | High fever, mouth sores, foul diarrhea, discharge |
| **Brucellosis** | Cow, Buffalo, Goat, Sheep | Medium | Late-term abortion, retained placenta, joint swelling |
| **Hemorrhagic Septicemia (HS)** | Cow, Buffalo | **CRITICAL** | Severe throat swelling, respiratory distress, fever |
| **Bloat (Tympanites)** | Cow, Buffalo, Goat, Sheep | High | Distended left abdomen, breathing difficulty, kicking belly |

---

## 🛠 Tech Stack

- **Backend:** Python 3.10+, Django 5.x
- **API Framework:** Django REST Framework (DRF)
- **Database:** SQLite (default) / compatible with PostgreSQL & MySQL
- **Frontend:** Django Templates, Vanilla HTML5 & CSS3, Bootstrap 5.3, Bootstrap Icons
- **Testing:** Django Test Runner & DRF APITestCase

---

## 📁 Project Architecture

```text
PashuRakshak/
│
├── livestock_health/           # Project Configuration Package
│   ├── settings.py             # Django settings & third-party app configs
│   ├── urls.py                 # Root URL router
│   ├── wsgi.py                 # WSGI entry point for web deployment
│   └── asgi.py                 # ASGI entry point for async servers
│
├── diagnosis/                  # Core Business Application
│   ├── models.py               # Database schemas (Disease & Diagnosis)
│   ├── services.py             # Rule-based screening & scoring engine
│   ├── views.py                # Web view controllers & DRF API views
│   ├── forms.py                # Health screening form & validation
│   ├── urls.py                 # App-level routing (/result/, /history/, /api/...)
│   ├── serializers.py          # DRF serializers for JSON APIs
│   ├── admin.py                # Django admin customizations
│   ├── tests.py                # Automated test suite (11 test cases)
│   │
│   ├── management/commands/
│   │   └── seed_diseases.py    # Database seeder for livestock diseases
│   │
│   ├── static/diagnosis/       # Static Assets
│   │   ├── css/style.css       # Custom stylesheets & responsive layout
│   │   └── js/main.js          # Live search filter & dynamic UI interactions
│   │
│   └── templates/diagnosis/    # User Interface Templates
│       ├── base.html           # Base layout, navbar, & shared footer
│       ├── home.html           # Landing page & screening form
│       ├── result.html         # Assessment report & confidence meter
│       ├── history.html        # Historical records table
│       └── about.html          # Mission, methodology, & disclaimers
│
├── manage.py                   # Django CLI utility
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.10 or higher** installed on your system.
- `pip` (Python package manager).

### Installation Steps

1. **Clone or navigate to the project directory:**
   ```bash
   cd c:\Projects\PashuRakshak
   ```

2. **Create and activate a virtual environment (recommended):**
   - **Windows (PowerShell):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - **Linux / macOS:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Seed the livestock disease knowledge base:**
   ```bash
   python manage.py seed_diseases
   ```
   *This populates the database with 10 essential livestock diseases and core symptoms.*

6. **Create an admin superuser (optional, to access `/admin`):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the local development server:**
   ```bash
   python manage.py runserver
   ```

8. **Open in browser:**
   - 🌐 Web Interface: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**
   ---

## 🧪 Running Automated Tests

PashuRakshak includes an automated test suite verifying the screening engine, web forms, and REST API endpoints:

```bash
python manage.py test
```

Expected output:
```text
Found 11 test(s).
Creating test database for alias 'default'...
...........
----------------------------------------------------------------------
Ran 11 tests in 0.16s

OK
Destroying test database for alias 'default'...
```

---

## 📡 REST API Reference

PashuRakshak provides REST endpoints for programmatic access and external client integration.

### 1. Perform Animal Health Screening
- **Endpoint:** `POST /api/diagnose/`
- **Payload Example:**
  ```json
  {
    "animal_type": "cow",
    "age": 3.5,
    "gender": "Female",
    "symptoms": [
      "fever",
      "skin nodules",
      "swelling",
      "loss of appetite"
    ],
    "other_symptoms": "Nodules appeared on neck this morning"
  }
  ```
- **Response (`201 Created`):**
  ```json
  {
    "id": 1,
    "animal_type": "cow",
    "age": 3.5,
    "gender": "Female",
    "selected_symptoms": ["fever", "skin nodules", "swelling", "loss of appetite"],
    "predicted_disease": "Lumpy Skin Disease",
    "confidence": 75.0,
    "risk_level": "HIGH",
    "matched_symptoms": ["Fever", "Skin Nodules", "Swelling", "Loss Of Appetite"],
    "recommendation": "Isolate the animal immediately in an insect-free area. Disinfect premises...",
    "created_at": "2026-09-12T21:00:00Z",
    "warning": "This preliminary assessment is generated by an automated screening tool. Please consult a licensed veterinarian."
  }
  ```

### 2. Retrieve Screening History
- **Endpoint:** `GET /api/diagnoses/`
- **Response:** List of past screening objects with pagination support.

### 3. Get Specific Diagnosis Details
- **Endpoint:** `GET /api/diagnoses/<id>/`

### 4. Reference Disease Catalog
- **Endpoint:** `GET /api/diseases/`
- **Response:** List of all known disease profiles, symptoms, and care guidelines.

---

## ⚠️ Veterinary & Safety Disclaimer

> **IMPORTANT NOTICE:**  
> PashuRakshak is an **educational and preliminary screening prototype**. It is **NOT** a certified veterinary diagnostic instrument.
> 
> - Never administer prescription medications, antibiotics, or invasive treatments without explicit instructions from a registered veterinary practitioner.
> - For severe or sudden symptoms (uncontrolled bleeding, acute bloat, collapse, rapid mortality), seek **emergency veterinary intervention immediately**.
