from rest_framework.decorators import api_view, throttle_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.throttles import MonthlyRateThrottle, OneTimeRateThrottle, BulkRateThrottle, NoThrottle
from rest_framework.authtoken.models import Token
from .utils import check_token, call_vton_service
from .serializers import vtonSerializer
from .models import Outfit

@api_view(['POST'])
@throttle_classes([NoThrottle])
def vton(request):
    auth_header = request.headers.get('Authorization')
    is_token_valid = check_token(auth_header)
    if is_token_valid:
        data = request.data
        vton_serializer = vtonSerializer(data=request.data)
        if vton_serializer.is_valid():
            data = vton_serializer.data
            output_image = call_vton_service(data['input_image'], data['outfit_image'], data['body_measurement'])
            return Response({"data": output_image}, status=200)
        
    return Response({"data": "Invalid Data"}, status=500)

@api_view(['GET'])
@throttle_classes([NoThrottle])
def outfits(request):
    auth_header = request.headers.get('Authorization')
    is_token_valid = check_token(auth_header)
    if is_token_valid:
        outfits = Outfit.objects.all()
        # add here
        
    return Response({"data": "Invalid Data"}, status=500)