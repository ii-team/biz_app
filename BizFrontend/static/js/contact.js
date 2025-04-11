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
    if (org_name == "" || responsible_person == "" || email == "" || phone == "" || webpage == "" || linkedin == "" || description == "" || short_desc == "") {
        document.getElementById("loader").style.display = "none";
        alert("Please fill in all fields.");
        return false;
    }
    var pdf = document.getElementById("company_banner");
    if (pdf && pdf.files && pdf.files.length > 0) {

    } else {
        document.getElementById("loader").style.display = "none";
        alert("Please attach PDF");
        return false; // No file selected
    }
    var profile_photo = document.getElementById("profile_photo");
    if (profile_photo && profile_photo.files && profile_photo.files.length > 0) {

    } else {
        document.getElementById("loader").style.display = "none";
        alert("Please attach Profile Photo");
        return false; // No file selected
    }
    var company_logo = document.getElementById("company_logo");
    if (company_logo && company_logo.files && company_logo.files.length > 0) {

    } else {
        document.getElementById("loader").style.display = "none";
        alert("Please attach Company Logo");
        return false; // No file selected
    }

    var formData = new FormData();
    formData.append("org_name", org_name);
    formData.append("responsible_person", responsible_person);
    formData.append("email", email);
    formData.append("phone", phone);
    formData.append("webpage", webpage);
    formData.append("linkedin", linkedin);
    formData.append("description", description);
    formData.append("company_banner", pdf.files[0]);
    formData.append("profile_pic", profile_photo.files[0]);
    formData.append("company_logo", company_logo.files[0]);
    formData.append("short_desc", short_desc);
    
    var xhr = new XMLHttpRequest();
    xhr.open("POST", BACKEND_URL + "/createBusinessCard", true);
    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 201) {
            document.getElementById("loader").style.display = "none";
            alert("Form submitted successfully.");
            document.getElementById("contact_form").reset();
        } else if (xhr.readyState == 4) {
            document.getElementById("loader").style.display = "none";
            alert("Error submitting form.");
        }
    };
    xhr.send(formData);
}
