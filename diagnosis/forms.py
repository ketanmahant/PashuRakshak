from django import forms
from .services import ALL_SYMPTOMS

ANIMAL_CHOICES = [
    ('cow', 'Cow'),
    ('buffalo', 'Buffalo'),
    ('goat', 'Goat'),
    ('sheep', 'Sheep'),
    ('pig', 'Pig'),
    ('poultry', 'Poultry'),
]

GENDER_CHOICES = [
    ('Female', 'Female'),
    ('Male', 'Male'),
]

SYMPTOM_CHOICES = [(s, s) for s in ALL_SYMPTOMS]


class HealthScreeningForm(forms.Form):
    animal_type = forms.ChoiceField(
        choices=ANIMAL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg', 'id': 'animal_type'}),
        label="Animal Type",
        help_text="Select the species of the animal",
        required=True,
    )
    age = forms.FloatField(
        required=False,
        min_value=0.0,
        max_value=35.0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'e.g. 3.5',
            'step': '0.5',
            'id': 'age'
        }),
        label="Age (Years)",
        help_text="Approximate age of the animal in years (optional)"
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'}),
        label="Gender",
        required=True,
        initial='Female'
    )
    symptoms = forms.MultipleChoiceField(
        choices=SYMPTOM_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'btn-check'}),
        required=False,
        label="Observed Symptoms"
    )
    other_symptoms = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Describe any other unusual signs, behavior changes, or duration...',
            'id': 'other_symptoms'
        }),
        label="Other Symptoms / Additional Notes"
    )

    def clean(self):
        cleaned_data = super().clean()
        symptoms = cleaned_data.get('symptoms', [])
        other_symptoms = cleaned_data.get('other_symptoms', '').strip()

        if not symptoms and not other_symptoms:
            raise forms.ValidationError(
                "Please select at least one symptom before continuing."
            )
        return cleaned_data
