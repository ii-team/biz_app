from django.db import models 
class Organization(models.Model):
    org_name = models.CharField(max_length=1000)
    responsible_person = models.CharField(max_length=1000,null=True,blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=1000,null=True,blank=True)
    webpage = models.CharField(max_length=1000,null=True,blank=True)
    linkedin = models.CharField(max_length=1000,null=True,blank=True)
    profile_pic = models.FileField(null=True,blank=True,upload_to='static/profile_images/')
    description = models.TextField(null=True,blank=True)
    pdf = models.FileField(null=True,blank=True,upload_to='static/pdf/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
