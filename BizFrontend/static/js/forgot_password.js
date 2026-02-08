// Forgot Password Page Logic

document.addEventListener('DOMContentLoaded', function() {
    // Handle forgot password form submission
    const forgotPasswordForm = document.getElementById('forgot-password-form');
    forgotPasswordForm.addEventListener('submit', handleForgotPassword);
});

/**
 * Handle forgot password
 */
async function handleForgotPassword(e) {
    e.preventDefault();
    hideMessage();
    
    const email = document.getElementById('email').value.trim();
    
    // Validate email
    if (!validateEmail(email)) {
        showMessage('Please enter a valid email address', 'error');
        return;
    }
    
    // Set loading state
    setButtonLoading('send-otp-btn', true);
    
    try {
        const response = await makeAPIRequest(API_ENDPOINTS.FORGOT_PASSWORD, 'POST', {
            email: email
        });
        
        if (response.success) {
            // Save email temporarily for password reset
            saveTempEmail(email);
            
            showMessage('Reset code sent! Redirecting...', 'success');
            
            // Redirect to reset password page
            setTimeout(() => {
                window.location.href = 'reset-password.html';
            }, 1500);
        } else {
            showMessage(response.message || 'Failed to send reset code', 'error');
        }
    } catch (error) {
        showMessage('An error occurred. Please try again.', 'error');
        console.error('Forgot password error:', error);
    } finally {
        setButtonLoading('send-otp-btn', false);
    }
}