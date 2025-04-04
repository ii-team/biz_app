// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Load service cards
    loadServices();
    
    // Listen for language changes
    document.addEventListener('languageChanged', function(e) {
        // Reload services when language changes
        loadServices(e.detail.language);
    });
});

