// Add any interactive elements or animations here

document.addEventListener('DOMContentLoaded', function() {
    // Add a subtle hover effect to the card
    const card = document.querySelector('.card');
    
    card.addEventListener('mouseover', function() {
        this.style.transform = 'translateY(-5px)';
        this.style.boxShadow = '0 15px 30px rgba(0, 0, 0, 0.15)';
        this.style.transition = 'all 0.3s ease';
    });
    
    card.addEventListener('mouseout', function() {
        this.style.transform = 'translateY(0)';
        this.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.1)';
        this.style.transition = 'all 0.3s ease';
    });
    
    // Create a click effect that could be used to flip the card
    card.addEventListener('click', function() {
        this.classList.toggle('flipped');
    });
});