// translations.js - Contains all site text in both languages

const translations = {
    "en": {
        // Header elements
        "title": "Biz",
        "home": "Home",
        "about": "About",
        "contact": "Contact",
        
    
        // Contact page elements
        "contact_us": "Contact Us",
        "address_title": "Address",
        "address_value": "iiTeam sro – Gorkého 6, Košice, Slovakia",
        "phone_title": "Phone",
        "phone_value": "+421 908 322 546",
        "email_title": "Email",
        "email_value": "info@iiteam.eu",
        "submit_org": "Submit Your Organization",
        "org_name": "Organization Name",
        "org_name_tooltip": "Name of your Organization",
        "org_name_placeholder": "Awesome Organization",
        "responsible_person": "Responsible Person",
        "responsible_person_tooltip": "Your name or name of person responsible for this organization",
        "responsible_person_placeholder": "John Doe",
        "email_label": "Email",
        "email_tooltip": "Email address for the responsible person or your organization",
        "email_placeholder": "johndoe@awesome.com",
        "phone_label": "Phone",
        "phone_tooltip": "Phone number for the responsible person or your organization",
        "phone_placeholder": "+1234567890",
        "webpage_label": "Webpage",
        "webpage_tooltip": "Website for your organization",
        "webpage_placeholder": "https://awesome-organization.com/",
        "linkedin_label": "Linkedin",
        "linkedin_tooltip": "Linkedin page for your organization",
        "linkedin_placeholder": "https://linkedin.com/in/awesomeOrganization",
        "pdf_label": "Company Banner",
        "pdf_tooltip": "Company Banner (used on cards and in listings). ",
        "profile_photo_label": "Your Photo",
        "profile_photo_tooltip": "Profile photo of your organization. This will be used as a profile picture for your card.",
        "description_label": "Description",
        "description_tooltip": "Description of your organization. This will be used as a description for your card.",
        "description_placeholder": "My Organization is AWESOME! Here are some facts about us...",
        "submit_button": "Submit",
        "company_logo_label": "Company Logo",
        "company_logo_tooltip": "Your organization's logo that will appear on the card.",
        
        "representative_photo_label": "Representative Photo",
        "representative_photo_tooltip": "Photo of the responsible person or representative of your organization.",
        
        "short_description_label": "Short Description",
        "short_description_tooltip": "A brief description (max 100 characters) that will appear on the front of your card.",
        "short_description_placeholder": "One-line description of your organization",
        "company_banner_label": "Company Banner",
        "company_banner_tooltip": "Company Banner (used on cards and in listings).",
        
    },
    "sk": {
        // Header elements
        "title": "Biz",
        "home": "Domov",
        "about": "O nás",
        "contact": "Kontakt",
        "company_banner_label": "Banner spoločnosti",
        "company_banner_tooltip": "Banner spoločnosti (používa sa na kartách a v zoznamoch).",
        
        
        // Contact page elements
        "contact_us": "Kontaktujte nás",
        "address_title": "Adresa",
        "address_value": "iiTeam sro – Gorkého 6, Košice, Slovensko",
        "phone_title": "Telefón",
        "phone_value": "+421 908 322 546",
        "email_title": "Email",
        "email_value": "info@iiteam.eu",
        "submit_org": "Pridajte vašu organizáciu",
        "org_name": "Názov organizácie",
        "org_name_tooltip": "Názov vašej organizácie",
        "org_name_placeholder": "Úžasná organizácia",
        "responsible_person": "Zodpovedná osoba",
        "responsible_person_tooltip": "Vaše meno alebo meno osoby zodpovednej za túto organizáciu",
        "responsible_person_placeholder": "Ján Novák",
        "email_label": "Email",
        "email_tooltip": "Emailová adresa zodpovednej osoby alebo vašej organizácie",
        "email_placeholder": "jannovak@uzasna.sk",
        "phone_label": "Telefón",
        "phone_tooltip": "Telefónne číslo zodpovednej osoby alebo vašej organizácie",
        "phone_placeholder": "+421123456789",
        "webpage_label": "Webová stránka",
        "webpage_tooltip": "Webová stránka vašej organizácie",
        "webpage_placeholder": "https://uzasna-organizacia.sk/",
        "linkedin_label": "Linkedin",
        "linkedin_tooltip": "Linkedin stránka vašej organizácie",
        "linkedin_placeholder": "https://linkedin.com/in/uzasnaOrganizacia",
        "pdf_label": "Company Banner",
        "pdf_tooltip": "Company Banner (used on cards and in listings).",
        "profile_photo_label": "Vaša fotografia",
        "profile_photo_tooltip": "Profilová fotografia vašej organizácie. Bude použitá ako profilový obrázok pre vašu kartu.",
        "description_label": "Popis",
        "description_tooltip": "Popis vašej organizácie. Bude použitý ako popis pre vašu kartu.",
        "description_placeholder": "Moja organizácia je ÚŽASNÁ! Tu sú nejaké fakty o nás...",
        "submit_button": "Odoslať",
        "company_logo_label": "Logo spoločnosti",
        "company_logo_tooltip": "Logo vašej organizácie, ktoré sa zobrazí na karte.",
        
        "representative_photo_label": "Fotografia zástupcu",
        "representative_photo_tooltip": "Fotografia zodpovednej osoby alebo zástupcu vašej organizácie.",
        
        "short_description_label": "Krátky popis",
        "short_description_tooltip": "Stručný popis (max. 100 znakov), ktorý sa zobrazí na prednej strane vašej karty.",
        "short_description_placeholder": "Jednoriadkový popis vašej organizácie"
    }
};

// Function to apply translations to all elements with data-key attribute
function applyTranslations(lang) {
    // Update all elements with data-key attribute
    document.querySelectorAll("[data-key]").forEach((element) => {
        const key = element.getAttribute("data-key");
        if (translations[lang][key]) {
            // Handle different types of elements
            if (element.tagName === "INPUT" || element.tagName === "TEXTAREA") {
                element.placeholder = translations[lang][key];
            } else if (element.tagName === "BUTTON") {
                element.textContent = translations[lang][key];
            } else {
                element.textContent = translations[lang][key];
            }
        }
    });
    
    // Update the page title
    document.querySelector("title").textContent = translations[lang]["title"];
    
    // Update header anchor tags with specific class
    document.querySelectorAll(".header_anchor_tags").forEach((el) => {
        const key = el.getAttribute("data-key") || el.textContent.toLowerCase();
        if (key && translations[lang][key]) {
            el.textContent = translations[lang][key];
        }
    });
}