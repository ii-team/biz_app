// Index Page Authentication Logic

document.addEventListener('DOMContentLoaded', async function() {
    // Attempt auto-login
    const isLoggedIn = await attemptAutoLogin();
    
    if (!isLoggedIn) {
        // Redirect to login page
        redirectToLogin();
        return;
    }
    
    // User is logged in, show user menu
    displayUserMenu();
});

/**
 * Display user menu with user name
 */
function displayUserMenu() {
    const userData = getUserData();
    
    if (!userData) {
        redirectToLogin();
        return;
    }
    
    // Show user menu in desktop header
    const userMenu = document.getElementById('user_menu');
    if (userMenu) {
        userMenu.style.display = 'block';
        
        const userName = document.getElementById('user_name');
        if (userName) {
            // Display first name or email
            const displayName = userData.name 
                ? userData.name.split(' ')[0] 
                : userData.email.split('@')[0];
            userName.textContent = displayName;
        }
    }
    
    // Show user menu in mobile sidebar
    const userMenuMob = document.getElementById('user_menu_mob');
    if (userMenuMob) {
        userMenuMob.style.display = 'block';
    }
}

/**
 * Toggle user dropdown menu
 */
function toggleUserDropdown() {
    const dropdown = document.getElementById('user_dropdown');
    if (dropdown) {
        dropdown.classList.toggle('show');
    }
}

// Close dropdown when clicking outside
window.addEventListener('click', function(e) {
    if (!e.target.matches('.user_button') && !e.target.closest('.user_button')) {
        const dropdown = document.getElementById('user_dropdown');
        if (dropdown && dropdown.classList.contains('show')) {
            dropdown.classList.remove('show');
        }
    }
});