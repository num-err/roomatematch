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
    // Maybe use document.getElementById("submit"); instead?
    // Maybe change to an onclick event too?
    // const form = document.querySelector('form');
    // form.addEventListener('submit', function(event) {
    const form = document.getElementById("sendAnswers");
    form.addEventListener('click', function(event) {
        event.preventDefault();

        console.log("Testing");

        // Get all form data
        const bedtime = document.querySelector('select[name="bedtime"]').value;
        const bedtimeImportance = document.querySelector('input[name="bedtime-importance"]:checked').value;
        const lights = document.querySelector('input[name="lights"]:checked').value;
        const lightsImportance = document.querySelector('input[name="lights-importance"]:checked').value;
        const guests = document.querySelector('input[name="guests"]:checked').value;
        const guestsImportance = document.querySelector('input[name="guests-importance"]:checked').value;

        // Bug starting here.  Seems that not all of this exists on the frontend?
        const personalityType = "";//document.querySelector('input[name="personality-type"]:checked').value;
        const personalityImportance = "";//document.querySelector('input[name="personality-importance"]:checked').value;
        const goingOutFrequency = "";//document.querySelector('input[name="going-out-frequency"]:checked').value;
        const goingOutImportance = "";// = document.querySelector('input[name="going-out-importance"]:checked').value;
        const peopleOverPreference = "";// = document.querySelector('input[name="people-over-preference"]:checked').value;
        const peopleOverImportance = "";// = document.querySelector('input[name="people-over-importance"]:checked').value;
        const roommateGoingOutPreference = "";// = document.querySelector('input[name="roommate-going-out-preference"]:checked').value;

        // Printing some inputs for testing purposes
        console.log(bedtime, bedtimeImportance);

        // Get user from localStorage
        const user = JSON.parse(localStorage.getItem('user'));
        if (!user || !user.id) {
            alert('Please login to submit the form');
            return;
        }

        // Create and send the request
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4) {
                if (this.status == 200) {
                    console.log("Response Received: " + this.responseText);
                    let data = JSON.parse(this.responseText);
                    if ("error" in data) {
                        alert("Questionnaire submission failed. Please try again!");
                    } else {
                        alert("Questionnaire submitted successfully!");
                    }
                } else {
                    alert("Error submitting questionnaire. Please try again.");
                }
            }
        };

        xhttp.open("POST", "/api/questionnaire", true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send(
            "user_id=" + user.id +
            "&bedtime=" + bedtime +
            "&bedtime_importance=" + bedtimeImportance +
            "&lights=" + lights +
            "&lights_importance=" + lightsImportance +
            "&guests=" + guests +
            "&guests_importance=" + guestsImportance +
            "&personality_type=" + personalityType +
            "&personality_importance=" + personalityImportance +
            "&going_out_frequency=" + goingOutFrequency +
            "&going_out_importance=" + goingOutImportance +
            "&people_over_preference=" + peopleOverPreference +
            "&people_over_importance=" + peopleOverImportance +
            "&roommate_going_out_preference=" + roommateGoingOutPreference
        );
        console.log("Questionnaire Request Sent");
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
function submitFormData(userData, userId) {
    console.log(userData, userId);

    const user = JSON.parse(localStorage.getItem('user'));
    if (!user || !user.id) {
        alert('Please login to submit the form');
        return;
    }

    fetch('/api/questionnaire', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            answers: userData,
            user_id: user.id
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        alert('Form submitted successfully!');
    });
}
