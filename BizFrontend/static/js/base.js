const BACKEND_URL = "http://127.0.0.1:8000"

// Check if default lang is present if not set deault lang as english
var lang = getCookie("def_biz_lang");
if (lang == null || lang == "") {
    set_lang_to_english();
}
else {
    if (lang == "en") {
        set_lang_to_english();
    }
    else {
        set_lang_to_slovak();
    }
}

// Function to set default language to English
function set_lang_to_english() {
    setCookie("def_biz_lang", "en", 30, "/", false, "lax");
    document.getElementById('english_lang').style.display = "none";
    document.getElementById('slovak_lang').style.display = "block";
    document.getElementById('english_lang_mob').style.display = "none";
    document.getElementById('slovak_lang_mob').style.display = "block";

}

// Function to set default language to Slovak
function set_lang_to_slovak() {
    setCookie("def_biz_lang", "sl", 30, "/", false, "lax");
    document.getElementById('english_lang').style.display = "block";
    document.getElementById('slovak_lang').style.display = "none";
    document.getElementById('english_lang_mob').style.display = "block";
    document.getElementById('slovak_lang_mob').style.display = "none";
}






function setCookie(name, value, days = 30, path = '/', secure = false, sameSite = 'lax') {
    // Create a date object for the expiry date
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    const expires = `expires=${date.toUTCString()}`;
    // Build cookie string
    let cookieString = `${name}=${encodeURIComponent(value)}; ${expires}; path=${path}`;
    // Add secure flag if needed
    if (secure) {
        cookieString += '; secure';
    }
    // Add SameSite attribute
    cookieString += `; samesite=${sameSite}`;
    // Set the cookie
    document.cookie = cookieString;
}

function getCookie(name) {
    // Get all cookies as a semicolon-separated string
    const cookies = document.cookie;
    // Split into individual cookies
    const cookieArray = cookies.split('; ');
    // Find the specific cookie we want
    const cookie = cookieArray.find(c => c.startsWith(`${name}=`));
    // Return the value if found, otherwise null
    return cookie ? decodeURIComponent(cookie.split('=')[1]) : null;
}



function openMobileHeader(){
    document.getElementById("mySidenav").style.width = "300px";
}
function closeMobileHeader(){
    document.getElementById("mySidenav").style.width = "0";
}