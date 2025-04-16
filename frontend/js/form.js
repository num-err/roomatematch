//We need to handle the logic for the form navigating to the next step
//we need to handle the logic for the form navigating to previous step
//we need to handle the logic for the form submitting

document.addEventListener("DOMContentLoaded", function() {
    const nextButtons = document.querySelectorAll('[id^="next"]');
    const prevButtons = document.querySelectorAll('[id^="prev"]');
    const sections = document.querySelectorAll('.section');

    // Hide all sections except the first one
    sections.forEach((section, index) => {
        if (index !== 0) {
            section.classList.add('hidden');
        }
    });

    nextButtons.forEach(button => {
        button.addEventListener('click', function() {
            const currentSection = this.closest('.section');
            const currentIndex = Array.from(sections).indexOf(currentSection);
            const nextSection = sections[currentIndex + 1];

            if (validateSection(currentSection) && nextSection) {
                currentSection.classList.add('hidden');
                nextSection.classList.remove('hidden');
            }
        });
    });

    prevButtons.forEach(button => {
        button.addEventListener('click', function() {
            const currentSection = this.closest('.section');
            const currentIndex = Array.from(sections).indexOf(currentSection);
            const prevSection = sections[currentIndex - 1];

            if (prevSection) {
                currentSection.classList.add('hidden');
                prevSection.classList.remove('hidden');
            }
        });
    });
    
    // Handle form submission
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            if (validateForm()) {
                const formData = new FormData(form);
                const userData = Object.fromEntries(formData.entries());
                submitFormData(userData);
            } else {
                alert('Please fill out all required fields');
            }
        });
    });
});

function validateSection(section) {
    let valid = true;
    const requiredFields = section.querySelectorAll('[required]');

    requiredFields.forEach(field => {
        if (!field.value) {
            valid = false;
            field.classList.add('error');
        } else {
            field.classList.remove('error');
        }
    });
    
    if (!valid) {
        alert('Please fill out all required fields');
    }
    return valid;
}

function validateForm() {
    let valid = true;
    const requiredFields = document.querySelectorAll('[required]');

    requiredFields.forEach(field => {
        if (!field.value) {
            valid = false;
            field.classList.add('error');
        } else {
            field.classList.remove('error');
        }
    });
    
    return valid;
}

function submitFormData(userData) {
    // Combine all form data
    const allForms = document.querySelectorAll('form');
    const combinedData = {};
    
    allForms.forEach(form => {
        const formData = new FormData(form);
        Object.assign(combinedData, Object.fromEntries(formData.entries()));
    });

    // Send to server
    fetch('/api/questionnaire', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_id: 1, // TODO: Get actual user ID
            answers: combinedData
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Submission failed: ' + data.error);
        } else {
            alert('Questionnaire submitted successfully!');
            if (data.match) {
                alert('We found a match for you!');
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to submit questionnaire. Please try again.');
    });
}