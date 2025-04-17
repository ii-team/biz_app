const BACKEND_URL = "https://bizbackend.famsketch.eu";

// Check if default lang is present; if not, set default lang as English
var lang = getCookie("def_biz_lang");
if (!lang) {
    set_lang_to_english();
} else {
    lang === "en" ? set_lang_to_english() : set_lang_to_slovak();
}

// Function to set default language to English
function set_lang_to_english() {
    setCookie("def_biz_lang", "en", 30, "/", false, "lax");
    updateLanguage("en");
}

// Function to set default language to Slovak
function set_lang_to_slovak() {
    setCookie("def_biz_lang", "sk", 30, "/", false, "lax");
    updateLanguage("sk");
}

// Function to update UI text based on selected language
function updateLanguage(lang) {
    // Try to load translations if not already loaded
    if (typeof translations === 'undefined') {
        fetch("static/js/translations.js")
            .then(response => response.text())
            .then(text => {
                eval(text); // Load translations
                applyAllTranslations(lang);
            })
            .catch(error => {
                console.error("Failed to load translations:", error);
            });
    } else {
        // Translations already loaded, apply them
        applyAllTranslations(lang);
    }
}

// Function that handles all translation application
function applyAllTranslations(lang) {
    // Apply translations to all elements with data-key attributes
    applyTranslations(lang);
    
    // Update document language attribute
    document.documentElement.lang = lang;
    
    // Toggle visibility of language buttons
    document.getElementById("english_lang").style.display = lang === "en" ? "none" : "block";
    document.getElementById("slovak_lang").style.display = lang === "en" ? "block" : "none";
    
    // Toggle mobile language buttons if they exist
    const englishMob = document.getElementById("english_lang_mob");
    const slovakMob = document.getElementById("slovak_lang_mob");
    
    if (englishMob) englishMob.style.display = lang === "en" ? "none" : "block";
    if (slovakMob) slovakMob.style.display = lang === "en" ? "block" : "none";
    
    // Trigger a custom event that other scripts can listen for
    document.dispatchEvent(new CustomEvent('languageChanged', { detail: { language: lang } }));
}

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

// Mobile menu functions
function openMobileHeader() {
    document.getElementById("mySidenav").style.width = "300px";
}
function closeMobileHeader() {
    document.getElementById("mySidenav").style.width = "0";
}
