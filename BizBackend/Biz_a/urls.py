from django.urls import path
from . import views

urlpatterns = [
    path('getBusinessCards', views.get_business_cards, name='get_business_cards'),
    path('createBusinessCard', views.create_business_card, name='create_business_card'),
    path('updateBusinessCard', views.update_business_card, name='update_business_card'),
    path('deleteBusinessCard', views.delete_business_card, name='delete_business_card'),
    path('getBusinessCard', views.get_business_card, name='get_business_card'),
    path('chat', views.chat, name='chat'),
]
