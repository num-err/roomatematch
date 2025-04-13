//We need to handle the logic for the form navigating to the next step
//we need to handle the logic for the form navigating to previous step
//we need to handle the logic for the form submitting

document.addEventListener("DOMContentLoaded", function() {

    const nextButtons = document.querySelectorAll('[id^="next"]');
    const prevButtons = document.querySelectorAll('[id^="prev"]');

    nextButtons.forEach(button => {
        button.addEventListener('click', function() {
            const curentSection = this.closest('.section');
            const nextSection = curentSection.nextElementSibling;

            if (validateSection(currentSection)) {
                curentSection.classList.add('hidden');
                nextSection.classList.remove('hidden'); }
        });
        });

    prevButtons.forEach(button => {
        button.addEventListener('click', function() {
            const currentSection = this.closest('.section');
            const prevSection = currentSection.previousElementSibling;

            currentSection.classList.add('hidden');
            prevSection.classList.remove('hidden');
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
            submitFormData( userData);
        } else {
            alert('Please fill out all required fields');
        }
    });
});
// check that all the required fields have been entered in 
// the current section before moving to the next section
function validateSection(section){

    let valid = true;
    const requiredFields = section.querySelectorAll('[required]');

    requiredFields.forEach(field => {
        if (!field.value) {
            valid = false;
            field.classList.add('error');} // Checkpoint: we will need to style this in css
            // I would say border: 1px solid red;
            
        else{
            field.classList.remove('error');}
        });
        
        if (!valid) {
            alert('Please fill out all required fields'); // we alert the user
        }
    return valid;
}
function validateForm(){

    let valid = true;
    const requiredFields = document.querySelectorAll('[required]');

    requiredFields.forEach(field => {
        if (!field.value) {
            valid = false;
            field.classList.add('error');}
        
        else{
            field.classList.remove('error');}
        });
    
    return valid;
}
// this is the function that will handle the form submission
// this function will send the data to the server
// this function will be called when we click the submit button 
function submitFormData(userData){
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
        alert('Form submitted successfully!'); });

}
