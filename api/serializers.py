from .models import *
from rest_framework import serializers

class vtonSerializer(serializers.Serializer):
    input_image = serializers.CharField()
    outfit_image = serializers.CharField()
    body_measurement = serializers.CharField()
