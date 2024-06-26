from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from api.throttles import  OneTimeRateThrottle, NoThrottle
from .utils import check_token, call_vton_service, is_valid_email, is_valid_phone
from .serializers import vtonSerializer, OutfitSerializer
from .models import Outfit, Client
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

@api_view(['POST'])
@throttle_classes([OneTimeRateThrottle])
def vton(request):
    auth_header = request.headers.get('Authorization')
    is_token_valid, user = check_token(auth_header)
    if is_token_valid:
        data = request.data
        vton_serializer = vtonSerializer(data=request.data)
        if vton_serializer.is_valid():
            data = vton_serializer.data
            output_image = call_vton_service(data['input_image'], data['outfit_image'], data['body_measurement'])
            return Response({"data": output_image}, status=200)
        
    return Response({"data": "Invalid Data"}, status=500)

@api_view(['GET', 'POST'])
@throttle_classes([NoThrottle])
def outfits(request):
    if request.method == 'GET':
        auth_header = request.headers.get('Authorization')
        is_token_valid, user = check_token(auth_header)
        if is_token_valid and user:
            client = Client.objects.filter(user=user).last()
            if client:
                outfits = Outfit.objects.filter(added_by=client)
                if outfits.count()  > 0:
                    serializer = OutfitSerializer(outfits, many=True)
                    if serializer.data:
                        return Response(serializer.data, status=200)
                else:
                    return Response({"data": "No Outfits"}, status=200)
            else:
                return Response({"data": "Client Not Available"}, status=404)
    if request.method == 'POST':
        auth_header = request.headers.get('Authorization')
        is_token_valid, user = check_token(auth_header)
        if is_token_valid and user:
            client = Client.objects.filter(user=user).last()
            if client:
                data = {
                    'added_by': client.id,
                    'binary_code': request.data['binary_code'],
                    'image': request.data['image']
                }
                serializer = OutfitSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=200)
                else:
                    return Response({"data": serializer.errors}, status=200)
            else:
                return Response({"data": "Client Not Available"}, status=404)
    return Response({"data": "Invalid Data"}, status=500)


@api_view(['POST'])
@throttle_classes([NoThrottle])
def register(request):
    if request.method == 'POST':
        username = request.data.get('name')
        email_or_phone = request.data.get('email_or_phone')
        password = request.data.get('password')
        email = None
        phone = None

        if not username or not password or not email_or_phone:
            return Response({'error': 'Please provide username, email/phone and password'}, status=400)

        is_email = is_valid_email(email_or_phone)
        is_phone = is_valid_phone(email_or_phone)

        if is_email:
            email = email_or_phone
            if User.objects.filter(email=email).exists():
                return Response({'error': 'Email already exists, Please Login'}, status=400)
            
        if is_phone:
            phone = email_or_phone
            if Client.objects.filter(phone=phone).exists():
                return Response({'error': 'Phone number already exists, Please Login'}, status=400)

        if not email and not phone:
            return Response({'error': 'Please provide valid Email or Phone'}, status=400)

        user = User.objects.create_user(username=username, password=password, email=email)
        customer = Client.objects.create(user=user,phone=phone, name=username)
        if user and customer:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=201)
        else:
            return Response({'error': 'Failed to create user'}, status=500)
    else:
        return Response({'error': 'Method not allowed'}, status=405)
    
@api_view(['POST'])
@throttle_classes([NoThrottle])
def login(request):
    if request.method == 'POST':
        email_or_phone = request.data.get('email_or_phone')
        password = request.data.get('password')
        user = None

        if not email_or_phone or not password:
            return Response({'error': 'Please provide email/phone and password'}, status=400)

        is_email = is_valid_email(email_or_phone)
        is_phone = is_valid_phone(email_or_phone)

        if is_email:
            try:
                user = User.objects.get(email=email_or_phone)
            except User.DoesNotExist:
                return Response({'error': 'Invalid email or password'}, status=400)
        elif is_phone:
            try:
                customer = Client.objects.get(phone=email_or_phone)
                user = customer.user
            except Client.DoesNotExist:
                return Response({'error': 'Invalid phone number or password'}, status=400)
        else:
            return Response({'error': 'Please provide valid email or phone number'}, status=400)

        if user and user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=200)
        else:
            return Response({'error': 'Invalid email/phone or password'}, status=400)
    else:
        return Response({'error': 'Method not allowed'}, status=405)
