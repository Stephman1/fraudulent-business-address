from rest_framework import serializers
from . import models

class AddressSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Address
    fields = '__all__'

class UserDataSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.UserData
    fields = '__all__'