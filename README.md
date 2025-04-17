# Biz - Business Card Management Platform

## Overview
Biz is a comprehensive business card management platform that allows organizations to create digital business cards with integrated AI chat capabilities. The platform consists of a Django backend and HTML/CSS/JavaScript frontend.

## Project Structure

### Backend (Django)
- **Main App**: Handles core application functions
- **API Endpoints**: RESTful endpoints for CRUD operations on business cards
- **AI Integration**: Integration with iiElara for chat capabilities
- **Database**: PostgreSQL for data persistence

### Frontend
- **Home Page**: Displays all active business cards
- **Contact Page**: Form for creating new business cards
- **Chat Page**: Interactive chat interface with AI responses
- **Translation Support**: Multi-language support (English and Slovak)

## Key Features

- **Business Card Creation**: Organizations can create digital business cards with their information
- **AI-Powered Chat**: Integrated chat functionality using iiElara API
- **Multilingual Support**: Toggle between English and Slovak languages
- **Responsive Design**: Compatible with both desktop and mobile devices
- **File Uploads**: Support for company logos, banners, and profile pictures

## Technologies Used

### Backend
- Django 5.1.7
- Django REST Framework
- PostgreSQL
- Python 3
- Whitenoise for static file handling
- Google Translator 

### Frontend
- HTML5
- CSS3
- JavaScript
- jQuery
- Responsive design

### External Integrations
- iiElara API for chat functionality
- Google Translator API for language translation

## Getting Started

### Prerequisites
- Python 3.x
- PostgreSQL
- Required Python packages (see requirements.txt)

### Installation
1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   - DB_NAME
   - DB_USER
   - DB_PASSWORD
   - DB_HOST
   - DB_PORT
   - EMAIL_PORT
   - EMAIL_HOST_USER
   - EMAIL_HOST_PASSWORD
   - BASE_URL
   - USER_ID (for iiElara API)
   - API_PASSWORD (for iiElara API)

5. Run migrations:
   ```
   python manage.py migrate
   ```
6. Start the development server:
   ```
   python manage.py runserver
   ```

## API Endpoints

- `GET /getBusinessCards` - Retrieve all active business cards
- `GET /getBusinessCard` - Retrieve a specific business card by ID
- `POST /createBusinessCard` - Create a new business card
- `PUT /updateBusinessCard` - Update an existing business card
- `DELETE /deleteBusinessCard` - Delete a business card
- `POST /chat` - Send a message to the AI chat system

## Security Notes

- Development debug mode is currently enabled and should be disabled in production
- Secret key is exposed in settings.py and should be moved to environment variables for production
- CORS is currently set to allow all origins

## Future Improvements

- Implement authentication system
- Add user roles and permissions
- Enhance AI chat capabilities
- Expand language support
- Add analytics for business card engagement

## Contributors

- Project maintained by the iiTeam Organisation.

## License

This project is proprietary and confidential. Unauthorized copying, distribution, or use is prohibited.
