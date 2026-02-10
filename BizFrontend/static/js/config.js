// Configuration - API Endpoints and Settings

// Backend API URL - Update this based on your environment
const BACKEND_URL = 'https://bizbackend.famsketch.eu';
// const BACKEND_URL = 'http://localhost:8003';


// Google OAuth Client ID - Get from Google Cloud Console
const GOOGLE_CLIENT_ID = '891480935469-3s8ndgrc86r0l548vglsibnstm8uocp1.apps.googleusercontent.com';

// Apple OAuth Client ID - Get from Apple Developer Portal
const APPLE_CLIENT_ID = 'com.yourdomain.biz';

// API Endpoints
const API_ENDPOINTS = {
    // Authentication
    SIGNUP: `${BACKEND_URL}/auth/signup`,
    VERIFY_OTP: `${BACKEND_URL}/auth/verify-otp`,
    RESEND_OTP: `${BACKEND_URL}/auth/resend-otp`,
    LOGIN: `${BACKEND_URL}/auth/login`,
    GOOGLE_AUTH: `${BACKEND_URL}/auth/google`,
    APPLE_AUTH: `${BACKEND_URL}/auth/apple`,
    AUTO_LOGIN: `${BACKEND_URL}/auth/auto-login`,
    LOGOUT: `${BACKEND_URL}/auth/logout`,
    FORGOT_PASSWORD: `${BACKEND_URL}/auth/forgot-password`,
    RESET_PASSWORD: `${BACKEND_URL}/auth/reset-password`,
    
    // Business Cards (existing)
    GET_BUSINESS_CARDS: `${BACKEND_URL}/getBusinessCards`,
    GET_BUSINESS_CARD: `${BACKEND_URL}/getBusinessCard`,
    CREATE_BUSINESS_CARD: `${BACKEND_URL}/createBusinessCard`,
    UPDATE_BUSINESS_CARD: `${BACKEND_URL}/updateBusinessCard`,
    DELETE_BUSINESS_CARD: `${BACKEND_URL}/deleteBusinessCard`,
    CHAT: `${BACKEND_URL}/chat`,
};

// Local Storage Keys
const STORAGE_KEYS = {
    AUTH_TOKEN: 'biz_auth_token',
    USER_DATA: 'biz_user_data',
    TEMP_EMAIL: 'biz_temp_email',
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        BACKEND_URL,
        GOOGLE_CLIENT_ID,
        APPLE_CLIENT_ID,
        API_ENDPOINTS,
        STORAGE_KEYS,
    };
}