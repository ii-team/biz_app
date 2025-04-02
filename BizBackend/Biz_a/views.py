from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os
from dotenv import load_dotenv 
load_dotenv()
import json
from rest_framework import viewsets
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import Http404
from rest_framework import filters, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.core.mail import send_mail


@api_view (['GET'])
def get_business_cards(request):
    Organizations = Organization.objects.all()
    serializer = OrganizationSerializer(Organizations, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view (['POST'])
def create_business_card(request):
    try:
        if "email" not in request.data or "org_name" not in request.data:
            return Response({
                'success': False,
                'message': 'Email and org name is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        email = request.data.get('email')
        org_name = request.data.get('org_name')

        if Organization.objects.filter(email=email).exists():
            return Response({
                'success': False,
                'message': 'Email already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if Organization.objects.filter(org_name=org_name).exists():
            return Response({
                'success': False,
                'message': 'Organization name already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        org = Organization.objects.create(
            org_name=request.data.get('org_name'),
            email=request.data.get('email'),
        )   
            # Extract form data
        if "responsible_person" in request.data:
            org.responsible_person = request.data.get('responsible_person')
        if "phone" in request.data:
            org.phone = request.data.get('phone')
        if "webpage" in request.data:
            org.webpage = request.data.get('webpage')
        if "linkedin" in request.data:
            org.linkedin = request.data.get('linkedin')
        if "description" in request.data:
            org.description = request.data.get('description')
        
        # Handle file uploads if present
        if 'profile_pic' in request.FILES:
            org.profile_pic = request.FILES['profile_pic']
        
        if 'pdf' in request.FILES:
            org.pdf = request.FILES['pdf']
            
        org.save()
        org = OrganizationSerializer(org)
        return Response({
            'success': True,
            'message': 'Organization created successfully',
            'org': org.data,
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        # Return error response
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['PUT'])
def update_business_card(request):
    try:
        if "email" not in request.data:
            return Response({
                'success': False,
                'message': 'Email is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        email = request.data.get('email')
        if not Organization.objects.filter(email=email).exists():
            return Response({
                'success': False,
                'message': 'Invalid email'
            }, status=status.HTTP_400_BAD_REQUEST)  

        # Get the organization instance
        organization = Organization.objects.get(email=email)
        
        # For form data with file uploads
        if "org_name" in request.data:
            organization.org_name = request.data.get('org_name')
        if "responsible_person" in request.data:
            organization.responsible_person = request.data.get('responsible_person')
        if "phone" in request.data:
            organization.phone = request.data.get('phone')
        if "webpage" in request.data:
            organization.webpage = request.data.get('webpage')
        if "linkedin" in request.data:
            organization.linkedin = request.data.get('linkedin')
        if "description" in request.data:
            organization.description = request.data.get('description')
        # Handle file uploads if present

        if 'profile_pic' in request.FILES:
            organization.profile_pic = request.FILES['profile_pic']
        if 'pdf' in request.FILES:
            organization.pdf = request.FILES['pdf']
        # Save the updated organization instance
        organization.save()
        # Serialize the updated organization instance
        org = OrganizationSerializer(organization)
        # Return success response
        return Response({
            'success': True,
            'message': 'Organization updated successfully',
            'org': org.data,
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        # Return error response
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def delete_business_card(request):
    try:
        if "email" not in request.data:
            return Response({
                'success': False,
                'message': 'Email is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        

        email = request.data.get('email')
        if not Organization.objects.filter(email=email).exists():
            return Response({
                'success': False,
                'message': 'Invalid Email'
            }, status=status.HTTP_400_BAD_REQUEST)  
        # Get the organization instance
        organization = Organization.objects.get(email=email)
        
        # Delete the organization instance
        organization.delete()
        
        # Return success response
        return Response({
            'success': True,
            'message': 'Organization deleted successfully'
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        # Return error response
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    
