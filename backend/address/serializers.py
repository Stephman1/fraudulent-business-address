from rest_framework import serializers
from . import models

class UserAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserAttribute
        fields = '__all__'

class UserDataSerializer(serializers.ModelSerializer):
    attributes = UserAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = models.UserData
        fields = '__all__'