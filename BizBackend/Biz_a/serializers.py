from rest_framework import serializers 
from .models import Organization, User, OrganizationPDF
import os 

class OrganizationPDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationPDF
        fields = ['id', 'pdf_file', 'file_name', 'uploaded_at']

class OrganizationSerializer(serializers.ModelSerializer): 
    profile_pic = serializers.SerializerMethodField()
    company_banner = serializers.SerializerMethodField()
    pdfs = OrganizationPDFSerializer(many=True, read_only=True)
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

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'name',
            'profile_picture',
            'auth_provider',
            'is_verified',
            'created_at',
            'last_login'
        ]
        read_only_fields = ['id', 'created_at', 'last_login']
    
    def to_representation(self, instance):
        """
        Customize the output representation
        """
        data = super().to_representation(instance)
        
        # Format dates
        if data.get('created_at'):
            data['created_at'] = instance.created_at.strftime('%Y-%m-%d %H:%M:%S')
        if data.get('last_login'):
            data['last_login'] = instance.last_login.strftime('%Y-%m-%d %H:%M:%S')
        
        return data