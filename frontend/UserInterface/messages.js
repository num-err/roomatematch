document.addEventListener('DOMContentLoaded', () => {
    const sendButton = document.getElementById('send-message');
    const messageText = document.getElementById('message-text');
    const messageStatus = document.getElementById('message-status');

    sendButton.addEventListener('click', () => {
        if (!messageText.value.trim()) {
            alert('Please enter a message');
            return;
        }

        // Show loading state
        sendButton.disabled = true;
        sendButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';

        // Simulate sending a message
        setTimeout(() => {
            // Reset button
            sendButton.disabled = false;
            sendButton.innerHTML = '<i class="fas fa-paper-plane"></i> Send Message';
            
            // Clear message
            messageText.value = '';
            
            // Show success message
            messageStatus.classList.remove('hidden');
            
            // Hide success message after 3 seconds
            setTimeout(() => {
                messageStatus.classList.add('hidden');
            }, 3000);
        }, 1500); // Simulate network delay
    });
}); 