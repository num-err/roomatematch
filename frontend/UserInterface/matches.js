document.addEventListener('DOMContentLoaded', async () => {
    const matchesList = document.getElementById('matches-list');
    const matchTemplate = document.getElementById('match-template');
    
    try {
        // Get the current user's ID from session storage
        const userId = getCurrentUserId();
        if (!userId) {
            console.error('No user ID found. Please log in.');
            return;
        }
        
        // Fetch the match from the backend
        const response = await fetch(`/api/match/${userId}`);
        const matchData = await response.json();
        
        if (matchData && !matchData.message) {
            // Update the first card with the match data
            const firstCard = matchesList.querySelector('.match-card');
            if (firstCard) {
                firstCard.innerHTML = matchTemplate.innerHTML;
                
                // Fill in the match data
                firstCard.querySelector('.match-name').textContent = matchData.name;
                firstCard.querySelector('.match-year').textContent = matchData.year;
                firstCard.querySelector('.score').textContent = '90%'; // You can calculate this based on your matching algorithm
                
                // Update other details based on the questionnaire data
                firstCard.querySelector('.sleep-info').textContent = matchData.sleep_schedule || 'Not specified';
                firstCard.querySelector('.clean-info').textContent = matchData.cleanliness || 'Not specified';
                firstCard.querySelector('.study-info').textContent = matchData.study_habits || 'Not specified';
                firstCard.querySelector('.social-info').textContent = matchData.social_preferences || 'Not specified';
                
                // Add event listeners for buttons
                firstCard.querySelector('.view-profile').addEventListener('click', () => {
                    window.location.href = `/profile/${matchData.id}`;
                });
                
                firstCard.querySelector('.send-message').addEventListener('click', () => {
                    // Implement message functionality
                    console.log('Message button clicked');
                });
            }
        }
    } catch (error) {
        console.error('Error fetching matches:', error);
    }
});

function getCurrentUserId() {
    // First try sessionStorage
    let userData = sessionStorage.getItem('userData');
    
    // If not in sessionStorage, try localStorage (for backward compatibility)
    if (!userData) {
        userData = localStorage.getItem('user');
    }
    
    if (!userData) {
        return null;
    }
    
    try {
        const user = JSON.parse(userData);
        return user.id;
    } catch (e) {
        console.error('Error parsing user data:', e);
        return null;
    }
} 