// Business Card Implementation - Final Layout

// Function to fetch business cards from the backend
function fetchBusinessCards() {
    // Show a loading indicator or message if needed
    const cardsContainer = document.getElementById('cards');
    cardsContainer.innerHTML = '<p>Loading cards...</p>';
    
    // Fetch data from the backend
    fetch(BACKEND_URL +'/getBusinessCards')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Clear the loading message
            cardsContainer.innerHTML = '';
            
            // Process the data and create cards
            createBusinessCards(data);
        })
        .catch(error => {
            console.error('Error fetching business cards:', error);
            cardsContainer.innerHTML = '<p>Failed to load business cards. Please try again later.</p>';
        });
}

function capitalizeWords(str) {
    return str.split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
        .join(' ');
}

// Function to create business cards from data
function createBusinessCards(cardsData) {
    const cardsContainer = document.getElementById('cards');
    
    // Loop through each card data and create a card element
    cardsData.forEach(card => {
        // Create card container
        const cardContainer = document.createElement('div');
        cardContainer.className = 'card-container';
        cardContainer.id = `card-${card.id}`;
        cardContainer.title = 'Click To Chat';
        
        // Create card HTML structure with updated layout
        cardContainer.innerHTML = `
            <div class="card">
                <div class="card-front">
                    <div class="card-header">
                        <img src="${card.company_logo}" alt="${card.org_name}"  class="card-logo">
                    </div>
                    
                    <div class="card-description-front">
                        <p class="company-info">We are a rapidly developing IT company founded in 2020.</p>
                    </div>
                    
                    <div class="card-footer">
                        <div class="profile-wrapper">
                            <div class="profile-image-container">
                                <img src="${card.profile_pic}" alt="${card.org_name}" class="card-image">
                            </div>
                            <div class="profile-details">
                                <div class="card-name">${capitalizeWords(card.responsible_person)}</div>
                                <div class="card-position">CEO ${(card.org_name)}</div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="card-back">
                    <div class="card-description">
                        <h2 class="org_name">${capitalizeWords(card.org_name)}</h2>
                        <p class="description">${card.description}</p>
                        <p class="website"><span class="bold">Website:</span> ${card.webpage}</p>
                        <p class="linkedin"><span class="bold">LinkedIn:</span> ${card.linkedin}</p>
                        <div class="contact-info">
                            <p><span class="bold">Email:</span> ${card.email}</p>
                            <p><span class="bold">Phone:</span> ${card.phone}</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Add click event listener to the card
        cardContainer.addEventListener('click', function() {
            start_chat(card.id);
        });
        
        // Append the card to the container
        cardsContainer.appendChild(cardContainer);
    });
}

// Function to start chat with a business
function start_chat(cardId) {
    console.log(`Starting chat with business ID: ${cardId}`);
    // Implement your chat functionality here
    window.location.href = `chat.html?id=${cardId}`;
}

// Function to detect language and update content
function updateCardLanguage(language) {
    // Update card text elements based on selected language
    const elements = document.querySelectorAll('[data-translate]');
    
    elements.forEach(element => {
        const key = element.getAttribute('data-translate');
        if (translations[language] && translations[language][key]) {
            element.textContent = translations[language][key];
        }
    });
}

// Add language detection event handler
document.addEventListener('languageChanged', function(e) {
    updateCardLanguage(e.detail.language);
});

// Call the function when the page loads
document.addEventListener('DOMContentLoaded', function() {
    // Create cards container if it doesn't exist
    if (!document.getElementById('cards')) {
        const cardsSection = document.createElement('section');
        cardsSection.id = 'card_section';
        
        const cardsTitle = document.createElement('h2');
        cardsTitle.textContent = 'Business Cards';
        cardsTitle.setAttribute('data-key', 'business_cards_title');
        cardsTitle.className = 'section_title';
        
        const cardsContainer = document.createElement('div');
        cardsContainer.id = 'cards';
        
        cardsSection.appendChild(cardsTitle);
        cardsSection.appendChild(cardsContainer);
        
        // Insert before footer or at the end of body
        document.body.appendChild(cardsSection);
    }
    
    // Fetch business cards
    fetchBusinessCards();
});