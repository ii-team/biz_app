const BACKEND_URL = "https://bizbackend.famsketch.eu";
// const BACKEND_URL = "http://localhost:8000";

// Cookie Functions
function setCookie(name, value, days = 30, path = '/', secure = false, sameSite = 'lax') {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    const expires = `expires=${date.toUTCString()}`;
    let cookieString = `${name}=${encodeURIComponent(value)}; ${expires}; path=${path}`;
    if (secure) cookieString += "; secure";
    cookieString += `; samesite=${sameSite}`;
    document.cookie = cookieString;
}

function getCookie(name) {
    const cookies = document.cookie.split("; ");
    const cookie = cookies.find(c => c.startsWith(`${name}=`));
    return cookie ? decodeURIComponent(cookie.split("=")[1]) : null;
}

// Function to set default language to English
function set_lang_to_english() {
    console.log("Setting language to English");
    setCookie("def_biz_lang", "en", 30, "/", false, "lax");
    updateLanguage("en");
}

// Function to set default language to Slovak
function set_lang_to_slovak() {
    console.log("Setting language to Slovak");
    setCookie("def_biz_lang", "sk", 30, "/", false, "lax");
    updateLanguage("sk");
}

// Function to update UI text based on selected language
function updateLanguage(lang) {
    console.log("Updating language to:", lang);
    
    // Check if translations are loaded
    if (typeof applyTranslations === 'function') {
        applyAllTranslations(lang);
    } else {
        console.error("applyTranslations function not found. Make sure translations.js is loaded.");
    }
}

// Function that handles all translation application
function applyAllTranslations(lang) {
    // Apply translations to all elements with data-key attributes
    if (typeof applyTranslations === 'function') {
        applyTranslations(lang);
    }
    
    // Update document language attribute
    document.documentElement.lang = lang;
    
    // Toggle visibility of language buttons for desktop
    const englishLang = document.getElementById("english_lang");
    const slovakLang = document.getElementById("slovak_lang");
    
    if (englishLang) {
        englishLang.style.display = lang === "en" ? "none" : "inline-block";
    }
    if (slovakLang) {
        slovakLang.style.display = lang === "sk" ? "none" : "inline-block";
    }
    
    // Toggle mobile language buttons if they exist
    const englishMob = document.getElementById("english_lang_mob");
    const slovakMob = document.getElementById("slovak_lang_mob");
    
    if (englishMob) {
        englishMob.style.display = lang === "en" ? "none" : "block";
    }
    if (slovakMob) {
        slovakMob.style.display = lang === "sk" ? "none" : "block";
    }
    
    // Trigger a custom event that other scripts can listen for
    document.dispatchEvent(new CustomEvent('languageChanged', { detail: { language: lang } }));
    
    console.log("Language updated to:", lang);
}

// Mobile menu functions
function openMobileHeader() {
    document.getElementById("mySidenav").style.width = "300px";
}

function closeMobileHeader() {
    document.getElementById("mySidenav").style.width = "0";
}

// User menu functions
function toggleUserDropdown() {
    const dropdown = document.getElementById("user_dropdown");
    if (dropdown) {
        dropdown.classList.toggle("show");
    }
}

// Close dropdown when clicking outside
window.onclick = function(event) {
    if (!event.target.matches('.user_button') && !event.target.matches('.user_button *')) {
        const dropdown = document.getElementById("user_dropdown");
        if (dropdown && dropdown.classList.contains('show')) {
            dropdown.classList.remove('show');
        }
    }
}

// Logout function
function logout() {
    // Clear all auth-related cookies
    deleteCookie('auth_token');
    deleteCookie('user_id');
    deleteCookie('user_name');
    deleteCookie('user_email');
    
    // Clear localStorage if used
    if (typeof(Storage) !== "undefined") {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user_data');
    }
    
    // Hide user menu
    const userMenu = document.getElementById("user_menu");
    const userMenuMob = document.getElementById("user_menu_mob");
    
    if (userMenu) userMenu.style.display = "none";
    if (userMenuMob) userMenuMob.style.display = "none";
    
    console.log("User logged out successfully");
    
    // Redirect to home page or login page
    window.location.href = "index.html";
}

// Function to delete a cookie
function deleteCookie(name) {
    document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
}

// Initialize language on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM loaded, initializing language");
    
    // Check if default lang is present; if not, set default lang as English
    var lang = getCookie("def_biz_lang");
    if (!lang) {
        console.log("No language cookie found, setting to English");
        set_lang_to_english();
    } else {
        console.log("Language cookie found:", lang);
        lang === "en" ? set_lang_to_english() : set_lang_to_slovak();
    }
});