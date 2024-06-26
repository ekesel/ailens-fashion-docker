from rest_framework.authtoken.models import Token
import re

def check_token(auth_header):
    if auth_header and auth_header.startswith('Token '):
        auth_token = auth_header.split(' ')[1]
        if Token.objects.filter(key=auth_token).exists():
            return True, Token.objects.filter(key=auth_token).last().user

    return False

def call_vton_service(input_image, outfit_images, body_measurement):
    output_image = ""
    return output_image

def is_valid_email(email):
    # Regular expression for email validation
    regex = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'
    
    # Check if the provided email matches the regex pattern
    if re.match(regex, email):
        return True
    else:
        return False

def is_valid_phone(phone):
    # Regular expression for phone number validation
    regex = r'^\+?[\d\s-]+$'
    
    # Check if the provided phone number matches the regex pattern
    if re.match(regex, phone):
        return True
    else:
        return False