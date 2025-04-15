// Chat functionality
document.addEventListener('DOMContentLoaded', function() {
    const messageInput = document.getElementById('message_input');
    const sendButton = document.getElementById('send_button');
    const chatbox = document.getElementById('chatbox');
    
    // Function to add a new message
    function addMessage(text, isUser) {
        const messageContainer = document.createElement('div');
        messageContainer.className = isUser ? 'message-container user-container' : 'message-container elara-container';
        
        const avatarWrapper = document.createElement('div');
        avatarWrapper.className = 'avatar-wrapper';
        
        const avatar = document.createElement('img');
        avatar.className = 'avatar';
        avatar.src = isUser ? 'static/images/main.jpeg' : 'static/images/iiteam_logo.jpeg';
        avatar.alt = isUser ? 'Lubos' : 'Ananya';
        
        const userName = document.createElement('div');
        userName.className = 'user-name';
        userName.textContent = isUser ? 'Lubos' : 'Ananya';
        
        const message = document.createElement('div');
        message.className = isUser ? 'message user-message' : 'message elara-message';
        message.textContent = text;
        
        avatarWrapper.appendChild(avatar);
        avatarWrapper.appendChild(userName);
        
        messageContainer.appendChild(avatarWrapper);
        messageContainer.appendChild(message);
        
        chatbox.appendChild(messageContainer);
        
        // Scroll to bottom
        chatbox.scrollTop = chatbox.scrollHeight;
    }
    
    // Function to handle sending messages
    function sendMessage() {
        const messageText = messageInput.value.trim();
        if (messageText !== '') {
            addMessage(messageText, true);
            messageInput.value = '';
            
            // Simulate response (in a real app, this would come from a server)
            setTimeout(() => {
                const responses = [
                    "That's interesting!",
                    "I see what you mean.",
                    "Thanks for sharing that.",
                    "Let me think about that for a moment.",
                    "Good point!"
                ];
                const randomResponse = responses[Math.floor(Math.random() * responses.length)];
                addMessage(randomResponse, false);
            }, 1000);
        }
    }
    
    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});