from rest_framework import serializers 
from .models import Organization
import os 

class OrganizationSerializer(serializers.ModelSerializer): 
    profile_pic = serializers.SerializerMethodField()
    pdf = serializers.SerializerMethodField()

    class Meta: 
        model = Organization 
        fields = '__all__'

    def get_profile_pic(self, obj):
        if obj.profile_pic and hasattr(obj.profile_pic, 'url'):
            return os.getenv('BASE_URL') + obj.profile_pic.url
        return None
    
    def get_pdf(self, obj):
        if obj.pdf and hasattr(obj.pdf, 'url'):
            return os.getenv('BASE_URL') + obj.pdf.url
        return None
    
