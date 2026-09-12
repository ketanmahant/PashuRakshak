// PashuRakshak interactive features

document.addEventListener('DOMContentLoaded', function () {
  const symptomSearchInput = document.getElementById('symptomSearch');
  const symptomItems = document.querySelectorAll('.symptom-pill');
  const selectedCountBadge = document.getElementById('selectedSymptomCount');
  const checkboxes = document.querySelectorAll('.symptom-checkbox');
  const clearBtn = document.getElementById('clearSymptomsBtn');

  // Update selected symptoms count badge
  function updateCount() {
    const checkedCount = document.querySelectorAll('.symptom-checkbox:checked').length;
    if (selectedCountBadge) {
      selectedCountBadge.textContent = checkedCount;
      if (checkedCount > 0) {
        selectedCountBadge.classList.remove('bg-secondary');
        selectedCountBadge.classList.add('bg-success');
      } else {
        selectedCountBadge.classList.remove('bg-success');
        selectedCountBadge.classList.add('bg-secondary');
      }
    }
  }

  checkboxes.forEach(cb => {
    cb.addEventListener('change', updateCount);
  });
  updateCount();

  // Search filter for symptoms
  if (symptomSearchInput) {
    symptomSearchInput.addEventListener('input', function (e) {
      const term = e.target.value.toLowerCase().trim();
      symptomItems.forEach(item => {
        const text = item.textContent.toLowerCase();
        if (text.includes(term)) {
          item.style.display = '';
        } else {
          item.style.display = 'none';
        }
      });
    });
  }

  // Clear all button
  if (clearBtn) {
    clearBtn.addEventListener('click', function () {
      checkboxes.forEach(cb => cb.checked = false);
      updateCount();
    });
  }

  // Form submit check
  const healthForm = document.getElementById('healthScreeningForm');
  if (healthForm) {
    healthForm.addEventListener('submit', function (e) {
      const checkedCount = document.querySelectorAll('.symptom-checkbox:checked').length;
      const otherSymptoms = document.getElementById('other_symptoms')?.value.trim();

      if (checkedCount === 0 && (!otherSymptoms || otherSymptoms.length === 0)) {
        e.preventDefault();
        const alertBox = document.getElementById('clientAlert');
        if (alertBox) {
          alertBox.textContent = 'Please select at least one symptom before checking animal health.';
          alertBox.classList.remove('d-none');
          alertBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      }
    });
  }

  // Dynamic progress bar width initialization (e.g. screening confidence bar)
  const progressBars = document.querySelectorAll('.progress-bar[data-confidence]');
  progressBars.forEach(bar => {
    const val = parseFloat(bar.getAttribute('data-confidence')) || 0;
    bar.style.width = val + '%';
  });
});

