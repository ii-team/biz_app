// Signup Page Logic

document.addEventListener('DOMContentLoaded', async function() {
    // Check if user is already logged in
    const isLoggedIn = await attemptAutoLogin();
    if (isLoggedIn) {
        redirectToIndex();
        return;
    }
    
    // Handle signup form submission
    const signupForm = document.getElementById('signup-form');
    signupForm.addEventListener('submit', handleSignup);
    
    // Initialize Google Sign-In
    initializeGoogleSignIn();
    
    // Initialize Apple Sign-In
    initializeAppleSignIn();
});

/**
 * Handle email/password signup
 */
async function handleSignup(e) {
    e.preventDefault();
    hideMessage();
    
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    
    // Validate inputs
    if (!name) {
        showMessage('Please enter your full name', 'error');
        return;
    }
    
    if (!validateEmail(email)) {
        showMessage('Please enter a valid email address', 'error');
        return;
    }
    
    const passwordValidation = validatePassword(password);
    if (!passwordValidation.valid) {
        showMessage(passwordValidation.message, 'error');
        return;
    }
    
    if (password !== confirmPassword) {
        showMessage('Passwords do not match', 'error');
        return;
    }
    
    // Set loading state
    setButtonLoading('signup-btn', true);
    
    try {
        const response = await makeAPIRequest(API_ENDPOINTS.SIGNUP, 'POST', {
            name: name,
            email: email,
            password: password
        });
        
        if (response.success) {
            // Save email temporarily for OTP verification
            saveTempEmail(email);
            
            showMessage('Account created! Redirecting to OTP verification...', 'success');
            
            // Redirect to OTP verification page
            setTimeout(() => {
                window.location.href = 'verify-otp.html';
            }, 1500);
        } else {
            showMessage(response.message || 'Signup failed', 'error');
        }
    } catch (error) {
        showMessage('An error occurred. Please try again.', 'error');
        console.error('Signup error:', error);
    } finally {
        setButtonLoading('signup-btn', false);
    }
}

/**
 * Initialize Google Sign-In
 */
function initializeGoogleSignIn() {
    if (typeof google !== 'undefined') {
        google.accounts.id.initialize({
            client_id: GOOGLE_CLIENT_ID,
            callback: handleGoogleSignIn,
            auto_select: false,
        });
        
        const googleBtn = document.getElementById('google-signup-btn');
        if (googleBtn) {
            googleBtn.addEventListener('click', () => {
                google.accounts.id.prompt();
            });
        }
    }
}

/**
 * Handle Google Sign-In response
 */
async function handleGoogleSignIn(response) {
    hideMessage();
    setButtonLoading('google-signup-btn', true);
    
    try {
        const apiResponse = await makeAPIRequest(API_ENDPOINTS.GOOGLE_AUTH, 'POST', {
            token: response.credential
        });
        
        if (apiResponse.success) {
            // Save token and user data
            saveAuthToken(apiResponse.token);
            saveUserData(apiResponse.user);
            
            showMessage('Google signup successful! Redirecting...', 'success');
            
            // Redirect to index page
            setTimeout(() => {
                redirectToIndex();
            }, 1000);
        } else {
            showMessage(apiResponse.message || 'Google signup failed', 'error');
        }
    } catch (error) {
        showMessage('Google signup failed. Please try again.', 'error');
        console.error('Google signup error:', error);
    } finally {
        setButtonLoading('google-signup-btn', false);
    }
}

/**
 * Initialize Apple Sign-In
 */
function initializeAppleSignIn() {
    if (typeof AppleID !== 'undefined') {
        AppleID.auth.init({
            clientId: APPLE_CLIENT_ID,
            scope: 'name email',
            redirectURI: window.location.origin,
            usePopup: true
        });
        
        const appleBtn = document.getElementById('apple-signup-btn');
        if (appleBtn) {
            appleBtn.addEventListener('click', handleAppleSignIn);
        }
    }
}

/**
 * Handle Apple Sign-In
 */
async function handleAppleSignIn() {
    hideMessage();
    setButtonLoading('apple-signup-btn', true);
    
    try {
        const response = await AppleID.auth.signIn();
        
        const apiResponse = await makeAPIRequest(API_ENDPOINTS.APPLE_AUTH, 'POST', {
            token: response.authorization.id_token,
            user: response.user
        });
        
        if (apiResponse.success) {
            // Save token and user data
            saveAuthToken(apiResponse.token);
            saveUserData(apiResponse.user);
            
            showMessage('Apple signup successful! Redirecting...', 'success');
            
            // Redirect to index page
            setTimeout(() => {
                redirectToIndex();
            }, 1000);
        } else {
            showMessage(apiResponse.message || 'Apple signup failed', 'error');
        }
    } catch (error) {
        if (error.error !== 'popup_closed_by_user') {
            showMessage('Apple signup failed. Please try again.', 'error');
            console.error('Apple signup error:', error);
        }
    } finally {
        setButtonLoading('apple-signup-btn', false);
    }
}