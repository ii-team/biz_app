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
        avatar.src = isUser ? 'static/images/default.jpeg' : document.getElementById("company_logo").src;
        avatar.alt = isUser ? 'Lubos' : 'User';
        
        const userName = document.createElement('div');
        userName.className = 'user-name';
        if (!isUser) {
            userName.classList.add('company-avatar');
        }
        userName.textContent = isUser ? 'Lubos' : 'User';
        
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
            
            var url = BACKEND_URL + "/chat";
            var index_id = document.getElementById("index_id").value;
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    "question": messageText,
                    "index_id": index_id
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            }
            )
            .then(data => {
                addMessage(data["message"], false);
            })
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

// getting id from url
function getIdFromUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get('id');
    return id ? id : null;
}

// querying the database
function queryDatabase(id) {
    const url = BACKEND_URL + `/getBusinessCard?id=${id}`;
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const org = data["org"];
            document.getElementById("company_name").innerHTML = org["org_name"];
            document.getElementById("company_logo").src = org["company_logo"];
            document.getElementById("description").innerHTML = org["description"];
            document.getElementById("inner_email").innerHTML = org["email"];
            document.getElementById("inner_phone").innerHTML = org["phone"];
            document.getElementById("inner_webpage").innerHTML = org["webpage"];
            document.getElementById("inner_linkedin").innerHTML = org["linkedin"];
            document.getElementById("responsible_person_logo").src = org["profile_pic"];
            document.getElementById("responsible_person").innerHTML = org["responsible_person"];
            var company_avatars= document.getElementsByClassName("company-avatar");
            for (var i = 0; i < company_avatars.length; i++) {
                company_avatars[i].src = org["company_logo"];
            }
            var company_name_avatar = document.getElementsByClassName("company-name-avatar");
            for (var i = 0; i < company_name_avatar.length; i++) {
                company_name_avatar[i].innerHTML = org["org_name"];
            }
            document.getElementById("index_id").value = org["iiealra_index_id"];
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}
// Call the function to get the ID from the URL
const id = getIdFromUrl();
console.log(`ID from URL: ${id}`);
if (id) {
    queryDatabase(id);
} else {
    console.error('No ID found in the URL');
}
