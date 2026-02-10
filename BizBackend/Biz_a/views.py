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
from deep_translator import GoogleTranslator
from django.contrib.auth.hashers import make_password
import difflib
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import User, OTPVerification
from .serializers import UserSerializer
import os
from dotenv import load_dotenv
import secrets
import string
from datetime import datetime, timedelta
import jwt
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import requests



@api_view (['GET'])
def get_business_cards(request):
    Organizations = Organization.objects.filter(active=True)
    serializer = OrganizationSerializer(Organizations, many=True)
    print(serializer.data)
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

@api_view(['POST'])
def create_business_card(request):
    try:
        if "email" not in request.data or "org_name" not in request.data:
            print(1)
            return Response({
                'success': False,
                'message': 'Email and org name is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        email = request.data.get('email')
        org_name = request.data.get('org_name')
        
        if Organization.objects.filter(email=email).exists():
            print(2)
            return Response({
                'success': False,
                'message': 'Email already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if Organization.objects.filter(org_name=org_name).exists():
            print(3)
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

        org.save()

        # Handle multiple PDF uploads
        pdf_files = request.FILES.getlist('pdf_files')  # Get list of files
        if pdf_files:
            for pdf_file in pdf_files:
                OrganizationPDF.objects.create(
                    organization=org,
                    pdf_file=pdf_file,
                    file_name=pdf_file.name
                )

        # Existing API calls
        data = {
            "user_id": os.getenv("USER_ID"),
            "api_password": os.getenv("API_PASSWORD"),
            "data": request.data.get('description'),
            "name": org_name,
        }
        r = requests.post('https://iielara.com/api/addData', data=data)
        org.iiealra_index_id = r.json().get('index')       
        org.save()

        data_of_company = f'''\n\n-----------------------\n 
        Organization Name: {org_name} \n 
        Email: {email} \n 
        Responseible Person: {request.data.get('responsible_person')}  \n
        Phone: {request.data.get('phone')} \n
        Webpage: {request.data.get('webpage')} \n
        LinkedIn: {request.data.get('linkedin')} \n
        Short Description: {request.data.get('short_desc')} \n
        -----------------------
        '''

        # base biz data update
        data = {
            "user_id": os.getenv("USER_ID"),
            "api_password": os.getenv("API_PASSWORD"),
            "index_id": os.getenv("INDEX_ID"),
            "data": data_of_company,
            "method": "append"
        }
        r = requests.post('https://iielara.com/api/updateData', data=data)
        if r.status_code != 200:
            print(r.text)
            return Response({
                'success': False,
                'message': 'Error in fetching chat response'
            }, status=status.HTTP_400_BAD_REQUEST)        

        org_serializer = OrganizationSerializer(org)
        return Response({
            'success': True,
            'message': 'Organization created successfully',
            'org': org_serializer.data,
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        print(e)
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

        organization = Organization.objects.get(email=email)
        
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
        if 'profile_pic' in request.FILES:
            organization.profile_pic = request.FILES['profile_pic']

        organization.save()

        # Handle multiple PDF uploads for update
        pdf_files = request.FILES.getlist('pdf_files')
        if pdf_files:
            # Option 1: Add new PDFs without deleting old ones
            for pdf_file in pdf_files:
                OrganizationPDF.objects.create(
                    organization=organization,
                    pdf_file=pdf_file,
                    file_name=pdf_file.name
                )
            
            # Option 2: Replace all PDFs (uncomment if you want this behavior)
            # organization.pdfs.all().delete()
            # for pdf_file in pdf_files:
            #     OrganizationPDF.objects.create(
            #         organization=organization,
            #         pdf_file=pdf_file,
            #         file_name=pdf_file.name
            #     )

        org = OrganizationSerializer(organization)
        return Response({
            'success': True,
            'message': 'Organization updated successfully',
            'org': org.data,
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
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
    try:
        if "index_id" not in request.data or "question" not in request.data or "language" not in request.data:
            return Response({
                'success': False,
                'message': 'Index ID,language and question are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        index_id = request.data.get('index_id')
        question = request.data.get('question')
        language = request.data.get('language')
        if generic_question(question):
            answer = generic_question(question) 
            if language == "sk":
                answer = convert_to_slovak(answer)
            return Response({
                'success': True,
                'message': answer
            }, status=status.HTTP_200_OK)
        
        user_id = os.getenv("USER_ID")
        api_password = os.getenv("API_PASSWORD")
        data = {
            "user_id": user_id,
            "api_password": api_password,
            "index_id": index_id,
            "question": question,
        }
        print("Data sent to API:", data)
        r = requests.post('https://iielara.com/api/chat', data=data)
        if r.status_code != 200:
            print(r.text)
            return Response({
                'success': False,
                'message': 'Error in fetching chat response'
            }, status=status.HTTP_400_BAD_REQUEST)
        response_data = r.json()
        response= response_data['data']
        response = remove_html_codes(response)
        if language == "sk":
            response = convert_to_slovak(response)

        return Response({
            'success': True,
            'message': response,
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    

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

    if highest_ratio >= 0.9:
        return best_match["answer"]
    else:
        return None
    
def convert_to_slovak(text):
    translated = GoogleTranslator(source='auto', target="sk").translate(text)
    return translated

def generate_otp(length=6):
    """Generate a random OTP"""
    return ''.join(secrets.choice(string.digits) for _ in range(length))

def generate_token(user_id):
    """Generate JWT token for user authentication"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=30),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, os.getenv('JWT_SECRET_KEY'), algorithm='HS256')
    return token

def verify_token(token):
    """Verify JWT token and return user_id"""
    try:
        payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def send_otp_email(email, otp):
    """Send OTP to user email"""
    try:
        subject = 'Your OTP for Biz Registration'
        message = f'''
        Hello,
        
        Your One-Time Password (OTP) for Biz registration is: {otp}
        
        This OTP is valid for 10 minutes.
        
        If you didn't request this, please ignore this email.
        
        Best regards,
        Biz Team
        '''
        
        send_mail(
            subject,
            message,
            os.getenv('EMAIL_HOST_USER'),
            [email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# API Views

@api_view(['POST'])
def signup(request):
    """
    Handle user signup with email and password
    Sends OTP for verification
    """
    try:
        # Validate required fields
        if 'email' not in request.data or 'password' not in request.data:
            return Response({
                'success': False,
                'message': 'Email and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        email = request.data.get('email').lower().strip()
        password = request.data.get('password')
        name = request.data.get('name', '')
        
        # Validate email format
        import re
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            return Response({
                'success': False,
                'message': 'Invalid email format'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            return Response({
                'success': False,
                'message': 'Email already registered'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate password strength
        if len(password) < 8:
            return Response({
                'success': False,
                'message': 'Password must be at least 8 characters long'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate OTP
        otp = generate_otp()
        
        # Create or update OTP verification record
        OTPVerification.objects.filter(email=email).delete()  # Remove old OTPs
        otp_record = OTPVerification.objects.create(
            email=email,
            otp=otp,
            expires_at=datetime.now() + timedelta(minutes=10)
        )
        
        # Send OTP email
        if not send_otp_email(email, otp):
            return Response({
                'success': False,
                'message': 'Failed to send OTP. Please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Store temporary user data (will be created after OTP verification)
        # Using OTP record to store this temporarily
        otp_record.temp_password = make_password(password)
        otp_record.temp_name = name
        otp_record.save()
        
        return Response({
            'success': True,
            'message': 'OTP sent to your email',
            'email': email
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def verify_otp(request):
    """
    Verify OTP and create user account
    """
    try:
        if 'email' not in request.data or 'otp' not in request.data:
            return Response({
                'success': False,
                'message': 'Email and OTP are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        email = request.data.get('email').lower().strip()
        otp = request.data.get('otp')
        
        # Find OTP record
        try:
            otp_record = OTPVerification.objects.get(email=email, otp=otp)
        except OTPVerification.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Invalid OTP'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if OTP is expired
        # if datetime.now() > otp_record.expires_at:
        #     otp_record.delete()
        #     return Response({
        #         'success': False,
        #         'message': 'OTP has expired. Please request a new one.'
        #     }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create user account
        user = User.objects.create(
            email=email,
            password=otp_record.temp_password,
            name=otp_record.temp_name,
            is_verified=True,
            auth_provider='email'
        )
        
        # Delete OTP record
        otp_record.delete()
        
        # Generate authentication token
        token = generate_token(user.id)
        
        # Serialize user data
        user_serializer = UserSerializer(user)
        
        return Response({
            'success': True,
            'message': 'Account created successfully',
            'token': token,
            'user': user_serializer.data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def resend_otp(request):
    """
    Resend OTP to user email
    """
    try:
        if 'email' not in request.data:
            return Response({
                'success': False,
                'message': 'Email is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        email = request.data.get('email').lower().strip()
        
        # Check if there's a pending OTP request
        try:
            otp_record = OTPVerification.objects.get(email=email)
        except OTPVerification.DoesNotExist:
            return Response({
                'success': False,
                'message': 'No pending verification found'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate new OTP
        otp = generate_otp()
        otp_record.otp = otp
        otp_record.expires_at = datetime.now() + timedelta(minutes=10)
        otp_record.save()
        
        # Send OTP email
        if not send_otp_email(email, otp):
            return Response({
                'success': False,
                'message': 'Failed to send OTP. Please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({
            'success': True,
            'message': 'OTP resent successfully'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    """
    Handle user login with email and password
    """
    try:
        if 'email' not in request.data or 'password' not in request.data:
            return Response({
                'success': False,
                'message': 'Email and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        email = request.data.get('email').lower().strip()
        password = request.data.get('password')
        
        # Find user
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Invalid email or password'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if user registered with social auth
        if user.auth_provider != 'email':
            return Response({
                'success': False,
                'message': f'Please login using {user.auth_provider.title()}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Verify password
        if not check_password(password, user.password):
            return Response({
                'success': False,
                'message': 'Invalid email or password'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if user is verified
        if not user.is_verified:
            return Response({
                'success': False,
                'message': 'Please verify your email first'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Generate authentication token
        token = generate_token(user.id)
        
        # Update last login
        user.last_login = datetime.now()
        user.save()
        
        # Serialize user data
        user_serializer = UserSerializer(user)
        
        return Response({
            'success': True,
            'message': 'Login successful',
            'token': token,
            'user': user_serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def google_auth(request):
    try:
        token = request.data.get('token')
        if not token:
            return Response(
                {'success': False, 'message': 'Google token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verify token with Google
        resp = requests.get(
            'https://oauth2.googleapis.com/tokeninfo',
            params={'id_token': token},
            timeout=5
        )

        if resp.status_code != 200:
            return Response(
                {'success': False, 'message': 'Invalid Google token'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        data = resp.json()

        # VERY IMPORTANT security check
        if data.get('aud') != os.getenv('GOOGLE_CLIENT_ID'):
            return Response(
                {'success': False, 'message': 'Invalid token audience'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        email = data.get('email', '').lower()
        name = data.get('name', '')
        google_id = data.get('sub')
        picture = data.get('picture', '')

        if not email:
            return Response(
                {'success': False, 'message': 'Email not provided by Google'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get or create user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'name': name,
                'google_id': google_id,
                'profile_picture': picture,
                'auth_provider': 'google',
                'is_verified': True,
            }
        )

        if not created and not user.google_id:
            user.google_id = google_id
            user.save()

        user.last_login = datetime.now()
        user.save()

        token = generate_token(user.id)
        serializer = UserSerializer(user)

        return Response({
            'success': True,
            'message': 'Google login successful',
            'token': token,
            'user': serializer.data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'success': False, 'message': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
def apple_auth(request):
    """
    Handle Apple OAuth authentication
    """
    try:
        if 'token' not in request.data:
            return Response({
                'success': False,
                'message': 'Apple token is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        apple_token = request.data.get('token')
        user_data = request.data.get('user', {})
        
        # Decode Apple ID token
        try:
            # Apple's public keys endpoint
            jwks_url = 'https://appleid.apple.com/auth/keys'
            jwks_response = requests.get(jwks_url)
            jwks = jwks_response.json()
            
            # Decode the token (simplified - in production use proper JWT verification)
            decoded = jwt.decode(
                apple_token,
                options={"verify_signature": False}  # In production, verify with Apple's public key
            )
            
            email = decoded.get('email', '').lower().strip()
            apple_id = decoded.get('sub')
            
            # Apple may not provide email if user denied permission
            if not email:
                email = user_data.get('email', '').lower().strip()
            
            name = user_data.get('name', {})
            full_name = f"{name.get('firstName', '')} {name.get('lastName', '')}".strip()
            
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Invalid Apple token'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if not email:
            return Response({
                'success': False,
                'message': 'Email is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user exists
        try:
            user = User.objects.get(email=email)
            
            # Update Apple ID if not set
            if not user.apple_id:
                user.apple_id = apple_id
                user.save()
                
        except User.DoesNotExist:
            # Create new user
            user = User.objects.create(
                email=email,
                name=full_name,
                apple_id=apple_id,
                is_verified=True,
                auth_provider='apple'
            )
        
        # Update last login
        user.last_login = datetime.now()
        user.save()
        
        # Generate authentication token
        token = generate_token(user.id)
        
        # Serialize user data
        user_serializer = UserSerializer(user)
        
        return Response({
            'success': True,
            'message': 'Apple authentication successful',
            'token': token,
            'user': user_serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def auto_login(request):
    """
    Auto-login user using JWT token
    """
    try:
        if 'token' not in request.data:
            return Response({
                'success': False,
                'message': 'Token is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        token = request.data.get('token')
        
        # Verify token
        user_id = verify_token(token)
        if not user_id:
            return Response({
                'success': False,
                'message': 'Invalid or expired token'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Get user
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Update last login
        user.last_login = datetime.now()
        user.save()
        
        # Serialize user data
        user_serializer = UserSerializer(user)
        
        return Response({
            'success': True,
            'message': 'Auto-login successful',
            'user': user_serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout(request):
    """
    Logout user (frontend should delete token)
    """
    return Response({
        'success': True,
        'message': 'Logout successful'
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def forgot_password(request):
    """
    Send OTP for password reset
    """
    try:
        if 'email' not in request.data:
            return Response({
                'success': False,
                'message': 'Email is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        email = request.data.get('email').lower().strip()
        
        # Check if user exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Don't reveal if email exists or not for security
            return Response({
                'success': True,
                'message': 'If the email exists, an OTP has been sent'
            }, status=status.HTTP_200_OK)
        
        # Only allow password reset for email auth users
        if user.auth_provider != 'email':
            return Response({
                'success': False,
                'message': f'This account uses {user.auth_provider.title()} login'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate OTP
        otp = generate_otp()
        
        # Create or update OTP verification record
        OTPVerification.objects.filter(email=email).delete()
        OTPVerification.objects.create(
            email=email,
            otp=otp,
            expires_at=datetime.now() + timedelta(minutes=10),
            is_password_reset=True
        )
        
        # Send OTP email
        send_otp_email(email, otp)
        
        return Response({
            'success': True,
            'message': 'OTP sent to your email',
            'email': email
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def reset_password(request):
    """
    Reset password with OTP verification
    """
    try:
        if 'email' not in request.data or 'otp' not in request.data or 'new_password' not in request.data:
            return Response({
                'success': False,
                'message': 'Email, OTP, and new password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        email = request.data.get('email').lower().strip()
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')
        
        # Validate password strength
        if len(new_password) < 8:
            return Response({
                'success': False,
                'message': 'Password must be at least 8 characters long'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Find OTP record
        try:
            otp_record = OTPVerification.objects.get(
                email=email, 
                otp=otp, 
                is_password_reset=True
            )
        except OTPVerification.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Invalid OTP'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if OTP is expired
        if datetime.now() > otp_record.expires_at:
            otp_record.delete()
            return Response({
                'success': False,
                'message': 'OTP has expired'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get user
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Update password
        user.password = make_password(new_password)
        user.save()
        
        # Delete OTP record
        otp_record.delete()
        
        return Response({
            'success': True,
            'message': 'Password reset successful'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)