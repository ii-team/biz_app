
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
        
        // Create card HTML structure
        cardContainer.innerHTML = `
            <div class="card">
                <div class="card-front">
                    <img src="${card.profile_pic}" alt="${capitalizeWords(card.org_name)}" class="card-image">
                    <div class="card-name">${capitalizeWords(card.responsible_person)}</div>
                </div>
                <div class="card-back">
                    <div class="card-description">
                        <h2 class="org_name">${capitalizeWords(card.org_name)}</h2>
                        <p class="description">${card.description}</p>
                        <p class="website"><span class="bold"> Website:</span> ${card.webpage}</p>
                        <p class="linkedin"><span class="bold"> LinkedIn:</span> ${card.linkedin}</p>
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
    alert(`Starting chat with business ID: ${cardId}`);
}

// Call the function when the page loads
document.addEventListener('DOMContentLoaded', fetchBusinessCards);