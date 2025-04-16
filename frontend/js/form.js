//We need to handle the logic for the form navigating to the next step
//we need to handle the logic for the form navigating to previous step
//we need to handle the logic for the form submitting

document.addEventListener("DOMContentLoaded", function() {
    const nextButtons = document.querySelectorAll('[id^="next"]');
    const prevButtons = document.querySelectorAll('[id^="prev"]');
    const sections = document.querySelectorAll('.section');

    // Function to show a specific section
    function showSection(sectionId) {
        sections.forEach(section => {
            if (section.id === sectionId) {
                section.classList.remove('hidden');
            } else {
                section.classList.add('hidden');
            }
        });
    }

    nextButtons.forEach(button => {
        button.addEventListener('click', function() {
            const currentSection = this.closest('.section');
            const currentSectionId = currentSection.id;
            const currentSectionNumber = parseInt(currentSectionId.replace('section', ''));
            const nextSectionId = `section${currentSectionNumber + 1}`;
            
            if (validateSection(currentSection)) {
                showSection(nextSectionId);
            }
        });
    });

    prevButtons.forEach(button => {
        button.addEventListener('click', function() {
            const currentSection = this.closest('.section');
            const currentSectionId = currentSection.id;
            const currentSectionNumber = parseInt(currentSectionId.replace('section', ''));
            const prevSectionId = `section${currentSectionNumber - 1}`;
            
            showSection(prevSectionId);
        });
    });
    
    // this is the form submission
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        if (validateForm()) {
            // here we can submit the form(QUESTION: do we need to convert it to JSON?)
            const formData = new FormData(form);
            const userData = Object.fromEntries(formData.entries());
            alert('Form submitted successfully!');
            submitFormData(userData);
        } else {
            alert('Please fill out all required fields');
        }
    });
});

// check that all the required fields have been entered in 
// the current section before moving to the next section
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

// this is the function that will handle the form submission
// this function will send the data to the server
// this function will be called when we click the submit button 
function submitFormData(userData) {
    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    })
    .then(response => response.text())
    .then(data => {
        console.log('Success:', data);
        alert('Form submitted successfully!');
    });
}
