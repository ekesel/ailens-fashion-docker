from rest_framework.authtoken.models import Token

def check_token(auth_header):
    if auth_header and auth_header.startswith('Token '):
        auth_token = auth_header.split(' ')[1]
        if Token.objects.filter(key=auth_token).exists():
            return True, Token.objects.filter(key=auth_token).last().user

    return False

def call_vton_service(input_image, outfit_images, body_measurement):
    output_image = ""
    return output_image