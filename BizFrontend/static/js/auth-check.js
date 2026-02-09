// Authentication Check Utility
async function checkAuthentication() {
    const token = getAuthToken();
    
    if (!token) {
        // No token found, redirect to login
        window.location.href = 'login.html';
        return false;
    }
    
    // Verify token with backend using existing attemptAutoLogin function
    const isValid = await attemptAutoLogin();
    
    if (!isValid) {
        // Token is invalid or expired
        window.location.href = 'login.html';
        return false;
    }
    
    // Token is valid, show logout button
    showLogoutButton();
    return true;
}

function showLogoutButton() {
    const logoutBtn = document.getElementById('logout_btn');
    const logoutBtnMob = document.getElementById('logout_btn_mob');
    
    if (logoutBtn) {
        logoutBtn.style.display = 'inline-block';
    }
    if (logoutBtnMob) {
        logoutBtnMob.style.display = 'block';
    }
}

async function handleLogout() {
    try {
        // Call the logout function from auth.js
        await logout();
    } catch (error) {
        console.error('Logout error:', error);
        // Force logout even on error
        removeAuthToken();
        window.location.href = 'login.html';
    }
}