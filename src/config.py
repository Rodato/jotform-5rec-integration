import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# JotForm API Configuration
JOTFORM_API_KEY = os.getenv('JOTFORM_API_KEY')
FORM_ID = os.getenv('FORM_ID')

# Email Configuration
GMAIL_USER = os.getenv('GMAIL_USER')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))

# Project Configuration
PROJECT_NAME = os.getenv('PROJECT_NAME', '5REC')
FROM_NAME = 'Equipo 5REC'

# Validate required environment variables
required_vars = ['JOTFORM_API_KEY', 'FORM_ID', 'GMAIL_USER', 'GMAIL_PASSWORD']
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")