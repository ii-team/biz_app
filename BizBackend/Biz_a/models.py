from django.db import models 
from django.contrib.auth.hashers import make_password

class Organization(models.Model):
    org_name = models.CharField(max_length=1000)
    responsible_person = models.CharField(max_length=1000,null=True,blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=1000,null=True,blank=True)
    webpage = models.CharField(max_length=1000,null=True,blank=True)
    linkedin = models.CharField(max_length=1000,null=True,blank=True)
    profile_pic = models.FileField(null=True,blank=True,upload_to='static/profile_images/')
    company_banner = models.FileField(null=True,blank=True,upload_to='static/company_banners/')
    company_logo = models.FileField(null=True,blank=True,upload_to='static/company_logos/')
    short_description = models.TextField(null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    active = models.BooleanField(default=False)
    iiealra_index_id = models.CharField(max_length=1000,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class User(models.Model):
    """
    Custom User model for authentication
    """
    AUTH_PROVIDERS = (
        ('email', 'Email'),
        ('google', 'Google'),
        ('apple', 'Apple'),
    )
    
    email = models.EmailField(unique=True, db_index=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.URLField(null=True, blank=True)
    
    # OAuth IDs
    google_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
    apple_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
    
    # Authentication provider
    auth_provider = models.CharField(max_length=10, choices=AUTH_PROVIDERS, default='email')
    
    # Verification status
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        # Ensure email is lowercase
        if self.email:
            self.email = self.email.lower().strip()
        super().save(*args, **kwargs)


class OTPVerification(models.Model):
    """
    Model to store OTP for email verification and password reset
    """
    email = models.EmailField(db_index=True)
    otp = models.CharField(max_length=6)
    
    # Temporary storage for signup data
    temp_password = models.CharField(max_length=255, null=True, blank=True)
    temp_name = models.CharField(max_length=255, null=True, blank=True)
    
    # OTP metadata
    is_password_reset = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'otp_verifications'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.email} - {self.otp}"