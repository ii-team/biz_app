from django.urls import path
from . import views

urlpatterns = [
    path('getBusinessCards', views.get_business_cards, name='get_business_cards'),
    path('createBusinessCard', views.create_business_card, name='create_business_card'),
    path('updateBusinessCard', views.update_business_card, name='update_business_card'),
    path('deleteBusinessCard', views.delete_business_card, name='delete_business_card'),
    path('getBusinessCard', views.get_business_card, name='get_business_card'),
    path('chat', views.chat, name='chat'),
    path('auth/signup', views.signup, name='signup'),
    path('auth/verify-otp', views.verify_otp, name='verify_otp'),
    path('auth/resend-otp', views.resend_otp, name='resend_otp'),
    path('auth/login', views.login, name='login'),
    path('auth/google', views.google_auth, name='google_auth'),
    path('auth/apple', views.apple_auth, name='apple_auth'),
    path('auth/auto-login', views.auto_login, name='auto_login'),
    path('auth/logout', views.logout, name='logout'),
    path('auth/forgot-password', views.forgot_password, name='forgot_password'),
    path('auth/reset-password', views.reset_password, name='reset_password'),
]
