//We need to handle the logic for the form navigating to the next step
//we need to handle the logic for the form navigating to previous step
//we need to handle the logic for the form submitting

document.addEventListener("DOMContentLoaded", function() {
   
    // this is the form submission
    // Maybe use document.getElementById("submit"); instead?
    // Maybe change to an onclick event too?
    // const form = document.querySelector('form');
    // form.addEventListener('submit', function(event) {



    const form = document.querySelector("#roommate-form")

    function sendData (){
        const formData = new FormData(form);

        const userStr = localStorage.getItem("user");  
        const user = userStr ? JSON.parse(userStr) : {};

        const user_id = user.id;     
        
        if (!user_id) {
            alert("Missing user_id")
        }

        formData.append("user_id", user_id)

        for (let [key, val] of formData.entries()) {
            console.log(key, '→', val);
        }

        const xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
          if (this.readyState === 4) {
            if (this.status === 200) {
              console.log("Response Received: " + this.responseText);
              const data = JSON.parse(this.responseText);
              if (data.error) {
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
        xhttp.send(formData);
    }


    form.addEventListener("submit", (event) => {
        event.preventDefault();
        sendData();
    })

    // const submitButton = document.getElementById("sendAnswers");
    // submitButton.addEventListener('click', function(event) {
    //     event.preventDefault();

    //     console.log("Testing");

    //     // Get all form data
    //     const bedtime = document.querySelector('select[name="bedtime"]').value;
    //     const bedtime_importance = document.querySelector('input[name="bedtime_importance"]:checked').value;
    //     const lights = document.querySelector('input[name="lights"]:checked').value;
    //     const lights_importance = document.querySelector('input[name="lights_importance"]:checked').value;
    //     const guests = document.querySelector('input[name="guests"]:checked').value;
    //     const guests_importance = document.querySelector('input[name="guests_importance"]:checked').value;

    //     // Cleanliness section
    //     const clean = document.querySelector('input[name="clean"]:checked').value;
    //     const clean_importance = document.querySelector('input[name="clean_importance"]:checked').value;
    //     const mess = document.querySelector('input[name="mess"]:checked').value;
    //     const mess_importance = document.querySelector('input[name="mess_importance"]:checked').value;
    //     const sharing = document.querySelector('input[name="sharing"]:checked').value;
    //     const sharing_importance = document.querySelector('input[name="sharing_importance"]:checked').value;

    //     // Study habits section
    //     const study_location = document.querySelector('input[name="study_location"]:checked').value;
    //     const study_location_importance = document.querySelector('input[name="study_location_importance"]:checked').value;
    //     const noise_preference = document.querySelector('input[name="noise_preference"]:checked').value;
    //     const noise_importance = document.querySelector('input[name="noise_importance"]:checked').value;
    //     const intended_major = document.querySelector('select[name="intended_major"]').value;
    //     const major_importance = document.querySelector('input[name="major_importance"]:checked').value;

    //     // Personality section
        

    //     // Bug starting here.  Seems that not all of this exists on the frontend?
    //     const personality_type = document.querySelector('input[name="personality_type"]:checked').value;
    //     const personality_importance = document.querySelector('input[name="personality_importance"]:checked').value;
    //     const going_out_frequency = document.querySelector('input[name="going_out_frequency"]:checked').value;
    //     const going_out_importance = document.querySelector('input[name="going_out_importance"]:checked').value;
    //     const people_over_preference = document.querySelector('input[name="people_over_preference"]:checked').value;
    //     const people_over_importance  = document.querySelector('input[name="people_over_importance"]:checked').value;
       

    //     // Printing some inputs for testing purposes
    //     console.log(bedtime, bedtimeImportance);
    //     console.log(clean, clean_importance);
    //     console.log(study_location, study_location_importance);
    //     console.log(personalityType, personalityImportance);
    //     // Get user from localStorage
    //     const user = JSON.parse(localStorage.getItem('user'));
    //     if (!user || !user.id) {
    //         alert('Please login to submit the form');
    //         return;
    //     }

    //     // Create and send the request
    //     var xhttp = new XMLHttpRequest();
    //     xhttp.onreadystatechange = function() {
    //         if (this.readyState == 4) {
    //             if (this.status == 200) {
    //                 console.log("Response Received: " + this.responseText);
    //                 let data = JSON.parse(this.responseText);
    //                 if ("error" in data) {
    //                     alert("Questionnaire submission failed. Please try again!");
    //                 } else {
    //                     alert("Questionnaire submitted successfully!");
    //                 }
    //             } else {
    //                 alert("Error submitting questionnaire. Please try again.");
    //             }
    //         }
    //     };

    //     xhttp.open("POST", "/api/questionnaire", true);
    //     xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        
    //     const params = new URLSearchParams({
    //         user_id: user.id,
    //         bedtime,
    //         bedtime_importance,
    //         lights,
    //         lights_importance,
    //         guests,
    //         guests_importance,
    //         clean,
    //         clean_importance,
    //         mess,
    //         mess_importance,
    //         sharing,
    //         sharing_importance,
    //         study_location,
    //         study_location_importance,
    //         noise_preference,
    //         noise_importance,
    //         intended_major,
    //         major_importance,
    //         personality_type,
    //         personality_importance,
    //         going_out_frequency,
    //         going_out_importance,
    //         people_over_preference,
    //         people_over_importance
    //     });
        
    //     xhttp.send(params.toString());
    //     console.log("Questionnaire Request Sent");
    // });
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
/*function submitFormData(userData, userId) {
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
}*/