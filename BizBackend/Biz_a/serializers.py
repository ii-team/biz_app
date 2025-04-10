from rest_framework import serializers 
from .models import Organization
import os 

class OrganizationSerializer(serializers.ModelSerializer): 
    profile_pic = serializers.SerializerMethodField()
    company_banner = serializers.SerializerMethodField()
    company_logo = serializers.SerializerMethodField()

    class Meta: 
        model = Organization 
        fields = '__all__'

    def get_profile_pic(self, obj):
        if obj.profile_pic and hasattr(obj.profile_pic, 'url'):
            return os.getenv('BASE_URL') + obj.profile_pic.url
        return None

    def get_company_banner(self, obj):
        if obj.company_banner and hasattr(obj.company_banner, 'url'):
            return os.getenv('BASE_URL') + obj.company_banner.url
        return None
    
    def get_company_logo(self, obj):
        if obj.company_logo and hasattr(obj.company_logo, 'url'):
            return os.getenv('BASE_URL') + obj.company_logo.url
        return None
    
    
    
