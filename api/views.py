from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from api.throttles import  OneTimeRateThrottle, NoThrottle
from .utils import check_token, call_vton_service
from .serializers import vtonSerializer, OutfitSerializer
from .models import Outfit, Client

@api_view(['POST'])
@throttle_classes([NoThrottle])
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