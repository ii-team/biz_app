// Reset Password Page Logic

document.addEventListener('DOMContentLoaded', function() {
    // Check if email is available in session storage
    const email = getTempEmail();
    
    if (!email) {
        // No email found, redirect to forgot password
        window.location.href = 'forgot-password.html';
        return;
    }
    
    // Display email
    document.getElementById('user-email').textContent = email;
    
    // Setup OTP inputs
    setupOTPInputs();
    
    // Handle reset password form submission
    const resetPasswordForm = document.getElementById('reset-password-form');
    resetPasswordForm.addEventListener('submit', handleResetPassword);
    
    // Handle resend OTP
    const resendLink = document.getElementById('resend-otp');
    resendLink.addEventListener('click', handleResendOTP);
    
    // Start resend timer
    startResendTimer(60);
});

/**
 * Handle reset password
 */
async function handleResetPassword(e) {
    e.preventDefault();
    hideMessage();
    
    const otp = getOTPValue();
    const email = getTempEmail();
    const newPassword = document.getElementById('new-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    
    // Validate inputs
    if (otp.length !== 6) {
        showMessage('Please enter the complete 6-digit OTP', 'error');
        return;
    }
    
    const passwordValidation = validatePassword(newPassword);
    if (!passwordValidation.valid) {
        showMessage(passwordValidation.message, 'error');
        return;
    }
    
    if (newPassword !== confirmPassword) {
        showMessage('Passwords do not match', 'error');
        return;
    }
    
    // Set loading state
    setButtonLoading('reset-btn', true);
    
    try {
        const response = await makeAPIRequest(API_ENDPOINTS.RESET_PASSWORD, 'POST', {
            email: email,
            otp: otp,
            new_password: newPassword
        });
        
        if (response.success) {
            // Remove temporary email
            removeTempEmail();
            
            showMessage('Password reset successful! Redirecting to login...', 'success');
            
            // Redirect to login page
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 2000);
        } else {
            showMessage(response.message || 'Password reset failed', 'error');
            clearOTPInputs();
        }
    } catch (error) {
        showMessage('An error occurred. Please try again.', 'error');
        console.error('Reset password error:', error);
    } finally {
        setButtonLoading('reset-btn', false);
    }
}

/**
 * Handle resend OTP
 */
async function handleResendOTP(e) {
    e.preventDefault();
    hideMessage();
    
    const resendLink = e.target;
    if (resendLink.classList.contains('disabled')) {
        return;
    }
    
    const email = getTempEmail();
    
    try {
        const response = await makeAPIRequest(API_ENDPOINTS.FORGOT_PASSWORD, 'POST', {
            email: email
        });
        
        if (response.success) {
            showMessage('OTP resent successfully! Check your email.', 'success');
            clearOTPInputs();
            startResendTimer(60);
        } else {
            showMessage(response.message || 'Failed to resend OTP', 'error');
        }
    } catch (error) {
        showMessage('An error occurred. Please try again.', 'error');
        console.error('Resend OTP error:', error);
    }
}