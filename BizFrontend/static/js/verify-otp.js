// OTP Verification Page Logic

document.addEventListener('DOMContentLoaded', function() {
    // Check if email is available in session storage
    const email = getTempEmail();
    
    if (!email) {
        // No email found, redirect to signup
        window.location.href = 'signup.html';
        return;
    }
    
    // Display email
    document.getElementById('user-email').textContent = email;
    
    // Setup OTP inputs
    setupOTPInputs();
    
    // Handle OTP form submission
    const otpForm = document.getElementById('otp-form');
    otpForm.addEventListener('submit', handleOTPVerification);
    
    // Handle resend OTP
    const resendLink = document.getElementById('resend-otp');
    resendLink.addEventListener('click', handleResendOTP);
    
    // Start resend timer
    startResendTimer(60);
});

/**
 * Handle OTP verification
 */
async function handleOTPVerification(e) {
    e.preventDefault();
    hideMessage();
    
    const otp = getOTPValue();
    const email = getTempEmail();
    
    // Validate OTP
    if (otp.length !== 6) {
        showMessage('Please enter the complete 6-digit OTP', 'error');
        return;
    }
    
    // Set loading state
    setButtonLoading('verify-btn', true);
    
    try {
        const response = await makeAPIRequest(API_ENDPOINTS.VERIFY_OTP, 'POST', {
            email: email,
            otp: otp
        });
        
        if (response.success) {
            // Save token and user data
            saveAuthToken(response.token);
            saveUserData(response.user);
            
            // Remove temporary email
            removeTempEmail();
            
            showMessage('Verification successful! Redirecting...', 'success');
            
            // Redirect to index page
            setTimeout(() => {
                redirectToIndex();
            }, 1500);
        } else {
            showMessage(response.message || 'Invalid OTP', 'error');
            clearOTPInputs();
        }
    } catch (error) {
        showMessage('An error occurred. Please try again.', 'error');
        console.error('OTP verification error:', error);
    } finally {
        setButtonLoading('verify-btn', false);
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
        const response = await makeAPIRequest(API_ENDPOINTS.RESEND_OTP, 'POST', {
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