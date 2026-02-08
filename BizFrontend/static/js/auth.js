// Authentication Utilities - Common Functions

/**
 * Show message to user
 */
function showMessage(message, type = 'info') {
    const messageDiv = document.getElementById('auth-message');
    if (!messageDiv) return;
    
    messageDiv.textContent = message;
    messageDiv.className = `auth-message ${type}`;
    messageDiv.style.display = 'block';
    
    // Auto-hide success messages after 5 seconds
    if (type === 'success') {
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 5000);
    }
}

/**
 * Hide message
 */
function hideMessage() {
    const messageDiv = document.getElementById('auth-message');
    if (messageDiv) {
        messageDiv.style.display = 'none';
    }
}

/**
 * Toggle password visibility
 */
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const icon = document.getElementById(`${inputId}-icon`);
    
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

/**
 * Set loading state for button
 */
function setButtonLoading(buttonId, isLoading) {
    const button = document.getElementById(buttonId);
    if (!button) return;
    
    const btnText = button.querySelector('.btn-text');
    const btnLoader = button.querySelector('.btn-loader');
    
    if (isLoading) {
        button.disabled = true;
        if (btnText) btnText.style.display = 'none';
        if (btnLoader) btnLoader.style.display = 'inline-block';
    } else {
        button.disabled = false;
        if (btnText) btnText.style.display = 'inline-block';
        if (btnLoader) btnLoader.style.display = 'none';
    }
}

/**
 * Validate email format
 */
function validateEmail(email) {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailRegex.test(email);
}

/**
 * Validate password strength
 */
function validatePassword(password) {
    if (password.length < 8) {
        return {
            valid: false,
            message: 'Password must be at least 8 characters long'
        };
    }
    return {
        valid: true,
        message: 'Password is valid'
    };
}

/**
 * Save auth token to localStorage
 */
function saveAuthToken(token) {
    localStorage.setItem(STORAGE_KEYS.AUTH_TOKEN, token);
}

/**
 * Get auth token from localStorage
 */
function getAuthToken() {
    return localStorage.getItem(STORAGE_KEYS.AUTH_TOKEN);
}

/**
 * Remove auth token from localStorage
 */
function removeAuthToken() {
    localStorage.removeItem(STORAGE_KEYS.AUTH_TOKEN);
    localStorage.removeItem(STORAGE_KEYS.USER_DATA);
}

/**
 * Save user data to localStorage
 */
function saveUserData(userData) {
    localStorage.setItem(STORAGE_KEYS.USER_DATA, JSON.stringify(userData));
}

/**
 * Get user data from localStorage
 */
function getUserData() {
    const userData = localStorage.getItem(STORAGE_KEYS.USER_DATA);
    return userData ? JSON.parse(userData) : null;
}

/**
 * Check if user is authenticated
 */
function isAuthenticated() {
    return !!getAuthToken();
}

/**
 * Redirect to login page
 */
function redirectToLogin() {
    window.location.href = 'login.html';
}

/**
 * Redirect to index page
 */
function redirectToIndex() {
    window.location.href = 'index.html';
}

/**
 * Save temporary email (for OTP verification)
 */
function saveTempEmail(email) {
    sessionStorage.setItem(STORAGE_KEYS.TEMP_EMAIL, email);
}

/**
 * Get temporary email
 */
function getTempEmail() {
    return sessionStorage.getItem(STORAGE_KEYS.TEMP_EMAIL);
}

/**
 * Remove temporary email
 */
function removeTempEmail() {
    sessionStorage.removeItem(STORAGE_KEYS.TEMP_EMAIL);
}

/**
 * Make API request with error handling
 */
async function makeAPIRequest(url, method = 'GET', data = null) {
    try {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(url, options);
        const responseData = await response.json();
        
        return responseData;
    } catch (error) {
        console.error('API Request Error:', error);
        return {
            success: false,
            message: 'Network error. Please check your connection and try again.'
        };
    }
}

/**
 * Logout user
 */
async function logout() {
    try {
        // Call logout endpoint
        await makeAPIRequest(API_ENDPOINTS.LOGOUT, 'POST');
        
        // Clear local storage
        removeAuthToken();
        
        // Redirect to login
        redirectToLogin();
    } catch (error) {
        console.error('Logout error:', error);
        // Clear local storage anyway
        removeAuthToken();
        redirectToLogin();
    }
}

/**
 * Auto-login if token exists
 */
async function attemptAutoLogin() {
    const token = getAuthToken();
    
    if (!token) {
        return false;
    }
    
    try {
        const response = await makeAPIRequest(API_ENDPOINTS.AUTO_LOGIN, 'POST', { token });
        
        if (response.success) {
            saveUserData(response.user);
            return true;
        } else {
            // Token is invalid, remove it
            removeAuthToken();
            return false;
        }
    } catch (error) {
        console.error('Auto-login error:', error);
        removeAuthToken();
        return false;
    }
}

/**
 * OTP Input Auto-focus
 */
function setupOTPInputs() {
    const inputs = document.querySelectorAll('.otp-input');
    
    inputs.forEach((input, index) => {
        // Auto-focus next input
        input.addEventListener('input', (e) => {
            if (e.target.value.length === 1 && index < inputs.length - 1) {
                inputs[index + 1].focus();
            }
        });
        
        // Handle backspace
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Backspace' && !e.target.value && index > 0) {
                inputs[index - 1].focus();
            }
        });
        
        // Only allow numbers
        input.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^0-9]/g, '');
        });
        
        // Handle paste
        input.addEventListener('paste', (e) => {
            e.preventDefault();
            const pastedData = e.clipboardData.getData('text');
            const digits = pastedData.replace(/[^0-9]/g, '').split('');
            
            digits.forEach((digit, idx) => {
                if (index + idx < inputs.length) {
                    inputs[index + idx].value = digit;
                }
            });
            
            // Focus last filled input
            const lastIndex = Math.min(index + digits.length, inputs.length - 1);
            inputs[lastIndex].focus();
        });
    });
    
    // Focus first input on load
    if (inputs.length > 0) {
        inputs[0].focus();
    }
}

/**
 * Get OTP from inputs
 */
function getOTPValue() {
    const inputs = document.querySelectorAll('.otp-input');
    let otp = '';
    inputs.forEach(input => {
        otp += input.value;
    });
    return otp;
}

/**
 * Clear OTP inputs
 */
function clearOTPInputs() {
    const inputs = document.querySelectorAll('.otp-input');
    inputs.forEach(input => {
        input.value = '';
    });
    if (inputs.length > 0) {
        inputs[0].focus();
    }
}

/**
 * Start resend timer
 */
function startResendTimer(seconds = 60) {
    const resendLink = document.getElementById('resend-otp');
    const timerElement = document.getElementById('timer');
    
    if (!resendLink || !timerElement) return;
    
    let timeLeft = seconds;
    resendLink.classList.add('disabled');
    
    const timer = setInterval(() => {
        timeLeft--;
        timerElement.textContent = `Resend available in ${timeLeft}s`;
        
        if (timeLeft <= 0) {
            clearInterval(timer);
            timerElement.textContent = '';
            resendLink.classList.remove('disabled');
        }
    }, 1000);
}