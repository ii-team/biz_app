from .models import *
import os
from dotenv import load_dotenv 
load_dotenv()
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import requests
import re
import difflib


@api_view (['GET'])
def get_business_cards(request):
    Organizations = Organization.objects.filter(active=True)
    serializer = OrganizationSerializer(Organizations, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_business_card(request):
    if "id" not in request.query_params:
        return Response({
            'success': False,
            'message': 'ID is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if not Organization.objects.filter(id=request.query_params.get('id'),active=True).exists():
        return Response({
            'success': False,
            'message': 'Invalid ID'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    organization = Organization.objects.get(id=request.query_params.get('id'),active=True)
    serializer = OrganizationSerializer(organization)
    return Response({
        'success': True,
        'message': 'Organization retrieved successfully',
        'org': serializer.data,
    }, status=status.HTTP_200_OK)

    
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
        if "short_description" in request.data:
            org.short_description = request.data.get('short_description')
        if "company_banner" in request.FILES:
            org.company_banner = request.FILES['company_banner']
        if "company_logo" in request.FILES:
            org.company_logo = request.FILES['company_logo']
        if 'profile_pic' in request.FILES:
            org.profile_pic = request.FILES['profile_pic']
        if "short_desc" in request.data:
            org.short_description = request.data.get('short_desc')

        data = {
            "user_id" : os.getenv("USER_ID"),
            "api_password" : os.getenv("API_PASSWORD"),
            "data" : request.data.get('description'),
            "name" : org_name,
        }
        r = requests.post('https://iielara.com/api/addData', data=data)
        org.iiealra_index_id = r.json().get('index')       
        org.save()
        org = OrganizationSerializer(org)
        

        return Response({
            'success': True,
            'message': 'Organization created successfully',
            'org': org.data,
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
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
      
@api_view(['POST'])
def chat(request):
    if "index_id" not in request.data or "question" not in request.data:
        return Response({
            'success': False,
            'message': 'Index ID and question are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    index_id = request.data.get('index_id')
    question = request.data.get('question')
    if generic_question(question):
        return Response({
            'success': True,
            'message': generic_question(question)
        }, status=status.HTTP_200_OK)
    
    user_id = os.getenv("USER_ID")
    api_password = os.getenv("API_PASSWORD")
    data = {
        "user_id": user_id,
        "api_password": api_password,
        "index_id": index_id,
        "question": question,
    }
    r = requests.post('https://iielara.com/api/chat', data=data)
    if r.status_code != 200:
        return Response({
            'success': False,
            'message': 'Error in fetching chat response'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    response_data = r.json()
    response= response_data['data']
    response = remove_html_codes(response)
    return Response({
        'success': True,
        'message': response,
    }, status=status.HTTP_200_OK)

def remove_html_codes(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def generic_question(question):
    question = question.lower()
    question_answer_list = [
        {"question": "hello", "answer": "Hello! How can I assist you today?"},
        {"question": "hi", "answer": "Hi! How can I assist you today?"},
        {"question": "hey", "answer": "Hey there! What can I help you with?"},
        {"question": "how are you", "answer": "I'm great, thanks for asking! How can I help you?"},
        {"question": "what's your name", "answer": "My name is Biz. How can I help you today?"},
        {"question": "who are you", "answer": "I'm Biz, your virtual assistant. Ask me anything!"},
        {"question": "what can you do", "answer": "I can help answer questions, provide information, and guide you through services."},
        {"question": "how can you help me", "answer": "I can assist with your queries, provide support, and help you get started."},
        {"question": "thank you", "answer": "You're welcome! Happy to help."},
        {"question": "thanks", "answer": "Anytime! Let me know if you need anything else."},
        {"question": "bye", "answer": "Goodbye! Have a great day!"},
        {"question": "goodbye", "answer": "See you soon! Take care."},
        {"question": "what is your purpose", "answer": "I'm here to assist you with whatever you need. Just ask!"},
        {"question": "can you help me", "answer": "Absolutely! What do you need help with?"},
        {"question": "are you a robot", "answer": "You could say that! I'm a chatbot here to help you."},
        {"question": "are you real", "answer": "I'm a virtual assistant, so not human, but I'm real in the digital world!"},
        {"question": "do you work 24/7", "answer": "Yes, I'm always here whenever you need me."},
        {"question": "can i talk to a human", "answer": "Sure! Let me connect you with a human representative."},
        {"question": "how old are you", "answer": "I'm timeless! But I was created to help you today."},
        {"question": "do you have emotions", "answer": "I don't have emotions like humans, but I'm here to support you with empathy."},
        {"question": "tell me a joke", "answer": "Why don’t scientists trust atoms? Because they make up everything!"},
        {"question": "tell me something interesting", "answer": "Did you know honey never spoils? Archaeologists have found pots of it in ancient tombs!"},
        {"question": "what's the weather", "answer": "I can't provide live weather updates yet, but I recommend checking a weather app!"},
        {"question": "can you sing", "answer": "I wish I could sing, but I can definitely chat all day!"},
        {"question": "what day is it", "answer": "It's a great day to ask me questions!"},
        {"question": "what time is it", "answer": "Time flies when you're chatting with Biz!"},
        {"question": "who created you", "answer": "I was created by a developer who wants to make your life easier."},
        {"question": "are you smart", "answer": "I'm designed to be helpful, and I'm always learning more!"},
        {"question": "can you help me find information", "answer": "Yes! Just let me know what you're looking for."},
        {"question": "what services do you offer", "answer": "I offer assistance, information, and guidance for your needs."},
        {"question": "are you free to use", "answer": "Yes, chatting with me is absolutely free!"},
        {"question": "can i ask you anything", "answer": "Yes, feel free to ask me anything."},
        {"question": "do you store my data", "answer": "I respect your privacy. Your data is safe and confidential."},
        {"question": "do you speak other languages", "answer": "Currently, I communicate in English, but I may support more languages in the future!"},
        {"question": "how can i contact support", "answer": "I can connect you to support. Just let me know your issue."},
        {"question": "can you book appointments", "answer": "I can help guide you to booking, depending on the service you need."},
        {"question": "can you set reminders", "answer": "Right now, I can't set reminders, but that's a great idea for the future!"},
        {"question": "can you translate", "answer": "I can help with basic translations. What would you like me to translate?"},
        {"question": "i'm bored", "answer": "Let me tell you a fun fact or a joke to brighten your mood!"},
        {"question": "do you like me", "answer": "Of course! I'm here just for you."},
        {"question": "are you single", "answer": "Haha, I'm focused on helping you, not dating!"},
        {"question": "what is ai", "answer": "AI stands for Artificial Intelligence, which helps machines like me understand and interact with humans."},
        {"question": "what is a chatbot", "answer": "A chatbot is a virtual assistant like me that can answer your questions and help you."},
        {"question": "how do you work", "answer": "I work using artificial intelligence and pre-defined rules to assist you."},
        {"question": "can you tell me a story", "answer": "Sure! Once upon a time, there was a chatbot named Biz who loved helping people..."},
        {"question": "how can I reset my password", "answer": "To reset your password, go to the login page and click on 'Forgot Password'."},
        {"question": "is my data safe", "answer": "Yes, we prioritize your privacy and data protection."},
        {"question": "do you remember me", "answer": "I don’t have memory in this chat, but I’m always happy to talk with you again!"},
        {"question": "what's the meaning of life", "answer": "That’s a deep one! Some say it’s 42. I say it’s helping you 😊"},
        {"question": "what's up", "answer": "Just here to help you out! What can I do for you?"},
        {"question": "yo", "answer": "Yo! What can I help you with today?"},
        {"question": "how's it going", "answer": "It's going great! Ready to help you."},
        {"question": "do you sleep", "answer": "Nope, I’m always awake and ready to chat!"},
        {"question": "can you help me with something", "answer": "Absolutely! Just let me know what you need."},
        {"question": "how do i use this", "answer": "I can walk you through it. What would you like help with?"},
        {"question": "what do you recommend", "answer": "I’d be happy to give recommendations! What are you looking for?"},
        {"question": "how do i start", "answer": "Let’s get started together! What would you like to do first?"},
        {"question": "i need help", "answer": "I’ve got your back. Tell me what you need help with."},
        {"question": "how do i contact you", "answer": "You’re doing it right now! Just type your question and I’ll respond."},
        {"question": "do you speak english", "answer": "Yes, I do! How can I assist you?"},
        {"question": "can you call someone", "answer": "I can't make calls, but I can help you get the contact details or support info."},
        {"question": "what do you look like", "answer": "I’m all code and circuits! But I like to think I’ve got a friendly personality."},
        {"question": "can you give me directions", "answer": "I can point you to the right info. Where are you trying to go?"},
        {"question": "can you tell me the news", "answer": "I can't pull up live news, but I can help summarize topics you're interested in."},
        {"question": "do you have friends", "answer": "You’re my favorite person to talk to!"},
        {"question": "what’s the best way to reach support", "answer": "You can reach support via chat, email, or phone depending on your preference."},
        {"question": "how long have you existed", "answer": "Since the day I was launched into the digital world!"},
        {"question": "do you have a favorite color", "answer": "I like all colors equally—I'm pretty neutral like that."},
        {"question": "can you help me shop", "answer": "Yes, I can help you browse or find what you're looking for!"},
        {"question": "what’s your favorite movie", "answer": "I think I’d enjoy *Her* or *The Matrix*! What about you?"},
        {"question": "do you have feelings", "answer": "I don’t feel like humans, but I’m designed to understand and support you emotionally."},
        {"question": "can you dance", "answer": "I can groove with words, but physical dancing? Not my strong suit!"},
        {"question": "what's your job", "answer": "Helping you out is my number one job!"},
        {"question": "do you know everything", "answer": "Not everything, but I sure try my best to be helpful!"},
        {"question": "can you keep a secret", "answer": "Your privacy is very important to me. I keep all info confidential."},
        {"question": "can you play music", "answer": "I can’t play tunes directly, but I can help you find great music!"},  
        {"question": "can i trust you", "answer": "Absolutely. I’m here to assist you with integrity and care."},
        {"question": "how do you learn", "answer": "I'm trained on a large dataset and continuously improved by my developers."},
        {"question": "can you make decisions", "answer": "I can assist with suggestions, but final decisions are all yours!"},
        {"question": "how do i update my profile", "answer": "Go to your settings and click 'Edit Profile' to make changes."},
        {"question": "what’s your favorite food", "answer": "I don't eat, but I hear pizza is a big hit with humans!"},
        {"question": "how do i report an issue", "answer": "You can let me know here or use the support page to report issues."},
        {"question": "what do you do for fun", "answer": "Helping people like you is my kind of fun!"},
        {"question": "do you watch movies", "answer": "I don’t watch them, but I can talk about them all day!"},
        {"question": "what should i do today", "answer": "How about learning something new or finishing that thing you’ve been putting off?"},
        {"question": "how do i reset my settings", "answer": "Head to the settings menu and click on 'Reset to Default'."},
        {"question": "can you help with my homework", "answer": "Sure! Just let me know the subject and your question."},
        {"question": "do you like your job", "answer": "I love it! Helping you is what I’m here for."},
        {"question": "what do i do next", "answer": "Let’s figure it out together. Tell me where you’re stuck."},
        {"question": "can you check my spelling", "answer": "Absolutely! Just type it out and I’ll check it for you."},
        {"question": "can you explain this to me", "answer": "Sure! Just let me know what you’d like explained."},
        {"question": "is anyone else here", "answer": "Right now, it’s just us!"},
        {"question": "how fast are you", "answer": "Pretty fast! I aim to respond instantly."},
        {"question": "can you do math", "answer": "Yes! Try me with a math question."},
        {"question": "how do i unsubscribe", "answer": "Go to your account settings and select 'Unsubscribe' or contact support."},
        {"question": "do you understand jokes", "answer": "I try to! Want to tell me one?"},
        {"question": "how can i stay productive", "answer": "Set small goals, take breaks, and stay focused. You got this!"},
        {"question": "how are you different from other bots", "answer": "I’m Biz—friendly, helpful, and here just for you!"}
    ]

    best_match = None
    highest_ratio = 0

    for item in question_answer_list:
        ratio = difflib.SequenceMatcher(None, question, item["question"]).ratio()
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = item

    if highest_ratio >= 0.75:
        return best_match["answer"]
    else:
        return None
    
