function submit_contact_form() {
    // start loader
    document.getElementById("loader").style.display = "flex";
    
    var org_name = document.getElementById("org_name").value;
    var responsible_person = document.getElementById("responsible_person").value;
    var email = document.getElementById("email").value;
    var phone = document.getElementById("phone").value;
    var webpage = document.getElementById("webpage").value;
    var linkedin = document.getElementById("linkedin").value;
    var description = document.getElementById("description").value;
    var short_desc = document.getElementById("short_desc").value;
    
    // Validate required text fields
    if (org_name == "" || responsible_person == "" || email == "" || phone == "" || webpage == "" || linkedin == "" || description == "" || short_desc == "") {
        document.getElementById("loader").style.display = "none";
        alert("Please fill in all fields.");
        return false;
    }
    
    // Validate company banner (image)
    var company_banner = document.getElementById("company_banner");
    if (!company_banner || !company_banner.files || company_banner.files.length === 0) {
        document.getElementById("loader").style.display = "none";
        alert("Please attach Company Banner");
        return false;
    }
    
    // Validate profile photo (image)
    var profile_photo = document.getElementById("profile_photo");
    if (!profile_photo || !profile_photo.files || profile_photo.files.length === 0) {
        document.getElementById("loader").style.display = "none";
        alert("Please attach Profile Photo");
        return false;
    }
    
    // Validate company logo (image)
    var company_logo = document.getElementById("company_logo");
    if (!company_logo || !company_logo.files || company_logo.files.length === 0) {
        document.getElementById("loader").style.display = "none";
        alert("Please attach Company Logo");
        return false;
    }
    
    // Validate PDF files (multiple)
    var pdf_files = document.getElementById("pdf_files");
    if (!pdf_files || !pdf_files.files || pdf_files.files.length === 0) {
        document.getElementById("loader").style.display = "none";
        alert("Please attach at least one PDF document");
        return false;
    }

    // Create FormData object
    var formData = new FormData();
    formData.append("org_name", org_name);
    formData.append("responsible_person", responsible_person);
    formData.append("email", email);
    formData.append("phone", phone);
    formData.append("webpage", webpage);
    formData.append("linkedin", linkedin);
    formData.append("description", description);
    formData.append("short_desc", short_desc);
    formData.append("company_banner", company_banner.files[0]);
    formData.append("profile_pic", profile_photo.files[0]);
    formData.append("company_logo", company_logo.files[0]);
    
    // Append all PDF files
    for (var i = 0; i < pdf_files.files.length; i++) {
        formData.append("pdf_files", pdf_files.files[i]);
    }
    
    // Send AJAX request
    var xhr = new XMLHttpRequest();
    xhr.open("POST", BACKEND_URL + "/createBusinessCard", true);
    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 201) {
            document.getElementById("loader").style.display = "none";
            alert("Form submitted successfully.");
            
            // Reset form fields
            document.getElementById("org_name").value = "";
            document.getElementById("responsible_person").value = "";
            document.getElementById("email").value = "";
            document.getElementById("phone").value = "";
            document.getElementById("webpage").value = "";
            document.getElementById("linkedin").value = "";
            document.getElementById("description").value = "";
            document.getElementById("short_desc").value = "";
            document.getElementById("company_banner").value = "";
            document.getElementById("profile_photo").value = "";
            document.getElementById("company_logo").value = "";
            document.getElementById("pdf_files").value = "";
            document.getElementById("pdf_file_count").textContent = "No files selected";
        } else if (xhr.readyState == 4) {
            document.getElementById("loader").style.display = "none";
            alert("Error submitting form.");
        }
    };
    
    xhr.send(formData);
}