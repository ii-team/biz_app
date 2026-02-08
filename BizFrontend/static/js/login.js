// Login Page Logic

document.addEventListener('DOMContentLoaded', async function() {
    // Check if user is already logged in
    const isLoggedIn = await attemptAutoLogin();
    if (isLoggedIn) {
        redirectToIndex();
        return;
    }
    
    // Handle login form submission
    const loginForm = document.getElementById('login-form');
    loginForm.addEventListener('submit', handleLogin);
    
    // Initialize Google Sign-In
    initializeGoogleSignIn();
    
    // Initialize Apple Sign-In
    initializeAppleSignIn();
});

/**
 * Handle email/password login
 */
async function handleLogin(e) {
    e.preventDefault();
    hideMessage();
    
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    
    // Validate inputs
    if (!validateEmail(email)) {
        showMessage('Please enter a valid email address', 'error');
        return;
    }
    
    if (!password) {
        showMessage('Please enter your password', 'error');
        return;
    }
    
    // Set loading state
    setButtonLoading('login-btn', true);
    
    try {
        const response = await makeAPIRequest(API_ENDPOINTS.LOGIN, 'POST', {
            email: email,
            password: password
        });
        
        if (response.success) {
            // Save token and user data
            saveAuthToken(response.token);
            saveUserData(response.user);
            
            showMessage('Login successful! Redirecting...', 'success');
            
            // Redirect to index page
            setTimeout(() => {
                redirectToIndex();
            }, 1000);
        } else {
            showMessage(response.message || 'Login failed', 'error');
        }
    } catch (error) {
        showMessage('An error occurred. Please try again.', 'error');
        console.error('Login error:', error);
    } finally {
        setButtonLoading('login-btn', false);
    }
}

/**
 * Initialize Google Sign-In
 */
// function initializeGoogleSignIn() {
//     const waitForGoogle = setInterval(() => {
//         if (window.google && google.accounts && google.accounts.id) {
//             clearInterval(waitForGoogle);

//             google.accounts.id.initialize({
//                 client_id: GOOGLE_CLIENT_ID,
//                 callback: handleGoogleSignIn,
//                 auto_select: false,
//             });

//             const googleBtn = document.getElementById('google-signin-btn');
//             if (googleBtn) {
//                 googleBtn.addEventListener('click', () => {
//                     google.accounts.id.prompt();
//                 });
//             }

//             console.log('✅ Google Sign-In initialized');
//         }
//     }, 100);
// }

function initializeGoogleSignIn() {
    if (!window.google || !google.accounts || !google.accounts.id) {
        console.error('Google GSI not loaded');
        return;
    }

    google.accounts.id.initialize({
        client_id: GOOGLE_CLIENT_ID,
        callback: handleGoogleSignIn,
    });

    // Render button INSIDE your existing button
    google.accounts.id.renderButton(
        document.getElementById('google-signin-btn'),
        {
            theme: 'outline',
            size: 'large',
            text: 'continue_with',
            shape: 'rectangular',
        }
    );
}



/**
 * Handle Google Sign-In response
 */
async function handleGoogleSignIn(response) {
    hideMessage();
    setButtonLoading('google-signin-btn', true);
    
    try {
        const apiResponse = await makeAPIRequest(API_ENDPOINTS.GOOGLE_AUTH, 'POST', {
            token: response.credential
        });
        
        if (apiResponse.success) {
            // Save token and user data
            saveAuthToken(apiResponse.token);
            saveUserData(apiResponse.user);
            
            showMessage('Google login successful! Redirecting...', 'success');
            
            // Redirect to index page
            setTimeout(() => {
                redirectToIndex();
            }, 1000);
        } else {
            showMessage(apiResponse.message || 'Google login failed', 'error');
        }
    } catch (error) {
        showMessage('Google login failed. Please try again.', 'error');
        console.error('Google login error:', error);
    } finally {
        setButtonLoading('google-signin-btn', false);
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
        
        const appleBtn = document.getElementById('apple-signin-btn');
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
    setButtonLoading('apple-signin-btn', true);
    
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
            
            showMessage('Apple login successful! Redirecting...', 'success');
            
            // Redirect to index page
            setTimeout(() => {
                redirectToIndex();
            }, 1000);
        } else {
            showMessage(apiResponse.message || 'Apple login failed', 'error');
        }
    } catch (error) {
        if (error.error !== 'popup_closed_by_user') {
            showMessage('Apple login failed. Please try again.', 'error');
            console.error('Apple login error:', error);
        }
    } finally {
        setButtonLoading('apple-signin-btn', false);
    }
}