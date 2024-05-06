document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        let messageContainer = document.getElementById('message-container');

        if (messageContainer) {
            messageContainer.style.display = 'none';
        }
    }, 5000);
});
